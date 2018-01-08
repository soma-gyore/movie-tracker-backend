import time

import os

from datetime import datetime

from dateutil import parser

from app.videos.controller import VideoController
from app.authentication.controller import UserController
from app.authentication.model import User


class TestVideoController(object):

    @classmethod
    def setup_class(cls):
        cls.sample_video_dict = {
            "closeTimeStamp": 1511095414,
            "title": "A.Simpson.csalad.8x11.DVDrip.XviD.CUSTOM.HunDub-RH.avi",
            "lastPosition": 669,
            "duration": 1313
        }

        cls.sample_video_dict2 = {
            "closeTimeStamp": 1511095404,
            "title": "A.Simpson.csalad.8x12.DVDrip.XviD.CUSTOM.HunDub-RH.avi",
            "lastPosition": 659,
            "duration": 1323
        }

        cls.sample_videos = [cls.sample_video_dict, cls.sample_video_dict2]

        cls.video_controller = VideoController()
        cls.user_controller = UserController()

        cls.user_controller.delete_every_user()

        test_user_dict = {
            'username': 'testuser', 'password': 'testpw'
        }

        cls.user_controller.create_user(test_user_dict)
        cls.user_obj = cls.user_controller.get_user_by_username('testuser')

    @staticmethod
    def replace_close_date_to_close_time_stamp(fetched_videos):
        for fetched_video in fetched_videos:
            fetched_video['closeTimeStamp'] = int(fetched_video.pop('closeDate').timestamp())

    def test_create_video(self):

        self.video_controller.create_video(self.sample_video_dict, self.user_obj)

        fetched_videos = self.video_controller.get_videos_by_username(self.user_obj.username)

        fetched_videos[0]['closeTimeStamp'] = int(fetched_videos[0].pop('closeDate').timestamp())
        del fetched_videos[0]['imageUrl']
        assert fetched_videos[0] == self.sample_video_dict

    def test_get_videos_by_username(self):
        self.video_controller.delete_videos()

        self.video_controller.create_video(self.sample_video_dict, self.user_obj)
        self.video_controller.create_video(self.sample_video_dict2, self.user_obj)

        fetched_videos = self.video_controller.get_videos_by_username('testuser')

        self.replace_close_date_to_close_time_stamp(fetched_videos)

        for fetched_video in fetched_videos:
            del fetched_video['imageUrl']

        assert fetched_videos == self.sample_videos

    @classmethod
    def teardown_class(cls):
        user_controller = UserController()
        user_controller.delete_every_user()
