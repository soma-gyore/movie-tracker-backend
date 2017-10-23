from flask import json
from app.shared.response import ResponseCreator


class TestResponse(object):
    @classmethod
    def setup_class(cls):
        cls.response_creator = ResponseCreator()

    def test_create_response(self):
        message_dict = {
            "message": "Test message",
            "asd": "dsa"
        }

        message_json = json.dumps(message_dict)
        self.response_creator.create_response(message_json)

        message_json_list = list()
        message_json_list.append(bytes(message_json, 'utf-8'))

        assert self.response_creator.response_obj.response == message_json_list
        assert self.response_creator.response_obj.status_code == 200
        assert self.response_creator.response_obj.mimetype == 'application/json'
