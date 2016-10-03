from functools import wraps
from flask import request, g, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from ajabpay.index import app

from copy import copy
import xml.etree.ElementTree as ET
import urllib
import urllib2
import json

from ajabpay.config import get_default_config
Config = get_default_config()

TWO_WEEKS = 1209600

def generate_token(user, expiration=TWO_WEEKS):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({
        'id': user.id,
        'email': user.email,
    })
    return token

def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return None
    return data

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        
        if token:
            string_token = token.encode('ascii', 'ignore')
            user = verify_token(string_token)
            if user:
                g.current_user = user
                return f(*args, **kwargs)

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
API_URL = Config.API_URL 
API_SEND_PATH = Config.API_SEND_PATH 
API_GET_PATH = Config.API_GET_PATH 
SMS_XML_TEMPLATE = Config.SMS_XML_TEMPLATE 
MESSAGES_TEMPLATE = Config.MESSAGES_TEMPLATE 

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
    # API Call to Send Message(s)
    # Request	
    tumasms = Tumasms(API_KEY, API_SIGNATURE) # Instantiate API library

    if type(smses) not in (list, tuple):
        smses = [smses]
    
    for sms in smses:
        tumasms.queue_sms(sms.message_recipient, sms.message)
        app.logger.info('SMS_QUEUED', extra={
            recipient=sms.message_recipient,
            message=sms.message
        })
    
    tumasms.send_sms()

    if tumasms.status in ('SUCCESS' or 'FAIL'):
        if tumasms.status == 'SUCCESS':
            app.logger.info('SMS_SENT', extra={
                recipient=sms.message_recipient,
                message=sms.message,
                return_message=tumasms.message,
                return_description=tumasms.description,
                return_dict=response_dict
            })