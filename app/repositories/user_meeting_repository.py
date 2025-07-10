from app.models.user_meeting import UserMeeting
from app import db

class UserMeetingRepository:
    @staticmethod
    def create(user_id, meeting_id):
        user_meeting = UserMeeting(user_id=user_id, meeting_id=meeting_id)
        db.session.add(user_meeting)
        db.session.commit()
        return user_meeting

    @staticmethod
    def get_all():
        return UserMeeting.query.all()

    @staticmethod
    def get_by_id(user_meeting_id):
        return UserMeeting.query.get(user_meeting_id)

    @staticmethod
    def update(user_meeting, user_id=None, meeting_id=None):
        if user_id is not None:
            user_meeting.user_id = user_id
        if meeting_id is not None:
            user_meeting.meeting_id = meeting_id
        db.session.commit()
        return user_meeting

    @staticmethod
    def delete(user_meeting):
        db.session.delete(user_meeting)
        db.session.commit()
