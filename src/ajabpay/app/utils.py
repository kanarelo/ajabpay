from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from ajabpay.index import app

from flask import (
    request, render_template, jsonify, url_for, redirect, g, session)
from flask_login import (login_user as flask_login_user, 
    logout_user, current_user, login_required)

from copy import copy
import xml.etree.ElementTree as ET
import urllib
import urllib2
import json
import requests

TWO_WEEKS = 1209600

def login_user(user, *args, **kwargs):
    flask_login_user(user, *args, **kwargs)
    session['token'] = generate_token(user)

def generate_token(user, expiration=TWO_WEEKS):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({
        'id': user.id,
        'email': user.email,
    })
    return token

def verify_token(token):
    try:
        s = Serializer(app.config['SECRET_KEY'])
        return s.loads(token)
    except (BadSignature, SignatureExpired):
        pass

def api_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        
        if token:
            string_token = token.encode('ascii', 'ignore')
            user = verify_token(string_token)

            if user:
                g.current_user = user
                return login_required(f)(*args, **kwargs)

        return jsonify(message="Authentication is required to access this resource"), 401
    return decorated

def to_dict(et):
    """Convert Etree to dictionary
    Values picked from node text - keys from tags.
    """
    result = {}
    for item in et:
        if item.text:
            result[item.tag] = item.text
        else:
            result[item.tag] = to_dict(item)
    return result

#------------
API_URL = app.config['TUMA_SMS_API_URL'] 
API_SEND_PATH = app.config['TUMA_SMS_API_SEND_PATH'] 
API_GET_PATH = app.config['TUMA_SMS_API_GET_PATH'] 
SMS_XML_TEMPLATE = app.config['TUMA_SMS_XML_TEMPLATE'] 
MESSAGES_TEMPLATE = app.config['TUMA_SMS_MESSAGES_TEMPLATE'] 

class Tumasms(object):
    def __init__(self, api_key, api_signature, api_parameters={}, sms_messages=[]):
        """Initialize connector instance.
        """
        self.api_parameters = api_parameters
        self.api_parameters.update(dict(api_key=api_key, api_signature=api_signature))
        self.sms_messages = sms_messages
        self.response = None
        self.status = None
            
    def queue_sms(self, recipient, message, sender = "", scheduled_date = ""):
        """Add an sms to list of messages to send"""
        self.sms_messages.append(SMS_XML_TEMPLATE % (recipient, message, sender, scheduled_date))

    def _get_messages(self):
        return MESSAGES_TEMPLATE % "".join(self.sms_messages)

    def send_sms(self):
        """Build messages into parameters for a send operation
        """
        self.execute( {"messages": self._get_messages()} )

    def get_balance(self):
        """Get available text messages
        """
        self.execute({}, action=API_GET_PATH)

    def status(self):
        if self.response:
            return self.response_dict["status"]["type"]

    def message(self):
        if self.response:
            return int(self.response_dict["content"]["messages"]["message"])

    def description(self):
        if self.response:
            return self.response_dict["description"]

    def execute(self, params, action=API_SEND_PATH):
        """Send HTTP POST to action url with encoded paramters
        """
        
        #include api parameters in request (always a POST)
        params.update(self.api_parameters)
        _url = "%s%s" %(API_URL, action)
        request = urllib2.Request(_url, urllib.urlencode(params))
        self.response = urllib2.urlopen(request).read()
        self.response_xml = self.response
        _etree = ET.fromstring(self.response)
        self.response_dict = to_dict(_etree)
        self.response_json = json.dumps(self.response_dict)

def send_sms_via_tumasms(smses):
    '''
    API Call to Send Message(s) Request

    Check: ajabpay.app.models.SMSMessage

    Usage:
        >>> send_sms_via_tumasms(<smsobject>)
    '''
    tumasms = Tumasms(app.config['API_KEY'], app.config['API_SIGNATURE']) # Instantiate API library

    if smses is not None and type(smses) not in (list, tuple):
        smses = [smses]
    else:
        return
    
    for sms in smses:
        tumasms.queue_sms(sms.message_recipient, sms.message)
        app.logger.debug('SMS_QUEUED', extra=dict(
            recipient=sms.message_recipient, message=sms.message))
    
    try:
        tumasms.send_sms()

        if tumasms.status in ('SUCCESS', 'FAIL'):
            if tumasms.status == 'SUCCESS':
                for sms in smses:
                    app.logger.info('SMS_SENT', extra=dict(
                        recipient=sms.message_recipient,
                        message=sms.message,
                        return_message=tumasms.message,
                        return_description=tumasms.description,
                        return_dict=tumasms.response_dict))
            else:
                app.logger.info('SMS_SEND_FAILED', extra=dict(
                    return_message=tumasms.message,
                    return_description=tumasms.description,
                    return_dict=tumasms.response_dict))
    except Exception as e:
        app.logger.exception(e)

    return tumasms.response_dict

def send_verification_notification():
    if user.is_active:
        return
    
    if not user.email_verified:
        send_email_via_sendgrid(emails)

    if not user.phone_verified:
        send_sms_via_tumasms(sms)    

def send_html_email(emails):
    '''
    API Call to Send HTML Email(s)

    Check: ajabpay.app.models.EmailMessage

    Usage:
        >>> send_html_email(<emailobject>)
    '''
    pass

def send_push_notification(notifications):
    '''
    API Call to Send Push notification(s)

    Check: ajabpay.app.models.PushMessage

    Usage:
        >>> send_push_notification(<pushobject>)
    '''
    pass

def create_mpesa_payment_request(**kwargs):
    response = requests.post(
        '%s/payment/request' % app.config['MPESA_PROJECT_MULLA_URL'], 
        json=dict(**kwargs), 
        auth=(app.config['MPESA_HTACCESS_USER'], app.config['MPESA_HTACCESS_PASSWORD'])
    )
    app.logger.info('create_mpesa_payment_request', extra=kwargs)

    return response

def confirm_mpesa_payment_request(mpesa_txn_id):
    response = requests.get(
        '%s/payment/confirm/%s' % (app.config['MPESA_PROJECT_MULLA_URL'], mpesa_txn_id),
        auth=(app.config['MPESA_HTACCESS_USER'], app.config['MPESA_HTACCESS_PASSWORD'])
    )

    app.logger.info('confirm_mpesa_payment_request', extra={
        'mpesa_transaction_id': mpesa_txn_id})

    return response
    