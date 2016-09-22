"""empty message

Revision ID: b2e11c97f93a
Revises: 93e27f53e870
Create Date: 2016-09-20 14:42:42.868326

"""

# revision identifiers, used by Alembic.
revision = 'b2e11c97f93a'
down_revision = '93e27f53e870'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'configexchangerate', ['code'])
    op.drop_constraint(u'configledgeraccountingrule_ibfk_3', 'configledgeraccountingrule', type_='foreignkey')
    op.drop_constraint(u'configledgeraccountingrule_ibfk_1', 'configledgeraccountingrule', type_='foreignkey')
    op.drop_constraint(u'configledgeraccountingrule_ibfk_2', 'configledgeraccountingrule', type_='foreignkey')
    op.create_foreign_key(None, 'configledgeraccountingrule', 'configtransactiontype', ['transaction_type_id'], ['id'])
    op.create_foreign_key(None, 'configledgeraccountingrule', 'configledgeraccount', ['debit_account_id'], ['id'])
    op.create_foreign_key(None, 'configledgeraccountingrule', 'configledgeraccount', ['credit_account_id'], ['id'])
    op.create_unique_constraint(None, 'configpaypalaccountwebhook', ['code'])
    op.create_unique_constraint(None, 'configwebhookeventtype', ['code'])
    op.add_column('emailmessage', sa.Column('message_sender', sa.String(length=100), nullable=True))
    op.drop_constraint(u'emailmessage_ibfk_1', 'emailmessage', type_='foreignkey')
    op.drop_column('emailmessage', 'email_arguments')
    op.drop_column('emailmessage', 'template_id')
    op.add_column('paypaltransaction', sa.Column('invoice_number', sa.String(length=50), nullable=True))
    op.add_column('paypaltransaction', sa.Column('parent_transaction_id', sa.Integer(), nullable=True))
    op.add_column('paypaltransaction', sa.Column('paypal_payer_id', sa.String(length=50), nullable=True))
    op.add_column('paypaltransaction', sa.Column('sale_id', sa.String(length=50), nullable=True))
    op.add_column('paypaltransaction', sa.Column('update_time', sa.Date(), nullable=True))
    op.create_foreign_key(None, 'paypaltransaction', 'transaction', ['parent_transaction_id'], ['id'])
    op.create_foreign_key(None, 'paypaltransaction', 'paypalprofile', ['paypal_payer_id'], ['payer_id'])
    op.add_column('smsmessage', sa.Column('message_sender', sa.String(length=15), nullable=True))
    op.drop_constraint(u'smsmessage_ibfk_2', 'smsmessage', type_='foreignkey')
    op.drop_column('smsmessage', 'message_arguments')
    op.drop_column('smsmessage', 'template_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('smsmessage', sa.Column('template_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('smsmessage', sa.Column('message_arguments', mysql.VARCHAR(length=255), nullable=True))
    op.create_foreign_key(u'smsmessage_ibfk_2', 'smsmessage', 'confignotificationtemplate', ['template_id'], ['id'])
    op.drop_column('smsmessage', 'message_sender')
    op.drop_constraint(None, 'paypaltransaction', type_='foreignkey')
    op.drop_constraint(None, 'paypaltransaction', type_='foreignkey')
    op.drop_column('paypaltransaction', 'update_time')
    op.drop_column('paypaltransaction', 'sale_id')
    op.drop_column('paypaltransaction', 'paypal_payer_id')
    op.drop_column('paypaltransaction', 'parent_transaction_id')
    op.drop_column('paypaltransaction', 'invoice_number')
    op.add_column('emailmessage', sa.Column('template_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('emailmessage', sa.Column('email_arguments', mysql.VARCHAR(length=255), nullable=True))
    op.create_foreign_key(u'emailmessage_ibfk_1', 'emailmessage', 'confignotificationtemplate', ['template_id'], ['id'])
    op.drop_column('emailmessage', 'message_sender')
    op.drop_constraint(None, 'configwebhookeventtype', type_='unique')
    op.drop_constraint(None, 'configpaypalaccountwebhook', type_='unique')
    op.drop_constraint(None, 'configledgeraccountingrule', type_='foreignkey')
    op.drop_constraint(None, 'configledgeraccountingrule', type_='foreignkey')
    op.drop_constraint(None, 'configledgeraccountingrule', type_='foreignkey')
    op.create_foreign_key(u'configledgeraccountingrule_ibfk_2', 'configledgeraccountingrule', 'configledgeraccount', ['debit_account_id'], ['id'])
    op.create_foreign_key(u'configledgeraccountingrule_ibfk_1', 'configledgeraccountingrule', 'configledgeraccount', ['credit_account_id'], ['id'])
    op.create_foreign_key(u'configledgeraccountingrule_ibfk_3', 'configledgeraccountingrule', 'configtransactiontype', ['transaction_type_id'], ['id'])
    op.drop_constraint(None, 'configexchangerate', type_='unique')
    ### end Alembic commands ###
