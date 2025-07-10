from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
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
    if not user_id or not meeting_id:
        return jsonify({'error': 'user_id and meeting_id are required'}), 400
    user_meeting = UserMeetingRepository.create(user_id=user_id, meeting_id=meeting_id)
    return jsonify({'id': user_meeting.id, 'user_id': user_meeting.user_id, 'meeting_id': user_meeting.meeting_id}), 201

@user_meeting_bp.route('/', methods=['GET'])
@jwt_required()
def list_user_meetings():
    user_meetings = UserMeetingRepository.get_all()
    return jsonify([
        {'id': um.id, 'user_id': um.user_id, 'meeting_id': um.meeting_id, 'joined_at': str(um.joined_at)}
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
    user_meeting = UserMeetingRepository.get_by_id(user_meeting_id)
    if not user_meeting:
        return jsonify({'error': 'UserMeeting not found'}), 404
    data = request.get_json()
    user_meeting = UserMeetingRepository.update(user_meeting, user_id=data.get('user_id'), meeting_id=data.get('meeting_id'))
    return jsonify({'id': user_meeting.id, 'user_id': user_meeting.user_id, 'meeting_id': user_meeting.meeting_id, 'joined_at': str(user_meeting.joined_at)})

@user_meeting_bp.route('/<int:user_meeting_id>', methods=['DELETE'])
@jwt_required()
def delete_user_meeting(user_meeting_id):
    user_meeting = UserMeetingRepository.get_by_id(user_meeting_id)
    if not user_meeting:
        return jsonify({'error': 'UserMeeting not found'}), 404
    UserMeetingRepository.delete(user_meeting)
    return jsonify({'message': 'UserMeeting deleted'})
