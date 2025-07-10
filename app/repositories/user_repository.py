from app.models.user import User
from app import db

class UserRepository:
    @staticmethod
    def create_user(username=None, login_id=None, login_id_type=None, password=None):
        user = User(username=username, login_id=login_id, login_id_type=login_id_type)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_login_id(login_id):
        return User.query.filter_by(login_id=login_id).first()
    
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)
