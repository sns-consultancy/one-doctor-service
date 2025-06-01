from flask import Blueprint, request, jsonify
from src.db import db
from src.auth import require_api_key
import logging

health_bp = Blueprint('health', __name__)

@health_bp.route('/api/health', methods=['POST'])
@require_api_key
def receive_health_data():
    data = request.json
    try:
        user_id = data['user_id']
        health_data = {
            'heartbeat': data.get('heartbeat', 0),
            'temperature': data.get('temperature', 0.0),
            'blood_pressure': data.get('blood_pressure', '0/0'),
            'oxygen_level': data.get('oxygen_level', 0.0),
            'last_updated': data.get('last_updated', '')
        }
        db.collection('health_data').document(user_id).set(health_data)
        return jsonify({'status': 'success', 'message': 'Data stored successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@health_bp.route('/api/health/<user_id>', methods=['GET'])
@require_api_key
def get_health_data(user_id):
    try:
        doc_ref = db.collection('health_data').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            logging.info(f"Health data retrieved for user: {user_id}")
            return jsonify({'status': 'success', 'data': doc.to_dict()}), 200
        else:
            logging.warning(f"No health data found for user: {user_id}")
            return jsonify({'status': 'error', 'message': 'User data not found'}), 404
    except Exception as e:
        logging.exception("Failed to retrieve health data")
        return jsonify({'status': 'error', 'message': str(e)}), 500