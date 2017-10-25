class UserController(object):
    def __init__(self):
        self.user_object = None
        self.user_dict = {}

    def user_object_to_dict(self):
        self.user_dict = {
            "id": self.user_object.id,
            "username": self.user_object.username,
            "password": self.user_object.password
        }

    def get_user_by_id(self, user_id):
        from .model import User
        self.user_object = User.query.filter_by(id=user_id).first()
        self.user_object_to_dict()
        return self.user_dict

    def get_user_by_username(self, username):
        from .model import User
        self.user_object = User.query.filter_by(username=username).first()
        return self.user_object

    def is_username_password_valid(self, username, password):
        fetched_user_obj = self.get_user_by_username(username)
        if fetched_user_obj.password == password:
            return True
        return False

    @staticmethod
    def create_user(user_dict):
        from .model import User
        from application import db
        new_user_obj = User(user_dict['username'], user_dict['password'])
        db.session.add(new_user_obj)
        db.session.commit()
