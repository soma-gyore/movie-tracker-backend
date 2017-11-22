import datetime
import requests
import flask_jwt_extended
from dateutil import parser

from app.authentication.controller import UserController
from app.videos.controller import VideoController


class TestVideoResources(object):
    PORT = 5001

    @classmethod
    def setup_class(cls):
        cls.user_controller = UserController()
        cls.video_controller = VideoController()

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

    def test_post_invalid_api_key(self):
        video_dict = {
            "closeTimeStamp": 1511095414,
            "title": "A.Simpson.csalad.8x11.DVDrip.XviD.CUSTOM.HunDub-RH.avi",
            "lastPosition": 669,
            "duration": 1313
        }

        response_post_videos_request = \
            requests.post('http://127.0.0.1:{}/videos'.format(self.PORT), json=video_dict, headers={'x-api-key': 'a'})

        assert response_post_videos_request.status_code == 401

    def test_post_ok(self):
        test_user_dict = {
            "username": "testuser2",
            "password": "testpw2"
        }

        requests.post('http://127.0.0.1:{}/register'.format(self.PORT), json=test_user_dict)

        user_obj = self.user_controller.get_user_by_username('testuser2')

        video_dict = {
            "closeTimeStamp": 1511095414,
            "title": "A.Simpson.csalad.8x11.DVDrip.XviD.CUSTOM.HunDub-RH.avi",
            "lastPosition": 669,
            "duration": 1313
        }

        response_post_videos_request = \
            requests.post('http://127.0.0.1:{}/videos'
                          .format(self.PORT), json=video_dict, headers={'x-api-key': user_obj.api_key})

        assert response_post_videos_request.status_code == 200

    def test_get_ok(self):
        user_obj = self.user_controller.get_user_by_username('testuser')

        video_dict = {
            "closeTimeStamp": 1511095414,
            "title": "A.Simpson.csalad.8x11.DVDrip.XviD.CUSTOM.HunDub-RH.avi",
            "lastPosition": 669,
            "duration": 1313
        }

        requests.post('http://127.0.0.1:{}/videos'
                      .format(self.PORT), json=video_dict, headers={'x-api-key': user_obj.api_key})

        response_get_videos_request = \
            requests.get('http://127.0.0.1:{}/videos'.format(self.PORT), headers=self.headers)

        fetched_videos = response_get_videos_request.json()

        fetched_videos[0]['closeTimeStamp'] = int(parser.parse(fetched_videos[0].pop('closeDate')).timestamp())
        assert fetched_videos[0] == video_dict

    @classmethod
    def teardown_class(cls):
        user_controller = UserController()
        user_controller.delete_every_user()
        video_controller = VideoController()
        video_controller.delete_videos()
