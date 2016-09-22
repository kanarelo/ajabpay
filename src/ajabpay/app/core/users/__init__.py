from flask import request, jsonify, g

from ajabpay.app.models import *
from ajabpay.index import app, db

from sqlalchemy.exc import IntegrityError
from ajabpay.app.utils import generate_token, requires_auth

@app.route("/api/v1/auth/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(user=g.current_user)

@app.route("/auth/oauth/paypal/create_session", methods=["GET"])
def create_session():
    data = request.args
    return jsonify(dict(**data))
 
