"""empty message

Revision ID: e426ef99dc97
Revises: 70b0bd6ebb82
Create Date: 2016-09-21 17:00:56.390119

"""

# revision identifiers, used by Alembic.
revision = 'e426ef99dc97'
down_revision = '70b0bd6ebb82'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('transaction_id_2', table_name='paypaltransaction')
    op.drop_column('paypaltransaction', 'paypal_transaction_id')
    op.drop_column('paypaltransaction', 'transaction_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paypaltransaction', sa.Column('transaction_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('paypaltransaction', sa.Column('paypal_transaction_id', mysql.VARCHAR(length=50), nullable=True))
    op.create_index('transaction_id_2', 'paypaltransaction', ['transaction_id'], unique=True)
    ### end Alembic commands ###
