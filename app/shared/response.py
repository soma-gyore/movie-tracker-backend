from flask import Response, json


class ResponseCreator(object):
    def __init__(self):
        self.response_obj = None

    def create_response(self, message, status_code=200, mimetype='application/json'):
        self.response_obj = Response(response=message, status=status_code, mimetype=mimetype)
        return self.response_obj

    def ok(self):
        ok_message_json = json.dumps({"message": "OK"})
        self.create_response(ok_message_json)
        return self.response_obj

    def created(self):
        created_message_json = json.dumps({"message": "Created"})
        self.create_response(created_message_json, 201)
        return self.response_obj

    def unauthorized(self):
        unauthorized_message_json = json.dumps({"message": "Unauthorized"})
        self.create_response(unauthorized_message_json, 401)
        return self.response_obj

    def invalid_api_key(self):
        unauthorized_message_json = json.dumps({"message": "Invalid API key"})
        self.create_response(unauthorized_message_json, 401)
        return self.response_obj

    def internal_server_error(self):
        internal_server_error_message_json = json.dumps({"message": "Internal server error"})
        self.create_response(internal_server_error_message_json, 500)
        return self.response_obj

    def user_already_exists(self):
        user_already_exist_message_json = json.dumps({"message": "User already exists"})
        self.create_response(user_already_exist_message_json, 409)
        return self.response_obj

    def user_does_not_exist(self):
        user_does_not_exist_message_json = json.dumps({"message": "User does not exist"})
        self.create_response(user_does_not_exist_message_json, 404)
        return self.response_obj

    def api_key_does_not_exist(self):
        api_key_does_not_exist_message_json = json.dumps({"message": "Api key does not exist"})
        self.create_response(api_key_does_not_exist_message_json, 404)
        return self.response_obj
