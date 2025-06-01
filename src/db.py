import os
import sys
import json
import base64
import logging
import firebase_admin
from firebase_admin import credentials, firestore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Try to initialize the database
try:
    # Check for environment variable with highest priority
    if 'FIREBASE_CREDENTIALS_BASE64' in os.environ:
        logger.info("Found FIREBASE_CREDENTIALS_BASE64 environment variable")
        encoded = os.environ.get('FIREBASE_CREDENTIALS_BASE64')
        try:
            decoded = base64.b64decode(encoded).decode('utf-8')
            cred_dict = json.loads(decoded)
            cred = credentials.Certificate(cred_dict)
            logger.info("Successfully loaded Firebase credentials from base64")
        except Exception as e:
            logger.error(f"Failed to decode Firebase credentials: {str(e)}")
            logger.error(f"Base64 length: {len(encoded)}")
            # Do not crash in development/testing
            if os.environ.get('FLASK_ENV') in ['development', 'testing']:
                from unittest.mock import MagicMock
                firebase_admin._apps = {'[DEFAULT]': MagicMock()}
                db = MagicMock()
                logger.warning("Using mock database for development")
            else:
                raise
    # Use local file if available
    elif os.environ.get('FIRESTORE_SERVICE_ACCOUNT'):
        path = os.environ.get('FIRESTORE_SERVICE_ACCOUNT')
        logger.info(f"Using Firebase credentials file: {path}")
        if os.path.exists(path):
            cred = credentials.Certificate(path)
        else:
            logger.error(f"Firebase credentials file not found: {path}")
            if os.environ.get('FLASK_ENV') in ['development', 'testing']:
                from unittest.mock import MagicMock
                firebase_admin._apps = {'[DEFAULT]': MagicMock()}
                db = MagicMock()
                logger.warning("Using mock database for development")
            else:
                raise FileNotFoundError(f"Firebase credentials file not found: {path}")
    # No credentials found
    else:
        logger.error("No Firebase credentials found in environment variables")
        if os.environ.get('FLASK_ENV') in ['development', 'testing']:
            from unittest.mock import MagicMock
            firebase_admin._apps = {'[DEFAULT]': MagicMock()}
            db = MagicMock()
            logger.warning("Using mock database for development")
        else:
            raise ValueError("No Firebase credentials found")
    
    # Initialize Firebase if not already mocked
    if not hasattr(locals(), 'db'):
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        logger.info("Firebase initialized successfully")

except Exception as e:
    logger.error(f"Failed to initialize Firebase: {str(e)}")
    # Handle development vs production differently
    if os.environ.get('FLASK_ENV') in ['development', 'testing'] or os.environ.get('DEBUG') == 'True':
        from unittest.mock import MagicMock
        # Create a mock DB for development
        db = MagicMock()
        logger.warning("Using mock database due to initialization failure")
    else:
        # In production, re-raise the error
        raise