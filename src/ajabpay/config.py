import os
from setup import basedir

from flask import g
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_cors import CORS, cross_origin

import raven
from raven.contrib.flask import Sentry
from raven import Client

import logging
from datetime import timedelta

from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger as json_logger

STATIC_FOLDER = os.path.join(basedir, "..", "static") 
TEMPLATE_FOLDER = os.path.join(basedir, "templates")

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SESSION_SECRET_KEY',
        "=6hkjs.872293yn.,;xlnmpq.,L?A2hjsAS.-.||05b32j782ajg08guoy24t129thjvd?/@>@%6jhwmna966241?kGSHHY2932hnaj8892n?==\0\+\_\OPaa")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    STAGE = os.environ.get('STAGE', 'develop')

    STATIC_FOLDER = os.environ.get("STATIC_FOLDER", STATIC_FOLDER)
    TEMPLATE_FOLDER = os.environ.get("TEMPLATE_FOLDER", TEMPLATE_FOLDER)

    LOGGING_LOCATION = os.environ.get('LOGGING_LOCATION', '/var/log/ajabpay/ajabpay.app.log')

    MPESA_PROJECT_MULLA_URL = os.environ.get('MPESA_ENDPOINT_URL')
    MPESA_HTACCESS_USER = os.environ.get('MPESA_HTACCESS_USER')
    MPESA_HTACCESS_PASSWORD = os.environ.get('MPESA_HTACCESS_PASSWORD')

    TUMA_SMS_API_KEY = os.environ.get('TUMA_SMS_API_KEY')
    TUMA_SMS_API_SECRET = os.environ.get('TUMA_SMS_API_SECRET')
    TUMA_SMS_API_URL = "http://tumasms.co.ke/ts/api/"
    TUMA_SMS_API_SEND_PATH = "send_sms"
    TUMA_SMS_API_GET_PATH = "get_balance"
    TUMA_SMS_XML_TEMPLATE = "<sms><recipient>%s</recipient><message>%s</message><sender>%s</sender><scheduled_date>%s</scheduled_date></sms>"
    TUMA_SMS_MESSAGES_TEMPLATE = "<request>%s</request>"

    SENTRY_INCLUDE_PATHS = [__name__.split('.', 1)[0]]
    SENTRY_USER_ATTRS = ['email']

    MAILGUN_ENDPOINT = os.environ.get("MAILGUN_ENDPOINT")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

    AJABPAY_MAIN_EMAIL = os.environ.get('AJABPAY_MAIN_EMAIL', "info@ajabworld.net")

    try: 
        SENTRY_RELEASE = raven.fetch_git_sha(os.path.dirname(__file__))
    except:
        pass
    
    SENTRY_STAGE = STAGE.split('-')[0]
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    SITE_URL = 'http://localhost:8000'

#------------------
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://ajabpay:ajabpay@localhost:3306/ajabpay'

    DEBUG = True
    
    PAYPAL_MODE = "sandbox"
    PAYPAL_CLIENT_ID = "ATo_Io1R9XCX9SmfHdGbeXYSKZnireDROhLUwcjO_VtLiUx7yB7CuMjTWJO0JgfGSXhxCLsLXna3KIn0"
    PAYPAL_CLIENT_SECRET = "EE-kTL5Jy9hnFpFW_MFPJTmanXog_SSqcEOeVc7HQPEH7a5bc7G2ERGaW-09MDaa85g3dEmeH8OzSsvr"
    PAYPAL_OAUTH_REDIRECT_URI='http://localhost:8000/auth/oauth/paypal/create_session'

#------------------
class StagingBaseConfig(BaseConfig):
    DEBUG = True
    
    PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'live')
    
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID', '')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET', '')

    SITE_URL = 'https://staging.ajabworld.net'
    PAYPAL_OAUTH_REDIRECT_URI='%s/auth/oauth/paypal/create_session' % SITE_URL

class StagingAppConfig(StagingBaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('STAGING_APP_DB_URL', '')

class StagingAdminConfig(StagingBaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('STAGING_ADMIN_DB_URL', '')

#------------------
class ProductionBaseConfig(BaseConfig):
    PAYPAL_MODE = "live"

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID', '')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET', '')

    SITE_URL = 'https://ajabpay.ajabworld.net'
    PAYPAL_OAUTH_REDIRECT_URI='%s/auth/oauth/paypal/create_session' % SITE_URL

class ProductionAdminConfig(ProductionBaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('ADMIN_DB_URL', '')

class ProductionAppConfig(ProductionBaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('APP_DB_URL', '')

#------------------
class TestingConfig(DevelopmentConfig):
    """Development configuration."""
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG_TB_ENABLED = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

#------------------
def get_default_config(mode='app'):
    stage = os.environ.get('STAGE', ('develop-%s' % mode))

    if stage in ('develop-admin', 'develop-app'):
        return DevelopmentConfig()
    elif stage in ('staging-admin', 'staging-app'):
        if '-admin' in stage:
            return StagingAdminConfig()
        else:
            return StagingAppConfig()
    elif stage in ('production-admin', 'production-app'):
        if '-admin' in stage:
            return ProductionAdminConfig()
        else:
            return ProductionAppConfig()
    else:
        raise Exception('Kindly set a valid stage for AjabPay')

def setup_database(app):
    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)

    return db, bcrypt

def setup_auth(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    return login_manager

def setup_cors(app):
    cors = CORS(app)

    return cors

def setup_session(app):
    app.permanent_session_lifetime = timedelta(hours=1)

def setup_logging(app):
    if (app.config['DEBUG'] == False) or ('production' in app.config['STAGE']):
        formatter = json_logger.JsonFormatter()
    else:
        logging.getLogger('flask_cors').level = logging.DEBUG
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    client = Client()
    sentry = Sentry(app, client=client, logging=True, level=logging.INFO)

    log_handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=10000, backupCount=10)
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)

    return (sentry, client)

def setup_current_user(client):
    def wrap():
        g.user = current_user
        
        if hasattr(g.user, 'email'):
            client.user_context({ 'email': g.user.email })

    return wrap