from flask import render_template
from ajabpay.index import app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

from .transactions.paypal.endpoints import *
from .transactions.mpesa.endpoints import *

from .users import *
from .auth import *

@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return render_template('index.html')