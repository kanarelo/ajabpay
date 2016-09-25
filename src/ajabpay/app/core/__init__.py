from flask import render_template
from ajabpay.index import app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

from .users import *
from .transactions import *

@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return page_not_found()