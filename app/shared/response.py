from flask import Response


class ResponseCreator(object):
    def __init__(self):
        self.response_obj = None

    def create_response(self, message, status_code=200, mimetype='application/json'):
        self.response_obj = Response(response=message, status=status_code, mimetype=mimetype)

    def ok(self):
        self.create_response("OK")
        return self.response_obj
