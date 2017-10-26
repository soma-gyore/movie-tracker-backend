import os
import shlex
import signal
import subprocess

import requests
import time

from app.authentication.controller import UserController


class TestAuthenticationResources(object):

    pid = 0
    jwt = ""
    user_controller = UserController()

    @classmethod
    def setup_class(cls):
        command = shlex.split("gunicorn --bind '127.0.0.1:5002' wsgi:flask_app")
        process = subprocess.Popen(command)
        cls.pid = process.pid

        test_user_dict = {
            "username": "testuser",
            "password": "testpw"
        }

        cls.user_controller.delete_every_user()
        cls.user_controller.create_user(test_user_dict)

        login_response = requests.post('http://127.0.0.1:5002/login', json=test_user_dict)

        jwt = login_response.json()['accessToken']

        refresh_jwt = login_response.json()['refreshToken']

        cls.headers = {
            "Authorization": "Bearer {}".format(jwt)
        }

        cls.refresh_headers = {
            "Authorization": "Bearer {}".format(refresh_jwt)
        }

    @classmethod
    def teardown_class(cls):
        os.kill(cls.pid, signal.SIGTERM)

    def test_register_and_login_ok(self):
        self.user_controller.delete_every_user()
        test_user_dict = {
            "username": "testuser2",
            "password": "testpw2"
        }

        requests.post('http://127.0.0.1:5002/register', json=test_user_dict)

        login_response = requests.post('http://127.0.0.1:5002/login', json=test_user_dict)

        assert login_response.status_code == 200

    def test_refresh_token_unauthorized(self):
        refresh_token_response = requests.get('http://127.0.0.1:5002/refresh-token')

        assert refresh_token_response.status_code == 401

    def test_refresh_token_unauthorized_with_access_token(self):
        refresh_token_response = requests.get('http://127.0.0.1:5002/refresh-token', headers=self.headers)
        assert refresh_token_response.status_code == 422

    def test_refresh_token_ok(self):
        refresh_token_response = requests.get('http://127.0.0.1:5002/refresh-token', headers=self.refresh_headers)

        assert refresh_token_response.status_code == 200

    def test_register_user_already_exist(self):
        self.user_controller.delete_every_user()
        test_user_dict = {
            "username": "testuser3",
            "password": "testpw3"
        }

        requests.post('http://127.0.0.1:5002/register', json=test_user_dict)
        register_response = requests.post('http://127.0.0.1:5002/register', json=test_user_dict)

        assert register_response.status_code == 409

    def test_login_unauthorized(self):
        self.user_controller.delete_every_user()
        test_user_dict = {
            "username": "testuser4",
            "password": "testpw4"
        }

        requests.post('http://127.0.0.1:5002/register', json=test_user_dict)

        login_user_dict = {
            "username": "testuser4",
            "password": "somethingelse"
        }

        login_response = requests.post('http://127.0.0.1:5002/login', json=login_user_dict)

        assert login_response.status_code == 401

    def test_delete_user_unauthorized(self):
        delete_response = requests.delete('http://127.0.0.1:5002/users?username=testuser')
        assert delete_response.status_code == 401

    def test_delete_user_user_does_not_exist(self):
        delete_response = requests.delete('http://127.0.0.1:5002/users?username=nonexistinguser', headers=self.headers)
        assert delete_response.status_code == 404

    def test_delete_user_user_ok(self):
        self.user_controller.delete_every_user()
        test_user_dict = {
            "username": "testuser5",
            "password": "testpw5"
        }

        requests.post('http://127.0.0.1:5002/register', json=test_user_dict)

        delete_response = requests.delete('http://127.0.0.1:5002/users?username=testuser5', headers=self.headers)
        assert delete_response.status_code == 200

    def test_get_user_unauthorized(self):
        delete_response = requests.get('http://127.0.0.1:5002/users?api-key=someapikey')
        assert delete_response.status_code == 401

    def test_get_user_user_does_not_exist(self):
        delete_response = requests.get('http://127.0.0.1:5002/users?api-key=someapikey', headers=self.headers)
        assert delete_response.status_code == 404

    def test_get_user_user_ok(self):
        self.user_controller.delete_every_user()
        test_user_dict = {
            "username": "testuser6",
            "password": "testpw6"
        }

        requests.post('http://127.0.0.1:5002/register', json=test_user_dict)

        fetched_user = self.user_controller.get_user_by_username('testuser6')

        delete_response = requests.get(
            'http://127.0.0.1:5002/users?api-key={}'.format(fetched_user.api_key),
            headers=self.headers
        )
        assert delete_response.status_code == 200

    def test_logout_access_unauthorized(self):
        response_logout_access = requests.delete('http://127.0.0.1:5002/logout-access')
        assert response_logout_access.status_code == 401

    def test_logout_access_ok(self):
        response_logout_access = requests.delete('http://127.0.0.1:5002/logout-access', headers=self.headers)
        assert response_logout_access.status_code == 200

    def test_logout_refresh_unauthorized(self):
        response_logout_access = requests.delete('http://127.0.0.1:5002/logout-refresh')
        assert response_logout_access.status_code == 401

    def test_logout_resfresh_ok(self):
        response_logout_access = requests.delete('http://127.0.0.1:5002/logout-refresh', headers=self.refresh_headers)
        assert response_logout_access.status_code == 200


