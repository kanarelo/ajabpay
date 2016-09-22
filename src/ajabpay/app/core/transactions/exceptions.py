class TransactionException(Exception): pass
class PaypalTransactionException(TransactionException): pass
class NotificationException(Exception): pass