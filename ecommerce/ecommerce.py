import os
import csv
import sqlalchemy as sa
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import as_declarative
from alembic import command
from alembic.config import Config

class ECommerce:
    def __init__(self, url=None, engine=None):
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

    def create_customer(self, session=None):
        if session is None:
            session = self.session

        customer = Customer()
        session.add(customer)
        session.commit()
        return customer

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

class Cart(Base):
    __tablename__ = 'python_ecommerce_cart'

    customer_id = sa.Column(sa.Integer, sa.ForeignKey(Customer.id), index=True)
    product_id = sa.Column(sa.Integer, sa.ForeignKey(Product.id), index=True)
    count = sa.Column(sa.Integer, default=0)

    __table_args__ = (
        UniqueConstraint('customer_id', 'product_id',
                         name='ux_python_ecommerce_cart_customer_id_product_id'),
    )
