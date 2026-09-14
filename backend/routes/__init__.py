from flask import Blueprint
from routes.health_routes import health_bp
from routes.user_routes import user_bp
from routes.trial_routes import trial_bp
from routes.quest_routes import quest_bp
from routes.ai_routes import ai_bp
from routes.battle_routes import battle_bp

def register_routes(app):
    """Register all API Blueprints under the /api prefix."""
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(trial_bp, url_prefix="/api")
    app.register_blueprint(quest_bp, url_prefix="/api")
    app.register_blueprint(ai_bp, url_prefix="/api")
    app.register_blueprint(battle_bp, url_prefix="/api")
