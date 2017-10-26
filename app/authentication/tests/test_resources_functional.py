import os
import shlex
import signal
import subprocess

import requests
import time

from app.authentication.controller import UserController


class TestAuthenticationResources(object):

    PORT = 5001

    @classmethod
    def setup_class(cls):
        test_user_dict = {
            "username": "testuser",
            "password": "testpw"
        }

        requests.post('http://127.0.0.1:{}/register'.format(cls.PORT), json=test_user_dict)

        login_response = requests.post('http://127.0.0.1:{}/login'.format(cls.PORT), json=test_user_dict)

        jwt = login_response.json()['accessToken']

        refresh_jwt = login_response.json()['refreshToken']

        cls.headers = {
            "Authorization": "Bearer {}".format(jwt)
        }

        cls.refresh_headers = {
            "Authorization": "Bearer {}".format(refresh_jwt)
        }

    def test_register_and_login_ok(self):
        test_user_dict = {
            "username": "testuser2",
            "password": "testpw2"
        }

        requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)

        login_response = requests.post('http://127.0.0.1:{}/login'.format(self.PORT), json=test_user_dict)

        assert login_response.status_code == 200

    def test_refresh_token_unauthorized(self):
        refresh_token_response = requests.get('http://127.0.0.1:{}/refresh-token'.format(self.PORT))

        assert refresh_token_response.status_code == 401

    def test_refresh_token_unauthorized_with_access_token(self):
        refresh_token_response = requests.get('http://127.0.0.1:{}/refresh-token'.format(self.PORT), headers=self.headers)
        assert refresh_token_response.status_code == 422

    def test_refresh_token_ok(self):
        refresh_token_response = requests.get('http://127.0.0.1:{}/refresh-token'.format(self.PORT), headers=self.refresh_headers)

        assert refresh_token_response.status_code == 200

    def test_register_user_already_exist(self):
        test_user_dict = {
            "username": "testuser3",
            "password": "testpw3"
        }

        requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)
        register_response = requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)

        assert register_response.status_code == 409

    def test_login_unauthorized(self):
        test_user_dict = {
            "username": "testuser4",
            "password": "testpw4"
        }

        requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)

        login_user_dict = {
            "username": "testuser4",
            "password": "somethingelse"
        }

        login_response = requests.post('http://127.0.0.1:{}/login'.format(self.PORT), json=login_user_dict)

        assert login_response.status_code == 401

    def test_delete_user_unauthorized(self):
        delete_response = requests.delete('http://127.0.0.1:{}/users?username=testuser'.format(self.PORT))
        assert delete_response.status_code == 401

    def test_delete_user_user_does_not_exist(self):
        delete_response = requests.delete('http://127.0.0.1:{}/users?username=nonexistinguser'.format(self.PORT), headers=self.headers)
        assert delete_response.status_code == 404

    def test_delete_user_user_ok(self):
        test_user_dict = {
            "username": "testuser5",
            "password": "testpw5"
        }

        requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)

        delete_response = requests.delete(
            'http://127.0.0.1:{}/users?username=testuser5'.format(self.PORT),
            headers=self.headers
        )
        assert delete_response.status_code == 200

    def test_get_user_unauthorized(self):
        delete_response = requests.get('http://127.0.0.1:{}/users?api-key=someapikey'.format(self.PORT))
        assert delete_response.status_code == 401

    def test_get_user_user_does_not_exist(self):
        delete_response = requests.get(
            'http://127.0.0.1:{}/users?api-key=someapikey'.format(self.PORT), headers=self.headers
        )
        assert delete_response.status_code == 404

    def test_logout_access_unauthorized(self):
        response_logout_access = requests.delete('http://127.0.0.1:{}/logout-access'.format(self.PORT))
        assert response_logout_access.status_code == 401

    def test_logout_access_ok(self):
        response_logout_access = requests.delete(
            'http://127.0.0.1:{}/logout-access'.format(self.PORT),
            headers=self.headers)
        assert response_logout_access.status_code == 200

    def test_logout_refresh_unauthorized(self):
        response_logout_access = requests.delete('http://127.0.0.1:{}/logout-refresh'.format(self.PORT))
        assert response_logout_access.status_code == 401

    def test_logout_resfresh_ok(self):
        response_logout_access = requests.delete(
            'http://127.0.0.1:{}/logout-refresh'.format(self.PORT), headers=self.refresh_headers
        )
        assert response_logout_access.status_code == 200
