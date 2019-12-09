"""add price to order product

Revision ID: a562e4acac0e
Revises: be5b5fe265d0
Create Date: 2019-12-09 10:19:54.356429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a562e4acac0e'
down_revision = 'be5b5fe265d0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('python_ecommerce_order_product', sa.Column('purchase_price', sa.DECIMAL(18, 2)))


def downgrade():
    op.drop_column('python_ecommerce_order_product', 'purchase_price')
