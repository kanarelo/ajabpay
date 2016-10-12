from flask import request, render_template, jsonify, url_for, redirect, g

from ajabpay.app.models import *
from ajabpay.app.utils import login_required
from ajabpay.app.core.utils import VALID_SAFARICOM_NO_REGEX
from ajabpay.index import app, cross_origin

from sqlalchemy import or_, Date, cast
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError

from datetime import date
from .actions.payment import *

from .webhooks import webhook

import wtforms as forms

class PaypalPaymentForm(forms.Form):
    #0703266888, not +254703266888
    mobile_phone_no = forms.StringField('recipient',
        validators=[forms.validators.data_required(), 
        forms.validators.Regexp(VALID_SAFARICOM_NO_REGEX)])
    amount = forms.DecimalField('amount', places=2, rounding=None, validators=[
        forms.validators.data_required(), forms.validators.NumberRange(0, 251)])

@app.route('/txn/p2m', methods=['GET', 'POST'])
@login_required
def paypal2mpesa():
    form = PaypalPaymentForm(request.form)

    if request.method == 'POST' and form.validate():
        email = g.user.email
        amount = form.amount.data
        mpesa_recipient = form.mobile_phone_no.data

        try:
            payment = create_payment_transaction(email, mpesa_recipient, amount=amount,
                return_url=url_for('paypal2mpesa_return'), cancel_url=url_for('paypal2mpesa_cancel'))
        except PaypalTransactionException as e:
            app.logger.exception(e)
            return jsonify(success=False, status_code=500, error_code="ERR_P02",
                message="ERR_P02: Error making payment.")
        except Exception as e:
            app.logger.exception(e)
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

def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)

    def _length(form, field):
        l = field.data and len(field.data) or 0
        if (l < min) or (max != -1) and (l > max):
            raise forms.validators.ValidationError(message)

    return _length

class PaypalReturnForm(forms.Form):
    paymentId = forms.StringField('paymentId', validators=[
        forms.validators.data_required(), length(min=26, max=31),
        forms.validators.Regexp(r'^PAY-(\w{22,27})$')])
    PayerID = forms.StringField('PayerID', validators=[
        forms.validators.data_required(), length(min=11, max=18),
        forms.validators.Regexp(r'^(\w{11,18})$')])
    token = forms.StringField('token', validators=[
        forms.validators.data_required(), length(min=19, max=23),
        forms.validators.Regexp(r'^EC-(\w{16,20})$')])

def clean_amount(amount):
    if not amount:
        return 0

    try:
        amount = D(amount)
    except:
        return 0
    else:
        if (amount < 0) and (amount > 50000):
            return 0

        return amount

@app.route('/txn/p2m/calc', methods=['POST'])
def paypal2mpesa_calculate():
    incoming = request.get_json() or {}

    exchange_amount = 0
    
    from_currency = incoming.get("from_currency", "KES")
    amount = clean_amount(incoming.get("amount", "0"))
    to_currency = incoming.get("to_currency", "USD")

    try:
        exchange_amount = get_exchange_amount(D(amount), 
            from_currency=from_currency, to_currency=to_currency)
    except:
        return jsonify(message="Error calculating: Invalid data", success=False), 400

    return jsonify(success=True,
        exchange_amount=exchange_amount, product="p2m")

@app.route('/txn/p2m/r', methods=['GET'])
@cross_origin()
def paypal2mpesa_return():
    data = request.args
    form = PaypalReturnForm(data)

    if form.validate():
        payment_id = data.get('paymentId')
        payer_id = data.get('PayerID')
        token = data.get('token')

        if payment_id and payer_id and token:
            try:
                acknowledge_payment(payment_id, payer_id, token)
                db.session.commit()

                return jsonify(
                    message='Payment %s acknownledged and posted to ledger' % payment_id, success=True)
            except Exception as e:
                db.session.rollback()

                app.logger.exception(e)
                return jsonify(message='Could not acknowledge payment', success=False), 500
        else:
            return jsonify(message='Resource not found', success=False), 404
    else:
        return jsonify(success=False, message="Data did not validate."), 403

@app.route('/txn/p2m/c')
@cross_origin()
def paypal2mpesa_cancel():
    data = request.args

    message = 'Paypal to M-Pesa transaction cancelled'
    app.logger.info(message, extra=dict(data))

    return jsonify(success=True, message=message)