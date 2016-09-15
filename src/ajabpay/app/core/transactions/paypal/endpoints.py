from flask import request, render_template, jsonify, url_for, redirect, g

from ajabpay.app.models import *
from ajabpay.app.utils import requires_auth
from ajabpay.index import app, db

from sqlalchemy import or_, Date, cast
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError

from datetime import date

from .actions.sale import *

from wtforms import (Form, DecimalField, BooleanField, StringField, PasswordField, validators)

class PaypalWithdrawForm(Form):
    email = StringField('Email Address', validators=[
        validators.required(), validators.Length(min=6, max=72)
    ])
    amount = DecimalField('Amount', validators=[
        validators.required(), validators.NumberRange(0, 250)], places=2, rounding=None)

@requires_auth
@app.route('/transaction/withdraw/', methods=['POST'])
def paypal_withdraw_amount():
    form = PaypalWithdrawForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data
        amount = form.amount.data

        payment = create_paypal_payment_transaction(
            amount,
            return_url=url_for('paypal_return_url'),
            cancel_url=url_for('paypal_cancel_url'),
            create=True
        )

        if payment:
            link = [l for l in payment.links if l['ref'] == 'approval_url']
            return redirect(link[0]['href'])
        else:
            return jsonify(success=False)

    return render_template('register.html', form=form)

@app.route('/transaction/sale/return')
def paypal_return_url():
    data = request.get_json()

    print data

    return jsonify(success=True)

@app.route('/transaction/sale/cancel/')
def paypal_cancel_url():
    data = request.get_json()

    print data

    return jsonify(success=True)