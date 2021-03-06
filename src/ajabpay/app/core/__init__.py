import os

from flask import render_template, g, send_from_directory
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
    return render_template('home.html')

@app.route('/instructions', methods=['GET'])
def instructions():
    return render_template('instructions.html')

@app.route('/aw', methods=['GET'])
def aw():
    return render_template('ajabworld.website/index.html')

@app.route('/ac', methods=['GET'])
def ac():
    return render_template('ajabcapital.website/index.html')

from .users import *
from .transactions import *

@app.route('/static/<folder>/<path:path>')
def serve_static(folder, path):
    return send_from_directory(os.path.join(app.config['STATIC_FOLDER'], folder), path)

@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return page_not_found()