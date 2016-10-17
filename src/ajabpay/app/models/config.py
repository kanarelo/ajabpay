from ajabpay.index import db
from decimal import Decimal as D

from sqlalchemy_utils import ChoiceType

class ConfigExchangeRate(db.Model):
    __tablename__ = "configexchangerate"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(50), unique=True)

    local_currency = db.Column(db.String(3))
    foreign_currency = db.Column(db.String(3))

    buying  = db.Column(db.Numeric(6, 2))
    selling = db.Column(db.Numeric(6, 2))

    date_created = db.Column(db.DateTime())

    def __unicode__(self):
        return self.name
    
class ConfigProductType(db.Model):
    __tablename__ = "configproducttype"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(20), unique=True)

    def __unicode__(self):
        return self.name

class ConfigCurrency(db.Model):
    __tablename__ = "configcurrency"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(10), unique=True)

    is_active = db.Column(db.Boolean, default=False)

    def __unicode__(self):
        return self.name

class ConfigAccountStatus(db.Model):
    __tablename__ = "configaccountstatus"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)

    def __unicode__(self):
        return self.name

class ConfigTransactionStatus(db.Model):
    __tablename__ = "configtransactionstatus"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)

    def __unicode__(self):
        return self.name

class ConfigLedgerAccountCategory(db.Model):
    __tablename__ = "configledgeraccountcategory"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)

    def __unicode__(self):
        return self.name

class ConfigTransactionType(db.Model):
    __tablename__ = "configtransactiontype"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100), unique=True)
    code = db.Column(db.String(100))

    def __unicode__(self):
        return self.name

class ConfigPaypalTransactionType(db.Model):
    __tablename__ = "configpaypaltransactiontype"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(50), unique=True)

    def __unicode__(self):
        return self.name


class ConfigLedgerAccount(db.Model):
    __tablename__ = "configledgeraccount"

    NORMAL = 'NORMAL'
    CONTRA = 'CONTRA'
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100), unique=True)
    code = db.Column(db.String(100), unique=True)

    account_category = db.relationship('ConfigLedgerAccountCategory')
    account_category_id = db.Column(db.Integer, db.ForeignKey('configledgeraccountcategory.id'))
    
    #contra|normal
    balance_direction = db.Column(db.String(10), default=NORMAL)

    date_created = db.Column(db.DateTime())

    def __unicode__(self):
        return self.name

class ConfigLedgerAccountingRule(db.Model):
    __tablename__ = "configledgeraccountingrule"
    
    id = db.Column(db.Integer(), primary_key=True)

    product = db.relationship('Product')
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    
    transaction_type = db.relationship('ConfigTransactionType', backref='accounting_rules')
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('configtransactiontype.id'))

    debit_account_id = db.Column(db.Integer, db.ForeignKey('configledgeraccount.id'))
    debit_account = db.relationship('ConfigLedgerAccount', backref='debits', foreign_keys=[debit_account_id])

    credit_account_id = db.Column(db.Integer, db.ForeignKey('configledgeraccount.id'))
    credit_account = db.relationship('ConfigLedgerAccount', backref='credits', foreign_keys=[credit_account_id])

    date_created = db.Column(db.DateTime())

    def __unicode__(self):
        return self.transaction_type.name

class ConfigSMSGateway(db.Model):
    __tablename__ = "configsmsgateway"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)

    api_key = db.Column(db.String(100))
    api_secret = db.Column(db.String(255))

    endpoint = db.Column(db.String(255), nullable=True)

    def __unicode__(self):
        return self.name

class ConfigNotificationType(db.Model):
    __tablename__ = "confignotificationtype"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)

    email_template = db.Column(db.String(500), nullable=True)
    email_html_template = db.Column(db.String(500), nullable=True)
    sms_template = db.Column(db.String(160), nullable=True)

    date_created = db.Column(db.DateTime())

    def __unicode__(self):
        return self.name

class SMSMessage(db.Model):
    __tablename__ = "smsmessage"
    
    INCOMING = 0
    OUTGOING = 1

    id = db.Column(db.Integer(), primary_key=True)

    notification_type_id = db.Column(db.Integer, db.ForeignKey('confignotificationtype.id'), nullable=False)
    notification_type = db.relationship('ConfigNotificationType')

    message_type = db.Column(db.Integer(), default=INCOMING)
    message_sender = db.Column(db.String(15), nullable=True)
    message_recipient = db.Column(db.String(15), nullable=True)
    message = db.Column(db.String(320))

    delivered = db.Column(db.Boolean, default=False)
    date_delivered = db.Column(db.DateTime())
    
    date_created = db.Column(db.DateTime())    

class EmailMessage(db.Model):
    __tablename__ = "emailmessage"
    
    INCOMING = 0
    OUTGOING = 1

    id = db.Column(db.Integer(), primary_key=True)

    email_type = db.Column(db.Integer(), default=OUTGOING)

    notification_type_id = db.Column(db.Integer, db.ForeignKey('confignotificationtype.id'), nullable=False)
    notification_type = db.relationship('ConfigNotificationType')

    message_subject = db.Column(db.String(255))
    
    message_recipient = db.Column(db.String(100))
    message_sender = db.Column(db.String(100))

    delivered = db.Column(db.Boolean, default=False)
    date_delivered = db.Column(db.DateTime())

    date_created = db.Column(db.DateTime())
