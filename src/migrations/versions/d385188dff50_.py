"""empty message

Revision ID: d385188dff50
Revises: 42b597636881
Create Date: 2016-10-17 18:36:18.800488

"""

# revision identifiers, used by Alembic.
revision = 'd385188dff50'
down_revision = '42b597636881'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('smsmessage', 'message_recipient')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('smsmessage', sa.Column('message_recipient', mysql.VARCHAR(length=15), nullable=True))
    ### end Alembic commands ###