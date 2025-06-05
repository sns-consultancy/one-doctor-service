import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables from .env file 
load_dotenv(verbose=True)
from src.api.health import health_bp
from src.api.authentication import authentication_bp
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def create_app():
    logger.info("Creating Flask application")
    try:
        app = Flask(__name__)
        
        # Configure JWT
        app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
        jwt = JWTManager(app)
        
        # Enable CORS
        CORS(app)
        
        # Register blueprints
        app.register_blueprint(health_bp, url_prefix='/api')
        
        # IMPORTANT CHANGE: Remove the /auth prefix from blueprint registration
        # since it's already included in your route definitions
        app.register_blueprint(authentication_bp, url_prefix='')
        
        @app.errorhandler(500)
        def handle_500(e):
            logger.error(f"Internal server error: {str(e)}")
            return jsonify({'error': str(e)}), 500
            
        @app.route('/')
        def index():
            return jsonify({"status": "success", "message": "One Doctor Service API"})
            
        logger.info("Flask application created successfully")
        return app
    except Exception as e:
        logger.critical(f"Failed to create Flask application: {str(e)}")
        raise

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)