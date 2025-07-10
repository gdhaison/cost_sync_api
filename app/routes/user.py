from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.user_repository import UserRepository

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