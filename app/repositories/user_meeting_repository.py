from app.models.user_meeting import UserMeeting
from app import db
from datetime import datetime, timezone

class UserMeetingRepository:
    @staticmethod
    def create(user_id, meeting_id, meeting_date=None, meeting_key=None):
        user_meeting = UserMeeting(user_id=user_id, meeting_id=meeting_id, meeting_date=meeting_date, meeting_key=meeting_key)
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
    def get_by_meeting_key(meeting_key):
        return UserMeeting.query.filter_by(meeting_key=meeting_key).first()
    
    @staticmethod
    def get_number_of_joined_people(meeting_date):

        import logging as log
        # t khổ vl =))
        user_meetings = UserMeeting.query.filter(UserMeeting.meeting_key.contains(meeting_date)).all()
        if not user_meetings:
            return 0
        return sum(um.guests for um in user_meetings)

    @staticmethod
    def update(user_meeting, guest, user_id=None, meeting_id=None):
        if guest is not None:
            user_meeting.guests = guest
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
