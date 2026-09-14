from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from models.battle_model import BattleModel
from services.quest_service import QuestService
from services.battle_service import BattleService

battle_bp = Blueprint("battles", __name__)

@battle_bp.route("/battles", methods=["POST"])
def create_battle():
    """Creates a new 1v1 Battle challenge."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request body. JSON object expected."}), 400

    user_id = data.get("user_id")
    quest_id = data.get("quest_id")
    opponent_id = data.get("opponent_id")

    if not user_id or not quest_id:
        return jsonify({"status": "error", "message": "Fields 'user_id' and 'quest_id' are required."}), 400

    creator = UserModel.get_by_id(str(user_id).strip())
    if not creator:
        return jsonify({"status": "error", "message": f"User '{user_id}' not found."}), 404

    raw_quest = QuestService.get_quest(str(quest_id).strip(), sanitize=False)
    if not raw_quest:
        return jsonify({"status": "error", "message": f"Quest '{quest_id}' not found."}), 404

    opponent = None
    if opponent_id:
        opp_id = str(opponent_id).strip().lower()
        if opp_id == "algo_bot":
            opponent = {"user_id": "algo_bot", "name": "AlgoBot [AI Rival]"}
        else:
            opp_user = UserModel.get_by_id(opp_id)
            if not opp_user:
                return jsonify({"status": "error", "message": f"Opponent user '{opponent_id}' not found."}), 404
            if opp_user["user_id"] == creator["user_id"]:
                return jsonify({"status": "error", "message": "Cannot challenge yourself to a battle."}), 400
            opponent = opp_user

    battle = BattleModel.create(creator=creator, quest_id=str(quest_id).strip(), opponent=opponent)
    return jsonify({
        "status": "success",
        "message": "Battle challenge created successfully",
        "battle": battle
    }), 201

@battle_bp.route("/battles/<battle_id>", methods=["GET"])
def get_battle(battle_id):
    """Retrieves battle details and participants."""
    battle = BattleModel.get_by_id(str(battle_id).strip())
    if not battle:
        return jsonify({"status": "error", "message": f"Battle '{battle_id}' not found."}), 404

    return jsonify({
        "status": "success",
        "battle": battle
    }), 200

@battle_bp.route("/battles/<battle_id>/join", methods=["POST"])
def join_battle(battle_id):
    """Joins an open/waiting battle as Player 2."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request body. JSON object expected."}), 400

    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"status": "error", "message": "Field 'user_id' is required."}), 400

    battle = BattleModel.get_by_id(str(battle_id).strip())
    if not battle:
        return jsonify({"status": "error", "message": f"Battle '{battle_id}' not found."}), 404

    if battle["status"] != "waiting":
        return jsonify({"status": "error", "message": f"Battle is not open for joining (Status: {battle['status']})."}), 400

    if battle.get("player1", {}).get("user_id") == str(user_id).strip():
        return jsonify({"status": "error", "message": "Cannot join your own battle."}), 400

    user = UserModel.get_by_id(str(user_id).strip())
    if not user:
        return jsonify({"status": "error", "message": f"User '{user_id}' not found."}), 404

    updated_battle = BattleModel.join(battle["battle_id"], user)
    return jsonify({
        "status": "success",
        "message": f"Joined battle '{battle_id}' successfully",
        "battle": updated_battle
    }), 200

@battle_bp.route("/battles/<battle_id>/submit", methods=["POST"])
def submit_battle(battle_id):
    """Submits duel reasoning answers and calculates speed and accuracy."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request body. JSON object expected."}), 400

    user_id = data.get("user_id")
    answers = data.get("answers")
    time_taken = data.get("time_taken_seconds", 30)

    if not user_id or answers is None:
        return jsonify({"status": "error", "message": "Fields 'user_id' and 'answers' are required."}), 400

    battle = BattleModel.get_by_id(str(battle_id).strip())
    if not battle:
        return jsonify({"status": "error", "message": f"Battle '{battle_id}' not found."}), 404

    if battle["status"] == "waiting":
        return jsonify({"status": "error", "message": "Cannot submit yet. Awaiting an opponent to join."}), 400

    if battle["status"] == "completed":
        return jsonify({"status": "error", "message": "Battle has already been completed."}), 400

    uid = str(user_id).strip()
    p1 = battle.get("player1", {})
    p2 = battle.get("player2", {})

    is_p1 = p1.get("user_id") == uid
    is_p2 = p2 and p2.get("user_id") == uid

    if not (is_p1 or is_p2):
        return jsonify({"status": "error", "message": "User is not a participant in this battle."}), 403

    # Check for duplicate submission
    if (is_p1 and p1.get("submitted")) or (is_p2 and p2.get("submitted")):
        return jsonify({"status": "error", "message": "User has already submitted for this battle."}), 400

    # Calculate score
    raw_quest = QuestService.get_quest(battle["quest_id"], sanitize=False)
    performance = BattleService.calculate_player_score(
        quest=raw_quest,
        answers=answers,
        time_taken_seconds=time_taken
    )

    # Record player submission
    updated_battle = BattleModel.record_submission(
        battle_id=battle["battle_id"],
        user_id=uid,
        answers=answers,
        score=performance["total_score"],
        time_taken_seconds=time_taken
    )

    # Resolve winner if both players have submitted
    final_battle = BattleService.resolve_battle_if_ready(battle["battle_id"])

    return jsonify({
        "status": "success",
        "message": "Battle answers submitted successfully",
        "performance": performance,
        "battle_completed": final_battle["status"] == "completed",
        "battle": final_battle
    }), 200

@battle_bp.route("/users/<user_id>/battle-history", methods=["GET"])
def get_battle_history(user_id):
    """Retrieves full duel match history for a user."""
    user = UserModel.get_by_id(str(user_id).strip())
    if not user:
        return jsonify({"status": "error", "message": f"User '{user_id}' not found."}), 404

    battles = BattleModel.get_user_battles(user["user_id"])
    victories = len([b for b in battles if b.get("winner_id") == user["user_id"]])

    return jsonify({
        "status": "success",
        "user_id": user["user_id"],
        "total_battles": len(battles),
        "victories": victories,
        "battles": battles
    }), 200
