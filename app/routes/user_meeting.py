from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_cors import CORS
from app.repositories.user_meeting_repository import UserMeetingRepository
from app.models.user_meeting import UserMeeting
from app import db

user_meeting_bp = Blueprint('user_meeting', __name__, url_prefix='/user_meetings')

@user_meeting_bp.route('/', methods=['POST'])
@jwt_required()
def create_user_meeting():
    data = request.get_json()
    user_id = data.get('user_id')
    meeting_id = data.get('meeting_id')
    meeting_date = data.get('meeting_date')
    meeting_key = data.get('meeting_key')

    if not user_id or not meeting_id:
        return jsonify({'error': 'user_id and meeting_id are required'}), 400
    user_meeting = UserMeetingRepository.create(user_id=user_id, meeting_id=meeting_id, meeting_date=meeting_date, meeting_key=meeting_key)
    return jsonify({'id': user_meeting.id, 'user_id': user_meeting.user_id, 'meeting_id': user_meeting.meeting_id, 'meeting_key': user_meeting.meeting_key}), 201

@user_meeting_bp.route('/', methods=['GET'])
@jwt_required()
def list_user_meetings():
    user_id = request.args.get('user_id')
    user_meetings = UserMeetingRepository.get_all()
    if user_id:
        user_meetings = [um for um in user_meetings if str(um.user_id) == str(user_id)]
    return jsonify([
        {'id': um.id, 'user_id': um.user_id, 'meeting_id': um.meeting_id, 'meeting_key': um.meeting_key, 'guest': getattr(um, 'guests', 0)}
        for um in user_meetings
    ])

@user_meeting_bp.route('/<int:user_meeting_id>', methods=['GET'])
@jwt_required()
def get_user_meeting(user_meeting_id):
    user_meeting = UserMeetingRepository.get_by_id(user_meeting_id)
    if not user_meeting:
        return jsonify({'error': 'UserMeeting not found'}), 404
    return jsonify({'id': user_meeting.id, 'user_id': user_meeting.user_id, 'meeting_id': user_meeting.meeting_id, 'joined_at': str(user_meeting.joined_at)})

@user_meeting_bp.route('/<int:user_meeting_id>', methods=['PUT'])
@jwt_required()
def update_user_meeting(user_meeting_id):
    data = request.get_json()
    guest = data.get('guest')
    guest = 0 if guest is None else guest
    user_meeting = UserMeetingRepository.get_by_id(user_meeting_id)
    if not user_meeting:
        return jsonify({'error': 'UserMeeting not found'}), 404
    user_meeting = UserMeetingRepository.update(user_meeting, guest, user_id=data.get('user_id'), meeting_id=data.get('meeting_id'))
    return jsonify({'id': user_meeting.id, 'user_id': user_meeting.user_id, 'meeting_id': user_meeting.meeting_id, 'joined_at': str(user_meeting.joined_at)})

@user_meeting_bp.route('/<int:user_meeting_id>', methods=['DELETE'])
@jwt_required()
def delete_user_meeting(user_meeting_id):
    user_meeting = UserMeetingRepository.get_by_id(user_meeting_id)
    if not user_meeting:
        return jsonify({'error': 'UserMeeting not found'}), 404
    UserMeetingRepository.delete(user_meeting)
    return jsonify({'message': 'UserMeeting deleted'})
    # user_meeting = UserMeetingRepository.get_by_meeting_key(meeting_key)
    # if not user_meeting:
    #     return jsonify({'error': 'UserMeeting not found'}), 404
    # UserMeetingRepository.delete(user_meeting)
    # return jsonify({'message': 'UserMeeting deleted'})

@user_meeting_bp.route('/count', methods=['GET'])
@jwt_required()
def get_meeting_join_count():
    meeting_date = request.args.get('meeting_date')
    if not meeting_date:
        return jsonify({'error': 'meeting_date is required'}), 400
    player_joined = UserMeetingRepository.get_number_of_joined_people(meeting_date)
    return jsonify({'meeting_date': meeting_date, 'player_joined': player_joined})
    
    