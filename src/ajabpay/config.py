import os

from setup import basedir

class BaseConfig(object):
    SECRET_KEY = "=6hkjs..-.||05b32j782ajg08guoy24t129thjvd?/@>@%6jhwmna966241?kGSHHY2932hnaj8892n?==\\\\"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/ajabpay.sqlite3'

class TestingConfig(object):
    """Development configuration."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG_TB_ENABLED = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
