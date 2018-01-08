import datetime
import os
import psycopg2
from urllib import parse


class Config(object):
    """Parent configuration class."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(Config):
    """Configurations for Development."""
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])

    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}/{}".format(
        url.username,
        url.password,
        url.hostname,
        url.port,
        url.path[1:]
    )
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)
    RECAPTCHA_ENABLED = True

    # official test keys. see: https://developers.google.com/recaptcha/docs/faq
    RECAPTCHA_SITE_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    RECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'


class TestConfig(Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'test'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=10)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(minutes=20)
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}/{}".format(
        url.username,
        url.password,
        url.hostname,
        url.port,
        url.path[1:]
    )
    RECAPTCHA_ENABLED = True

    # official test keys. see: https://developers.google.com/recaptcha/docs/faq
    RECAPTCHA_SITE_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    RECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'


class ProductionConfig(Config):
    """Configurations for Production."""
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=14)
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}/{}".format(
        url.username,
        url.password,
        url.hostname,
        url.port,
        url.path[1:]
    )
    SECRET_KEY = os.getenv('SECRET_KEY')
    RECAPTCHA_ENABLED = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'testing')
    app.config.from_object(app_config[config_name])
    # if config_name == 'production':
    #     app.config.from_pyfile('instance/config.py')
