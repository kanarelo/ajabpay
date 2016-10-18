from flask import (request, render_template, 
    jsonify, url_for, redirect, g, session, flash)

from paypalrestsdk.exceptions import (
    ConnectionError, MissingParam, MissingConfig)
from paypalrestsdk.openid_connect import Tokeninfo

from ajabpay.index import app, db, cross_origin
from ajabpay.app.models import User, AccountVerification
from sqlalchemy.exc import IntegrityError
from ajabpay.app.utils import (
    generate_token, verify_token, login_user, logout_user,
    send_registration_notification, send_verification_notification, 
    login_required, api_login_required)

from ajabpay.app.core.utils import (
    clean_phone_no, VALID_SAFARICOM_NO_REGEX)
from ajabpay.app.core.endpoint_helpers import (
    page_not_found, access_forbidden, internal_server_error)

from .paypal_oauth import (
    create_user_from_userinfo, 
    configure_openid_request, 
    configure_paypal_api)
import wtforms as forms
import datetime

#------------
paypalrestsdk = configure_paypal_api()
#------------

@app.route("/auth/user/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password\
        (incoming["email"], incoming["password"])
    
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

@app.route("/auth/user/logout", methods=["POST"])
@login_required
def logout():
    user = g.user

    if logout_user():
        return redirect(url_for("index"))
    
    return redirect(url_for("home"))

@app.route("/auth/user", methods=["GET"])
@api_login_required
def get_user():
    return jsonify(user=g.current_user)

@app.route("/auth/oauth/paypal/signin", methods=["GET"])
def login_via_paypal():
    try:
        options = configure_openid_request()

        login_url = Tokeninfo.authorize_url(options=options)
    except (ConnectionError, MissingParam, MissingConfig) as e:
        app.logger.exception(e)
        return internal_server_error()
    except Exception as e:
        app.logger.exception(e)
        return internal_server_error()

    #redirect to login page for approval
    return redirect(login_url)

class AccountVerificationForm(forms.Form):
    email_verification_code = forms.StringField('Email verification code',
        validators=[forms.validators.required()])
    mobile_verification_code = forms.StringField('Mobile verification code',
        validators=[forms.validators.required()])

def create_account_verification(user):
    now = datetime.datetime.now()
    expiry_date = now + datetime.timedelta(days=7)
    
    account_verification = AccountVerification(
        email_code=email_code,
        mobile_code=mobile_code,
        user_id=user.id,
        expiry_date=expiry_date,
        date_created=now)
    db.session.add(account_verification)

    try:
        db.session.commit()
        return account_verification
    except Exception as e:
        app.logger.exception(e)

@app.route("/auth/account-verification/verify", methods=["GET", "POST"])
def account_verification():
    mobile_code = ''
    email_code = ''

    if request.method == "GET":
        email_code = request.args.get("email_code", "")

        if email_code:
            if AccountVerification.query\
                .filter_by(email_code=email_code)\
                .filter(AccountVerification.expiry_date < datetime.datetime.now())\
                .first() is None:
                
                email_code = ''

    if request.method == "POST":
        form = AccountVerificationForm(request.form)

        if form.validate():
            email_code  = form.email_code.data
            mobile_code = form.mobile_verification_code.data

            account_verification = AccountVerification.query\
                .filter_by(mobile_code=mobile_code, email_code=email_code)\
                .filter(AccountVerification.expiry_date < datetime.datetime.now())\
                .first()

            if account_verification is not None:
                user = account_verification.user

                user.phone_verified = True
                user.email_verified = True

                db.session.commit()

                return render_template("authenticated_popup.html",
                    redirect_to=url_for('home'),
                    token=session['token'], 
                    user=user)

    return render_template("account_verification.html",
        form=form, 
        inital_mobile_code=mobile_code, 
        initial_email_code=email_code)

@app.route("/auth/oauth/paypal/create_session", methods=["GET"])
@cross_origin()
def create_session():
    data = request.args
    user = None
    registered = False

    if 'code' in data:
        code = data.get('code')
        
        try:
            options = configure_openid_request(code=code)
            
            tokeninfo = Tokeninfo.create(options=options)
            userinfo = tokeninfo.userinfo(options=options)

            userinfo_dict = userinfo.to_dict()

            if 'email' in userinfo_dict:
                email = userinfo_dict.get('email')

                user = User.query\
                    .filter_by(email=email)\
                    .first()

                if user is None:
                    user = create_user_from_userinfo(userinfo_dict)
                    registered = True
                    app.logger.debug("Paypal User %s created using userinfo" % email)
                else:
                    app.logger.debug("User %s found using email" % email)
            else:
                app.logger.debug("No email found using email")
            
            if user is not None:
                if not user.is_active:
                    app.logger.debug("User provided is inactive.")

                    flash("Your e-mail is not verified. Please check your "
                     "inbox to verify & activate your account.")
                    
                    try:
                        response = send_verification_notification(user)
                        app.logger.info(response)
                        
                        app.logger.debug('Sent verification notification to %s' % user.email)
                    except Exception as e:
                        app.logger.exception(e)

                    app.logger.debug('Redirecting to %s' % url_for("account_verification"))
                    return redirect(url_for("account_verification"))
                else:
                    app.logger.debug("User provided is active.")
                    
                    if login_user(user, remember=True):
                        app.logger.debug("logged in user: %s" % user.email)
                        app.logger.debug('session == %s' % session)
                        
                        if not registered and clean_phone_no(user.phone):
                            return render_template("authenticated_popup.html",
                                token=session['token'], user=user, redirect_to=url_for('home'))
                        elif registered:
                            if not clean_phone_no(user.phone):
                                return redirect(url_for('mpesa_mobile_phone_no'))
                            else:
                                flash("You have been registered successfully "
                                    "check your e-mail and phone for verification codes.")
                                
                                send_registration_notification(user)
                                return redirect(url_for("account_verification"))
                    else:
                        app.logger.debug("Could not login user")
                        return jsonify(success=False, message="Forbidden: error logging you in."), 403
            else:
                return jsonify(success=False, message="could not authenticate via paypal"), 403
        except Exception as e:
            app.logger.exception(e)
            return internal_server_error(e)

    elif 'error_uri' in data:
        error_uri = data.get('error_uri')
        error_description = data.get('error_description')
        error = data.get('error')

        return internal_server_error(error)
    
    return page_not_found()

class MobileNoForm(forms.Form):
    mobile_phone_no = forms.StringField('Your mobile number',
        validators=[forms.validators.required(), 
        forms.validators.Regexp(VALID_SAFARICOM_NO_REGEX)])

@app.route("/auth/profiles/mobile-no/complete", methods=["GET", "POST"])
@login_required
def mpesa_mobile_phone_no():
    form = MobileNoForm(request.form)

    if request.method == "POST" and form.validate():
        try:
            user = User.query\
                .filter_by(email=g.user.email)\
                .first()

            if user is not None:
                user.phone = form.mobile_phone_no.data

            flash("Phone number '%s' added successfully!" % user.phone)
            db.session.commit()
        except Exception as e:
            app.logger.exception(e)

        return render_template("authenticated_popup.html",
            token=session['token'], user=user, redirect_to=url_for('home'))

    return render_template('mpesa_phone_number.html', form=form)
    