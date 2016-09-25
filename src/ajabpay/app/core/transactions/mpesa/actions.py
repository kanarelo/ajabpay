from ajabpay.app.models import MPesaTransaction

def send_money(mobile_phone_number, exchange_amount, parent_transaction):
    MPesaTransaction(
        reference_id=parent_transaction.transaction_no,
    )