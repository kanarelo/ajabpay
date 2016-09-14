from ajabpay.index import db
from decimal import Decimal as D

class PaypalProfile(db.Model):
    __tablename__ = "paypalprofile"
    
    id = db.Column(db.Integer(), primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user    = db.relationship('User', backref='paypal_profile')

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account    = db.relationship('Account', backref='paypal_accounts')

    address = db.relationship('Address', backref='paypal_addresses')

    payer_id = db.Column(db.String(20), unique=True)
    paypal_user_id = name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)

    name = db.Column(db.String(100))
    given_name = db.Column(db.String(100))
    family_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    gender = db.Column(db.String(1))
    phone_number = db.Column(db.String(100))
    age_range = db.Column(db.String(10))

    email_verified = db.Column(db.Boolean, default=True)
    verified_account = db.Column(db.Boolean, default=False)
    account_type = db.Column(db.String(10))

    date_created = db.Column(db.Date())
    date_updated = db.Column(db.Date())

# class PaypalHistory(db.Model):
#     __tablename__ = "paypalhistory"
    
#     id = db.Column(db.Integer(), primary_key=True)

class PaypalAddress(db.Model):
    __tablename__ = "paypaladdress"
    
    id = db.Column(db.Integer(), primary_key=True)

    paypal_profile    = db.relationship('PaypalProfile', backref='addresses')
    paypal_profile_id = db.Column(db.Integer, db.ForeignKey('paypalprofile.id'))

    street_address = db.Column(db.String(100))
    locality = db.Column(db.String(50))
    region = db.Column(db.String(50))
    postal_code = db.Column(db.String(15))
    country = db.Column(db.String(100))

    date_created = db.Column(db.Date())

class PaypalToken(db.Model):
    __tablename__ = "paypaltoken"
    
    id = db.Column(db.Integer(), primary_key=True)

    paypal_profile    = db.relationship('PaypalProfile', backref='paypal_tokens')
    paypal_profile_id = db.Column(db.Integer, db.ForeignKey('paypalprofile.id'))

    scope = db.Column(db.String(100))

    access_token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    token_type = db.Column(db.String(15))
    expires_in = db.Column(db.Integer())

    exires_at = db.Column(db.Date())
    date_created = db.Column(db.Date())
