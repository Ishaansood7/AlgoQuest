from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from services.scoring_service import ScoringService
from services.recommendation_service import RecommendationService

trial_bp = Blueprint("trials", __name__)

@trial_bp.route("/trial", methods=["GET"])
def get_trial_questions():
    """Returns thinking trial questions with answers stripped for client safety."""
    questions = ScoringService.get_client_questions()
    return jsonify({
        "status": "success",
        "total_questions": len(questions),
        "questions": questions
    }), 200

@trial_bp.route("/trial/submit", methods=["POST"])
def submit_trial():
    """
    Submits answers for a thinking trial.
    Calculates deterministic skill scores, updates user mastery,
    and returns a personalized quest recommendation.
    """
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

    answers = data.get("answers")
    if answers is None or not isinstance(answers, dict):
        return jsonify({
            "status": "error",
            "message": "Field 'answers' must be a dictionary mapping question IDs to chosen option indices."
        }), 400

    # Verify user exists
    user = UserModel.get_by_id(str(user_id).strip())
    if not user:
        return jsonify({
            "status": "error",
            "message": f"User '{user_id}' not found."
        }), 404

    # Calculate deterministic scores
    evaluation = ScoringService.evaluate_trial(answers, user.get("skills"))

    # Generate personalized quest recommendation
    recommendation = RecommendationService.recommend_first_quest(evaluation["skill_scores"])

    now_iso = datetime.now(timezone.utc).isoformat()
    thinking_profile = {
        "overall_score": evaluation["overall_score"],
        "accuracy_percentage": evaluation["accuracy_percentage"],
        "correct_answers": evaluation["correct_answers"],
        "total_questions": evaluation["total_questions"],
        "strengths": evaluation["strengths"],
        "improvement_areas": evaluation["improvement_areas"],
        "skill_scores": evaluation["skill_scores"],
        "recommended_quest": recommendation,
        "completed_at": now_iso
    }

    # Persist updated skills & thinking profile
    UserModel.update_skills_and_profile(
        user_id=user["user_id"],
        new_skills=evaluation["skill_scores"],
        thinking_profile=thinking_profile
    )

    # Record trial attempt
    trial_record = {
        "user_id": user["user_id"],
        "answers": answers,
        "evaluation": evaluation,
        "recommendation": recommendation,
        "submitted_at": now_iso
    }
    UserModel.record_trial(trial_record)

    return jsonify({
        "status": "success",
        "message": "Thinking trial evaluated and profile updated successfully",
        "user_id": user["user_id"],
        "overall_score": evaluation["overall_score"],
        "accuracy_percentage": evaluation["accuracy_percentage"],
        "correct_answers": evaluation["correct_answers"],
        "total_questions": evaluation["total_questions"],
        "skill_scores": evaluation["skill_scores"],
        "strengths": evaluation["strengths"],
        "improvement_areas": evaluation["improvement_areas"],
        "recommendation": recommendation,
        "breakdown": evaluation["breakdown"]
    }), 200
