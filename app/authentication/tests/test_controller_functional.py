import time

from app.authentication.controller import UserController
from app.authentication.model import User


class TestUserController(object):
    @classmethod
    def setup_class(cls):
        cls.user_controller = UserController()

    def test_create_user_and_get_user(self):
        time.sleep(2)
        self.user_controller.delete_every_user()
        test_user = User('testuser', 'testpw')

        test_user_dict = {
            'username': 'testuser', 'password': 'testpw'
        }

        self.user_controller.create_user(test_user_dict)

        fetched_user = self.user_controller.get_user_by_username('testuser')

        assert test_user.username == fetched_user.username

    def test_is_username_password_valid(self):
        self.user_controller.delete_every_user()

        test_user_dict = {
            'username': 'testuser', 'password': 'testpw'
        }

        self.user_controller.create_user(test_user_dict)

        assert self.user_controller.is_username_password_valid('testuser', 'testpw')

    def test_is_username_password_invalid(self):
        self.user_controller.delete_every_user()

        test_user_dict = {
            'username': 'testuser', 'password': 'testpw'
        }

        self.user_controller.create_user(test_user_dict)

        assert not self.user_controller.is_username_password_valid('testuser', 'somethingelse')

    def test_delete_every_user(self):
        self.user_controller.delete_every_user()

        test_user_dict = {
            'username': 'testuser', 'password': 'testpw'
        }

        self.user_controller.create_user(test_user_dict)

        self.user_controller.delete_every_user()

        assert self.user_controller.get_number_of_users() == 0

    def test_get_number_of_users(self):
        self.user_controller.delete_every_user()

        test_user_dict = {
            'username': 'testuser', 'password': 'testpw'
        }

        self.user_controller.create_user(test_user_dict)

        assert self.user_controller.get_number_of_users() == 1

    def test_is_api_key_valid(self):
        self.user_controller.delete_every_user()

        test_user_dict = {
            'username': 'testuser', 'password': 'testpw'
        }

        self.user_controller.create_user(test_user_dict)

        fetched_user = self.user_controller.get_user_by_username('testuser')

        api_key = fetched_user.api_key

        assert self.user_controller.is_api_key_valid(api_key)

    def test_get_user_name_by_api_key(self):
        self.user_controller.delete_every_user()

        test_user_dict = {
            'username': 'testuser', 'password': 'testpw'
        }

        self.user_controller.create_user(test_user_dict)

        fetched_user = self.user_controller.get_user_by_username('testuser')

        api_key = fetched_user.api_key

        fetched_username = self.user_controller.get_user_name_by_api_key(api_key)

        assert fetched_user.username == fetched_username

    def test_delete_user(self):
        self.user_controller.delete_every_user()

        test_user_dict = {
            'username': 'testuser', 'password': 'testpw'
        }

        self.user_controller.create_user(test_user_dict)

        self.user_controller.delete_user('testuser')

        assert self.user_controller.get_number_of_users() == 0
