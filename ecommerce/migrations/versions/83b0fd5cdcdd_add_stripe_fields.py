"""add stripe fields

Revision ID: 83b0fd5cdcdd
Revises: 01ec6ed741fe
Create Date: 2019-11-19 10:22:56.378267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83b0fd5cdcdd'
down_revision = '01ec6ed741fe'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('python_ecommerce_customer', sa.Column('stripe_customer_id', sa.String(255)))
    op.add_column('python_ecommerce_customer', sa.Column('stripe_card_id', sa.String(255)))
    op.add_column('python_ecommerce_order', sa.Column('stripe_charge_id', sa.String(255)))


def downgrade():
    op.drop_column('python_ecomerce_customer', 'stripe_customer_id')
    op.drop_column('python_ecomerce_customer', 'stripe_card_id')
    op.drop_column('python_ecommerce_order', 'stripe_charge_id')
