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
        user_controller = UserController()
        user_controller.delete_every_user()

        test_user_dict = {
            "username": "testuser",
            "password": "testpw",
            "reCaptchaResponse": "asd"
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
            "password": "testpw2",
            "reCaptchaResponse": "asd"
        }

        requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)

        login_response = requests.post('http://127.0.0.1:{}/login'.format(self.PORT), json=test_user_dict)

        assert login_response.status_code == 200

    def test_refresh_token_unauthorized(self):
        refresh_token_response = requests.get('http://127.0.0.1:{}/refresh-token'.format(self.PORT))

        assert refresh_token_response.status_code == 401

    def test_refresh_token_unauthorized_with_access_token(self):
        refresh_token_response = requests.get('http://127.0.0.1:{}/refresh-token'.format(self.PORT),
                                              headers=self.headers)
        assert refresh_token_response.status_code == 422

    def test_refresh_token_ok(self):
        refresh_token_response = requests.get('http://127.0.0.1:{}/refresh-token'.format(self.PORT),
                                              headers=self.refresh_headers)

        assert refresh_token_response.status_code == 200

    def test_register_user_already_exist(self):
        test_user_dict = {
            "username": "testuser3",
            "password": "testpw3",
            "reCaptchaResponse": "asd"
        }

        requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)
        register_response = requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)

        assert register_response.status_code == 409

    def test_login_unauthorized(self):
        test_user_dict = {
            "username": "testuser4",
            "password": "testpw4",
            "reCaptchaResponse": "asd"
        }

        requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)

        login_user_dict = {
            "username": "testuser4",
            "password": "somethingelse",
            "reCaptchaResponse": "asd"
        }

        login_response = requests.post('http://127.0.0.1:{}/login'.format(self.PORT), json=login_user_dict)

        assert login_response.status_code == 401

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

    def test_delete_account_user_does_not_exists(self):
        test_user_dict = {
            "username": "testuser5",
            "password": "testpw5",
            "reCaptchaResponse": "asd"
        }

        requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)

        login_response = requests.post('http://127.0.0.1:{}/login'.format(self.PORT), json=test_user_dict)

        jwt = login_response.json()['accessToken']

        headers = {
            "Authorization": "Bearer {}".format(jwt)
        }

        requests.delete(
            'http://127.0.0.1:{}/account'.format(self.PORT), headers=headers
        )

        time.sleep(.1)

        response_delete_account = requests.delete(
            'http://127.0.0.1:{}/account'.format(self.PORT), headers=headers
        )
        assert response_delete_account.status_code == 404

    def test_delete_account_ok(self):
        test_user_dict = {
            "username": "testuser6",
            "password": "testpw6",
            "reCaptchaResponse": "asd"
        }

        requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)

        login_response = requests.post('http://127.0.0.1:{}/login'.format(self.PORT), json=test_user_dict)

        jwt = login_response.json()['accessToken']

        headers = {
            "Authorization": "Bearer {}".format(jwt)
        }

        time.sleep(.2)

        response_delete_account = requests.delete(
            'http://127.0.0.1:{}/account'.format(self.PORT), headers=headers
        )
        assert response_delete_account.status_code == 200

    @classmethod
    def teardown_class(cls):
        user_controller = UserController()
        user_controller.delete_every_user()
