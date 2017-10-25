import random
import string

from application import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(72), nullable=False)
    api_key = db.Column(db.String(32), unique=True, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.api_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

