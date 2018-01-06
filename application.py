from flask_recaptcha import ReCaptcha

import config

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.videos.resources import Videos
from app.authentication.resources import Login, Register, RefreshToken, LogoutAccess, LogoutRefresh, Account, ApiKey

flask_app = Flask(__name__)
bcrypt = Bcrypt(flask_app)
config.configure_app(flask_app)
db = SQLAlchemy(flask_app)
jwt = JWTManager(flask_app)
CORS(flask_app)
recaptcha = ReCaptcha(app=flask_app)

api = Api(flask_app, catch_all_404s=True)

api.add_resource(Videos, '/videos')
api.add_resource(Login, '/login')
api.add_resource(Account, '/account')
api.add_resource(LogoutAccess, '/logout-access')
api.add_resource(LogoutRefresh, '/logout-refresh')
api.add_resource(RefreshToken, '/refresh-token')
api.add_resource(Register, '/register')
api.add_resource(ApiKey, '/api-key')


blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


import app.authentication.model
import app.videos.model
