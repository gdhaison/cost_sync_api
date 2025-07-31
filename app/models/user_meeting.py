from .. import db

class UserMeeting(db.Model):
    __tablename__ = 'user_meeting'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    joined_at = db.Column(db.DateTime, server_default=db.func.now())
    meeting_date = db.Column(db.DateTime, nullable=False)
    guests = db.Column(db.Integer, default=0)
    meeting_key= db.Column(db.String(50), nullable=True) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    __table_args__ = (db.UniqueConstraint('user_id', 'meeting_id', name='_user_meeting_uc'),)
