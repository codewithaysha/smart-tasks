from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo, login_manager

class User(UserMixin):
    def __init__(self, user_data):
        self._id = user_data.get('_id')
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.password = user_data.get('password')
        self.theme = user_data.get('theme', 'light')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return str(self._id)
    
    @staticmethod
    def get_by_id(user_id):
        from bson.objectid import ObjectId
        user_doc = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        return User(user_doc) if user_doc else None
    
    @staticmethod
    def get_by_email(email):
        user_doc = mongo.db.users.find_one({'email': email})
        return User(user_doc) if user_doc else None

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)
