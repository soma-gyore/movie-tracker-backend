from flask import json
from app.shared.response import ResponseCreator


class TestResponse(object):
    @classmethod
    def setup_class(cls):
        cls.response_creator = ResponseCreator()

    def create_message_json_list(self, message_dict):
        message_json = json.dumps(message_dict)
        self.response_creator.create_response(message_json)

        message_json_list = list()
        message_json_list.append(bytes(message_json, 'utf-8'))

        return message_json_list

    def test_create_response(self):
        message_dict = {
            "message": "Test message",
            "asd": "dsa"
        }

        message_json_list = self.create_message_json_list(message_dict)

        assert self.response_creator.response_obj.response == message_json_list
        assert self.response_creator.response_obj.status_code == 200
        assert self.response_creator.response_obj.mimetype == 'application/json'

    def test_ok(self):

        message_dict = {
            "message": "OK"
        }

        response_obj = self.response_creator.ok()

        assert response_obj.response == self.create_message_json_list(message_dict)
        assert response_obj.status_code == 200
        assert response_obj.mimetype == 'application/json'

    def test_created(self):

        message_dict = {
            "message": "Created"
        }

        response_obj = self.response_creator.created()

        assert response_obj.response == self.create_message_json_list(message_dict)
        assert response_obj.status_code == 201
        assert response_obj.mimetype == 'application/json'

    def test_unauthorized(self):
        message_dict = {
            "message": "Unauthorized"
        }

        response_obj = self.response_creator.unauthorized()

        assert response_obj.response == self.create_message_json_list(message_dict)
        assert response_obj.status_code == 401
        assert response_obj.mimetype == 'application/json'

    def test_internal_server_error(self):
        message_dict = {
            "message": "Internal server error"
        }

        response_obj = self.response_creator.internal_server_error()

        assert response_obj.response == self.create_message_json_list(message_dict)
        assert response_obj.status_code == 500
        assert response_obj.mimetype == 'application/json'

    def test_user_already_exist(self):
        message_dict = {
            "message": "User already exist"
        }

        response_obj = self.response_creator.user_already_exist()

        assert response_obj.response == self.create_message_json_list(message_dict)
        assert response_obj.status_code == 409
        assert response_obj.mimetype == 'application/json'
