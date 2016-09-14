from ajabpay.index import db
from decimal import Decimal as D

class Product(db.Model):
    __tablename__ = "product"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(10))

    is_active = db.Column(db.Boolean, default=True)

    product_type_id = db.Column(db.Integer, db.ForeignKey('configproducttype.id'))
    product_type = db.relationship('ConfigProductType', backref='type_accounts')

    amount_currency_id = db.Column(db.Integer, db.ForeignKey('configcurrency.id'))
    amount_currency = db.relationship('ConfigCurrency')

    txn_withdrawal_limit = db.Column(db.Numeric(6, 2), default=D('0.0'))
    txn_deposit_limit  = db.Column(db.Numeric(6,2), default=D('0.0'))

    daily_withdraw_limit = db.Column(db.Numeric(6, 2), default=D('0.0'))
    daily_deposit_limit  = db.Column(db.Numeric(6,2), default=D('0.0'))

    weekly_withdraw_limit = db.Column(db.Numeric(6, 2), default=D('0.0'))
    weekly_deposit_limit  = db.Column(db.Numeric(6,2), default=D('0.0'))

    monthly_withdraw_limit = db.Column(db.Numeric(6, 2), default=D('0.0'))
    monthly_deposit_limit  = db.Column(db.Numeric(6,2), default=D('0.0'))

    yearly_withdraw_limit = db.Column(db.Numeric(6, 2), default=D('0.0'))
    yearly_deposit_limit  = db.Column(db.Numeric(6,2), default=D('0.0'))

    date_updated = db.Column(db.Date())
    date_created = db.Column(db.Date())

class Account(db.Model):
    __tablename__ = "account"
    
    id = db.Column(db.Integer(), primary_key=True)

    account_number = db.Column(db.String(20), unique=True)

    user    = db.relationship('User', backref='product_accounts')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    product = db.relationship('Product', backref='accounts')
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    notes = db.Column(db.String(400))
    account_status_date = db.Column(db.Date())

    txn_withdraw_limit = db.Column(db.Numeric(6, 2), default=D('0.0'))
    txn_deposit_limit  = db.Column(db.Numeric(6,2), default=D('0.0'))

    total_withdraws = db.Column(db.Numeric(6, 2), default=D('0.0'))
    total_deposits  = db.Column(db.Numeric(6,2), default=D('0.0'))
    
    last_deposit_date  = db.Column(db.Date())
    last_withdraw_date = db.Column(db.Date())

    date_created = db.Column(db.Date())
    date_updated = db.Column(db.Date())

class AccountStatus(db.Model):
    __tablename__ = "accountstatus"
    
    id = db.Column(db.Integer(), primary_key=True)

    account = db.relationship('Account', backref='statuses')
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    status_id = db.Column(db.Integer, db.ForeignKey('configaccountstatus.id'))
    status    = db.relationship('ConfigAccountStatus', backref='statuses')

    reason = db.Column(db.String(140))

    approved_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    approved_by    = db.relationship('User', backref='account_approvals')

    date_created = db.Column(db.Date())
