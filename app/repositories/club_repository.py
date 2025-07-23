from app.models.club import Club
from app import db

class ClubRepository:
    @staticmethod
    def create(name, user_id,description=None):
        club = Club(name=name, user_id=user_id, description=description)
        db.session.add(club)
        db.session.commit()
        return club

    @staticmethod
    def get_all():
        return Club.query.all()

    @staticmethod
    def get_by_id(club_id):
        return Club.query.get(club_id)

    @staticmethod
    def update(club, name=None, description=None):
        if name is not None:
            club.name = name
        if description is not None:
            club.description = description
        db.session.commit()
        return club

    @staticmethod
    def delete(club):
        db.session.delete(club)
        db.session.commit()
