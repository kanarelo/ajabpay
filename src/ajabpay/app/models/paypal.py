from ajabpay.index import db
from decimal import Decimal as D

class PaypalProfile(db.Model):
    __tablename__ = "paypalprofile"
    
    id = db.Column(db.Integer(), primary_key=True)

    user = db.relationship('User', backref='paypal_profile', uselist=False,
        primaryjoin='User.email==PaypalProfile.email')
    email = db.Column(db.String(100), db.ForeignKey('user.email'), unique=True, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref='paypal_accounts')

    address = db.relationship('PaypalAddress', backref='paypal_addresses')

    payer_id = db.Column(db.String(20), unique=True, nullable=False)
    paypal_user_id = name = db.Column(db.String(50), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    given_name = db.Column(db.String(100), nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    phone_number = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=False)

    email_verified = db.Column(db.Boolean, default=False, nullable=True)
    verified_account = db.Column(db.Boolean, default=False, nullable=False)

    account_type = db.Column(db.String(10), nullable=False)
    account_creation_date = db.Column(db.DateTime(), nullable=False)

    date_created = db.Column(db.DateTime(), nullable=False)
    date_updated = db.Column(db.DateTime(), nullable=False)

    def __unicode__(self):
        return '[%s] %s' % (self.paypal_user_id, self.email)

class PaypalAddress(db.Model):
    __tablename__ = "paypaladdress"
    
    id = db.Column(db.Integer(), primary_key=True)

    paypal_profile    = db.relationship('PaypalProfile', backref='addresses')
    paypal_profile_id = db.Column(db.Integer, db.ForeignKey('paypalprofile.id'), nullable=False)

    street_address = db.Column(db.String(100), nullable=False)
    locality = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(15), nullable=True)
    country = db.Column(db.String(3), nullable=False)

    date_created = db.Column(db.DateTime(), nullable=False)

class PaypalToken(db.Model):
    __tablename__ = "paypaltoken"
    
    id = db.Column(db.Integer(), primary_key=True)

    payer = db.relationship('PaypalProfile', backref='paypal_tokens',
        primaryjoin='PaypalProfile.payer_id==PaypalToken.payer_id',
        secondary=PaypalProfile.__table__,
        secondaryjoin='PaypalProfile.paypal_user_id==PaypalToken.paypal_user_id')
    payer_id = db.Column(db.String(50), db.ForeignKey('paypalprofile.payer_id'), nullable=True)
    paypal_user_id = db.Column(db.String(50), db.ForeignKey('paypalprofile.paypal_user_id'), nullable=True)

    scope = db.Column(db.String(100))

    access_token = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255), nullable=True)
    token_type = db.Column(db.String(15), nullable=False)
    expires_in = db.Column(db.Integer(), nullable=False)

    exires_at = db.Column(db.DateTime(), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False)


round_up = lambda (amount): ((amount * D('100')).to_integral_value()) / D('100')
round_down = lambda (amount) : ((amount * D('100')).to_integral_value()) / D('100')

class ConfigPaypalParameter(db.Model):
    __tablename__ = "configpaypalparameter"
    
    id = db.Column(db.Integer(), primary_key=True)

    paypal_charge_percentage = db.Column(db.Numeric(10,2), default=D('0.0')) #3
    paypal_charge_constant = db.Column(db.Numeric(10,2), default=D('0.0')) #0.3

    foreign_exchange_rate = db.Column(db.Numeric(10,2), default=D('0.0')) #101.4
    foreign_charge_percentage = db.Column(db.Numeric(10,2), default=D('0.0')) #1.5
    foreign_charge_constant = db.Column(db.Numeric(10,2), default=D('0.0')) #75

    service_charge_percentage = db.Column(db.Numeric(10,2), default=D('0.0')) #4.5
    service_charge_max = db.Column(db.Numeric(10,2), default=D('0.0')) #250
    mobile_money_charge = db.Column(db.Numeric(10,2), default=D('0.0')) #33

    date_created = db.Column(db.DateTime())

    def _get_percentage_service_charge(self, amount): 
        return (amount * (self.service_charge_percentage / D('100')))

    def _do_foreign_exchange(self, foreign_amount, currency='USD'):
        return (self.foreign_exchange_rate * foreign_amount)

    def _deduct_paypal_percentage(self, foreign_amount):
        difference = (D('100') - self.paypal_charge_percentage) / D('100') 
        return round_up((foreign_amount * difference) - self.paypal_charge_constant)
    
    def _deduct_foreign_charge(self, subtotal):
        difference = (D('100') - self.foreign_charge_percentage) / D('100') 
        return round_up((subtotal * difference) - self.foreign_charge_constant)

    def _deduct_service_charge(self, subtotal):
        service_charge = self._get_percentage_service_charge(subtotal)
        minimum_deduction = min(service_charge, self.service_charge_max)

        return round_up(subtotal - minimum_deduction)

    def _deduct_mobile_money_charge(self, subtotal): 
        return round_up(subtotal - self.mobile_money_charge)

    def get_exchange_amount(self, amount, currency='USD'):
        foreign_total = self._deduct_paypal_percentage(amount)

        subtotal = self._do_foreign_exchange(foreign_total, currency=currency)
        subtotal = self._deduct_foreign_charge(subtotal)
        subtotal = self._deduct_service_charge(subtotal)
        total = self._deduct_mobile_money_charge(subtotal)

        return total

    def get_effective_rate(amount):
        total_charge = self.get_total_charge(amount)

# --------------------------------------------
# PP: 3% and $.3 = $96.7
# FX: 101.4
# --------------------------------------------
# SUBTOTAL: 9,805.38
# --------------------------------------------

# FX: 1.5% + 75 KES 
# --------------------------------------------
# SUBTOTAL: (9,805.38 * 98.5%) - 75 = 9,583.29
# --------------------------------------------

# US: min((4.5% + 33), (250 + 33)) KES
# --------------------------------------------
# SUBTOTAL: (9,583.29 - 250) - 33 = 9,300.29
# --------------------------------------------

# --------------------------------------------
# EFFECTIVE RATE: KES. 93
# --------------------------------------------