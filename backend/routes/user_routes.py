from flask import Blueprint, request, jsonify
from models.user_model import UserModel

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["POST"])
def create_user():
    """Creates a new user profile."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Invalid request body. JSON object expected."
        }), 400

    name = data.get("name")
    if not name or not str(name).strip():
        return jsonify({
            "status": "error",
            "message": "Field 'name' is required."
        }), 400

    # Optional fields with validation
    valid_languages = ["python", "javascript", "java", "cpp", "c"]
    lang = str(data.get("preferred_language", "python")).strip().lower()
    if lang not in valid_languages:
        lang = "python"

    valid_levels = ["beginner", "intermediate", "advanced"]
    level = str(data.get("experience_level", "beginner")).strip().lower()
    if level not in valid_levels:
        level = "beginner"

    user_payload = {
        "user_id": data.get("user_id"),
        "name": str(name).strip(),
        "preferred_language": lang,
        "experience_level": level,
        "learning_goal": str(data.get("learning_goal", "placement")).strip()
    }

    user = UserModel.create(user_payload)
    return jsonify({
        "status": "success",
        "message": "User created successfully",
        "user": user
    }), 201

@user_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Retrieves user by ID."""
    user = UserModel.get_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": f"User '{user_id}' not found."
        }), 404

    return jsonify({
        "status": "success",
        "user": user
    }), 200

@user_bp.route("/users/<user_id>/profile", methods=["GET"])
def get_user_profile(user_id):
    """Retrieves rich user profile including skills and thinking profile."""
    user = UserModel.get_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": f"User '{user_id}' not found."
        }), 404

    trials = UserModel.get_user_trials(user_id)

    profile = {
        "user_id": user["user_id"],
        "name": user["name"],
        "preferred_language": user["preferred_language"],
        "experience_level": user["experience_level"],
        "learning_goal": user["learning_goal"],
        "xp": user["xp"],
        "level": user["level"],
        "learning_streak": user["learning_streak"],
        "skills": user["skills"],
        "thinking_profile": user.get("thinking_profile"),
        "trial_attempts_count": len(trials),
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }

    return jsonify({
        "status": "success",
        "profile": profile
    }), 200

@user_bp.route("/users/<user_id>/progress", methods=["GET"])
def get_user_progress(user_id):
    """Retrieves aggregated user progress across quests, attempts, and trial history."""
    from models.attempt_model import AttemptModel

    user = UserModel.get_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": f"User '{user_id}' not found."
        }), 404

    attempts = AttemptModel.get_by_user_id(user_id)
    trials = UserModel.get_user_trials(user_id)
    completed_quests = [a for a in attempts if a.get("status") == "completed"]

    progress_data = {
        "user_id": user["user_id"],
        "name": user["name"],
        "xp": user["xp"],
        "level": user["level"],
        "learning_streak": user["learning_streak"],
        "skills": user["skills"],
        "thinking_profile": user.get("thinking_profile"),
        "total_quests_completed": len(completed_quests),
        "total_attempts": len(attempts),
        "quest_attempts": attempts,
        "trial_attempts_count": len(trials)
    }

    return jsonify({
        "status": "success",
        "progress": progress_data
    }), 200

@user_bp.route("/users/<user_id>/attempts", methods=["GET"])
def get_user_attempts(user_id):
    """Retrieves all quest attempts made by the user."""
    from models.attempt_model import AttemptModel

    user = UserModel.get_by_id(user_id)
    if not user:
        return jsonify({
            "status": "error",
            "message": f"User '{user_id}' not found."
        }), 404

    attempts = AttemptModel.get_by_user_id(user_id)
    return jsonify({
        "status": "success",
        "user_id": user_id,
        "total_attempts": len(attempts),
        "attempts": attempts
    }), 200
