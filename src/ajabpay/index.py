from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

from werkzeug.routing import BaseConverter

from .config import get_default_config

#-----------
Config = get_default_config()

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

#-----
app = Flask(__name__, static_folder="../static", template_folder="./templates")
app.url_map.converters['regex'] = RegexConverter
app.config.from_object(Config)

#---setup logging
formatter = jsonlogger.JsonFormatter()
log_handler = RotatingFileHandler(Config.LOGGING_LOCATION, maxBytes=10000, backupCount=10)
log_handler.setFormatter(formatter)
logger = logging.getLogger()
#---end logging

app.logger.addHandler(log_handler) 


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
