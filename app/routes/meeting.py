from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.repositories.meeting_repository import MeetingRepository
from app.models.meeting import Meeting
from app import db
import logging as log

meeting_bp = Blueprint('meeting', __name__, url_prefix='/meetings')

@meeting_bp.route('/', methods=['POST'])
@jwt_required()
def create_meeting():
    data = request.get_json()
    club_id = data.get('club_id')
    title = data.get('title')
    description = data.get('description')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    recurrence = data.get('recurrence')
    days_of_week = data.get('days_of_week')
    day_of_month = data.get('day_of_month')
    if not club_id or not title or not start_time:
        return jsonify({'error': 'club_id, title, and start_time are required'}), 400
    try:
        meeting = MeetingRepository.create(
            club_id=club_id,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            recurrence=recurrence,
            days_of_week=days_of_week,
            day_of_month=day_of_month
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({
        'id': meeting.id,
        'club_id': meeting.club_id,
        'title': meeting.title,
        'description': meeting.description,
        'start_time': meeting.start_time.isoformat() if meeting.start_time else None,
        'end_time': meeting.end_time.isoformat() if meeting.end_time else None,
        'recurrence': meeting.recurrence,
        'days_of_week': meeting.days_of_week,
        'day_of_month': meeting.day_of_month
    }), 201

@meeting_bp.route('/', methods=['GET'])
@jwt_required()
def list_meetings():
    meetings = MeetingRepository.get_all()
    return jsonify([
        {'id': m.id, 'club_id': m.club_id, 'title': m.title, 'description': m.description, 'start_time': str(m.start_time), 'end_time': str(m.end_time), 'recurrence': m.recurrence}
        for m in meetings
    ])

@meeting_bp.route('/<int:meeting_id>', methods=['GET'])
@jwt_required()
def get_meeting(meeting_id):
    meeting = MeetingRepository.get_by_id(meeting_id)
    if not meeting:
        return jsonify({'error': 'Meeting not found'}), 404
    return jsonify({'id': meeting.id, 'club_id': meeting.club_id, 'title': meeting.title, 'description': meeting.description, 'start_time': str(meeting.start_time), 'end_time': str(meeting.end_time), 'recurrence': meeting.recurrence})

@meeting_bp.route('/<int:meeting_id>', methods=['PUT'])
@jwt_required()
def update_meeting(meeting_id):
    meeting = MeetingRepository.get_by_id(meeting_id)
    if not meeting:
        return jsonify({'error': 'Meeting not found'}), 404
    data = request.get_json()
    meeting = MeetingRepository.update(
        meeting,
        title=data.get('title'),
        description=data.get('description'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        recurrence=data.get('recurrence', meeting.recurrence)
    )
    return jsonify({'id': meeting.id, 'club_id': meeting.club_id, 'title': meeting.title, 'description': meeting.description, 'start_time': str(meeting.start_time), 'end_time': str(meeting.end_time), 'recurrence': meeting.recurrence})

@meeting_bp.route('/<int:meeting_id>', methods=['DELETE'])
@jwt_required()
def delete_meeting(meeting_id):
    meeting = MeetingRepository.get_by_id(meeting_id)
    if not meeting:
        return jsonify({'error': 'Meeting not found'}), 404
    MeetingRepository.delete(meeting)
    return jsonify({'message': 'Meeting deleted'})
