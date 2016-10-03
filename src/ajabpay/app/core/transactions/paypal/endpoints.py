from flask import request, render_template, jsonify, url_for, redirect, g

from ajabpay.app.models import *
from ajabpay.app.utils import requires_auth
from ajabpay.index import app, db

from sqlalchemy import or_, Date, cast
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError

from datetime import date
from .actions.payment import *

from .webhooks import webhook

import wtforms as forms 
class PaypalPaymentForm(forms.Form):
    email = forms.StringField('Email Address', validators=[
        forms.validators.required(), forms.validators.Length(min=6, max=72)])
    amount = forms.DecimalField('Amount', places=2, rounding=None, validators=[
        forms.validators.required(), forms.validators.NumberRange(0, 250)])

@requires_auth
@app.route('/transaction/withdraw', methods=['GET', 'POST'])
def paypal_withdraw_amount():
    form = PaypalPaymentForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data  
        amount = form.amount.data

        try:
            payment = create_payment_transaction(email, amount=amount,
                return_url=url_for('paypal_return_url'), cancel_url=url_for('paypal_cancel_url'))
        except PaypalTransactionException as e:
            print e
            return jsonify(success=False, status_code=500, error_code="ERR_P02",
                message="ERR_P02: Error making payment.")
        except Exception as e:
            print e
            return jsonify(success=False, status_code=500, error_code="ERR_P03",
                message="ERR_P03: Could not establish connection with Paypal, try again later.")

        if payment is not None:
            link = [l for l in payment.links if l['rel'] == 'approval_url']

            if len(link) == 1:
                return redirect(link.pop()['href'])
        else:
            return jsonify(success=False, status_code=500, error_code="ERR_P04",
                message="ERR_P04: Could not establish connection with Paypal, try again later.")

    return render_template('p2m.html', form=form)

@app.route('/transaction/withdraw/return')
def paypal_return_url():
    data = request.args

    payment_id = data.get('paymentId')
    payer_id = data.get('PayerID')
    token = data.get('token')

    acknowledge_payment(payment_id, payer_id, token)

    return jsonify(success=True)

@app.route('/transaction/withdraw/cancel')
def paypal_cancel_url():
    data = request.args

    return jsonify(success=True)

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp