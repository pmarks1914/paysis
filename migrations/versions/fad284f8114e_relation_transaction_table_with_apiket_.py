"""relation Transaction table with apiket table

Revision ID: fad284f8114e
Revises: a2a3e07b01d4
Create Date: 2024-03-25 23:52:29.345105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fad284f8114e'
down_revision = 'a2a3e07b01d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('apikey', schema=None) as batch_op:
        batch_op.add_column(sa.Column('transaction_id', sa.String(length=36), nullable=True))
        batch_op.create_foreign_key(None, 'transaction', ['transaction_id'], ['transaction_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('apikey', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('transaction_id')

    # ### end Alembic commands ###
