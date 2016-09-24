import os
import urllib

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
    PAYPAL_CLIENT_SECRET = "EIbbidsOH9Y_2aXPiInRs7Wf-2Emn6fBzTfHXjxgZwC23Lu00zhvA2rImcz-7nkr1OfaDNuwq4yUWgYV"
    PAYPAL_OAUTH_REDIRECT_URI='https://requestb.in/1mgb0721'

#------------------
class StagingBaseConfig(DevelopmentConfig):
    PAYPAL_MODE = "live"

    PAYPAL_CLIENT_ID = "AbkGI35O5ZanygiMziTYOI5UTDcu-DxyWxRg_3RnVjxDlcDsECuyt1JhY1e8T3gIe5Iasgn3h7V2J2ff"
    PAYPAL_CLIENT_SECRET = "EGpfDwk6j7Gk78AGv-B_57f5H372_cziqaEkT2yXjVMzGEvlY3bfswGfJ7_KaditWleKy9zMC61Cs10K"
    PAYPAL_OAUTH_REDIRECT_URI='https://requestb.in/1mgb0721'

class StagingAppConfig(StagingBaseConfig):
    SQLALCHEMY_DATABASE_URI = urllib.unquote(os.environ.get('AJABPAY_STAGING_APP_DB_URL'))

class StagingAdminConfig(StagingBaseConfig):
    SQLALCHEMY_DATABASE_URI = urllib.unquote(os.environ.get('AJABPAY_STAGING_ADMIN_DB_URL'))

#------------------
class ProductionBaseConfig(StagingConfig):
    PAYPAL_MODE = "live"

    DEBUG = False
    PAYPAL_CLIENT_ID = "AbkGI35O5ZanygiMziTYOI5UTDcu-DxyWxRg_3RnVjxDlcDsECuyt1JhY1e8T3gIe5Iasgn3h7V2J2ff"
    PAYPAL_CLIENT_SECRET = "EGpfDwk6j7Gk78AGv-B_57f5H372_cziqaEkT2yXjVMzGEvlY3bfswGfJ7_KaditWleKy9zMC61Cs10K"
    PAYPAL_OAUTH_REDIRECT_URI='https://requestb.in/1mgb0721'

class ProductionAdminConfig(ProductionBaseConfig):
    SQLALCHEMY_DATABASE_URI = urllib.unquote(os.environ.get('AJABPAY_PRODUCTION_ADMIN_DB_URL'))

class ProductionAppConfig(ProductionBaseConfig):
    SQLALCHEMY_DATABASE_URI = urllib.unquote(os.environ.get('AJABPAY_PRODUCTION_APP_DB_URL'))

#------------------

class TestingConfig(DevelopmentConfig):
    """Development configuration."""
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG_TB_ENABLED = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

#------------------

def get_default_config():
    stage = os.environ.get('AJABPAY_STAGE', ('develop-app'))

    if stage in ('develop-admin', 'develop-app'):
        return DevelopmentConfig
    elif stage in ('staging-admin', 'staging-app'):
        if stage == 'staging-admin':
            return StagingAdminConfig
        elif stage == 'staging-app':
            return StagingAppConfig
    elif stage in ('production-admin', 'production-app'):
        if stage == 'staging-admin':
            return ProductionAdminConfig
        elif stage == 'staging-app':
            return ProductionAppConfig
    else:
        raise Exception('Kindly set a valid stage for AjabPay')