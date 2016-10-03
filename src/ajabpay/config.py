import os

from setup import basedir

class BaseConfig(object):
    SECRET_KEY = "=6hkjs..-.||05b32j782ajg08guoy24t129thjvd?/@>@%6jhwmna966241?kGSHHY2932hnaj8892n?==\\\\"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

#------------------
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://ajabpay:ajabpay@localhost:3306/ajabpay'
    
    PAYPAL_MODE = "sandbox"
    PAYPAL_CLIENT_ID = "ATo_Io1R9XCX9SmfHdGbeXYSKZnireDROhLUwcjO_VtLiUx7yB7CuMjTWJO0JgfGSXhxCLsLXna3KIn0"
    PAYPAL_CLIENT_SECRET = "EE-kTL5Jy9hnFpFW_MFPJTmanXog_SSqcEOeVc7HQPEH7a5bc7G2ERGaW-09MDaa85g3dEmeH8OzSsvr"
    PAYPAL_OAUTH_REDIRECT_URI='https://localhost:8000/auth/oauth/paypal/create_session'

#------------------
class StagingBaseConfig(BaseConfig):
    PAYPAL_MODE = os.environ.get('AJABPAY_PAYPAL_MODE', 'live')
    
    PAYPAL_CLIENT_ID = os.environ.get('AJABPAY_PAYPAL_CLIENT_ID', '')
    PAYPAL_CLIENT_SECRET = os.environ.get('AJABPAY_PAYPAL_CLIENT_SECRET', '')

    PAYPAL_OAUTH_REDIRECT_URI='https://staging.ajabworld.net/auth/oauth/paypal/create_session'

class StagingAppConfig(StagingBaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('AJABPAY_STAGING_APP_DB_URL', '')

class StagingAdminConfig(StagingBaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('AJABPAY_STAGING_ADMIN_DB_URL', '')

#------------------
class ProductionBaseConfig(BaseConfig):
    PAYPAL_MODE = "live"

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    PAYPAL_CLIENT_ID = os.environ.get('AJABPAY_PAYPAL_CLIENT_ID', '')
    PAYPAL_CLIENT_SECRET = os.environ.get('AJABPAY_PAYPAL_CLIENT_SECRET', '')

    PAYPAL_OAUTH_REDIRECT_URI='https://ajabpay.ajabworld.net/auth/oauth/paypal/create_session'

#rpOAW6UhbG@b!tDVF#migJ$PQPxYK@4lChRZKrHt - ajabpay-app
#u#5YV7s@nn^FJpah43-If5^7o6-5ghas?sa#h$h(.OP099 - ajabpay-admn
class ProductionAdminConfig(ProductionBaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('AJABPAY_PRODUCTION_ADMIN_DB_URL', '')

class ProductionAppConfig(ProductionBaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('AJABPAY_PRODUCTION_APP_DB_URL', '')

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
    stage = os.environ.get('AJABPAY_STAGE', ('develop-%s' % mode))

    if stage in ('develop-admin', 'develop-app'):
        return DevelopmentConfig()
    elif stage in ('staging-admin', 'staging-app'):
        if stage == 'staging-admin':
            return StagingAdminConfig()
        elif stage == 'staging-app':
            return StagingAppConfig()
    elif stage in ('production-admin', 'production-app'):
        if stage == 'staging-admin':
            return ProductionAdminConfig()
        elif stage == 'staging-app':
            return ProductionAppConfig()
    else:
        raise Exception('Kindly set a valid stage for AjabPay')