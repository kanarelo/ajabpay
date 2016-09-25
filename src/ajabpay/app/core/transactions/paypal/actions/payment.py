import paypalrestsdk
import dateutil.parser

from ...exceptions import (
    PaypalTransactionException,
    NotificationException,
    ObjectNotFoundException
)
from ..utils import (
    create_paypalrestsdk_api,
    format_amount,
    round_down,
    round_up,
)
from ... import common as transaction_commons

from ajabpay.app.models import *

import logging
from decimal import Decimal as D

from sqlalchemy import or_, Date, cast
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError

INITIAL = D('0.0')

ENDPOINT = "http://localhost:8000"
PENDING_POSTING = "pending_posting"
POSTED = "posted"

def create_sms_message(paypal_transaction, notification_type=None, **kwargs):
    db.session.begin_nested()

    if notification_type is None:
        raise NotificationException()

    notification_type = ConfigNotificationType.query\
        .filter_by(code=notification_type).first()

    transaction = paypal_transaction.transaction
    paypal_payer = paypal_transaction.paypal_payer
    mobile_phone_number = paypal_payer.user.phone

    notification_template = transaction_commons.get_notification_template(
        paypal_transaction,
        notification_type)

    message = notification_template.sms_template.format(
        name=paypal_payer.name,
        email=paypal_payer.email,
        transaction_no=paypal_transaction.transaction_id,
        transaction_date=paypal_transaction.create_time,
        transaction_amount=transaction.amount,
        mobile_phone_number=mobile_phone_number,
        transaction_currency=transaction.currency_code,
        order_detail='KES {exchange_amount}'.format(
            exchange_amount=get_exchange_amount(transaction.amount, transaction.currency_code)
        ),
        **kwargs)

    outgoing_sms_message = SMSMessage(
        message_recipient=mobile_phone_number,
        message_type=SMSMessage.OUTGOING,
        message=message,
        template=notification_template)

    try:
        db.session.add(outgoing_sms_message)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()

    return outgoing_sms_message

def create_email_message(paypal_transaction, notification_type=None, **kwargs):
    db.session.begin_nested()
      
    if notification_type is None:
        raise NotificationException() 

    notification_type = ConfigNotificationType.query\
        .filter_by(code=notification_type).first()

    transaction = paypal_transaction.transaction
    paypal_payer = paypal_transaction.paypal_payer
    mobile_phone_number = paypal_payer.user.phone

    message = notification_template.email_template.format(
        name=paypal_payer.name,
        email=paypal_payer.email,
        transaction_no=paypal_transaction.transaction_id,
        transaction_date=paypal_transaction.create_time,
        transaction_amount=transaction.amount,
        mobile_phone_number=mobile_phone_number,
        transaction_currency=transaction.currency,
        order_detail='KES {exchange_amount}'.format(exchange_amount=get_exchange_amount(
           transaction.amount, transaction.currency
        )),
        **kwargs
    )

    outgoing_email_message = EmailMessage(
        message_recipient=mobile_phone_number,
        message_type=SMSMessage.OUTGOING,
        message=message,
        template=notification_template
    )

    try:
        db.session.add(outgoing_email_message)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()

    return outgoing_email_message

def create_push_message(paypal_transaction, notification_type=None, **kwargs):  
    pass

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
    api = create_paypalrestsdk_api()
    formated_amount = format_amount(amount)

    request = dict(
        intent=intent,
        redirect_urls=dict(
            return_url=(ENDPOINT + return_url),
            cancel_url=(ENDPOINT + cancel_url)
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

    payment = paypalrestsdk.Payment(request, api=api)

    if create:
        if not payment.create():
            raise PaypalTransactionException(payment.error)

    return payment

def create_payment_transaction(
    email,
    amount=D('100.00'), 
    transaction_type=None,
    currency='USD',
    user=None,
    return_url=None,
    cancel_url=None,
    create=True
):
    PRODUCT_CODE = 'PP2MP'
    db.session.begin_nested()

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

        validate_product_policy = lambda account, transaction: True #TODO, implement validate_product_policy
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
            intent=payment.intent,
            state=payment.state,
            create_time=dateutil.parser.parse(payment.create_time),
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

def get_exchange_amount(foreign_amount, currency='USD'):
    paypal_parameter = ConfigPaypalParameter.query\
        .order_by('date_created desc')\
        .limit(1)\
        .first()

    return paypal_parameter.get_exchange_amount(
        foreign_amount, currency=currency)

def acknowledge_payment(payment_id, payer_id, token):
    db.session.begin_nested()

    try:
        paypal_transaction = PaypalTransaction.query\
            .filter_by(transaction_id=payment_id, paypal_payer_id=payer_id)\
            .first()
        
        if paypal_transaction is None:
            raise ObjectNotFoundException('Transaction.transaction_id == %s' % payment_id)

        transaction = paypal_transaction.transaction
        transaction_no = transaction.transaction_no
        paypal_payer = paypal_transaction.paypal_payer
        mobile_phone_number = paypal_payer.user.phone

        exchange_amount = get_exchange_amount(transaction.amount, transaction.currency_code)
        mpesa_transaction_no = mpesa_transactions\
            .send_money(mobile_phone_number, exchange_amount, parent_transaction=transaction_no)

        if mpesa_transaction_no is not None:
            status_code = 'POSTED'
            #update status to posted
            transaction_commons.update_transaction_status(transaction, status_code)
            transaction_commons.notify_transaction_parties(paypal_transaction.transaction, [
                {'type': 'SMS', 'message': create_sms_message(transaction, 
                    notification_type='PAYMENT_DONE', mpesa_transaction_no=mpesa_transaction_no)},
                {'type': 'EMAIL', 'message': create_email_message(transaction, 
                    notification_type='PAYMENT_DONE', mpesa_transaction_no=mpesa_transaction_no)},
                {'type': 'PUSH', 'message': create_push_message(transaction, 
                    notification_type='PAYMENT_DONE', mpesa_transaction_no=mpesa_transaction_no)}
            ])

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise PaypalTransactionException(str(e))


def refund_payment(paypal_transaction):
    db.session.begin_nested()

    api = create_paypalrestsdk_api()
    sale = paypalrestsdk.Sale(api=api)\
        .find(paypal_transaction.paypal_transaction_id)

    refund = sale.refund()

    if refund.success():
        try:
            transaction = paypal_transaction.transaction
            reverse_transaction = transaction_commons.reverse_transaction(transaction)

            parent_transaction = PaypalTransaction.query\
                .filter_by(transaction_no=refund.parent_payment)

            paypal_transaction = PaypalTransaction(
                paypal_transaction_type_code='REFUND',
                paypal_transaction_id=refund.id,
                create_time=dateutil.parser.parse(refund.create_time),
                update_time=dateutil.parser.parse(refund.update_time),
                state=refund.state,
                date_created=db.func.now())

            db.session.add(paypal_transaction)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
        except PaypalTransactionException as e:
            db.session.rollback()

if __name__ == "__main__":
    # payment = create_payment_transaction(
    #     D('100.00'), 
    #     description=TransactionType("PayPal to M-Pesa").name,
    #     return_url="/transaction/3234/paypal/return/",
    #     cancel_url="/transaction/3234/paypal/cancel/"
    # )

    print get_exchange_amount(D('100.0'))