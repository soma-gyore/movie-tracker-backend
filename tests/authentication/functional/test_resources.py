from application import flask_app


class TestAuthenticationResources(object):
    @classmethod
    def setup_class(cls):
        cls.test_app = flask_app.app.test_client()
