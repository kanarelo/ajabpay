from .exceptions import (
    PaypalTransactionException,
    TransactionException
)

from ajabpay.app.models import *
from sqlalchemy.exc import IntegrityError

import logging
import random

from decimal import Decimal as D

INITIAL = D('0.0')

PENDING_POSTING = "pending_posting"
POSTED = "posted"

def get_reference_no(limit=10):
    possible_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    chosen_chars = ""
    z = 0

    while (z <= limit):
        chosen_chars = (chosen_chars + random.choice(possible_chars))
        z += 1

    return chosen_chars

def get_transaction_type_account_turple(transaction_type):
    accounting_rule = ConfigLedgerAccountingRule.query.filter_by(
        transaction_type_id=transaction_type.id
    ).first()

    if not accounting_rule:
        raise TransactionException('Please setup the accounting rules')

    return (
        accounting_rule.debit_account, 
        accounting_rule.credit_account
    )

def get_ledger_balance_increment(amount, account, item_type):
    #constants
    ASSET = "A"
    LIABILITY = "L"
    EQUITY = "E"
    INCOME = "I"
    EXPENSE = "E"

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

    #constants
    NORMAL_ACCOUNT = "N"
    CONTRA_ACCOUNT = "C"

    account_type_code = account.balance_direction.code

    #normal account
    if account_type_code == NORMAL_ACCOUNT:
        #for normal accounts, return amount as it is by this point
        return +(amount)
    elif account_type_code == CONTRA_ACCOUNT:
        #a contra account is a general ledger account which is intended 
        #to have its balance be the opposite of the normal balance for 
        #that account classification
        #In that case, lets negate the balance, so that we can get its opposite
        return -(amount)

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
                reversing_transaction=reversing_transaction,
                currency_id=currency.id,
                account_id=product_account.id,
                amount=amount,
                date_created=transaction_date
            )

            status = TransactionStatus(
                transaction=transaction,
                transaction_status=transaction_status,
                transaction_status_date=transaction_date,
                details="Transaction status by %s " % user,
                created_by=user,
                date_created=transaction_date
            )

            try:
                db.session.add(transaction)
                db.session.add(status)
                db.session.commit()

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
            ledger_balance_item_type=item_type,
            ledger_balance_increment=increment,
            ledger_transaction=transaction,
            product_account=transaction.product_account,
            ledger_account=ledger_account,
            created_by=user,
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

            if (debit_ledger_balance_increment and credit_ledger_balance_increment):
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

                db.session.commit()

                return (debit_entry, credit_entry)
            else:
                raise Exception("Increments not found")
        else:
            return transaction

    except IntegrityError as e:
        db.session.rollback()
        raise PaypalTransactionException(str(e))
    except Exception as e:
        db.session.rollback()
        raise PaypalTransactionException(str(e))

def reverse_transaction(transaction, user, notes, transaction_date=None):
    '''
    We will create a duplicate transaction, but switch the 
    debit and credit accounts.

    We only reverse posted items
    '''
    if transaction is None:
        raise Exception("Please provide a valid transaction")

    if user is None or not user.pk:
        raise Exception("Please provide a valid user")

    if notes is None:
        raise Exception("Please provide a valid note")

    transaction_type = transaction.transaction_type
    
    if transaction.last_status.code == POSTED:
        with db_transaction.atomic():
            #get all the transaction entries
            entries = transaction.entries.all()

            assert entries.count() == 2

            #get the entries
            debit_entry  = entries.get(item_type=TransactionEntry.DEBIT)
            credit_entry = entries.get(item_type=TransactionEntry.CREDIT)

            #get the accounts from the entries
            credit_account = credit_entry.ledger_account
            debit_account = debit_entry.ledger_account

            #get the other particulars
            product_account = transaction.account
            amount = transaction.amount
            currency = transaction.currency
                
            #status is set to none, as it will be received as pending
            status = None

            return create_transaction(
                transaction_type=transaction_type,  
                credit_account=debit_account,
                debit_account=credit_account,
                product_account=product_account,
                reversing_transaction=transaction,
                transaction_date=transaction_date,
                amount=amount,
                status=status,
                user=user, 
                notes=notes,
            )

def update_transaction_status(
    transaction, 
    status_code, 
    user, 
    details, 
    status_date=None
):
    if transaction is None:
        raise Exception("Please provide a valid transaction")

    if status_code is None:
        raise Exception("Please provide a valid status code")

    if user is None or not user.pk:
        raise Exception("Please provide a valid user")

    if details is None:
        raise Exception("Please provide a valid note")

    try:
        #get the transaction status and time now
        config_transaction_status = ConfigTransactionStatus.query.filter_by(
            code=status_code
        ).first()

        if not status_date:
            status_date = db.func.now()

        #create the transaction status
        transaction_status = TransactionStatus(
            transaction=transaction,
            transaction_status=config_transaction_status,
            transaction_status_date=status_date,
            notes=notes,
            created_by=user,
        )
        #update the transaction with the new status and date
        transaction.last_status = config_transaction_status
        transaction.last_status_date = status_date
        
        db.session.add(transaction_status)
        
        db.session.commit()
    except IntegrityError, e:
        db.session.rollback()
        raise PaypalTransactionException(str(e))

    return transaction_status