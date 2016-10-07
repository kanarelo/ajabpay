import sys, os, inspect

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from ajabpay import app 

flask_app = app.app
db = app.db

migrate = Migrate(flask_app, db)
manager = Manager(flask_app)

#admin
admin = Admin(flask_app, name='ajabpay', template_mode='bootstrap3')

admin.add_view(ModelView(app.Account, db.session))
admin.add_view(ModelView(app.AccountStatus, db.session))
admin.add_view(ModelView(app.ConfigExchangeRate, db.session))
admin.add_view(ModelView(app.ConfigProductType, db.session))
admin.add_view(ModelView(app.ConfigCurrency, db.session))
admin.add_view(ModelView(app.ConfigAccountStatus, db.session))
admin.add_view(ModelView(app.ConfigTransactionStatus, db.session))
admin.add_view(ModelView(app.ConfigLedgerAccountCategory, db.session))
admin.add_view(ModelView(app.ConfigTransactionType, db.session))

ledger_account_admin = ModelView(app.ConfigLedgerAccount, db.session)
ledger_account_admin.column_default_sort = 'code'
admin.add_view(ledger_account_admin)

admin.add_view(ModelView(app.ConfigLedgerAccountingRule, db.session))
admin.add_view(ModelView(app.ConfigPaypalParameter, db.session))
admin.add_view(ModelView(app.ConfigSMSGateway, db.session))
admin.add_view(ModelView(app.ConfigNotificationType, db.session))
admin.add_view(ModelView(app.ConfigNotificationTemplate, db.session))
admin.add_view(ModelView(app.EmailMessage, db.session))
admin.add_view(ModelView(app.MPesaTransaction, db.session))
admin.add_view(ModelView(app.PaypalTransaction, db.session))
admin.add_view(ModelView(app.PaypalProfile, db.session))
admin.add_view(ModelView(app.PaypalAddress, db.session))
# admin.add_view(ModelView(app.PaypalToken, db.session))
admin.add_view(ModelView(app.Product, db.session))
admin.add_view(ModelView(app.SMSMessage, db.session))
admin.add_view(ModelView(app.Transaction, db.session))
admin.add_view(ModelView(app.TransactionStatus, db.session))
admin.add_view(ModelView(app.TransactionEntry, db.session))
admin.add_view(ModelView(app.User, db.session))

# migrations
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host='0.0.0.0', port=8000))

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()

if __name__ == '__main__':
    manager.run()