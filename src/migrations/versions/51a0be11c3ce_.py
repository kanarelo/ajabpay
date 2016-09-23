"""empty message

Revision ID: 51a0be11c3ce
Revises: 454d9578c0be
Create Date: 2016-09-22 14:54:36.447295

"""

# revision identifiers, used by Alembic.
revision = '51a0be11c3ce'
down_revision = '454d9578c0be'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'mpesatransaction', 'user', ['recipient_phone_no'], ['phone'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mpesatransaction', type_='foreignkey')
    ### end Alembic commands ###
