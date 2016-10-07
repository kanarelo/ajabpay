import os

from setup import basedir

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SESSION_SECRET_KEY',
        "=6hkjs.872293yn.,;xlnmpq.,L?A2hjsAS.-.||05b32j782ajg08guoy24t129thjvd?/@>@%6jhwmna966241?kGSHHY2932hnaj8892n?==\0\+\_\OPaa")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    STAGE = os.environ.get('STAGE', 'develop')

    LOGGING_LOCATION = os.environ.get('LOGGING_LOCATION', '/var/log/ajabpay/ajabpay.app.log')

    MPESA_PROJECT_MULLA_URL = os.environ.get('MPESA_ENDPOINT_URL')
    MPESA_HTACCESS_USER = os.environ.get('MPESA_HTACCESS_USER')
    MPESA_HTACCESS_PASSWORD = os.environ.get('MPESA_HTACCESS_PASSWORD')

    TUMA_SMS_API_URL = "http://tumasms.co.ke/ts/api/"
    TUMA_SMS_API_SEND_PATH = "send_sms"
    TUMA_SMS_API_GET_PATH = "get_balance"
    TUMA_SMS_XML_TEMPLATE = "<sms><recipient>%s</recipient><message>%s</message><sender>%s</sender><scheduled_date>%s</scheduled_date></sms>"
    TUMA_SMS_MESSAGES_TEMPLATE = "<request>%s</request>"

    RAVEN_DSN = os.environ.get('RAVEN_DSN')
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