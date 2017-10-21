from flask_restful import Resource


class Videos(Resource):
    def get(self):
        return {"hello": "world"}
