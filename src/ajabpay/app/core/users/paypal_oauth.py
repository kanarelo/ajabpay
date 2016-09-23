import json
import os
import string
import random
import dateutil.parser

from ajabpay.index import app, db
from ajabpay.app.core.utils import get_reference_no
from ajabpay.app.models import *

import paypalrestsdk
from paypalrestsdk.openid_connect import Tokeninfo

from ajabpay.config import BaseConfig

def generate_random_password(length=15):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))

# paypalrestsdk.configure(dict(
#     mode=BaseConfig.PAYPAL_MODE,
#     client_id=BaseConfig.PAYPAL_CLIENT_ID,
#     client_secret=BaseConfig.PAYPAL_CLIENT_SECRET,
#     openid_client_id=BaseConfig.PAYPAL_CLIENT_ID,
#     openid_client_secret=BaseConfig.PAYPAL_CLIENT_SECRET,
#     openid_redirect_uri=BaseConfig.PAYPAL_OAUTH_REDIRECT_URI,
# ))

# options = dict(
#     scope='openid profile email address phone https://uri.paypal.com/services/paypalattributes'
# )

# login_url = Tokeninfo.authorize_url(options=options)

# print login_url

# code = raw_input('Authorize code: ')

# options['code'] = code
# tokeninfo = Tokeninfo.create(options=options)

# print 'tokeninfo', tokeninfo

# userinfo = tokeninfo.userinfo(options=options)

# print 'tokeninfo.userinfo', dir(userinfo), userinfo

# tokeninfo = tokeninfo.refresh(options=options)

# print 'tokeninfo.refresh', json.loads(userinfo)

# logout_url = tokeninfo.logout_url(options=options)

# print 'tokeninfo.logout_url', logout_url

def get_phone_number(phone_number):
    return '+254%s' % phone_number

def extract_paypal_user_id(user_id):
    regex = r'^https://www.paypal.com/webapps/auth/identity/user/(?P<slug>[-\w]+)$'
    
    return user_id

def create_user_object(userinfo):
    with db.session.begin_nested():
        first_name = userinfo.get('given_name')
        last_name = userinfo.get('family_name')
        email = userinfo.get('email')
        phone = userinfo.get('phone_number')
        password = generate_random_password()
        date_created = db.func.now()

        user = User(
            first_name=first_name, 
            last_name=last_name,
            email=email, 
            phone=get_phone_number(phone),
            password=password, 
            date_created=date_created,
            date_updated=date_created,
            date_joined=date_created
        )
        db.session.add(user)

        return user

def create_mpesa_profile(userinfo, account):
    with db.session.begin_nested():
        user = account.user
        date_created = db.func.now()
        
        mpesa_profile = MPesaProfile(
            account_id=account.id,
            user_id=user.id,
            mobile_phone_no=user.phone,
            date_created=date_created,
            date_updated=date_created,
        )
        
        db.session.add(mpesa_profile)
        return mpesa_profile

def create_paypal_profile(userinfo, account):
    user = account.user
    date_created = db.func.now()

    def create_paypal_address(addressinfo, paypal_profile):
        with db.session.begin_nested():
            paypal_address = PaypalAddress(
                paypal_profile_id=paypal_profile.id,
                street_address=addressinfo.get('street_address'),
                locality=addressinfo.get('locality'),
                region=addressinfo.get('region'),
                postal_code=addressinfo.get('postal_code'),
                country=addressinfo.get('country'),
                date_created=date_created
            )

            db.session.add(paypal_address)

            return paypal_address

    with db.session.begin_nested():
        paypal_profile = PaypalProfile(
            email=user.email,
            account_id=account.id,
            paypal_user_id=extract_paypal_user_id(userinfo.get('user_id')),
            name=user.get_full_name(),
            given_name=user.last_name,
            family_name=user.first_name,
            middle_name=userinfo.get('middle_name'),
            gender=userinfo.get('gender'),
            birthday=dateutil.parser.parse(userinfo.get('birthday')),
            phone_number=get_phone_number(userinfo.get('phone_number')),
            email_verified=userinfo.get('email_verified') == 'true',
            verified_account=userinfo.get('verified_account') == 'true',
            account_creation_date=dateutil.parser.parse(userinfo.get('account_creation_date')),
            account_type=userinfo.get('account_type'),
            date_created=date_created,
            date_updated=date_created
        )
        db.session.add(paypal_profile)

        addressinfo = userinfo.get('address')
        if addressinfo is not None:
            create_paypal_address(addressinfo, paypal_profile)

def create_account_object(userinfo, user, product, account_number=None):
    with db.session.begin_nested(): 
        user_id = user.id

        account_number = None
        while account_number is None:
            account_number = '{0}.{1}.{2}'.format(
                product.code, user_id, get_reference_no(limit=6))

            a = Account.query\
                .filter_by(account_number=account_number)\
                .first()

            if a is not None:
                account_number = None

            print ">?"

        date_created = db.func.now()

        account = Account(
            account_number=account_number,
            user_id=user_id,
            product=product,
            amount_currency_id=product.amount_currency_id,
            txn_withdrawal_limit=product.txn_withdrawal_limit,
            txn_deposit_limit=product.txn_deposit_limit,
            daily_withdraw_limit=product.daily_withdraw_limit,
            daily_deposit_limit=product.daily_deposit_limit,
            weekly_withdraw_limit=product.weekly_withdraw_limit,
            weekly_deposit_limit=product.weekly_deposit_limit,
            monthly_withdraw_limit=product.monthly_withdraw_limit,
            monthly_deposit_limit=product.monthly_deposit_limit,
            yearly_withdraw_limit=product.yearly_withdraw_limit,
            yearly_deposit_limit=product.yearly_deposit_limit,
            date_created=date_created,
            date_updated=date_created
        )
        db.session.add(account)

        return account

def create_user(userinfo=None):
    '''
    {
        'verified_account': u'false', 
        'family_name': u'Mukewa', 
        'age_range': u'26-30', 
        'user_id': u'https://www.paypal.com/webapps/auth/identity/user/vrn1jrqzaL-aToE5BHaz27GogjnL4myHYMIM2DtzWvw', 
        'name': u'Onesmus Mukewa', 
        'language': u'en_US', 
        'account_creation_date': u'2016-08-17', 
        'locale': u'en_US', 
        'zoneinfo': u'America/Los_Angeles', 
        'birthday': u'1990-03-19', 
        'given_name': u'Onesmus', 
        'address': {
            'country': u'KE', 
            'region': u'Nairobi', 
            'street_address': u'61, Mai Mahiu Road, Nairobi West', 
            'locality': u'Nairobi'
        }, 
        'account_type': u'BUSINESS', 
        'phone_number': u'703266966', 
        'email': u'info@ajabworld.net'
    }
    '''
    with db.session.begin_nested():
        user = create_user_object(userinfo)

        products = Product.query\
            .filter_by(is_active=True)\
            .all()

        for product in products:
            product_code = product.code
            
            account = create_account_object(userinfo, user, product)
            
            if ('PP' in product_code) or ('PAYPAL' in product_code):
                paypal_profile = create_paypal_profile(userinfo, account)

            if ('MPESA' in product_code) or ('M-PESA' in product_code):
                mpesa_profile = create_mpesa_profile(userinfo, account)

        return user


if __name__ == '__main__':
    user = create_user({
        'verified_account': u'false', 
        'family_name': u'Mukewa', 
        'age_range': u'26-30', 
        'user_id': u'https://www.paypal.com/webapps/auth/identity/user/vrn1jrqzaL-aToE5BHaz27GogjnL4myHYMIM2DtzWvw', 
        'name': u'Onesmus Mukewa', 
        'language': u'en_US', 
        'account_creation_date': u'2016-08-17', 
        'locale': u'en_US', 
        'zoneinfo': u'America/Los_Angeles', 
        'birthday': u'1990-03-19', 
        'given_name': u'Onesmus', 
        'address': {
            'country': u'KE', 
            'region': u'Nairobi', 
            'street_address': u'61, Mai Mahiu Road, Nairobi West', 
            'locality': u'Nairobi'
        }, 
        'account_type': u'BUSINESS', 
        'phone_number': u'713266966', 
        'email': u'info@ajabworld.net'
    })