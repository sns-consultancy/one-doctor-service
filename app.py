import os
import sys
import logging
from src.api.health import health_bp
from flask import Flask, jsonify
from flask_cors import CORS

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
        CORS(app)
        app.register_blueprint(health_bp)
        
        @app.errorhandler(500)
        def handle_500(e):
            logger.error(f"Internal server error: {str(e)}")
            return jsonify(error=str(e)), 500
            
        logger.info("Flask application created successfully")
        return app
    except Exception as e:
        logger.critical(f"Failed to create Flask application: {str(e)}")
        raise

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)