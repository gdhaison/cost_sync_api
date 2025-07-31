from .. import db
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
import logging as log

class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    recurrence = db.Column(db.String(10), nullable=True)  # 'daily', 'weekly', 'monthly', or None
    days_of_week = db.Column(db.String(50), nullable=True)  # Comma-separated days
    day_of_month = db.Column(db.Integer, nullable=True)  # 1 - 31

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    club = db.relationship('Club', backref=db.backref('meetings', lazy=True))

    # Optional: enforce day_of_month must be between 1 and 31 if not null
    __table_args__ = (
        CheckConstraint('day_of_month >= 1 AND day_of_month <= 31', name='valid_day_of_month'),
    )