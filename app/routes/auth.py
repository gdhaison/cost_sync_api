from flask import Blueprint, request, jsonify, session
from app.repositories.user_repository import UserRepository
from app import db
from app.models.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    login_id = data.get('login_id')
    login_id_type = data.get('login_id_type')  # 'email' or 'mobile'
    password = data.get('password')
    if not login_id or not login_id_type or not password:
        return jsonify({'error': 'login_id, login_id_type, and password required'}), 400
    if UserRepository.get_by_login_id(login_id):
        return jsonify({'error': 'login_id already exists'}), 409
    user = UserRepository.create_user(username=username, login_id=login_id, login_id_type=login_id_type, password=password)
    return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login_id = data.get('login_id')
    password = data.get('password')
    user = UserRepository.get_by_login_id(login_id)
    if user and user.check_password(password):
        session['user_id'] = user.id
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login successful', 'access_token': access_token})
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'})

@auth_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200
