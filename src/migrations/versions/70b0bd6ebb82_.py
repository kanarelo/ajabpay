"""empty message

Revision ID: 70b0bd6ebb82
Revises: 9effdc1d4cc6
Create Date: 2016-09-21 15:09:27.059155

"""

# revision identifiers, used by Alembic.
revision = '70b0bd6ebb82'
down_revision = '9effdc1d4cc6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paypaltransaction', sa.Column('parent_transaction_id', sa.String(length=50), nullable=True))
    op.create_foreign_key(None, 'paypaltransaction', 'transaction', ['parent_transaction_id'], ['transaction_no'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'paypaltransaction', type_='foreignkey')
    op.drop_column('paypaltransaction', 'parent_transaction_id')
    ### end Alembic commands ###
