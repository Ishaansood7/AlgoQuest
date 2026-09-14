from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from models.attempt_model import AttemptModel
from services.quest_service import QuestService, STAGE_ORDER
from services.recommendation_service import RecommendationService

quest_bp = Blueprint("quests", __name__)

@quest_bp.route("/worlds", methods=["GET"])
def get_worlds():
    """Lists all available learning worlds."""
    worlds = QuestService.load_worlds()
    return jsonify({
        "status": "success",
        "total_worlds": len(worlds),
        "worlds": worlds
    }), 200

@quest_bp.route("/worlds/<world_id>", methods=["GET"])
def get_world(world_id):
    """Retrieves detailed information and quest list for a specific world."""
    world = QuestService.get_world(world_id)
    if not world:
        return jsonify({
            "status": "error",
            "message": f"World '{world_id}' not found."
        }), 404

    return jsonify({
        "status": "success",
        "world": world
    }), 200

@quest_bp.route("/quests/<quest_id>", methods=["GET"])
def get_quest(quest_id):
    """Retrieves quest metadata and stage prompts (sanitized for client display)."""
    quest = QuestService.get_quest(quest_id, sanitize=True)
    if not quest:
        return jsonify({
            "status": "error",
            "message": f"Quest '{quest_id}' not found."
        }), 404

    return jsonify({
        "status": "success",
        "quest": quest
    }), 200

@quest_bp.route("/quests/<quest_id>/attempt", methods=["POST"])
def start_attempt(quest_id):
    """Initializes a new attempt for a quest."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Invalid request body. JSON object expected."
        }), 400

    user_id = data.get("user_id")
    if not user_id or not str(user_id).strip():
        return jsonify({
            "status": "error",
            "message": "Field 'user_id' is required."
        }), 400

    user = UserModel.get_by_id(str(user_id).strip())
    if not user:
        return jsonify({
            "status": "error",
            "message": f"User '{user_id}' not found."
        }), 404

    raw_quest = QuestService.get_quest(quest_id, sanitize=False)
    if not raw_quest:
        return jsonify({
            "status": "error",
            "message": f"Quest '{quest_id}' not found."
        }), 404

    attempt = AttemptModel.create(user["user_id"], quest_id)
    return jsonify({
        "status": "success",
        "message": "Quest attempt initialized successfully",
        "attempt": attempt
    }), 201

@quest_bp.route("/quests/<quest_id>/hint", methods=["POST"])
def get_hint(quest_id):
    """Returns progressive hint for the current stage with score deduction notice."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Invalid request body. JSON object expected."
        }), 400

    user_id = data.get("user_id")
    attempt_id = data.get("attempt_id")
    stage_id = data.get("stage_id")

    if not user_id or not attempt_id or not stage_id:
        return jsonify({
            "status": "error",
            "message": "Fields 'user_id', 'attempt_id', and 'stage_id' are required."
        }), 400

    user = UserModel.get_by_id(str(user_id).strip())
    if not user:
        return jsonify({"status": "error", "message": f"User '{user_id}' not found."}), 404

    raw_quest = QuestService.get_quest(quest_id, sanitize=False)
    if not raw_quest:
        return jsonify({"status": "error", "message": f"Quest '{quest_id}' not found."}), 404

    attempt = AttemptModel.get_by_id(str(attempt_id).strip())
    if not attempt:
        return jsonify({"status": "error", "message": f"Attempt '{attempt_id}' not found."}), 404

    if attempt["user_id"] != user["user_id"]:
        return jsonify({"status": "error", "message": "Attempt belongs to another user."}), 403

    if attempt["status"] == "completed":
        return jsonify({"status": "error", "message": "Attempt has already been completed."}), 400

    if stage_id in attempt.get("completed_stages", []):
        return jsonify({"status": "error", "message": f"Stage '{stage_id}' is already completed."}), 400

    if stage_id != attempt["current_stage"]:
        return jsonify({
            "status": "error",
            "message": f"Cannot request hint for '{stage_id}'. Current active stage is '{attempt['current_stage']}'."
        }), 400

    hints_used = attempt.get("hints_used", {}).get(stage_id, 0)
    hint_text, has_more = QuestService.get_stage_hint(raw_quest, stage_id, hints_used)
    
    # Increment hints used counter
    new_hint_count = AttemptModel.record_hint(attempt["attempt_id"], stage_id)

    return jsonify({
        "status": "success",
        "quest_id": quest_id,
        "stage_id": stage_id,
        "hint": hint_text,
        "hints_used_for_stage": new_hint_count,
        "has_more_hints": has_more,
        "hint_penalty_notice": "Each hint used deducts 2 points from this stage's score (min 20% floor)."
    }), 200

@quest_bp.route("/quests/<quest_id>/submit", methods=["POST"])
def submit_stage(quest_id):
    """Submits and evaluates answers for a single stage in order."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Invalid request body. JSON object expected."
        }), 400

    user_id = data.get("user_id")
    attempt_id = data.get("attempt_id")
    stage_id = data.get("stage_id")
    answer = data.get("answer")

    if not user_id or not attempt_id or not stage_id or answer is None:
        return jsonify({
            "status": "error",
            "message": "Fields 'user_id', 'attempt_id', 'stage_id', and 'answer' are required."
        }), 400

    user = UserModel.get_by_id(str(user_id).strip())
    if not user:
        return jsonify({"status": "error", "message": f"User '{user_id}' not found."}), 404

    raw_quest = QuestService.get_quest(quest_id, sanitize=False)
    if not raw_quest:
        return jsonify({"status": "error", "message": f"Quest '{quest_id}' not found."}), 404

    attempt = AttemptModel.get_by_id(str(attempt_id).strip())
    if not attempt:
        return jsonify({"status": "error", "message": f"Attempt '{attempt_id}' not found."}), 404

    if attempt["user_id"] != user["user_id"]:
        return jsonify({"status": "error", "message": "Attempt belongs to another user."}), 403

    if attempt["status"] == "completed":
        return jsonify({"status": "error", "message": "Attempt has already been completed."}), 400

    if stage_id in attempt.get("completed_stages", []):
        return jsonify({
            "status": "error",
            "message": f"Stage '{stage_id}' has already been completed."
        }), 400

    if stage_id != attempt["current_stage"]:
        return jsonify({
            "status": "error",
            "message": f"Invalid stage sequence. Expected '{attempt['current_stage']}', received '{stage_id}'."
        }), 400

    hints_used = attempt.get("hints_used", {}).get(stage_id, 0)
    evaluation = QuestService.evaluate_stage(raw_quest, stage_id, answer, hints_used)
    if not evaluation:
        return jsonify({"status": "error", "message": f"Invalid stage '{stage_id}' for quest."}), 400

    # Advance stage
    next_stage = evaluation["next_stage"]
    updated_attempt = AttemptModel.update_stage_progress(
        attempt_id=attempt["attempt_id"],
        stage_id=stage_id,
        answer=answer,
        score=evaluation["score"],
        next_stage=next_stage
    )

    # Check if this completed the entire quest (all 7 stages done)
    if next_stage == "completed":
        # Calculate totals
        stage_scores = updated_attempt.get("stage_scores", {})
        total_score = sum(stage_scores.values())
        percentage = round((total_score / 100.0) * 100, 1)

        # Scale XP reward by performance percentage (up to quest max XP)
        max_xp = raw_quest.get("xp_reward", 100)
        xp_earned = max(10, round(max_xp * (percentage / 100.0)))

        final_attempt = AttemptModel.mark_completed(
            attempt_id=attempt["attempt_id"],
            total_score=total_score,
            percentage=percentage,
            xp_earned=xp_earned
        )

        # Build skill updates dictionary
        skill_updates = {}
        for s in raw_quest.get("stages", []):
            sid = s["stage_id"]
            dim = s.get("skill_dimension")
            max_p = s.get("max_points", 10)
            earned_p = stage_scores.get(sid, 0)
            stage_pct = round((earned_p / max_p) * 100)
            skill_updates[dim] = stage_pct

        # Update user profile with earned XP and mastery
        updated_user = UserModel.award_xp_and_skills(
            user_id=user["user_id"],
            xp_gain=xp_earned,
            skill_updates=skill_updates
        )

        # Recommend next quest
        recommendation = RecommendationService.recommend_first_quest(updated_user["skills"])

        return jsonify({
            "status": "success",
            "message": "Quest completed successfully! Mastery updated.",
            "stage_feedback": evaluation,
            "quest_completed": True,
            "attempt_summary": {
                "attempt_id": final_attempt["attempt_id"],
                "status": "completed",
                "total_score": total_score,
                "percentage": percentage,
                "xp_earned": xp_earned,
                "completed_stages": final_attempt["completed_stages"],
                "stage_scores": final_attempt["stage_scores"]
            },
            "user_progress": {
                "xp": updated_user["xp"],
                "level": updated_user["level"],
                "skills": updated_user["skills"]
            },
            "recommendation": recommendation
        }), 200

    return jsonify({
        "status": "success",
        "stage_feedback": evaluation,
        "quest_completed": False,
        "attempt_progress": {
            "attempt_id": updated_attempt["attempt_id"],
            "current_stage": next_stage,
            "completed_stages": updated_attempt["completed_stages"],
            "stage_scores": updated_attempt["stage_scores"]
        }
    }), 200
