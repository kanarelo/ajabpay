"""empty message

Revision ID: 425863977cfb
Revises: 7903fbe22d9e
Create Date: 2016-09-22 13:50:24.630552

"""

# revision identifiers, used by Alembic.
revision = '425863977cfb'
down_revision = '7903fbe22d9e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mpesaprofile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('account_type', sa.String(length=10), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'account', sa.Column('daily_deposit_limit', sa.Numeric(precision=18, scale=2), nullable=True))
    op.add_column(u'account', sa.Column('daily_withdraw_limit', sa.Numeric(precision=18, scale=2), nullable=True))
    op.add_column(u'account', sa.Column('monthly_deposit_limit', sa.Numeric(precision=18, scale=2), nullable=True))
    op.add_column(u'account', sa.Column('monthly_withdraw_limit', sa.Numeric(precision=18, scale=2), nullable=True))
    op.add_column(u'account', sa.Column('txn_withdrawal_limit', sa.Numeric(precision=18, scale=2), nullable=True))
    op.add_column(u'account', sa.Column('weekly_deposit_limit', sa.Numeric(precision=18, scale=2), nullable=True))
    op.add_column(u'account', sa.Column('weekly_withdraw_limit', sa.Numeric(precision=18, scale=2), nullable=True))
    op.add_column(u'account', sa.Column('yearly_deposit_limit', sa.Numeric(precision=18, scale=2), nullable=True))
    op.add_column(u'account', sa.Column('yearly_withdraw_limit', sa.Numeric(precision=18, scale=2), nullable=True))
    op.alter_column(u'account', 'account_number',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
    op.alter_column(u'account', 'amount_currency_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column(u'account', 'date_created',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column(u'account', 'date_updated',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column(u'account', 'product_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column(u'account', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_column(u'account', 'txn_withdraw_limit')
    op.add_column(u'mpesatransaction', sa.Column('merchant_transaction_id', sa.String(length=50), nullable=True))
    op.add_column(u'mpesatransaction', sa.Column('reference_id', sa.String(length=50), nullable=True))
    op.add_column(u'mpesatransaction', sa.Column('total_amount', sa.String(length=50), nullable=False))
    op.add_column(u'mpesatransaction', sa.Column('total_amount_currency', sa.String(length=4), nullable=False))
    op.drop_constraint(u'mpesatransaction_ibfk_1', 'mpesatransaction', type_='foreignkey')
    op.create_foreign_key(None, 'mpesatransaction', 'transaction', ['mpesa_transaction_no'], ['transaction_no'])
    op.drop_column(u'mpesatransaction', 'transaction_id')
    op.alter_column(u'paypaladdress', 'country',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column(u'paypaladdress', 'date_created',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column(u'paypaladdress', 'locality',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column(u'paypaladdress', 'paypal_profile_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column(u'paypaladdress', 'region',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column(u'paypaladdress', 'street_address',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.add_column(u'paypalprofile', sa.Column('account_creation_date', sa.DateTime(), nullable=False))
    op.add_column(u'paypalprofile', sa.Column('date_of_birth', sa.Date(), nullable=False))
    op.alter_column(u'paypalprofile', 'email_verified',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    op.alter_column(u'paypalprofile', 'gender',
               existing_type=mysql.VARCHAR(length=1),
               nullable=True)
    op.drop_column(u'paypalprofile', 'age_range')
    op.drop_column(u'paypalprofile', 'middle_name')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'paypalprofile', sa.Column('middle_name', mysql.VARCHAR(length=100), nullable=False))
    op.add_column(u'paypalprofile', sa.Column('age_range', mysql.VARCHAR(length=10), nullable=False))
    op.alter_column(u'paypalprofile', 'gender',
               existing_type=mysql.VARCHAR(length=1),
               nullable=False)
    op.alter_column(u'paypalprofile', 'email_verified',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    op.drop_column(u'paypalprofile', 'date_of_birth')
    op.drop_column(u'paypalprofile', 'account_creation_date')
    op.alter_column(u'paypaladdress', 'street_address',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column(u'paypaladdress', 'region',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.alter_column(u'paypaladdress', 'paypal_profile_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column(u'paypaladdress', 'locality',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.alter_column(u'paypaladdress', 'date_created',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column(u'paypaladdress', 'country',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.add_column(u'mpesatransaction', sa.Column('transaction_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'mpesatransaction', type_='foreignkey')
    op.create_foreign_key(u'mpesatransaction_ibfk_1', 'mpesatransaction', 'transaction', ['transaction_id'], ['id'])
    op.drop_column(u'mpesatransaction', 'total_amount_currency')
    op.drop_column(u'mpesatransaction', 'total_amount')
    op.drop_column(u'mpesatransaction', 'reference_id')
    op.drop_column(u'mpesatransaction', 'merchant_transaction_id')
    op.add_column(u'account', sa.Column('txn_withdraw_limit', mysql.DECIMAL(precision=6, scale=2), nullable=True))
    op.alter_column(u'account', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column(u'account', 'product_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column(u'account', 'date_updated',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column(u'account', 'date_created',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column(u'account', 'amount_currency_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column(u'account', 'account_number',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
    op.drop_column(u'account', 'yearly_withdraw_limit')
    op.drop_column(u'account', 'yearly_deposit_limit')
    op.drop_column(u'account', 'weekly_withdraw_limit')
    op.drop_column(u'account', 'weekly_deposit_limit')
    op.drop_column(u'account', 'txn_withdrawal_limit')
    op.drop_column(u'account', 'monthly_withdraw_limit')
    op.drop_column(u'account', 'monthly_deposit_limit')
    op.drop_column(u'account', 'daily_withdraw_limit')
    op.drop_column(u'account', 'daily_deposit_limit')
    op.drop_table('mpesaprofile')
    ### end Alembic commands ###
