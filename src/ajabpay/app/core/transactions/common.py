from .exceptions import (
    PaypalTransactionException,
    TransactionException
)

from ajabpay.app.models import *
from sqlalchemy.exc import IntegrityError

import logging

from decimal import Decimal as D
from ajabpay.app.core.utils import get_reference_no

INITIAL = D('0.0')

PENDING_POSTING = "pending_posting"
POSTED = "posted"

def get_transaction_type_account_turple(transaction_type):
    accounting_rule = ConfigLedgerAccountingRule.query.filter_by(
        transaction_type_id=transaction_type.id
    ).first()

    if not accounting_rule:
        raise TransactionException('Please setup the accounting rules')

    return (accounting_rule.debit_account, accounting_rule.credit_account)

def get_ledger_balance_increment(amount, account, item_type):
    #constants
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

    NORMAL = "NORMAL"
    CONTRA = "CONTRA"

    if (amount is None) or (not amount):
        raise Exception("Invalid amount")

    if account.account_category.code in (ASSET, EXPENSE):
        #Assets and expenses increase with debit
        if (item_type is TransactionEntry.DEBIT):
            amount = +(amount)
        #Yet they decrease with credits
        elif (item_type is TransactionEntry.CREDIT):
            amount = -(amount)
    elif account.account_category.code in (LIABILITY, EQUITY, INCOME):
        #Liability, Equity and Income accounts decrease with debits
        if (item_type is TransactionEntry.DEBIT): 
            amount = -(amount)
        #Yet they increase with credits
        elif (item_type is TransactionEntry.CREDIT):
            amount = +(amount)
    else:
        raise Exception("Invalid account category")

    if account.balance_direction == CONTRA:
        #a contra account is a general ledger account which is intended 
        #to have its balance be the opposite of the normal balance for 
        #that account classification
        #In that case, lets negate the balance, so that we can get its opposite
        return -(amount)

    return amount

def create_transaction(
    transaction_type=None, 
    credit_account=None, 
    debit_account=None, 
    currency=None, 
    product_account=None, 
    amount=None, 
    status=None, 
    user=None, 
    notes=None, 
    commit=True,
    reversing_transaction=None, 
    transaction_no=None,
    transaction_date=None, 
    *args, **kwargs
):
    '''
    creates the real transaction 
    '''
    if not transaction_no:
        transaction_no = get_reference_no()

    if currency is not None:
        currency = ConfigCurrency.query.filter_by(code=currency).first()

    if transaction_date is None:
        transaction_date = db.func.now()

    if status is None:
        transaction_status = ConfigTransactionStatus.query.filter_by(
            code=PENDING_POSTING).first()
    else:
        transaction_status = status

    def create_transaction_obj(transaction_no=None):
        #check if the transaction number exists in the db
        if (transaction_no is not None) and not Transaction.query.filter_by(
            transaction_no=transaction_no
        ).exists() is True:
            #create the transaction
            transaction = Transaction(
                transaction_type=transaction_type,
                transaction_no=transaction_no,
                currency_id=currency.id,
                account_id=product_account.id,
                amount=amount,
                date_created=transaction_date
            )

            if reversing_transaction is not None:
                transaction.reversing_transaction_id = reversing_transaction.id

            status = TransactionStatus(
                transaction=transaction,
                status=transaction_status,
                date_created=transaction_date
            )

            try:
                db.session.add(transaction)
                db.session.add(status)

                # l = dict(
                #     transaction_type=transaction_type.code,
                #     last_status=transaction_status,
                #     last_status_date=transaction_date,
                #     reversing_transaction=reversing_transaction,
                #     transaction_no=transaction_no,
                #     amount=amount,
                #     currency=currency,
                #     user=user,
                #     **kwargs
                # )

                # if (credit_account and debit_account):
                #     l.update(
                #         credit_account=credit_account.ledger_code,
                #         debit_account=debit_account.ledger_code,
                #     )

                # if (product_account is not None):
                #     l.update(product_account=product_account.account_number)

                # record_log(**l)
            except IntegrityError as e:
                raise PaypalTransactionException(str(e))

            return transaction
        else:
            return create_transaction_obj(transaction_no=get_reference_no())

    def create_transaction_entry(transaction, ledger_account, item_type, increment):
        #Adds entry for transaction
        le = TransactionEntry(
            item_type=item_type,
            balance_increment=increment,
            transaction=transaction,
            account_id=transaction.account_id,
            ledger_account_id=ledger_account.id
        )

        return le

    try:
        if not ((amount and currency) and transaction_type):
            raise Exception("Please provide valid parameters for this transaction.")

        transaction = create_transaction_obj(transaction_no=transaction_no)
        (debit_entry, credit_entry) = (None, None)

        if (debit_account and credit_account):
            #get the debit and credit ledger balance increments to use for the entries
            debit_ledger_balance_increment  = get_ledger_balance_increment(
                amount, debit_account, TransactionEntry.DEBIT
            )
            credit_ledger_balance_increment = get_ledger_balance_increment(
                amount, credit_account, TransactionEntry.CREDIT
            )

            if not (debit_ledger_balance_increment and credit_ledger_balance_increment):
                raise Exception("Increments not found")

            #Adds credit entry for transaction
            debit_entry  = create_transaction_entry(
                transaction, 
                debit_account,  
                TransactionEntry.DEBIT, 
                debit_ledger_balance_increment
            )
            credit_entry = create_transaction_entry(
                transaction,
                credit_account, 
                TransactionEntry.CREDIT, 
                credit_ledger_balance_increment
            )

            db.session.add(debit_entry)
            db.session.add(credit_entry)

            if commit:
                db.session.commit()

        return (debit_entry, credit_entry)

    except IntegrityError as e:
        if commit:
            db.session.rollback()
        raise PaypalTransactionException(str(e))
    except Exception as e:
        if commit:
            db.session.rollback()
        raise PaypalTransactionException(str(e))

def reverse_transaction(transaction, user=None, transaction_date=None):
    '''
    We will create a duplicate transaction, but switch the 
    debit and credit accounts.

    We only reverse posted items
    '''
    if transaction is None:
        raise Exception("Please provide a valid transaction")

    transaction_type = transaction.transaction_type

    last_transaction_status = TransactionStatus.query.filter_by(
        transaction_id=transaction.id).order_by('date_created desc').limit(1)
    
    if last_transaction_status.status.code == POSTED:
        #get all the transaction entries
        entries = transaction.entries.all()

        assert entries.count() == 2

        #get the entries
        debit_entry  = entries.get(item_type=TransactionEntry.DEBIT)
        credit_entry = entries.get(item_type=TransactionEntry.CREDIT)

        #get the accounts from the entries, and swap them
        debit_account = credit_entry.ledger_account
        credit_account = debit_entry.ledger_account

        #get the other particulars
        account = transaction.account
        amount = transaction.amount
        currency = transaction.currency
            
        #status is set to none, as it will be received as pending
        status = None

        return create_transaction(
            transaction_type=transaction_type,  
            credit_account=credit_account,
            debit_account=debit_account,
            product_account=account,
            reversing_transaction=transaction,
            transaction_date=transaction_date,
            amount=amount,
            status=status,
            user=user, 
        )

def update_transaction_status(
    transaction, 
    status_code,  
    status_date=None
):
    if transaction is None:
        raise Exception("Please provide a valid transaction")

    if status_code is None:
        raise Exception("Please provide a valid status code")

    if user is None or not user.pk:
        raise Exception("Please provide a valid user")

    if not status_date:
        status_date = db.func.now()

    try:
        #get the transaction status and time now
        config_transaction_status = ConfigTransactionStatus.query\
            .filter_by(code=status_code).first()

        #create the transaction status
        transaction_status = TransactionStatus(
            transaction_id=transaction.id,
            status_id=config_transaction_status.id,
            status_date=status_date
        )
        
        db.session.add(transaction_status)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise PaypalTransactionException(str(e))

    return transaction_status