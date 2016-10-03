"""empty message

Revision ID: 913c2fefea37
Revises: 6334b767fbed
Create Date: 2016-09-25 15:06:19.743500

"""

# revision identifiers, used by Alembic.
revision = '913c2fefea37'
down_revision = '6334b767fbed'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('paypaltransaction', 'paypal_payer_id',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('paypaltransaction', 'paypal_payer_id',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    ### end Alembic commands ###