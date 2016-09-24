import dateutil.parser

from ajabpay.index import db
from ajabpay.app.core.utils import (
    get_reference_no, generate_random_password)
from ajabpay.app.models import *

def get_phone_number(phone_number):
    return '+254%s' % phone_number

def create_user_object(phone=None, **kwargs):
    with db.session.begin_nested() as transaction:
        password = generate_random_password()

        date_created = db.func.now()

        user = User(
            phone=get_phone_number(phone), 
            date_created=date_created,
            date_updated=date_created,
            date_joined=date_created,
            password=password, 
            **kwargs)
        transaction.session.add(user)

        return user

def create_mpesa_profile(account):
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

def create_paypal_profile(account, user_id=None, address=None, **kwargs):
    user = account.user
    date_created = db.func.now()

    def create_paypal_address(paypal_profile, **address_kwargs):
        with db.session.begin_nested():
            paypal_address = PaypalAddress(
                paypal_profile_id=paypal_profile.id,
                date_created=date_created, 
                **address_kwargs)

            db.session.add(paypal_address)

            return paypal_address

    with db.session.begin_nested():
        paypal_profile = PaypalProfile(
            family_name=user.first_name,
            given_name=user.last_name,
            date_created=date_created,
            date_updated=date_created,
            name=user.get_full_name(),
            paypal_user_id=user_id,
            account_id=account.id,
            email=user.email,
            **kwargs)
        db.session.add(paypal_profile)

        if address is not None:
            create_paypal_address(paypal_profile, **address)

def create_account_object(user, product, account_number=None):
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

        date_created = db.func.now()

        account = Account(
            product=product,
            user_id=user_id,
            account_number=account_number,
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

