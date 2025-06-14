from src.api.health import health_bp
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(health_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)