import firebase_admin
from firebase_admin import credentials, firestore
from src.config import DB_KEY, FIREBASE_CONFIG

# Initialize Firebase with the appropriate credentials
if FIREBASE_CONFIG:
    # Using the parsed JSON config (from base64 on Heroku)
    cred = credentials.Certificate(FIREBASE_CONFIG)
else:
    # Using the file path (local development)
    cred = credentials.Certificate(DB_KEY)

firebase_admin.initialize_app(cred)
db = firestore.client()