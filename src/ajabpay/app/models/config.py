from ajabpay.index import db
from decimal import Decimal as D

class ConfigPaypalAPIAccount(db.Model):
    __tablename__ = "configpaypalapiaccount"
    
    id = db.Column(db.Integer(), primary_key=True)

    access_id = db.Column(db.String(100))
    private_key = db.Column(db.String(100))

    credit_card_enabled = db.Column(db.Boolean, default=False)

    date_created = db.Column(db.Date())

class ConfigExchangeRate(db.Model):
    __tablename__ = "configexchangerate"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(50))

    local_currency = db.Column(db.String(3))
    foreign_currency = db.Column(db.String(3))

    buying  = db.Column(db.Numeric(6, 2))
    selling = db.Column(db.Numeric(6, 2))

    date_created = db.Column(db.Date())
    
class ConfigProductType(db.Model):
    __tablename__ = "configproducttype"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(20), unique=True)

class ConfigCurrency(db.Model):
    __tablename__ = "configcurrency"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(10), unique=True)

    is_active = db.Column(db.Boolean, default=False)

class ConfigAccountStatus(db.Model):
    __tablename__ = "configaccountstatus"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)

class ConfigTransactionStatus(db.Model):
    __tablename__ = "configtransactionstatus"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)

class ConfigLedgerAccountCategory(db.Model):
    __tablename__ = "configledgeraccountcategory"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)

class ConfigTransactionType(db.Model):
    __tablename__ = "configtransactiontype"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100), unique=True)
    code = db.Column(db.String(100))

class ConfigLedgerAccount(db.Model):
    __tablename__ = "configledgeraccount"
    
    # __tablename__ = "configledgeraccount"
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100), unique=True)
    code = db.Column(db.String(100), unique=True)

    account_category_id = db.relationship('ConfigLedgerAccountCategory')
    account_category_id = db.Column(db.Integer, db.ForeignKey('configledgeraccountcategory.id'))
    
    #contra|normal
    balance_direction = db.Column(db.Integer())

    date_created = db.Column(db.Date())

class ConfigLedgerAccountingRule(db.Model):
    __tablename__ = "configledgeraccountingrule"
    
    id = db.Column(db.Integer(), primary_key=True)
    
    transaction_type = db.relationship('ConfigTransactionType', backref='accounting_rules')
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('configtransactiontype.id'))

    debit_account = db.relationship('ConfigLedgerAccount', backref='debits')
    debit_account_id = db.Column(db.Integer, db.ForeignKey('configledgeraccount.id'))

    credit_account = db.relationship('ConfigLedgerAccount', backref='credits')
    credit_account_id = db.Column(db.Integer, db.ForeignKey('configledgeraccount.id'))

    date_created = db.Column(db.Date())

class ConfigSMSGateway(db.Model):
    __tablename__ = "configsmsgateway"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)

    endpoint = db.Column(db.String(255))

class ConfigSMSTemplate(db.Model):
    __tablename__ = "configsmstemplate"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)

    template = db.Column(db.String(160))

class SMSMessage(db.Model):
    __tablename__ = "smsmessage"
    
    INCOMING = 0
    OUTGOING = 1

    id = db.Column(db.Integer(), primary_key=True)

    #incoming|outgoing
    message_type = db.Column(db.Integer(), default=INCOMING)
    message_text = db.Column(db.String(160))
    message_recipient = db.Column(db.String(15))

    sms_gateway_id = db.Column(db.Integer, db.ForeignKey('configsmsgateway.id'))
    sms_gateway = db.relationship('ConfigSMSGateway')

    sms_template_id = db.Column(db.Integer, db.ForeignKey('configsmstemplate.id'))
    sms_template = db.relationship('ConfigSMSTemplate')

    delivered = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.Date())
