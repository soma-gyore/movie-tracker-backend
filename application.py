import config

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from app.videos.resources import Videos
from app.authentication.resources import Authentication, Login

flask_app = Flask(__name__)
bcrypt = Bcrypt(flask_app)
config.configure_app(flask_app)
db = SQLAlchemy(flask_app)

api = Api(flask_app, catch_all_404s=True)
api.add_resource(Videos, '/videos')
# api.add_resource(Authentication, '/login/<int:user_id>')
api.add_resource(Login, '/login')

import app.authentication.model
import app.videos.model
