from flask import request, render_template, jsonify, url_for, redirect, g

from ajabpay.app.models import *
from ajabpay.app.utils import requires_auth
from ajabpay.index import app, db

from sqlalchemy import or_, Date, cast
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError

from datetime import date

@requires_auth
@app.route('/transaction/withdraw/<regex("^[+\d]{4}$"):id>/', methods=['POST'])
def withdraw_amount(id):
	#receive
    pass

@requires_auth
@app.route('/transaction/withdraw/<regex("^[+\d]{4}$"):id>/', methods=['POST'])
def deposit_amount(id):
	#payout
    pass