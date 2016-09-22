"""empty message

Revision ID: aaa49e535183
Revises: d43dda785144
Create Date: 2016-09-22 13:53:43.661663

"""

# revision identifiers, used by Alembic.
revision = 'aaa49e535183'
down_revision = 'd43dda785144'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mpesaprofile', sa.Column('account_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'mpesaprofile', 'account', ['account_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mpesaprofile', type_='foreignkey')
    op.drop_column('mpesaprofile', 'account_id')
    ### end Alembic commands ###
