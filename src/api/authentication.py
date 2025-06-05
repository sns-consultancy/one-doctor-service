import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from firebase_admin import firestore
from src.db import db

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint with a different name
authentication_bp = Blueprint('auth', __name__)  # Changed from auth_bp to authentication_bp

# Authentication routes
@authentication_bp.route('/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'status': 'error', 'message': 'Missing username or password'}), 400
        
        username = data['username']
        password = data['password']  # In production, hash this password
        
        # Check if user already exists
        user_ref = db.collection('users').document(username).get()
        if user_ref.exists:
            return jsonify({'status': 'error', 'message': 'User already exists'}), 400
        
        # Create new user
        user_data = {
            'username': username,
            'password': password,  # Store hashed password in production
            'created_at': firestore.SERVER_TIMESTAMP
        }
        db.collection('users').document(username).set(user_data)
        
        return jsonify({'status': 'success', 'message': 'User created successfully'}), 201
    
    except Exception as e:
        logger.error(f"Error in signup: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@authentication_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'status': 'error', 'message': 'Missing username or password'}), 400
        
        username = data['username']
        password = data['password']
        
        # Check if user exists
        user_ref = db.collection('users').document(username).get()
        if not user_ref.exists:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        
        # Verify password
        user_data = user_ref.to_dict()
        if user_data.get('password') != password:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        
        # Create access token
        access_token = create_access_token(identity=username)
        
        return jsonify({
            'status': 'success',
            'access_token': access_token,
            'username': username
        }), 200
    
    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@authentication_bp.route('/auth/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        current_user = get_jwt_identity()
        
        # Get user data
        user_ref = db.collection('users').document(current_user).get()
        if not user_ref.exists:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        user_data = user_ref.to_dict()
        # Remove sensitive information
        if 'password' in user_data:
            del user_data['password']
        
        return jsonify({
            'status': 'success',
            'data': user_data
        }), 200
    
    except Exception as e:
        logger.error(f"Error in profile: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500