from ajabpay.index import db
from decimal import Decimal as D

from sqlalchemy_utils import ChoiceType

class ConfigPaypalAPIAccount(db.Model):
    __tablename__ = "configpaypalapiaccount"
    
    id = db.Column(db.Integer(), primary_key=True)

    account_email = db.Column(db.String(100))
    client_id = db.Column(db.String(100))
    client_secret = db.Column(db.String(100))

    live = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime())

    def __unicode__(self):
        return self.account_email

class ConfigWebhookEventType(db.Model):
    __tablename__ = "configwebhookeventtype"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(50))

    is_active = db.Column(db.Boolean, default=False)

    def __unicode__(self):
        return self.name

class ConfigPaypalAccountWebhook(db.Model):
    __tablename__ = "configpaypalaccountwebhook"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(50))

    paypal_api = db.relationship('ConfigPaypalAPIAccount')
    paypal_api_id = db.Column(db.Integer, db.ForeignKey('configpaypalapiaccount.id'))

    url_for = db.Column(db.String(20))

    def __unicode__(self):
        return self.name

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

class ConfigLedgerAccount(db.Model):
    __tablename__ = "configledgeraccount"

    BALANCE_DIRECTIONS = (
        ('NORMAL', 'NORMAL'),
        ('CONTRA', 'CONTRA')
    )
    
    # __tablename__ = "configledgeraccount"
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100), unique=True)
    code = db.Column(db.String(100), unique=True)

    account_category = db.relationship('ConfigLedgerAccountCategory')
    account_category_id = db.Column(db.Integer, db.ForeignKey('configledgeraccountcategory.id'))
    
    #contra|normal
    balance_direction = db.Column(ChoiceType(BALANCE_DIRECTIONS))

    date_created = db.Column(db.DateTime())

    def __unicode__(self):
        return self.name

class ConfigLedgerAccountingRule(db.Model):
    __tablename__ = "configledgeraccountingrule"
    
    id = db.Column(db.Integer(), primary_key=True)
    
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

    def __unicode__(self):
        return self.name

class ConfigNotificationTemplate(db.Model):
    __tablename__ = "confignotificationtemplate"
    
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(100))
    code = db.Column(db.String(100), unique=True)

    notification_type_id = db.Column(db.Integer, 
        db.ForeignKey('confignotificationtype.id'))
    notification_type = db.relationship('ConfigNotificationType')

    email_template = db.Column(db.String(500))
    sms_template = db.Column(db.String(160))

    def __unicode__(self):
        return self.name

class SMSMessage(db.Model):
    __tablename__ = "smsmessage"
    
    INCOMING = 0
    OUTGOING = 1

    id = db.Column(db.Integer(), primary_key=True)

    #incoming|outgoing
    message_type = db.Column(db.Integer(), default=INCOMING)
    message_arguments = db.Column(db.String(255))
    message_recipient = db.Column(db.String(15))

    sms_gateway_id = db.Column(db.Integer, db.ForeignKey('configsmsgateway.id'))
    sms_gateway = db.relationship('ConfigSMSGateway')

    template_id = db.Column(db.Integer, db.ForeignKey('confignotificationtemplate.id'))
    template = db.relationship('ConfigNotificationTemplate')

    delivered = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime())
    date_delivered = db.Column(db.DateTime())

class EmailMessage(db.Model):
    __tablename__ = "emailmessage"
    
    INCOMING = 0
    OUTGOING = 1

    id = db.Column(db.Integer(), primary_key=True)

    #incoming|outgoing
    email_type = db.Column(db.Integer(), default=INCOMING)
    email_arguments = db.Column(db.String(255))
    message_recipient = db.Column(db.String(100))

    template_id = db.Column(db.Integer, db.ForeignKey('confignotificationtemplate.id'))
    template = db.relationship('ConfigNotificationTemplate')

    delivered = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime())
    date_delivered = db.Column(db.DateTime())
