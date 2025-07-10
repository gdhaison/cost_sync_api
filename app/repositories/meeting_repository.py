from app.models.meeting import Meeting
from app import db

class MeetingRepository:
    @staticmethod
    def create(club_id, title, description, start_time, end_time, recurrence):
        meeting = Meeting(club_id=club_id, title=title, description=description, start_time=start_time, end_time=end_time, recurrence=recurrence)
        db.session.add(meeting)
        db.session.commit()
        return meeting

    @staticmethod
    def get_all():
        return Meeting.query.all()

    @staticmethod
    def get_by_id(meeting_id):
        return Meeting.query.get(meeting_id)

    @staticmethod
    def update(meeting, title=None, description=None, start_time=None, end_time=None, recurrence=None):
        if title is not None:
            meeting.title = title
        if description is not None:
            meeting.description = description
        if start_time is not None:
            meeting.start_time = start_time
        if end_time is not None:
            meeting.end_time = end_time
        if recurrence is not None:
            meeting.recurrence = recurrence
        db.session.commit()
        return meeting

    @staticmethod
    def delete(meeting):
        db.session.delete(meeting)
        db.session.commit()
