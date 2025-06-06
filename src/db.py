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

# Check if we're in testing mode
is_testing = os.environ.get('FLASK_ENV') == 'testing'

# If we're testing, use mock DB immediately
if is_testing:
    logger.info("Test environment detected, using mock Firebase")
    from unittest.mock import MagicMock
    # Mock Firebase
    if not firebase_admin._apps:
        firebase_admin._apps = {'[DEFAULT]': MagicMock()}
    db = MagicMock()
else:
    # Try to initialize the database for real environments
    try:
        # Check for environment variable with highest priority
        if 'FIREBASE_CREDENTIALS_BASE64' in os.environ:
            logger.info("Found FIREBASE_CREDENTIALS_BASE64 environment variable")
            encoded = os.environ.get('FIREBASE_CREDENTIALS_BASE64')
            decoded = base64.b64decode(encoded).decode('utf-8')
            cred_dict = json.loads(decoded)
            cred = credentials.Certificate(cred_dict)
            logger.info("Successfully loaded Firebase credentials from base64")
        # Use local file if available
        elif os.environ.get('FIRESTORE_SERVICE_ACCOUNT'):
            path = os.environ.get('FIRESTORE_SERVICE_ACCOUNT')
            logger.info(f"Using Firebase credentials file: {path}")
            if os.path.exists(path):
                cred = credentials.Certificate(path)
            else:
                logger.error(f"Firebase credentials file not found: {path}")
                raise FileNotFoundError(f"Firebase credentials file not found: {path}")
        # No credentials found
        else:
            logger.error("No Firebase credentials found in environment variables")
            raise ValueError("No Firebase credentials found")
        
        # Initialize Firebase
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        logger.info("Firebase initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        # Only allow fallback to mock in development
        if os.environ.get('FLASK_ENV') == 'development' or os.environ.get('DEBUG') == 'True':
            from unittest.mock import MagicMock
            # Create a mock DB for development
            if not firebase_admin._apps:
                firebase_admin._apps = {'[DEFAULT]': MagicMock()}
            db = MagicMock()
            logger.warning("Using mock database due to initialization failure")
        else:
            # In production, re-raise the  error
            raise