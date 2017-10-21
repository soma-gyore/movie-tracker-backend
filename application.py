import config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from app.videos.resources import Videos


flask_app = Flask(__name__)

config.configure_app(flask_app)
api = Api(flask_app)
api.add_resource(Videos, '/')
db = SQLAlchemy(flask_app)

from app.authentication.model import User
