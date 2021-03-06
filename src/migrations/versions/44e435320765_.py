"""empty message

Revision ID: 44e435320765
Revises: cde981c615f0
Create Date: 2016-10-07 06:28:46.835150

"""

# revision identifiers, used by Alembic.
revision = '44e435320765'
down_revision = 'cde981c615f0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mpesatransaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mpesa_transaction_no', sa.String(length=50), nullable=True),
    sa.Column('mpesa_txn_id', sa.String(length=50), nullable=True),
    sa.Column('recipient_phone_no', sa.String(length=50), nullable=False),
    sa.Column('total_amount', sa.String(length=50), nullable=False),
    sa.Column('total_amount_currency', sa.String(length=4), nullable=False),
    sa.Column('reference_id', sa.String(length=50), nullable=True),
    sa.Column('merchant_transaction_id', sa.String(length=50), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_approved', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_transaction_id'], ['transaction.transaction_no'], ),
    sa.ForeignKeyConstraint(['recipient_phone_no'], ['mpesaprofile.mobile_phone_no'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mpesatransaction')
    ### end Alembic commands ###
