"""empty message

Revision ID: d4562b7632aa
Revises: 109070b76bcc
Create Date: 2016-09-25 17:14:23.534537

"""

# revision identifiers, used by Alembic.
revision = 'd4562b7632aa'
down_revision = '109070b76bcc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paypaltransaction', sa.Column('create_time', sa.DateTime(timezone=True), nullable=False))
    op.add_column('paypaltransaction', sa.Column('update_time', sa.DateTime(timezone=True), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('paypaltransaction', 'update_time')
    op.drop_column('paypaltransaction', 'create_time')
    ### end Alembic commands ###