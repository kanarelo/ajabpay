from ..exceptions import AjabPayException

class TransactionException(AjabPayException): pass
class NotificationException(AjabPayException): pass

class PaypalTransactionException(TransactionException): pass
class ObjectNotFoundException(AjabPayException): pass