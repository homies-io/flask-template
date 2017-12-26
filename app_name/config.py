"""
Configurations for various environments
"""
import os

# pylint: disable=too-few-public-methods


class Config(object):
    """
    Base Config class
    """
    CORS_HEADERS = 'Content-Type'

    SECURITY_URL_PREFIX = "/admin"

    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    SECURITY_TRACKABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_EMAIL_SENDER = ''
    SECURITY_SEND_REGISTER_EMAIL = True
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = True

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SUPERUSER_EMAIL = 'lol'

    FACEBOOK_APP_ID = 'lol'
    FACEBOOK_APP_SECRET = 'lol'

    MAIL_DEFAULT_SENDER = ''
    MAIL_SERVER = ''
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_PORT = 587
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    DEFAULT_USER_TYPE = 'ExampleUser'


class ProductionConfig(Config):
    """
    Config vars exclusively for production
    """
    PRODUCTION = True

    SECRET_KEY = 'lol'

    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'lol'

    SUPERUSER_PASSWORD = 'lol'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'

    PORT = 80


class DevelopmentConfig(Config):
    """
    Config vars exclusively for development
    """
    DEBUG = True

    SECRET_KEY = 'lol'

    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'lol'

    SUPERUSER_PASSWORD = 'lol'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

    PORT = 5000


class LocalConfig(DevelopmentConfig):
    """
    Config vars exclusively for local development
    """
    LOCAL = True

    SUPERUSER_PASSWORD = 'lol'

    HOST = 'http://0.0.0.0'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///local.db'


class TestingConfig(DevelopmentConfig):
    """
    Config vars exclusively for testing
    """
    TESTING = True

    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'


CONFIGS = {
    'PRODUCTION': 'ProductionConfig',
    'DEVELOPMENT': 'DevelopmentConfig',
    'LOCAL': 'LocalConfig',
    'TESTING': 'TestingConfig'
}


def get_config():
    """
    Gets the config type set by environment variable
    :return: config object
    """

    config_type = os.getenv('ENVIRONMENT', 'LOCAL')
    return 'app_name.config.' + CONFIGS.get(config_type)