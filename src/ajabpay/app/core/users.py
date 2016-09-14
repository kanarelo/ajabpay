from flask import request, jsonify, g

from ajabpay.app.models import *
from ajabpay.index import app, db

from sqlalchemy.exc import IntegrityError
from ajabpay.app.utils import generate_token, requires_auth

@app.route("/api/v1/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(user=g.current_user)

@app.route("/api/v1/user/create", methods=["POST"])
def create_user():
    incoming = request.get_json()
    
    user = User(
        full_name=incoming["full_name"],
        email=incoming["email"],
        password=incoming["password"],
        phone=incoming["phone"]
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    return jsonify(id=user.id, token=generate_token(user))
