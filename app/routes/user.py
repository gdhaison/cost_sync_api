from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.user_repository import UserRepository
from app.helper.datetime import serialize_datetime

user_bp = Blueprint('user', __name__)
@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = UserRepository.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    club = [club.id for club in getattr(user, 'clubs', [])]
    return jsonify({
        'id': user.id,
        'username': user.username,
        'login_id': user.login_id,
        'login_id_type': user.login_id_type
    }), 200

@user_bp.route('/my-clubs', methods=['GET'])
@jwt_required()
def get_user_clubs():
    user_id = get_jwt_identity()
    user = UserRepository.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # Assuming user.clubs is a relationship/list of Club objects
    clubs = getattr(user, 'clubs', [])
    club_list = [
        {
            'id': club.id,
            'name': club.name,
            'description': getattr(club, 'description', ''),
            'created_at': getattr(club, 'created_at', None)
        }
        for club in clubs
    ]
    return jsonify({'clubs': club_list}), 200

@user_bp.route('/my-clubs-meetings', methods=['GET'])
@jwt_required()
def get_user_clubs_meetings():
    user_id = get_jwt_identity()
    user = UserRepository.get_by_id(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    clubs = getattr(user, 'clubs', [])
    club_list = []

    for club in clubs:
        meetings = getattr(club, 'meetings', [])
        meeting_list = [
            {
                'id': meeting.id,
                'title': getattr(meeting, 'title', ''),
                'description': getattr(meeting, 'description', ''),
                'start_time': serialize_datetime(getattr(meeting, 'start_time', None)),
                'end_time': serialize_datetime(getattr(meeting, 'end_time', None)),
                'recurrence': getattr(meeting, 'recurrence', None),
                'days_of_week': getattr(meeting, 'days_of_week', None),
                'day_of_month': getattr(meeting, 'day_of_month', None),
                'created_at': serialize_datetime(getattr(meeting, 'created_at', None))
            }
            for meeting in meetings
        ]

        club_list.append({
            'id': club.id,
            'name': club.name,
            'description': getattr(club, 'description', ''),
            'created_at': serialize_datetime(getattr(club, 'created_at', None)),
            'meetings': meeting_list
        })

    return jsonify({'clubs': club_list}), 200
