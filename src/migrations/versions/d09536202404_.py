"""empty message

Revision ID: d09536202404
Revises: e6029f2bcc1d
Create Date: 2016-10-18 09:20:47.341562

"""

# revision identifiers, used by Alembic.
revision = 'd09536202404'
down_revision = 'e6029f2bcc1d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accountverification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_code', sa.String(length=15), nullable=False),
    sa.Column('mobile_code', sa.String(length=10), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('expiry_date', sa.DateTime(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mobile_code', 'email_code')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accountverification')
    ### end Alembic commands ###