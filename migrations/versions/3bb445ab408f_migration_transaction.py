"""migration transaction

Revision ID: 3bb445ab408f
Revises: 9c1757c0f240
Create Date: 2024-03-21 23:23:30.848490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bb445ab408f'
down_revision = '9c1757c0f240'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('apikey', schema=None) as batch_op:
        batch_op.drop_constraint('apikey_transaction_id_fkey', type_='foreignkey')
        batch_op.drop_column('transaction_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('apikey', schema=None) as batch_op:
        batch_op.add_column(sa.Column('transaction_id', sa.VARCHAR(length=36), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('apikey_transaction_id_fkey', 'transaction', ['transaction_id'], ['transaction_id'])

    # ### end Alembic commands ###