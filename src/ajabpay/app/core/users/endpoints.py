from flask import (request, render_template, 
    jsonify, url_for, redirect, g, session, flash)

from paypalrestsdk.exceptions import (
    ConnectionError, MissingParam, MissingConfig)

from ajabpay.index import app, db, cross_origin
from ajabpay.app.models import User
from sqlalchemy.exc import IntegrityError
from ajabpay.app.utils import (
    generate_token, verify_token, login_user,
    send_verification_notification, login_required, api_login_required)

from ajabpay.app.core.utils import clean_phone_no, VALID_SAFARICOM_NO_REGEX
from ajabpay.app.core.endpoint_helpers import (
    page_not_found, access_forbidden, internal_server_error)

from .paypal_oauth import (
    create_user_from_userinfo, 
    configure_openid_request, 
    configure_paypal_api)
import wtforms as forms

#------------
paypalrestsdk = configure_paypal_api()
from paypalrestsdk.openid_connect import Tokeninfo
#------------

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

@app.route("/auth/oauth/paypal/create_session", methods=["GET"])
@cross_origin()
def create_session():
    data = request.args
    user = None

    if 'code' in data:
        code = data.get('code')
        
        try:
            options = configure_openid_request(code=code)
            
            tokeninfo = Tokeninfo.create(options=options)
            userinfo = tokeninfo.userinfo(options=options)

            userinfo_dict = userinfo.to_dict()

            if 'email' in userinfo_dict:
                user = User.query\
                    .filter_by(email=userinfo_dict.get('email'))\
                    .first()

                if user is None:
                    user = create_user_from_userinfo(userinfo_dict)
            
            if user is not None:
                if not user.is_active:
                    flash("Your e-mail is not verified. Please check your "
                     "inbox to verify & activate your account.")
                    send_verification_notification(user)

                    return redirect(url_for("email-verification"))
                else:
                    if login_user(user, remember=True):
                        app.logger.debug("logged in user: %s" % user.email)
                        app.logger.debug('session == %s' % session)
                        
                        if clean_phone_no(user.phone):
                            return render_template("authenticated_popup.html",
                                token=session['token'], user=user, redirect_to=url_for('home'))
                        else:
                            return redirect(url_for('mpesa_mobile_phone_no'))
                    else:
                        jsonify(success=False, message="Forbidden: error logging you in."), 403
            else:
                return jsonify(success=False, message="could not authenticate via paypal"), 403
        except Exception as e:
            app.logger.exception(e)
            return internal_server_error(e)
    elif 'error_uri' in data:
        error_uri = data.get('error_uri')
        error_description = data.get('error_description')
        error = data.get('error')

        return internal_server_error()
    else:
        return page_not_found()

    return jsonify(dict(**data))

class MobileNoForm(forms.Form):
    mobile_phone_no = forms.StringField('Update your M-Pesa Safaricom number',
        validators=[forms.validators.required(), 
        forms.validators.Regexp(VALID_SAFARICOM_NO_REGEX)])

@app.route("/auth/profiles/mobile-no/complete", methods=["GET", "POST"])
@login_required
def mpesa_mobile_phone_no():
    form = MobileNoForm(request.form)

    if request.method == "POST" and form.validated():
        try:
            user = User.query\
                .filter_by(email=g.user.email)
            user.phone = form.phone.data

            flash("Phone number '%s' added successfully!" % user.phone)
            db.session.commit()
        except Exception as e:
            app.logger.exception(e)

        return render_template("authenticated_popup.html",
            token=session['token'], user=user, redirect_to=url_for('home'))

    return render_template('mpesa_phone_number.html', form=form)
    