import datetime
import os


class Config(object):
    """Parent configuration class."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        os.getenv('MYSQL_USER', 'admin'),
        os.getenv('MYSQL_PASSWORD', 'admin'),
        os.getenv('MYSQL_HOST', 'localhost'),
        os.getenv('MYSQL_SCHEMA', 'dev_db')
    )
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)


class TestConfig(Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'test'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=14)
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        os.getenv('MYSQL_USER', 'admin'),
        os.getenv('MYSQL_PASSWORD', 'admin'),
        os.getenv('MYSQL_HOST', 'localhost'),
        os.getenv('MYSQL_SCHEMA', 'test_db')
    )


class ProductionConfig(Config):
    """Configurations for Production."""
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=14)


app_config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'testing')
    app.config.from_object(app_config[config_name])
    if config_name == 'production':
        app.config.from_pyfile('instance/config.py')
