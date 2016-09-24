from flask import request, render_template, jsonify, url_for, redirect, g

from ajabpay.app.models import *
from ajabpay.index import app, db

from sqlalchemy import or_, Date, cast
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError

from ajabpay.app.utils import generate_token, requires_auth, verify_token

import paypalrestsdk
from paypalrestsdk.openid_connect import Tokeninfo

from ajabpay.config import get_default_config

from .paypal_oauth import create_user_from_userinfo

#------------
Config = get_default_config()

@app.route("/auth/user/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])
    
    if user:
        return jsonify(token=generate_token(user))

    return jsonify(error=True), 403

@app.route("/auth/user/is_token_valid", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403

@app.route("/auth/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(user=g.current_user)

@app.route("/auth/oauth/paypal/signin", methods=["GET"])
def login_via_paypal():
    options = configure_paypal_sdk()

    login_url = Tokeninfo.authorize_url(options=options)

    #redirect to login page for approval
    return redirect(login_url)

@app.route("/auth/oauth/paypal/create_session", methods=["GET"])
def create_session():
    data = request.args
    
    code = data.get('code')

    options = configure_paypal_sdk()
    options['code'] = code

    tokeninfo = Tokeninfo.create(options=options)
    userinfo = tokeninfo.userinfo(options=options)

    create_user_from_userinfo(userinfo)

    return jsonify(dict(**data))
