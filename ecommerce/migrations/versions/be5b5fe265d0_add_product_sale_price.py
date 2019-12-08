"""add product sale price

Revision ID: be5b5fe265d0
Revises: 83b0fd5cdcdd
Create Date: 2019-12-08 13:04:34.272513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be5b5fe265d0'
down_revision = '83b0fd5cdcdd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('python_ecommerce_product', sa.Column('sale', sa.Boolean, default=False))
    op.add_column('python_ecommerce_product', sa.Column('sale_price', sa.DECIMAL(18, 2)))
    op.create_index(
        'ix_python_ecommerce_product_sale',
        'python_ecommerce_product',
        ['sale'])
    op.create_index(
        'ix_python_ecommerce_product_sale_price',
        'python_ecommerce_product',
        ['sale_price'])


def downgrade():
    op.drop_column('python_ecommerce_product', 'sale')
    op.drop_column('python_ecommerce_product', 'sale_price')
