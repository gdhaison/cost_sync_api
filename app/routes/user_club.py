from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.repositories.user_club_repository import UserClubRepository
from app.models.user_club import UserClub
from app import db

user_club_bp = Blueprint('user_club', __name__, url_prefix='/user_clubs')

@user_club_bp.route('/', methods=['POST'])
@jwt_required()
def create_user_club():
    data = request.get_json()
    user_id = data.get('user_id')
    club_id = data.get('club_id')
    if not user_id or not club_id:
        return jsonify({'error': 'user_id and club_id are required'}), 400
    user_club = UserClubRepository.create(user_id=user_id, club_id=club_id)
    return jsonify({'id': user_club.id, 'user_id': user_club.user_id, 'club_id': user_club.club_id}), 201

@user_club_bp.route('/', methods=['GET'])
@jwt_required()
def list_user_clubs():
    user_clubs = UserClubRepository.get_all()
    return jsonify([
        {'id': uc.id, 'user_id': uc.user_id, 'club_id': uc.club_id, 'joined_at': str(uc.joined_at)}
        for uc in user_clubs
    ])

@user_club_bp.route('/<int:user_club_id>', methods=['GET'])
@jwt_required()
def get_user_club(user_club_id):
    user_club = UserClubRepository.get_by_id(user_club_id)
    if not user_club:
        return jsonify({'error': 'UserClub not found'}), 404
    return jsonify({'id': user_club.id, 'user_id': user_club.user_id, 'club_id': user_club.club_id, 'joined_at': str(user_club.joined_at)})

@user_club_bp.route('/<int:user_club_id>', methods=['PUT'])
@jwt_required()
def update_user_club(user_club_id):
    user_club = UserClubRepository.get_by_id(user_club_id)
    if not user_club:
        return jsonify({'error': 'UserClub not found'}), 404
    data = request.get_json()
    user_club = UserClubRepository.update(user_club, user_id=data.get('user_id'), club_id=data.get('club_id'))
    return jsonify({'id': user_club.id, 'user_id': user_club.user_id, 'club_id': user_club.club_id, 'joined_at': str(user_club.joined_at)})

@user_club_bp.route('/<int:user_club_id>', methods=['DELETE'])
@jwt_required()
def delete_user_club(user_club_id):
    user_club = UserClubRepository.get_by_id(user_club_id)
    if not user_club:
        return jsonify({'error': 'UserClub not found'}), 404
    UserClubRepository.delete(user_club)
    return jsonify({'message': 'UserClub deleted'})
