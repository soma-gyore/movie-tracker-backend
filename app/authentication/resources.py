from flask import json, request
from flask_restful import Resource
from app.shared.response import ResponseCreator
from app.authentication.controller import UserController


class Authentication(Resource):
    def __init__(self):
        self.user_controller = UserController()
        self.response_creator = ResponseCreator()

    def get(self, user_id):
        user_dict = self.user_controller.get_user_by_id(user_id)
        user_json = json.dumps(user_dict)
        self.response_creator.create_response(user_json)
        return self.response_creator.response_obj


class Login(Resource):
    def __init__(self):
        self.user_controller = UserController()
        self.response_creator = ResponseCreator()

    def post(self):
        request_body_dict = request.json

        username, password = request_body_dict['username'], request_body_dict['password']

        if self.user_controller.is_username_password_valid(username, password):
            return True
