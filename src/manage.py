import sys, os, inspect

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from ajabpay import app 

flask_app = app.app
db = app.db

migrate = Migrate(flask_app, db)
manager = Manager(flask_app)

#admin
admin = Admin(flask_app, name='ajabpay', template_mode='bootstrap3')

admin.add_view(ModelView(app.User, db.session))

# migrations
manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()

if __name__ == '__main__':
    manager.run()