from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from raven.contrib.flask import Sentry

import logging
from logging.handlers import RotatingFileHandler

from .config import get_default_config

#-----------
Config = get_default_config()

#-----
app = Flask(__name__, static_folder="../static", template_folder="./templates")
app.config.from_object(Config)

# ---setup logging
if (Config.DEBUG == False) or ('production' in Config.STAGE):
    from pythonjsonlogger import jsonlogger
    formatter = jsonlogger.JsonFormatter()
    sentry = Sentry(app, dsn=Config.RAVEN_DSN, logging=True, level=logging.INFO)
else:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sentry = Sentry(app, dsn=Config.RAVEN_DSN, logging=True, level=logging.DEBUG)

log_handler = RotatingFileHandler(Config.LOGGING_LOCATION, maxBytes=10000, backupCount=10)
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)

#---end logging

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
