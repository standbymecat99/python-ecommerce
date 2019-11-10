import os
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.sql import func
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

        if engine:
            Base.metadata.create_all(engine)
        else:
            url = alembic_cfg.get_section_option('alembic', 'sqlalchemy.url')
            engine = create_engine(url)
            Base.metadata.create_all(engine)

@as_declarative()
class Base(object):
    __tableprefix__ = 'python_ecommerce_'

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True), onupdate=func.now())

class Product(Base):
    __tablename__ = 'python_ecommerce_product'

    name = sa.Column(sa.String(255), nullable=False, index=True)
    description = sa.Column(sa.Text, default='')
    stock = sa.Column(sa.Integer, default=0)
    price = sa.Column(sa.DECIMAL(18, 2))
