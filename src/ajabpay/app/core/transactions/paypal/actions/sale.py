import paypalrestsdk

from ...exceptions import (
    PaypalTransactionException
)
from ..utils import (
    create_paypalrestsdk_api,
    format_amount,
    round_down,
    round_up,
)
from ... import common as transaction_commons

import logging
from decimal import Decimal as D

INITIAL = D('0.0')

ENDPOINT = "http://localhost:5000"
PENDING_POSTING = "pending_posting"
POSTED = "posted"

def create_paypal_payment_transaction(
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
        if payment.create():
            return payment
        else:
            raise PaypalTransactionException(payment.error)

def create_sale_transaction(
    account,
    amount=D('100.00'), 
    transaction_type=None,
    currency='USD',
    user=None,
    return_url=None,
    cancel_url=None,
):
    try:
        if transaction_type is None:
            transaction_type = TransactionType.query.filter_by(code='PAYPAL-MPESA')

        payment = create_paypal_payment_transaction(
            amount, 
            description=transaction_type.name,
            return_url=return_url, 
            cancel_url=cancel_url
        )

        if payment is None:
            raise PaypalTransactionException("Error creating paypal payment transaction")

        (debit_account, credit_account) = get_transaction_type_account_turple(
            transaction_type
        )

        transaction = transaction_commons.create_transaction(
            amount=amount, 
            transaction_type=transaction_type, 
            product_account=account, 
            currency=currency, 
            user=user, 
            credit_account=credit_account, 
            debit_account=debit_account, 
            transaction_no=payment.id
        )

        pp_transaction = PaypalTransaction(
            paypal_transaction_id=payment.id,
            transaction_id=transaction.id,
            create_time=payment.create_time,
            state=payment.state,
            intent=payment.intent,
            payment_method=payment.payer['payment_method'],
            date_created=datetime.now(),
        )

        db.session.add(transaction)
        db.session.add(pp_transaction)
        db.session.commit()
    except IntegrityError, e:
        db.session.rollback()
        raise PaypalTransactionException(str(e))

if __name__ == "__main__":
    payment = create_payment_transaction(
        D('100.00'), 
        description=TransactionType("PayPal to M-Pesa").name,
        return_url="/transaction/3234/paypal/return/",
        cancel_url="/transaction/3234/paypal/cancel/"
    )
