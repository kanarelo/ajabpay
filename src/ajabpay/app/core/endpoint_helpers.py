from flask import render_template, jsonify, url_for
from ajabpay.index import app, db

@app.errorhandler(404)
def page_not_found(e=None, error_no=None):
    return render_template('404.html', error_no=error_no), 404

@app.errorhandler(403)
def access_forbidden(e=None, error_no=None):
    return render_template('403.html', error_no=error_no), 403

@app.errorhandler(500)
def internal_server_error(e=None, error_no=None):
    return render_template('500.html', error_no=error_no), 500