from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_cors import CORS, cross_origin

from raven.contrib.flask import Sentry
from raven import Client

import logging

from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger as json_logger

from .config import get_default_config

#---------------
app = Flask(__name__, static_folder="../static", template_folder="./templates")
app.config.from_object(get_default_config())

# ---setup logging
if (app.config['DEBUG'] == False) or ('production' in app.config['STAGE']):
    formatter = json_logger.JsonFormatter()
    sentry = Sentry(app, logging=True, level=logging.INFO)
else:
    logging.getLogger('flask_cors').level = logging.DEBUG
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

client = Client()
sentry = Sentry(app, client=client, logging=True, level=logging.INFO)

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
    
    client.user_context({
        'email': g.user.email
    })
#-------------

cors = CORS(app)
