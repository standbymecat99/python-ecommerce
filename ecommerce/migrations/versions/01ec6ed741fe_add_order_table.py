"""add order table

Revision ID: 01ec6ed741fe
Revises: 8d09262531d3
Create Date: 2019-11-19 10:09:09.160899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01ec6ed741fe'
down_revision = '8d09262531d3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'python_ecommerce_order',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('python_ecommerce_customer.id')),
        sa.Column('note', sa.Text),
        mysql_default_charset='utf8'
    )
    op.create_table(
        'python_ecommerce_order_product',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('python_ecommerce_order.id')),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('python_ecommerce_product.id')),
        sa.Column('count', sa.Integer, default=0),
        mysql_default_charset='utf8'
    )


def downgrade():
    op.drop_table('python_ecommerce_order_product')
    op.drop_table('python_ecommerce_order')
