import paypalrestsdk
import dateutil.parser

from ajabpay.app.core.transactions.exceptions import (
    PaypalTransactionException, NotificationException, ObjectNotFoundException)
from ajabpay.app.core.transactions.paypal.utils import (
    format_amount, round_down, round_up)
from ajabpay.app.core.transactions.mpesa import actions as mpesa_transactions
from ajabpay.app.core.transactions import common as transaction_commons

from ajabpay.app.models import *
from ajabpay.index import app

import logging
from decimal import Decimal as D

from sqlalchemy import or_, DateTime, cast, text
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError

INITIAL = D('0.0')

PENDING_POSTING = "pending_posting"
POSTED = "posted"

def make_paypal_payment_request(
    amount,
    description=None,
    currency="USD",
    payment_method='paypal',
    intent="sale",
    return_url=None,
    cancel_url=None,
    create=False
):
    formated_amount = format_amount(amount)

    request = dict(
        intent=intent,
        redirect_urls=dict(
            return_url=(app.config['SITE_URL'] + return_url),
            cancel_url=(app.config['SITE_URL'] + cancel_url)
        ),
        payer=dict(payment_method=payment_method),
        transactions=[
            dict(
                amount=dict(
                    total=formated_amount,
                    currency=currency
                ),
                description='%s amount: %s %s' % (
                    description, 
                    currency, 
                    formated_amount
                )
            )
        ]
    )

    payment = paypalrestsdk.Payment(request)

    if create:
        if not payment.create():
            raise PaypalTransactionException(payment.error)

    return payment

def create_payment_transaction(
    email,
    mpesa_recipient,
    amount=D('100.00'), 
    transaction_type=None,
    currency='USD',
    user=None,
    return_url=None,
    cancel_url=None,
    create=True
):
    PRODUCT_CODE = 'P2M'

    try:
        paypal_profile = db.session.query(PaypalProfile)\
            .join(User, User.email==PaypalProfile.email)\
            .filter(User.email==email)\
            .first()
            
        if paypal_profile is None:
            raise ObjectNotFoundException('User %s not found' % email)
        
        if transaction_type is None:
            transaction_type = ConfigTransactionType.query.filter_by(code='WITHDRAWAL').first()

        user = paypal_profile.user
        account = user.accounts\
            .join(Product, Product.id==Account.product_id)\
            .filter(Product.code==PRODUCT_CODE)\
            .first()

        if account is None:
            raise ObjectNotFoundException('Account %s not found' % email)

        validate_product_policy = lambda account, transaction: True #TODO: Implement validate_product_policy
        # is_valid = validate_product_policy(account, transaction)

        # if not is_valid:
        #     raise PaypalTransactionException('Invalid transaction')

        payment = make_paypal_payment_request(
            amount, 
            description=transaction_type.name,
            return_url=return_url, 
            cancel_url=cancel_url,
            create=create)

        if payment is None:
            raise PaypalTransactionException("Error creating paypal payment transaction")

        (debit_account, credit_account) = transaction_commons\
            .get_transaction_type_account_turple(transaction_type)

        if not (debit_account and credit_account):
            raise PaypalTransactionException("Please setup the chart of accounts")

        transaction_no = payment.id

        (debit_entry, credit_entry) = transaction_commons\
            .create_transaction(
                amount=amount, 
                transaction_type=transaction_type, 
                product_account=account,
                currency=currency, 
                user=user, 
                credit_account=credit_account, 
                debit_account=debit_account, 
                transaction_no=transaction_no,
                commit=False)
        transaction = credit_entry.transaction

        if payment.payer_id and paypal_profile.payer_id is None:
            paypal_profile.payer_id = payment.payer_id 

        pp_transaction = PaypalTransaction(
            payment_method=payment.payer['payment_method'],
            paypal_transaction_type_code='PAYMENT',
            payer_id=paypal_profile.id,
            paypal_transaction_id=transaction_no,
            mpesa_recipient=mpesa_recipient,
            intent=payment.intent,
            state=payment.state,
            create_time=payment.create_time,
            date_created=db.func.now())
        
        if payment.payer_id:
            pp_transaction.paypal_payer_id = payment.payer_id

        if payment.update_time:
            pp_transaction.update_time = dateutil.parser.parse(payment.update_time)

        db.session.add_all((transaction, pp_transaction))
        db.session.commit()

        return payment
    except IntegrityError, e:
        db.session.rollback()
        raise PaypalTransactionException(str(e))

def get_exchange_amount(foreign_amount, from_currency='USD', to_currency='KES'):
    if (foreign_amount < 0) or \
       (foreign_amount > 500) and (from_currency == 'USD') or \
       (foreign_amount > 50000) and (from_currency == 'KES'):
        return 0 

    paypal_parameter = ConfigPaypalParameter.query\
        .order_by(text('date_created desc'))\
        .limit(1)\
        .first()

    return paypal_parameter\
        .get_exchange_amount(foreign_amount, 
            from_currency=from_currency, to_currency=to_currency)

def acknowledge_payment(payment_id, payer_id, token):
    with db.session.begin_nested():
        paypal_transaction = PaypalTransaction.query\
            .filter_by(paypal_transaction_id=payment_id)\
            .first()
        
        if paypal_transaction is None:
            raise ObjectNotFoundException('Transaction.paypal_transaction_id == %s' % payment_id)

        transaction = paypal_transaction.transaction
        transaction_no = transaction.transaction_no
        paypal_payer = paypal_transaction.payer
        mpesa_recipient = paypal_transaction.mpesa_recipient

        mpesa_profile = \
            MPesaProfile.query\
                .filter_by(mobile_phone_no=mpesa_recipient)\
                .first()
        
        if mpesa_profile is None:
            client_name = paypal_payer.name
        else:
            client_name = mpesa_profile.registered_name

        client_location = paypal_payer.address.locality
        
        amount_to_send = \
            get_exchange_amount(transaction.amount, transaction.currency.code)
        mpesa_transactions\
            .send_money(mpesa_recipient, 
                amount_to_send,
                client_name=client_name, 
                client_location=client_location,
                merchant_transaction_id=transaction_no, 
                reference_id=payer_id)

def refund_payment(paypal_transaction):
    db.session.begin_nested()

    sale = paypalrestsdk.Sale()\
        .find(paypal_transaction.paypal_transaction_id)

    try:
        refund = sale.refund()

        if refund.success():
            transaction = paypal_transaction.transaction
            reverse_transaction = transaction_commons.reverse_transaction(transaction)

            parent_transaction = PaypalTransaction.query\
                .filter_by(transaction_no=refund.parent_payment)\
                .first()

            paypal_transaction = PaypalTransaction(
                paypal_transaction_id=refund.id,
                paypal_transaction_type_code='REFUND',
                state=refund.state,
                create_time=dateutil.parser.parse(refund.create_time),
                update_time=dateutil.parser.parse(refund.update_time),
                date_created=db.func.now())

            if parent_transaction is not None:
                paypal_transaction.parent_transaction_id = parent_transaction.paypal_transaction_id 

            db.session.add(paypal_transaction)
            db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
    except PaypalTransactionException as e:
        db.session.rollback()

if __name__ == "__main__":
    payment = create_payment_transaction(
        "musa@ajabworld.com",
        amount=D('100.00'), 
        return_url="/transaction/3234/paypal/return/",
        cancel_url="/transaction/3234/paypal/cancel/"
    )

    print get_exchange_amount(D('100.0'))