from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import BaseConfig
from flask_bcrypt import Bcrypt

from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__, static_folder="../static", template_folder="./templates")
app.url_map.converters['regex'] = RegexConverter
app.config.from_object(BaseConfig)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
