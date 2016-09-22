from ajabpay.index import db
from decimal import Decimal as D

from .config import *

class Transaction(db.Model):
    __tablename__ = "transaction"
    
    id = db.Column(db.Integer(), primary_key=True)

    transaction_no = db.Column(db.String(100), unique=True)
    transaction_type = db.relationship('ConfigTransactionType')
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('configtransactiontype.id'))

    account = db.relationship('Account')
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    reversing_transaction = db.relationship('Transaction', remote_side=[id], backref='reversal', uselist=False)
    reversing_transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=True)

    currency_id = db.Column(db.Integer, db.ForeignKey('configcurrency.id'))
    currency = db.relationship('ConfigCurrency')

    amount = db.Column(db.Numeric(18,2), default=D('0.0'))

    details = db.Column(db.String(255), nullable=True)
    notified = db.Column(db.Boolean, default=False)

    date_created = db.Column(db.DateTime())

    def __unicode__(self):
        return '%s' % self.transaction_no

class PaypalTransaction(db.Model):
    __tablename__ = "paypaltransaction"
    
    id = db.Column(db.Integer(), primary_key=True)
    paypal_transaction_type_code = db.Column(db.String(50), nullable=False)
    
    paypal_payer_id = db.Column(db.String(50), db.ForeignKey('paypalprofile.payer_id'), nullable=True)
    paypal_payer = db.relationship('PaypalProfile', backref='transactions',
        primaryjoin="PaypalProfile.payer_id==PaypalTransaction.paypal_payer_id")

    transaction = db.relationship('Transaction', backref='paypal_transactions', uselist=False,
        primaryjoin="Transaction.transaction_no==PaypalTransaction.paypal_transaction_id")
    paypal_transaction_id = db.Column(db.String(50), db.ForeignKey('transaction.transaction_no'), unique=True)

    sale_id = db.Column(db.String(50), nullable=True)
    invoice_number = db.Column(db.String(50), nullable=True)

    parent_transaction_id = db.Column(db.String(50), db.ForeignKey('transaction.transaction_no'), nullable=True)
    parent_transaction = db.relationship('Transaction', backref='child_transactions', uselist=False,
        primaryjoin="PaypalTransaction.parent_transaction_id==Transaction.transaction_no")

    create_time = db.Column(db.DateTime(), nullable=False)
    update_time = db.Column(db.DateTime(), nullable=False)

    state = db.Column(db.String(50), nullable=False)
    intent = db.Column(db.String(20), nullable=True)
    payment_method = db.Column(db.String(20), nullable=True)

    date_created = db.Column(db.DateTime(), nullable=False)

    def __unicode__(self):
        return '%s' % self.paypal_transaction_id

class MPesaTransaction(db.Model):
    __tablename__ = "mpesatransaction"
    
    id = db.Column(db.Integer(), primary_key=True)

    transaction = db.relationship('Transaction', backref='mpesa_transactions', uselist=False,
        primaryjoin="Transaction.transaction_no==MPesaTransaction.mpesa_transaction_no")
    mpesa_transaction_no = db.Column(db.String(50), 
        db.ForeignKey('transaction.transaction_no'), unique=True)

    # recipient = db.relationship('MPesaProfile', backref='transactions',
    #     primaryjoin="MPesaProfile.mobile_phone_no==MPesaTransaction.recipient_phone_no")
    # recipient_phone_no = db.Column(db.String(50), 
    #     db.ForeignKey('mpesaprofile.mobile_phone_no'), nullable=False)

    total_amount = db.Column(db.String(50), nullable=False)
    total_amount_currency = db.Column(db.String(4), nullable=False, default='KES')
    
    reference_id = db.Column(db.String(50), nullable=True)
    merchant_transaction_id = db.Column(db.String(50), nullable=True)

    #on response:


    date_created = db.Column(db.DateTime())

    def __unicode__(self):
        return '%s' % self.mpesa_transaction_no

class TransactionStatus(db.Model):
    __tablename__ = "transactionstatus"
    
    id = db.Column(db.Integer(), primary_key=True)

    transaction = db.relationship('Transaction', backref='transaction_statuses')
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))

    status = db.relationship('ConfigTransactionStatus', backref='transaction_statuses')
    status_id = db.Column(db.Integer, db.ForeignKey('configtransactionstatus.id'))

    details = db.Column(db.String(400), nullable=True)

    date_created = db.Column(db.DateTime())

    def __unicode__(self):
        return '%s %s' % (self.transaction, self.status)

class TransactionEntry(db.Model):
    __tablename__ = "transactionentry"
    
    (DEBIT, CREDIT) = (0, 1)
    (ITEM_TYPES) = ((DEBIT, 'Debit'), (CREDIT, 'Credit'))

    id = db.Column(db.Integer(), primary_key=True)
    
    transaction = db.relationship('Transaction', backref='transaction_entries')
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))

    account = db.relationship('Account', backref='account_entries')
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    ledger_account = db.relationship('ConfigLedgerAccount')
    ledger_account_id = db.Column(db.Integer, db.ForeignKey('configledgeraccount.id'))

    item_type = db.Column(db.Integer())
    balance_increment = db.Column(db.Numeric(6,2), default=D('0.0'))

    date_created = db.Column(db.DateTime())

    def __unicode__(self):
        return '%s %s' % (self.transaction, self.item_type)