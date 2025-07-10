from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    login_id = db.Column(db.String(120), unique=True, nullable=False)  # email or mobile
    login_id_type = db.Column(db.String(10), nullable=False)  # 'email' or 'mobile'
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    token = db.Column(db.String(256), unique=True, nullable=True)
    clubs = db.relationship('Club', secondary='user_club', back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username or self.login_id}>'

    def __str__(self):
        return self.username or self.login_id
