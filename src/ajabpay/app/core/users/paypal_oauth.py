import dateutil.parser

from ajabpay.index import app, db
from ajabpay.app.core.utils import extract_string, clean_phone_no
from ajabpay.app.models import Product

import paypalrestsdk
from paypalrestsdk.exceptions import UnauthorizedAccess

from sqlalchemy.exc import IntegrityError, OperationalError

from ajabpay.app.core.users.helpers import *

def configure_paypal_api():
    paypalrestsdk.configure(
        mode=app.config['PAYPAL_MODE'],
        client_id=app.config['PAYPAL_CLIENT_ID'],
        client_secret=app.config['PAYPAL_CLIENT_SECRET'],
        openid_client_id=app.config['PAYPAL_CLIENT_ID'],
        openid_client_secret=app.config['PAYPAL_CLIENT_SECRET'],
        openid_redirect_uri=app.config['PAYPAL_OAUTH_REDIRECT_URI'])

    return paypalrestsdk

def configure_openid_request(scope=None, code=None):
    if scope is None:
        scope = (
            'openid profile email address phone '
            'https://uri.paypal.com/services/paypalattributes '
            'https://uri.paypal.com/services/expresscheckout '
            'https://uri.paypal.com/services/invoicing')

    options = {'scope': scope}

    if code is not None:
        options.update(code=code)

    return options

USER_ID_ENDPOINT_REGEX = r'^https://www.paypal.com/webapps/auth/identity/user/(?P<user_id>[-\w]+)$'
extract_paypal_user_id = lambda user_id_url: extract_string(USER_ID_ENDPOINT_REGEX, user_id_url)

def create_user_from_userinfo(userinfo=None):
    '''{
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
         
    try:
        app.logger.debug(userinfo)

        #1. Create user
        user = create_user_object(
            email=userinfo.get('email'),
            last_name=userinfo.get('family_name'),
            first_name=userinfo.get('given_name'),
            phone=userinfo.get('phone_number'))
        
        #2. Create their paypal profile
        paypal_profile = create_paypal_profile(user,
            gender=userinfo.get('gender'),
            paypal_user_id=extract_paypal_user_id(userinfo.get('user_id')),
            birthday=dateutil.parser.parse(userinfo.get('birthday')),
            phone_number=clean_phone_no(userinfo.get('phone_number')),
            email_verified=userinfo.get('email_verified') == 'true',
            verified_account=userinfo.get('verified_account') == 'true',
            account_creation_date=dateutil.parser.parse(userinfo.get('account_creation_date')),
            account_type=userinfo.get('account_type'),
            address=userinfo.get('address'))

        #3. create their m-pesa profile
        mpesa_profile = create_mpesa_profile(user)

        #4. Subscribe to all active products
        products = Product.query\
            .filter_by(is_active=True)\
            .all()
        for product in products:
            #5. subscribe
            account = create_account_object(user, product)
        
        db.session.commit()
        
        return user
    except (IntegrityError, OperationalError) as e:
        app.logger.exception(e)
        db.session.rollback()
    except (UnauthorizedAccess) as e:
        app.logger.exception(e)
        db.session.rollback()
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()

if __name__ == '__main__':
    user = create_user_from_userinfo({
        'verified_account': u'false', 
        'family_name': u'Mukewa', 
        'age_range': u'26-30', 
        'user_id': u'https://www.paypal.com/webapps/auth/identity/user/vrn1jrqzaL-aToE5BG5Ts7GogjnL4myHYMIM2DtzWvw', 
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
        'phone_number': u'708866966', 
        'email': u'musa@ajabworld.com'
    })