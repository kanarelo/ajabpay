"""empty message

Revision ID: 7903fbe22d9e
Revises: 7e8b2b13f58a
Create Date: 2016-09-22 11:01:07.258116

"""

# revision identifiers, used by Alembic.
revision = '7903fbe22d9e'
down_revision = '7e8b2b13f58a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'paypalprofile', 'user', ['email'], ['email'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'paypalprofile', type_='foreignkey')
    ### end Alembic commands ###
