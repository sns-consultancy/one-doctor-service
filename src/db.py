import firebase_admin
from firebase_admin import credentials, firestore
from src.config import DB_KEY

cred = credentials.Certificate(DB_KEY)
firebase_admin.initialize_app(cred)
db = firestore.client()