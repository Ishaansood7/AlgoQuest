from flask import Blueprint, request, jsonify
from config import Config
from models.user_model import UserModel
from services.quest_service import QuestService, STAGE_ORDER
from services.ai_service import AIService

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/ai/hint", methods=["POST"])
def get_ai_hint():
    """Provides contextual, Socratic pedagogical hints with progressive tiers."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Invalid request body. JSON object expected."
        }), 400

    quest_id = data.get("quest_id")
    stage_id = data.get("stage_id")
    if not quest_id or not stage_id:
        return jsonify({
            "status": "error",
            "message": "Fields 'quest_id' and 'stage_id' are required."
        }), 400

    # Input length safety check
    user_answer = data.get("user_answer")
    if user_answer and len(str(user_answer)) > Config.AI_MAX_INPUT_CHARS:
        return jsonify({
            "status": "error",
            "message": f"Input exceeds maximum allowed length of {Config.AI_MAX_INPUT_CHARS} characters."
        }), 400

    # Validate quest exists
    raw_quest = QuestService.get_quest(str(quest_id).strip(), sanitize=False)
    if not raw_quest:
        return jsonify({
            "status": "error",
            "message": f"Quest '{quest_id}' not found."
        }), 404

    # Validate stage
    if stage_id not in STAGE_ORDER:
        return jsonify({
            "status": "error",
            "message": f"Invalid stage_id '{stage_id}'. Must be one of: {STAGE_ORDER}."
        }), 400

    # Validate user if provided
    user_id = data.get("user_id")
    user_lang = "python"
    if user_id:
        user = UserModel.get_by_id(str(user_id).strip())
        if not user:
            return jsonify({
                "status": "error",
                "message": f"User '{user_id}' not found."
            }), 404
        user_lang = user.get("preferred_language", "python")

    hints_used = int(data.get("hints_used", 0))

    hint_result = AIService.generate_hint(
        quest_id=str(quest_id).strip(),
        stage_id=str(stage_id).strip(),
        user_answer=user_answer,
        hints_used=hints_used,
        user_lang=user_lang
    )

    return jsonify({
        "status": "success",
        **hint_result
    }), 200

@ai_bp.route("/ai/explain", methods=["POST"])
def get_ai_explanation():
    """Explains an algorithmic concept or why a particular attempt was incorrect."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Invalid request body. JSON object expected."
        }), 400

    quest_id = data.get("quest_id")
    stage_id = data.get("stage_id")
    if not quest_id or not stage_id:
        return jsonify({
            "status": "error",
            "message": "Fields 'quest_id' and 'stage_id' are required."
        }), 400

    # Input length safety check
    user_answer = data.get("user_answer")
    question_context = data.get("question_context")
    if user_answer and len(str(user_answer)) > Config.AI_MAX_INPUT_CHARS:
        return jsonify({
            "status": "error",
            "message": f"Input exceeds maximum allowed length of {Config.AI_MAX_INPUT_CHARS} characters."
        }), 400
    if question_context and len(str(question_context)) > Config.AI_MAX_INPUT_CHARS:
        return jsonify({
            "status": "error",
            "message": f"Question context exceeds maximum allowed length of {Config.AI_MAX_INPUT_CHARS} characters."
        }), 400

    raw_quest = QuestService.get_quest(str(quest_id).strip(), sanitize=False)
    if not raw_quest:
        return jsonify({
            "status": "error",
            "message": f"Quest '{quest_id}' not found."
        }), 404

    if stage_id not in STAGE_ORDER:
        return jsonify({
            "status": "error",
            "message": f"Invalid stage_id '{stage_id}'. Must be one of: {STAGE_ORDER}."
        }), 400

    user_id = data.get("user_id")
    user_lang = "python"
    if user_id:
        user = UserModel.get_by_id(str(user_id).strip())
        if not user:
            return jsonify({
                "status": "error",
                "message": f"User '{user_id}' not found."
            }), 404
        user_lang = user.get("preferred_language", "python")

    explanation_result = AIService.generate_explanation(
        quest_id=str(quest_id).strip(),
        stage_id=str(stage_id).strip(),
        user_answer=user_answer,
        question_context=question_context,
        user_lang=user_lang
    )

    return jsonify({
        "status": "success",
        **explanation_result
    }), 200
