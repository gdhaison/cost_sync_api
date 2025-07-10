from .. import db

class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # e.g., 'image/png', 'application/pdf'
    url = db.Column(db.String(512), nullable=False)       # Path or URL to the file
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now())
    # Polymorphic association: only one of these should be set per record
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=True)
