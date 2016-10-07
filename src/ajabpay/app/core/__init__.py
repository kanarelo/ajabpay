from flask import render_template, g
from ajabpay.index import app
from ajabpay.app.utils import login_required

@app.route('/', methods=['GET'])
def index():
    
    if g.user.is_authenticated:
        return redirect(url_for('home'))

    return render_template('index.html')

@app.route('/home', methods=['GET'])
@login_required
def home():
    return redirect(url_for('paypal2mpesa'))

from .users import *
from .transactions import *

@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return page_not_found()