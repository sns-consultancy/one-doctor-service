import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('HEALTH_API_KEY')
DB_KEY = os.environ.get('FIRESTORE_SERVICE_ACCOUNT')