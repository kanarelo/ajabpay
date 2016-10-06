from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_cors import CORS, cross_origin

from raven.contrib.flask import Sentry

import logging
from logging.handlers import RotatingFileHandler

from .config import get_default_config

#---------------
app = Flask(__name__, static_folder="../static", template_folder="./templates")
app.config.from_object(get_default_config())

# ---setup logging
# if (app.config['DEBUG'] == False) or ('production' in app.config['STAGE']):
#     from pythonjsonlogger import jsonlogger
#     formatter = jsonlogger.JsonFormatter()
#     sentry = Sentry(app, dsn=app.config['RAVEN_DSN'], logging=True, level=logging.INFO)
# else:
logging.getLogger('flask_cors').level = logging.DEBUG
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sentry = Sentry(app, dsn=app.config['RAVEN_DSN'], logging=True, level=logging.DEBUG)

log_handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=10000, backupCount=10)
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)

#---end logging

#-------------
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#-------------

#-------------
login_manager = LoginManager()
login_manager.init_app(app)

@app.before_request
def before_request():
    g.user = current_user
#-------------

cors = CORS(app)
