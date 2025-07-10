from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.club_repository import ClubRepository
from app.models.club import Club
from app import db

club_bp = Blueprint('club', __name__, url_prefix='/clubs')

@club_bp.route('/', methods=['POST'])
@jwt_required()
def create_club():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    else:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        club = ClubRepository.create(name=name, description=description, user_id=user_id)
    return jsonify({'id': club.id, 'name': club.name, 'description': club.description}), 201

@club_bp.route('/', methods=['GET'])
@jwt_required()
def list_clubs():
    clubs = ClubRepository.get_all()
    return jsonify([{'id': c.id, 'name': c.name, 'description': c.description} for c in clubs])

@club_bp.route('/<int:club_id>', methods=['GET'])
@jwt_required()
def get_club(club_id):
    club = ClubRepository.get_by_id(club_id)
    if not club:
        return jsonify({'error': 'Club not found'}), 404
    return jsonify({'id': club.id, 'name': club.name, 'description': club.description})

@club_bp.route('/<int:club_id>', methods=['PUT'])
@jwt_required()
def update_club(club_id):
    club = ClubRepository.get_by_id(club_id)
    if not club:
        return jsonify({'error': 'Club not found'}), 404
    data = request.get_json()
    club = ClubRepository.update(club, name=data.get('name'), description=data.get('description'))
    return jsonify({'id': club.id, 'name': club.name, 'description': club.description})

@club_bp.route('/<int:club_id>', methods=['DELETE'])
@jwt_required()
def delete_club(club_id):
    club = ClubRepository.get_by_id(club_id)
    if not club:
        return jsonify({'error': 'Club not found'}), 404
    ClubRepository.delete(club)
    return jsonify({'message': 'Club deleted'})
