from app.models.user import User
from app import db

class UserRepository:
    @staticmethod
    def create_user(username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()
