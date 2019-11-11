"""add indices to product and cart

Revision ID: 471106abfdfa
Revises: 57d5acf23352
Create Date: 2019-11-10 21:38:02.263772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '471106abfdfa'
down_revision = '57d5acf23352'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        'ix_python_ecommerce_product_stock',
        'python_ecommerce_product',
        ['stock'])
    op.create_index(
        'ix_python_ecommerce_product_price',
        'python_ecommerce_product',
        ['price'])
    op.create_index(
        'ux_python_ecommerce_cart_customer_id_product_id',
        'python_ecommerce_cart',
        ['customer_id', 'product_id'],
        unique=True)


def downgrade():
    op.create_index(
        'ix_python_ecommerce_product_stock',
        'python_ecommerce_product')
    op.create_index(
        'ix_python_ecommerce_product_price',
        'python_ecommerce_product')
    op.create_index(
        'ux_python_ecommerce_cart_customer_id_product_id',
        'python_ecommerce_cart')
