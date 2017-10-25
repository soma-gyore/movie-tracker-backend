from flask import Response, json


class ResponseCreator(object):
    def __init__(self):
        self.response_obj = None

    def create_response(self, message, status_code=200, mimetype='application/json'):
        self.response_obj = Response(response=message, status=status_code, mimetype=mimetype)

    def ok(self):
        ok_message_json = json.dumps({"message": "OK"})
        self.create_response(ok_message_json)
        return self.response_obj

    def unauthorized(self):
        unauthorized_message_json = json.dumps({"message": "Unauthorized"})
        self.create_response(unauthorized_message_json, 401)
