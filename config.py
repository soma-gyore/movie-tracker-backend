import os


class Config(object):
    """Parent configuration class."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestConfig(Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Configurations for Production."""
    pass


app_config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'development')
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('instance/config.py')
