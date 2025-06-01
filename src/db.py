import os
import json
import base64
import logging
import firebase_admin
from firebase_admin import credentials, firestore

# Set up better logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting Firebase initialization...")
logger.info(f"Environment variables: {list(os.environ.keys())}")

try:
    # Check for Firebase credentials
    if 'FIREBASE_CREDENTIALS_BASE64' in os.environ:
        logger.info("Using base64 encoded credentials")
        try:
            encoded = os.environ.get('FIREBASE_CREDENTIALS_BASE64')
            logger.info(f"Base64 string length: {len(encoded)}")
            
            # Decode
            decoded = base64.b64decode(encoded).decode('utf-8')
            logger.info(f"Decoded JSON length: {len(decoded)}")
            
            # Parse
            service_account_info = json.loads(decoded)
            logger.info(f"Parsed JSON keys: {list(service_account_info.keys())}")
            
            # Initialize
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            logger.info("Firebase initialized successfully!")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise
    else:
        logger.warning("No FIREBASE_CREDENTIALS_BASE64 found!")
        service_account_path = os.environ.get('FIRESTORE_SERVICE_ACCOUNT')
        logger.info(f"Using file path: {service_account_path}")
        
        if service_account_path and os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            logger.info("Firebase initialized with file!")
        else:
            logger.error(f"Service account file not found at {service_account_path}")
            raise ValueError("No valid Firebase credentials found")

except Exception as e:
    logger.error(f"Firebase error: {str(e)}")
    
    # Provide mock DB for development
    if os.environ.get('FLASK_ENV') in ['development', 'testing']:
        from unittest.mock import MagicMock
        logger.warning("Using mock Firebase for development/testing!")
        db = MagicMock()
    else:
        raise