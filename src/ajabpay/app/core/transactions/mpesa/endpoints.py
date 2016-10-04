from flask import request, render_template, jsonify, url_for, redirect, g

from ajabpay.app.models import *
from ajabpay.app.utils import requires_auth
from ajabpay.index import app, db

from datetime import date
from .actions import send_money_success

@app.route('/mpesa/payments', methods=['POST'])
def mpesa_payments_endpoint():
    args = request.args
    data = request.json

    app.logger.debug(data)

    try:
        mpesa_txn_id = data['txn_id']
        send_money_success(mpesa_txn_id, args=args, data=data)
        
        return jsonify(success=True), 200
    except Exception as e:
        app.logger.exception(e)
        return jsonify(success=False), 500
