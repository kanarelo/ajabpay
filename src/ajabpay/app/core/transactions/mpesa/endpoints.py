from flask import request, render_template, jsonify, url_for, redirect, g

from ajabpay.app.models import *
from ajabpay.index import app, db, cross_origin

from datetime import date
from .actions import send_money_success

# import wtforms as forms
# class PaypalReturnForm(forms.Form):
#     paymentId = forms.StringField('paymentId', validators=[
#         forms.validators.required(), length(min=26, max=31),
#         forms.validators.Regexp(r'^PAY-(\w{22,27})$')])
#     PayerID = forms.StringField('PayerID', validators=[
#         forms.validators.required(), length(min=11, max=18),
#         forms.validators.Regexp(r'^(\w{11,18})$')])
#     token = forms.StringField('token', validators=[
#         forms.validators.required(), length(min=19, max=23),
#         forms.validators.Regexp(r'^EC-(\w{16,20})$')])

@app.route('/mpesa/payments', methods=['POST'])
@cross_origin()
def mpesa_payments_endpoint():
    args = request.args
    data = request.json

    app.logger.debug(data)

    try:
        mpesa_txn_id = data['txn_id']
        send_money_success(mpesa_txn_id, response=data)
        
        return jsonify(success=True), 200
    except Exception as e:
        app.logger.exception(e)
        return jsonify(success=False), 500
