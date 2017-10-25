from flask import json, request
from flask_restful import Resource
from app.shared.response import ResponseCreator
from app.authentication.controller import UserController
from app.shared import errorhandler

import flask_jwt_extended


class Register(Resource):
    def __init__(self):
        self.user_controller = UserController()
        self.response_creator = ResponseCreator()

    @errorhandler.internal_server_error
    @errorhandler.user_already_exists
    def post(self):
        request_body_dict = request.json
        self.user_controller.create_user(request_body_dict)
        return self.response_creator.created()


class Login(Resource):
    def __init__(self):
        self.user_controller = UserController()
        self.response_creator = ResponseCreator()

    @staticmethod
    def get_tokens_dict(username):
        tokens_dict = {
            'accessToken': flask_jwt_extended.create_access_token(identity=username),
            'refreshToken': flask_jwt_extended.create_refresh_token(identity=username)
        }

        return tokens_dict

    @errorhandler.internal_server_error
    @errorhandler.user_does_not_exist
    def post(self):
        request_body_dict = request.json

        username, password = request_body_dict['username'], request_body_dict['password']

        if self.user_controller.is_username_password_valid(username, password):

            tokens_json = json.dumps(self.get_tokens_dict(username))

            self.response_creator.create_response(tokens_json)
            return self.response_creator.response_obj
        return self.response_creator.unauthorized()


class RefreshToken(Resource):
    decorators = [flask_jwt_extended.jwt_refresh_token_required]

    def __init__(self):
        self.response_creator = ResponseCreator()

    def get(self):
        response_creator = ResponseCreator()
        current_user = flask_jwt_extended.get_jwt_identity()
        ret = {
            'accessToken': flask_jwt_extended.create_access_token(identity=current_user)
        }
        return response_creator.create_response(json.dumps(ret))
