from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

import logging
from logging.handlers import RotatingFileHandler

from .config import get_default_config

#-----------
Config = get_default_config()

#-----
app = Flask(__name__, static_folder="../static", template_folder="./templates")
app.config.from_object(Config)

#---setup logging
if (Config.DEBUG is False) or (Config.STAGE == 'production'):
    from pythonjsonlogger import jsonlogger
    formatter = jsonlogger.JsonFormatter()
    log_handler = RotatingFileHandler(
        Config.LOGGING_LOCATION, maxBytes=10000, backupCount=10)#10mbs create til .10
    log_handler.setFormatter(formatter)

    app.logger.addHandler(log_handler)
else:
    pass

#---end logging

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

def configure_paypal():
    import paypalrestsdk
    paypalrestsdk.configure(
        mode=Config.PAYPAL_MODE,
        client_id=Config.PAYPAL_CLIENT_ID,
        client_secret=Config.PAYPAL_CLIENT_SECRET,
        openid_client_id=Config.PAYPAL_CLIENT_ID,
        openid_client_secret=Config.PAYPAL_CLIENT_SECRET,
        openid_redirect_uri=Config.PAYPAL_OAUTH_REDIRECT_URI,
    )