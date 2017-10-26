
try:
    import mock
except ImportError:
    import mock

from app.authentication.controller import UserController
from app.authentication.model import User


class UnitTestUserController(object):
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


class FunctionalTestUserController(object):
    @classmethod
    def setup_class(cls):
        cls.user_controller = UserController()

    def test_create_user(self):
        test_user = {
            'username': 'testuser', 'password': 'testpw'
        }
        self.user_controller.create_user(test_user)

        self.user_controller.get_user_by_username('test_user')
