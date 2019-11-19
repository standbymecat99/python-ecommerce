"""update customer table

Revision ID: 8d09262531d3
Revises: 471106abfdfa
Create Date: 2019-11-19 00:21:09.875327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d09262531d3'
down_revision = '471106abfdfa'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('python_ecommerce_customer') as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(255)))
        batch_op.add_column(sa.Column('last_name', sa.String(255)))
        batch_op.add_column(sa.Column('phone', sa.String(50)))
        batch_op.add_column(sa.Column('email', sa.String(255)))
        batch_op.add_column(sa.Column('address_country', sa.String(2)))
        batch_op.add_column(sa.Column('address_state', sa.String(255)))
        batch_op.add_column(sa.Column('address_city', sa.String(255)))
        batch_op.add_column(sa.Column('address_line1', sa.Text))
        batch_op.add_column(sa.Column('address_line2', sa.Text))
        batch_op.add_column(sa.Column('address_postal_code', sa.String(50)))


def downgrade():
    with op.batch_alter_table('python_ecommerce_customer') as batch_op:
        batch_op.drop_column('first_name')
        batch_op.drop_column('last_name')
        batch_op.drop_column('phone')
        batch_op.drop_column('email')
        batch_op.drop_column('address_country')
        batch_op.drop_column('address_state')
        batch_op.drop_column('address_city')
        batch_op.drop_column('address_line1')
        batch_op.drop_column('address_line2')
        batch_op.drop_column('address_postal_code')
