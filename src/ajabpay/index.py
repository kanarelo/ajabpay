from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

from .config import get_default_config

#-----------
Config = get_default_config()

#-----
app = Flask(__name__, static_folder="../static", template_folder="./templates")
app.config.from_object(Config)

#---setup logging
formatter = jsonlogger.JsonFormatter()
log_handler = RotatingFileHandler(Config.LOGGING_LOCATION, maxBytes=10000, backupCount=10)#10mbs create til .10
log_handler.setFormatter(formatter)
logger = logging.getLogger()
#---end logging

app.logger.addHandler(log_handler)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)