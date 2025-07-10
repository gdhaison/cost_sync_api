from app.models.user_club import UserClub
from app import db

class UserClubRepository:
    @staticmethod
    def create(user_id, club_id):
        user_club = UserClub(user_id=user_id, club_id=club_id)
        db.session.add(user_club)
        db.session.commit()
        return user_club

    @staticmethod
    def get_all():
        return UserClub.query.all()

    @staticmethod
    def get_by_id(user_club_id):
        return UserClub.query.get(user_club_id)

    @staticmethod
    def update(user_club, user_id=None, club_id=None):
        if user_id is not None:
            user_club.user_id = user_id
        if club_id is not None:
            user_club.club_id = club_id
        db.session.commit()
        return user_club

    @staticmethod
    def delete(user_club):
        db.session.delete(user_club)
        db.session.commit()
