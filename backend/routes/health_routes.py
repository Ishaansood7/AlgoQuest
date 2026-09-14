from datetime import datetime, timezone
from flask import Blueprint, jsonify
from db import Database

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():
    """Returns application and database connectivity status."""
    db_status = Database.get_status()
    
    response = {
        "status": "success",
        "message": "AlgoQuest backend is running",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": {
            "configured": db_status["configured"],
            "connected": db_status["connected"],
            "name": db_status["database_name"],
            "status": "connected" if db_status["connected"] else "offline"
        }
    }
    
    if not db_status["connected"] and db_status["error"]:
        response["database"]["detail"] = db_status["error"]
        
    return jsonify(response), 200
