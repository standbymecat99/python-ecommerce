"""Initial migration

Revision ID: c29e63fb989b
Revises: 
Create Date: 2019-11-05 15:16:18.262533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c29e63fb989b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'python_ecommerce_product',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('description', sa.Text, default=''),
        sa.Column('stock', sa.Integer, default=0),
        sa.Column('price', sa.DECIMAL(18, 2))
    )


def downgrade():
    op.drop_table('python_ecommerce_product')
