"""empty message

Revision ID: 5265cd480689
Revises: 182db0573a31
Create Date: 2016-09-25 17:12:11.303961

"""

# revision identifiers, used by Alembic.
revision = '5265cd480689'
down_revision = '182db0573a31'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paypaltransaction', sa.Column('create_time', sa.String(length=30), nullable=False))
    op.add_column('paypaltransaction', sa.Column('update_time', sa.String(length=30), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('paypaltransaction', 'update_time')
    op.drop_column('paypaltransaction', 'create_time')
    ### end Alembic commands ###