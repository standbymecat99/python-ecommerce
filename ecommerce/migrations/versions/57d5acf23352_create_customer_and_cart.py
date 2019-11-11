"""create customer and cart

Revision ID: 57d5acf23352
Revises: c29e63fb989b
Create Date: 2019-11-10 20:51:25.458895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57d5acf23352'
down_revision = 'c29e63fb989b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'python_ecommerce_customer',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_table(
        'python_ecommerce_cart',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('python_ecommerce_customer.id')),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('python_ecommerce_product.id')),
        sa.Column('count', sa.Integer, default=0)
    )


def downgrade():
    op.drop_table('python_ecommerce_cart')
    op.drop_table('python_ecommerce_customer')
