from flask_restful import Resource
from flask import request, json

from app.shared import errorhandler
from app.shared.response import ResponseCreator
from app.videos.controller import VideoController
from app.authentication.controller import UserController

import flask_jwt_extended


class Videos(Resource):
    def __init__(self):
        self.video_controller = VideoController()
        self.response_creator = ResponseCreator()
        self.user_controller = UserController()

    @errorhandler.internal_server_error
    @errorhandler.invalid_api_key
    def post(self):
        api_key = request.headers.get('x-api-key')

        user = self.user_controller.get_user_by_api_key(api_key)

        self.video_controller.create_video(request.json, user)
        return self.response_creator.ok()

    @flask_jwt_extended.jwt_required
    @errorhandler.internal_server_error
    def get(self):
        username = flask_jwt_extended.get_jwt_identity()
        videos_dict = self.video_controller.get_videos_by_username(username)
        videos_json = json.dumps(videos_dict)
        return self.response_creator.create_response(videos_json)
