from ajabpay.app.models import MPesaTransaction
from ajabpay.index import db, app

from ajabpay.app.core.transactions import common as transaction_commons
from ajabpay.app.utils import (
    create_mpesa_payment_request, confirm_mpesa_payment_request)
from ajabpay.app.core.utils import clean_phone_no

def send_money(mobile_phone_no, total_amount, 
    client_name='', client_location='', 
    merchant_transaction_id=None, reference_id=None):

    mobile_phone_no = clean_phone_no(mobile_phone_no)
    if mobile_phone_no is None:
        raise Exception("Invalid mobile phone number")
    
    with db.session.begin_nested():
        mpesa_transaction = MPesaTransaction(
            merchant_transaction_id=merchant_transaction_id,
            recipient_phone_no=mobile_phone_no,
            total_amount=total_amount,
            date_created=db.func.now())
        
        response = create_mpesa_payment_request(
            phoneNumber=mobile_phone_no,
            totalAmount=total_amount,
            clientLocation=client_location,
            clientName=client_name,
            merchantTransactionID=merchant_transaction_id,
            referenceID=reference_id)

        if 'reference_id' in response:
            mpesa_transaction.reference_id = response['reference_id']

        if 'txn_id' in response:
            mpesa_txn_id = response['txn_id']
            mpesa_transaction.mpesa_txn_id = mpesa_txn_id        
            confirmation_response = \
                confirm_mpesa_payment_request(mpesa_txn_id)

        db.session.add(mpesa_transaction)

def send_money_success(mpesa_txn_id, response=None):
    try:
        mpesa_transaction = MPesaTransaction.query\
            .filter_by(mpesa_txn_id=mpesa_txn_id)\
            .first()

        if response is None:
            raise Exception("invalid response received")

        if mpesa_transaction is None:
            raise Exception("mpesa_transaction not found")

        if 'mpesa_transaction_no' in data:
            mpesa_transaction.mpesa_transaction_no = data['mpesa_transaction_no']

        mpesa_transaction.date_approved = db.func.now()
        transaction = mpesa_transaction.transaction

        status_code = 'POSTED'
        #update status to posted
        transaction_commons.update_transaction_status(transaction, status_code)
        responses = transaction_commons.notify_transaction_parties(transaction, [
            {'type': 'SMS', 'message': transaction_commons.create_sms_message(transaction, 
                notification_type='PAYMENT_DONE', mpesa_transaction_no=mpesa_transaction_no)},
            {'type': 'EMAIL', 'message': transaction_commons.create_email_message(transaction, 
                notification_type='PAYMENT_DONE', mpesa_transaction_no=mpesa_transaction_no)},
            {'type': 'PUSH', 'message': transaction_commons.create_push_message(transaction, 
                notification_type='PAYMENT_DONE', mpesa_transaction_no=mpesa_transaction_no)}])
        
        app.logger.info('PAYMENT_NOTIFICATION_RESPONSES', responses=responses)
        db.session.commit()
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback() 