import os
import json
import logging
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)

app = Flask(__name__)
CORS(app)
# Load environment variables from .env file
load_dotenv()

# API Key for security
API_KEY = os.environ.get('HEALTH_API_KEY')
DB_KEY = os.environ.get('FIRESTORE_SERVICE_ACCOUNT')

# Firebase Initialization
cred = credentials.Certificate(DB_KEY)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Authentication decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('x-api-key')
        if key != API_KEY:
            logging.warning("Unauthorized access attempt.")
            return jsonify({'status': 'unauthorized', 'message': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function
    
@app.route('/api/health', methods=['POST'])
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
        # Save to Firestore
        db.collection('health_data').document(user_id).set(health_data)
        return jsonify({'status': 'success', 'message': 'Data stored successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/health/<user_id>', methods=['GET'])
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
if __name__ == '__main__':
    app.run(debug=True)