from ajabpay.index import db
from ajabpay.app.core.utils import (round_down, round_up)
from decimal import Decimal as D

class PaypalProfile(db.Model):
    __tablename__ = "paypalprofile"
    
    id = db.Column(db.Integer(), primary_key=True)

    user = db.relationship('User', backref='paypal_profile', uselist=False,
        primaryjoin='User.email==PaypalProfile.email')
    email = db.Column(db.String(100), db.ForeignKey('user.email'), unique=True, nullable=False)

    address = db.relationship('PaypalAddress', backref='paypal_addresses', uselist=False)
    paypal_user_id = name = db.Column(db.String(100), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    given_name = db.Column(db.String(100), nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    
    gender = db.Column(db.String(10), nullable=True)

    phone_number = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date(), nullable=False)

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

class ConfigPaypalParameter(db.Model):
    __tablename__ = "configpaypalparameter"
    
    id = db.Column(db.Integer(), primary_key=True)

    paypal_charge_percentage = db.Column(db.Numeric(10,2), default=D('0.0')) #3%
    paypal_charge_constant = db.Column(db.Numeric(10,2), default=D('0.0')) #$0.3
    paypal_charge_constant_currency = db.Column(db.String(3), default='USD')

    local_currency = db.Column(db.String(3), default='KES')
    foreign_currency = db.Column(db.String(3), default='USD')
    foreign_exchange_rate = db.Column(db.Numeric(10,2), default=D('0.0')) #101.4 KES

    foreign_charge_percentage = db.Column(db.Numeric(10,2), default=D('0.0')) #0%
    foreign_charge_constant = db.Column(db.Numeric(10,2), default=D('0.0')) #3 KES
    foreign_charge_constant_currency = db.Column(db.String(3), default='KES')

    service_charge_percentage = db.Column(db.Numeric(10,2), default=D('0.0')) #4.5%
    service_charge_constant = db.Column(db.Numeric(5, 2), default=D('0.0')) #$1
    service_charge_constant_currency = db.Column(db.String(3), default='USD')

    service_charge_max = db.Column(db.Numeric(10,2), default=D('0.0')) #10000 KES
    service_charge_max_currency = db.Column(db.String(3), default='USD')

    mobile_money_charge = db.Column(db.Numeric(10,2), default=D('0.0')) #66 KES
    mobile_money_charge_currency = db.Column(db.String(3), default='KES')

    date_created = db.Column(db.DateTime(), nullable=False)

    def _do_foreign_exchange(self, amount, from_currency='USD', 
        to_currency='KES', exchange_rate=None):
        acceptable_currencies = (self.foreign_currency, self.local_currency)

        if from_currency not in acceptable_currencies:
            return
        elif to_currency not in acceptable_currencies:
            return
        elif from_currency == self.local_currency and to_currency == self.foreign_currency:
            return amount
        elif from_currency == self.foreign_currency and to_currency == self.local_currency:
            return ((exchange_rate or self.foreign_exchange_rate) * amount)
        else:
            return D('0.0')

    def _get_paypal_percentage(self, amount, currency=None):
        percentage = self.paypal_charge_percentage / D('100')
        percentage_charge = (amount * percentage)

        if currency is None:
            currency = self.foreign_currency #usd presumably

        return percentage_charge + self.paypal_charge_constant
    
    def _get_foreign_charge(self, subtotal, currency=None):
        if currency is None:
            currency = self.foreign_charge_constant_currency
        
        percentage_charge = D('0')
        if self.foreign_charge_percentage:
            percentage = self.foreign_charge_percentage / D('100')
            percentage_charge = (subtotal * percentage)

        constant_charge = D('0.0')
        if currency == self.foreign_charge_constant_currency:
            constant_charge = self.foreign_charge_constant
        elif not currency == self.foreign_charge_constant_currency:
            constant_charge = self._do_foreign_exchange(
                self.foreign_charge_constant, 
                from_currency=self.foreign_charge_constant_currency, 
                to_currency=self.local_currency)

        return (percentage_charge + constant_charge)

    def _get_service_charge(self, subtotal, currency=None):
        def get_percentage_service_charge(amount): 
            return (amount * (self.service_charge_percentage / D('100')))

        percentage_service_charge = get_percentage_service_charge(subtotal)

        if currency is None:
            currency = self.service_charge_constant_currency

        constant_charge = D('0.0')
        if currency == self.service_charge_constant_currency:
            constant_charge = self.service_charge_constant
        else:
            constant_charge = self._do_foreign_exchange(
                self.service_charge_constant, from_currency=currency, 
                to_currency=self.service_charge_constant_currency)

        return min(
            percentage_service_charge + (constant_charge or D('0.0')), 
            self._do_foreign_exchange(self.service_charge_max,
                from_currency=self.service_charge_max_currency, to_currency=currency))

    def _get_mobile_money_charge(self, currency=None):
        if currency is None:
            currency = self.mobile_money_charge_currency
        
        if currency == self.mobile_money_charge_currency:
            return self.mobile_money_charge
        else:
            return self._do_foreign_exchange(self.mobile_money_charge,
                from_currency=currency, to_currency=self.mobile_money_charge_currency)

    def get_exchange_amount(self, amount, from_currency=None, to_currency=None):
        if from_currency is None or to_currency is None:
            from_currency = self.foreign_currency
            to_currency = self.local_currency
        
        #--------------- less paypal charge
        paypal_charge = 0
        if self.paypal_charge_percentage and self.paypal_charge_constant:
            paypal_charge = self._get_paypal_percentage(amount, currency=from_currency)
        
        less_paypal_charge = amount - paypal_charge

        #--------------- less service charge
        service_charge = self._get_service_charge(less_paypal_charge, currency=from_currency)
        less_service_charge = less_paypal_charge - service_charge

        #--------------- less foreign exchange charge
        foreign_exchange_rate = self.foreign_exchange_rate
        foreign_exchange_rate_currency = self.local_currency

        foreign_charge = self._get_foreign_charge(
            foreign_exchange_rate, currency=foreign_exchange_rate_currency)
        exchange_rate = foreign_exchange_rate - foreign_charge
        
        #--------------- perform foreign exchange
        foreign_exchange = self._do_foreign_exchange(less_service_charge, 
            exchange_rate=exchange_rate)
            
        mobile_money_charge = self._get_mobile_money_charge(to_currency)
        total = foreign_exchange - mobile_money_charge

        if total > 0:
            return dict(
                equivalent_amount=less_paypal_charge,
                total=round_down(total))

        return dict(
            equivalent_amount=0, total=0)

    def get_effective_rate(amount):
        total_charge = self.get_total_charge(amount)

