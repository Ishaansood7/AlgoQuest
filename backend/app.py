import logging
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from db import Database
from routes import register_routes

# Configure clean logging format
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
)
logger = logging.getLogger("algoquest")

def create_app():
    """Application factory for AlgoQuest backend."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for all routes (crucial for frontend development and hackathon testing)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize Database connection
    with app.app_context():
        Database.initialize()

    # Register API routes
    register_routes(app)

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "status": "error",
            "code": 404,
            "message": "Resource or endpoint not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            "status": "error",
            "code": 500,
            "message": "Internal server error"
        }), 500

    return app

if __name__ == "__main__":
    app = create_app()
    logger.info(f"Starting AlgoQuest backend on port {Config.PORT} (Debug={Config.DEBUG})...")
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
