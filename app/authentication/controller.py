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

    def get_user_by_username(self, username):
        from .model import User
        self.user_object = User.query.filter_by(username=username).first()
        return self.user_object

    def get_api_key_by_username(self, username):
        from .model import User
        self.user_object = User.query.filter_by(username=username).first()
        return self.user_object.api_key

    def is_username_password_valid(self, username, password):
        from application import bcrypt
        fetched_user_obj = self.get_user_by_username(username)

        return bcrypt.check_password_hash(fetched_user_obj.password, password)

    @staticmethod
    def get_number_of_users():
        from .model import User
        return User.query.count()

    @staticmethod
    def delete_every_user():
        from application import db
        from .model import User
        User.query.delete()
        db.session.commit()

    @staticmethod
    def is_api_key_valid(api_key):
        from .model import User
        from application import db
        exists = db.session.query(User.id).filter_by(api_key=api_key).scalar() is not None
        return exists

    @staticmethod
    def get_user_name_by_api_key(api_key):
        from .model import User
        user_object = User.query.filter_by(api_key=api_key).first()
        return user_object.username

    @staticmethod
    def get_user_by_api_key(api_key):
        from .model import User
        user_object = User.query.filter_by(api_key=api_key).first()
        return user_object

    @staticmethod
    def create_user(user_dict):
        from .model import User
        from application import db
        from application import bcrypt

        username, password = user_dict['username'], user_dict['password']
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user_obj = User(username, password_hash)
        db.session.add(new_user_obj)
        db.session.commit()

    @staticmethod
    def delete_user(username):
        from .model import User
        from application import db
        User.query.filter_by(username=username).delete()
        db.session.commit()
