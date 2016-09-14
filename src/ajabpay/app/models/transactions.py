from ajabpay.index import db
from decimal import Decimal as D

class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    transaction_no = db.Column(db.String(100), unique=True)
    transaction_type = db.relationship('ConfigTransactionType')
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('configtransactiontype.id'))

    account = db.relationship('Account')
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    reversing_transaction = db.relationship('Transaction', remote_side=[id], backref='reversals')
    reversing_transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))

    currency_id = db.Column(db.Integer, db.ForeignKey('configcurrency.id'))
    currency = db.relationship('ConfigCurrency')

    amount = db.Column(db.Numeric(18,2), default=D('0.0'))

    details = db.Column(db.String(255))
    notified = db.Column(db.Boolean, default=True)

    status = db.relationship('ConfigTransactionStatus')
    status_id = db.Column(db.Integer, db.ForeignKey('configtransactionstatus.id'))

    paypal_transaction = db.relationship("PaypalTransaction", back_populates="pptransaction", uselist=False)
    mpesa_transaction = db.relationship("MPesaTransaction", back_populates="mtransaction", uselist=False) 

    status_date = db.Column(db.Date())
    date_created = db.Column(db.Date())

class PaypalTransaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    paypal_transaction_id = db.Column(db.String(50), unique=True)

    transaction    = db.relationship('Transaction', backref='paypal_transactions')
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))

    create_time = db.Column(db.Date())
    state = db.Column(db.String(50))
    intent = db.Column(db.String(20))
    payment_method = db.Column(db.String(20))

    date_created = db.Column(db.Date())

class MPesaTransaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    mpesa_transaction_no = db.Column(db.String(100), unique=True)

    transaction    = db.relationship('Transaction', backref='mpesa_transactions')
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))

    date_created = db.Column(db.Date())

class TransactionStatus(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    transaction = db.relationship('Transaction', backref='transaction_statuses')
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))

    status = db.relationship('ConfigTransactionStatus', backref='transaction_statuses')
    status_id = db.Column(db.Integer, db.ForeignKey('configtransactionstatus.id'))

    transaction_status_date = db.Column(db.Date())
    details = db.Column(db.String(400))

    date_created = db.Column(db.Date())

class TransactionEntry(db.Model):
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

    date_created = db.Column(db.Date())
