from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os
import logging
import sys

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/cost_sync_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'superjwtsecret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour in seconds


    # ---------- CẤU HÌNH LOG ----------
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("app_logger")

    # ---------- LOG MỌI REQUEST ----------
    @app.before_request
    def start_timer():
        request._start_time = logging.Formatter.formatTime(logging.Formatter(), None)

    @app.after_request
    def log_request(response):
        logger.info(f"{request.remote_addr} - {request.method} {request.path} - {response.status_code}")
        return response

    # ---------- LOG LỖI RIÊNG ----------
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception(f"🔥 Exception occurred: {e}")
        return {"error": "Internal Server Error"}, 500

    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)


    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from .routes.club import club_bp
    app.register_blueprint(club_bp)
    from .routes.meeting import meeting_bp
    app.register_blueprint(meeting_bp)
    from .routes.user_club import user_club_bp
    app.register_blueprint(user_club_bp)
    from .routes.user_meeting import user_meeting_bp
    app.register_blueprint(user_meeting_bp)

    from . import models

    return app
