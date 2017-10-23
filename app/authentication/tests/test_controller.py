
try:
    import mock
except ImportError:
    import mock

from app.authentication.controller import UserController
from app.authentication.model import User


class TestUserController(object):
    @classmethod
    def setup_class(cls):
        cls.user_controller = UserController()

    @mock.patch("app.authentication.model.User")
    def test_user_object_to_dict(self, mock_class):
        test_user = mock_class()

        test_user.id = 1
        test_user.username = 'testuser'
        test_user.password = 'testpw'

        self.user_controller.user_object = test_user

        self.user_controller.user_object_to_dict()

        user_dict = {
            'id': 1,
            'username': 'testuser',
            'password': 'testpw',
        }

        assert self.user_controller.user_dict == user_dict
