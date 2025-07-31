from app.models.meeting import Meeting
from app import db
import datetime
import logging as log

class MeetingRepository:
    @staticmethod
    def create(club_id, title, description, start_time, end_time, recurrence=None, days_of_week=None, day_of_month=None):
        # Validation for recurrence fields
        log.info(f"Creating meeting with data: {days_of_week}")
        if recurrence == 'weekly' and not days_of_week:
            raise ValueError('For weekly recurrence, days_of_week must not be empty.')
        if recurrence == 'monthly' and not day_of_month:
            raise ValueError('For monthly recurrence, day_of_month must not be empty.')
        # Convert start_time and end_time to time objects if they are strings
        if isinstance(start_time, str):
            start_time = datetime.time.fromisoformat(start_time)
        if isinstance(end_time, str):
            end_time = datetime.time.fromisoformat(end_time)
        meeting = Meeting(
            club_id=club_id,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            recurrence=recurrence,
            days_of_week=days_of_week,
            day_of_month=day_of_month
        )
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
    def get_by_club_id(club_id):
        return Meeting.query.filter_by(club_id=club_id).all()

    @staticmethod
    def update(meeting, title=None, description=None, start_time=None, end_time=None, recurrence=None, days_of_week=None, day_of_month=None):
        # Validation for recurrence fields
        if recurrence == 'weekly' and not days_of_week:
            raise ValueError('For weekly recurrence, days_of_week must not be empty.')
        if recurrence == 'monthly' and not day_of_month:
            raise ValueError('For monthly recurrence, day_of_month must not be empty.')
        # Convert start_time and end_time to time objects if they are strings
        if start_time is not None:
            if isinstance(start_time, str):
                start_time = datetime.time.fromisoformat(start_time)
            meeting.start_time = start_time
        if end_time is not None:
            if isinstance(end_time, str):
                end_time = datetime.time.fromisoformat(end_time)
            meeting.end_time = end_time
        if title is not None:
            meeting.title = title
        if description is not None:
            meeting.description = description
        if recurrence is not None:
            meeting.recurrence = recurrence
        if days_of_week is not None:
            meeting.days_of_week = days_of_week
        if day_of_month is not None:
            meeting.day_of_month = day_of_month
        db.session.commit()
        return meeting

    @staticmethod
    def delete(meeting):
        db.session.delete(meeting)
        db.session.commit()
