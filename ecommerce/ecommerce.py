import os
import csv
import sqlalchemy as sa
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import update
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import as_declarative
from alembic import command
from alembic.config import Config
import stripe

class ECommerce:
    def __init__(self, url=None, engine=None, stripe_api_key=None):
        self.db_table_prefix = 'python_ecommerce_'

        alembic_cfg = Config(os.path.dirname(os.path.realpath(__file__)) + '/alembic.ini')
        alembic_cfg.set_main_option("script_location", "ecommerce:migrations")
        if url:
            alembic_cfg.set_section_option('alembic', 'sqlalchemy.url', url)
        command.upgrade(alembic_cfg, "head")

        if not engine:
            url = alembic_cfg.get_section_option('alembic', 'sqlalchemy.url')
            engine = create_engine(url)
        Base.metadata.create_all(engine)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

        stripe.api_key = stripe_api_key

    def create_customer(self, session=None):
        if session is None:
            session = self.session

        customer = Customer()
        session.add(customer)
        session.commit()
        return customer

    def update_customer(self, customer, first_name=None, last_name=None,
                        phone=None, email=None, address_country=None,
                        address_state=None, address_city=None,
                        address_line1=None, address_line2=None,
                        address_postal_code=None, stripe_card_token=None,
                        session=None):
        if not isinstance(customer, Customer):
            raise Exception('customer must be of type Customer')

        if session is None:
            session = self.session

        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone = phone
        customer.email = email
        customer.address_country = address_country
        customer.address_state = address_state
        customer.address_city = address_city
        customer.address_line1 = address_line1
        customer.address_line2 = address_line2
        customer.address_postal_code = address_postal_code

        if customer.stripe_customer_id is None:
            stripe_customer = stripe.Customer.create()
            customer.stripe_customer_id = stripe_customer.id

        if stripe_card_token is not None and customer.stripe_card_id is None:
            stripe_card = stripe.Customer.create_source(
                customer.stripe_customer_id,
                source=stripe_card_token)
            customer.stripe_card_id = stripe_card.id

        session.commit()

    def get_card_info(self, customer, session=None):
        if not isinstance(customer, Customer):
            raise Exception('customer must be of type Customer')

        if session is None:
            session = self.session

        if customer.stripe_customer_id is None or \
           customer.stripe_card_id is None:
            return None

        return stripe.Customer.retrieve_source(
            customer.stripe_customer_id,
            customer.stripe_card_id)

    def add_to_cart(self, customer, product, count, session=None):
        if not isinstance(customer, Customer):
            raise Exception('customer must be of type Customer')
        if not isinstance(product, Product):
            raise Exception('product must be of type Product')
        if not isinstance(count, int):
            raise Exception('count must be of type Integer')

        if session is None:
            session = self.session

        cart_product = session.query(Cart).\
            filter(Cart.customer_id==customer.id, Cart.product_id==product.id).\
            first()

        if cart_product is None:
            cart_product = Cart(
                customer_id=customer.id,
                product_id=product.id,
                count=count
            )
            session.add(cart_product)
        else:
            cart_product.count = cart_product.count + count

        session.commit()

    def get_cart(self, customer, session=None):
        if not isinstance(customer, Customer):
            raise Exception('customer must be of type Customer')

        if session is None:
            session = self.session

        cart_products = session.query(Cart).\
            filter(Cart.customer_id==customer.id,
                   Cart.count>0).all()

        return cart_products

    def remove_from_cart(self, customer, product, count, session=None):
        if not isinstance(customer, Customer):
            raise Exception('customer must be of type Customer')
        if not isinstance(product, Product):
            raise Exception('product must be of type Product')
        if not isinstance(count, int):
            raise Exception('count must be of type Integer')

        if session is None:
            session = self.session

        cart_product = session.query(Cart).\
            filter(Cart.customer_id==customer.id, Cart.product_id==product.id).\
            one()

        cart_product.count = max(0, cart_product.count - count)
        session.commit()

    def clear_cart(self, customer, session=None):
        if not isinstance(customer, Customer):
            raise Exception('customer must be of type Customer')

        if session is None:
            session = self.session

        cart_products = session.query(Cart).\
            filter(Cart.customer_id==customer.id).all()
        for cart_product in cart_products:
            cart_product.count = 0
        session.commit()

    def set_cart(self, customer, product, count, session=None):
        if not isinstance(customer, Customer):
            raise Exception('customer must be of type Customer')
        if not isinstance(product, Product):
            raise Exception('product must be of type Product')
        if not isinstance(count, int):
            raise Exception('count must be of type Integer')
        if count < 0:
            raise Exception('count greater than or equal to 0')

        if session is None:
            session = self.session

        cart_product = session.query(Cart).\
            filter(Cart.customer_id==customer.id, Cart.product_id==product.id).\
            one()

        cart_product.count = count
        session.commit()

    def get_country_list(self, lang='en'):
        data_dir = os.path.join(os.path.dirname(__file__), 'country_data', lang)
        if os.path.isdir(data_dir):
            data_file = os.path.join(data_dir, 'country.csv')
            with open(data_file, 'r') as f:
                country_list = []
                reader = csv.reader(f)
                reader.next()
                for row in reader:
                    country_list.append({
                        'key': row[0],
                        'value': row[1]
                    })
                return country_list

    def checkout(self, customer, session=None):
        if not isinstance(customer, Customer):
            raise Exception('customer must be of type Customer')

        if session is None:
            session = self.session

        cart_products = self.get_cart(customer, session)
        total = 0
        products = []
        product_count_dict = {}
        for cart_product in cart_products:
            product = session.query(Product).\
                filter(Product.id==cart_product.product_id).\
                one()
            products.append(product)
            product_count_dict[product.id] = cart_product.count
            total += product.price * cart_product.count

        stripe_charge = stripe.Charge.create(
            amount=int(total * 100),
            currency="usd",
            customer=customer.stripe_customer_id,
            source=customer.stripe_card_id)

        order = Order(
            customer_id=customer.id,
            stripe_charge_id=stripe_charge.id)

        for product in products:
            order.products.append(product)
        session.add(order)

        for cart_product in cart_products:
            cart_product.count = 0

        session.commit()

        order_products = []
        for product in order.products:
            session.execute(
                update(order_product_table).where(sa.and_(
                    order_product_table.c.order_id==order.id,
                    order_product_table.c.product_id==product.id)
                ).values(count=product_count_dict[product.id]))
            session.commit()

            order_products.append({
                'product': product.id,
                'count': product_count_dict[product.id]
            })

        return order_products


@as_declarative()
class Base(object):
    __tableprefix__ = 'python_ecommerce_'

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True), default=func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True),
                           default=func.now(), onupdate=func.now())

class Product(Base):
    __tablename__ = 'python_ecommerce_product'

    name = sa.Column(sa.String(255), nullable=False, index=True)
    description = sa.Column(sa.Text, default='')
    stock = sa.Column(sa.Integer, default=0, index=True)
    price = sa.Column(sa.DECIMAL(18, 2), index=True)

class Customer(Base):
    __tablename__ = 'python_ecommerce_customer'
    first_name = sa.Column(sa.String(255))
    last_name = sa.Column(sa.String(255))
    phone = sa.Column(sa.String(50))
    email = sa.Column(sa.String(255))
    address_country = sa.Column(sa.String(2))
    address_state = sa.Column(sa.String(255))
    address_city = sa.Column(sa.String(255))
    address_line1 = sa.Column(sa.Text)
    address_line2 = sa.Column(sa.Text)
    address_postal_code = sa.Column(sa.String(50))
    stripe_customer_id = sa.Column(sa.String(255))
    stripe_card_id = sa.Column(sa.String(255))

class Cart(Base):
    __tablename__ = 'python_ecommerce_cart'

    customer_id = sa.Column(sa.Integer, sa.ForeignKey(Customer.id), index=True)
    product_id = sa.Column(sa.Integer, sa.ForeignKey(Product.id), index=True)
    count = sa.Column(sa.Integer, default=0)

    __table_args__ = (
        UniqueConstraint('customer_id', 'product_id',
                         name='ux_python_ecommerce_cart_customer_id_product_id'),
    )

order_product_table = sa.Table('python_ecommerce_order_product', Base.metadata,
    sa.Column('order_id', sa.Integer, sa.ForeignKey('python_ecommerce_order.id')),
    sa.Column('product_id', sa.Integer, sa.ForeignKey('python_ecommerce_product.id')),
    sa.Column('count', sa.Integer)
)

class Order(Base):
    __tablename__ = 'python_ecommerce_order'

    customer_id = sa.Column(sa.Integer, sa.ForeignKey(Customer.id), index=True)
    note = sa.Column(sa.Text)
    products = relationship('Product', secondary=order_product_table)
    stripe_charge_id = sa.Column(sa.String(255))
