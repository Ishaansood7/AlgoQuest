from models.user_model import UserModel
from models.battle_model import BattleModel
from services.quest_service import QuestService

WINNER_XP = 50
RUNNER_UP_XP = 15
DRAW_XP = 30

class BattleService:
    """Business logic for 1v1 Battles, scoring, speed calculations, and resolution."""

    @classmethod
    def calculate_player_score(cls, quest, answers, time_taken_seconds=0):
        """
        Calculates battle performance based on accuracy and speed:
        - Accuracy Score: up to 100 points
        - Speed Bonus: up to 20 bonus points (max(0, 20 - seconds // 10))
        """
        stages = quest.get("stages", [])
        if not stages:
            # Simple fallback scoring
            accuracy = 100 if answers else 0
        else:
            total_possible = sum(s.get("max_points", 10) for s in stages)
            earned = 0
            for s in stages:
                sid = s["stage_id"]
                exp = s.get("expected_answer")
                submitted = answers.get(sid)
                if submitted is not None:
                    try:
                        if int(submitted) == int(exp):
                            earned += s.get("max_points", 10)
                    except (ValueError, TypeError):
                        if str(submitted).strip().lower() == str(exp).strip().lower():
                            earned += s.get("max_points", 10)
            accuracy = round((earned / total_possible) * 100) if total_possible > 0 else 0

        # Speed bonus: faster submissions earn up to 20 bonus points
        try:
            sec = int(time_taken_seconds)
        except (ValueError, TypeError):
            sec = 30
        speed_bonus = max(0, min(20, 20 - (sec // 10)))

        return {
            "accuracy": accuracy,
            "speed_bonus": speed_bonus,
            "total_score": accuracy + speed_bonus
        }

    @classmethod
    def resolve_battle_if_ready(cls, battle_id):
        """
        Checks if both players have submitted, resolves winner, and distributes XP.
        """
        battle = BattleModel.get_by_id(battle_id)
        if not battle or battle["status"] == "completed":
            return battle

        p1 = battle.get("player1", {})
        p2 = battle.get("player2", {})

        if not (p1.get("submitted") and p2 and p2.get("submitted")):
            return battle

        p1_score = p1.get("score", 0)
        p2_score = p2.get("score", 0)
        p1_time = p1.get("time_taken_seconds", 999)
        p2_time = p2.get("time_taken_seconds", 999)

        # Winner resolution logic
        if p1_score > p2_score:
            winner_id = p1["user_id"]
            p1_xp, p2_xp = WINNER_XP, RUNNER_UP_XP
            summary = f"{p1['name']} claimed victory ({p1_score} vs {p2_score})!"
        elif p2_score > p1_score:
            winner_id = p2["user_id"]
            p1_xp, p2_xp = RUNNER_UP_XP, WINNER_XP
            summary = f"{p2['name']} claimed victory ({p2_score} vs {p1_score})!"
        else:
            # Score tie -> check fastest completion time
            if p1_time < p2_time:
                winner_id = p1["user_id"]
                p1_xp, p2_xp = WINNER_XP, RUNNER_UP_XP
                summary = f"{p1['name']} broke the tie with a faster completion time ({p1_time}s vs {p2_time}s)!"
            elif p2_time < p1_time:
                winner_id = p2["user_id"]
                p1_xp, p2_xp = RUNNER_UP_XP, WINNER_XP
                summary = f"{p2['name']} broke the tie with a faster completion time ({p2_time}s vs {p1_time}s)!"
            else:
                winner_id = "draw"
                p1_xp, p2_xp = DRAW_XP, DRAW_XP
                summary = f"Honorable Draw! Both players tied with {p1_score} points in {p1_time}s."

        # Award Battle XP
        UserModel.award_xp_and_skills(p1["user_id"], xp_gain=p1_xp)
        if p2["user_id"] != "algo_bot":
            UserModel.award_xp_and_skills(p2["user_id"], xp_gain=p2_xp)

        finalized = BattleModel.finalize_battle(
            battle_id=battle_id,
            winner_id=winner_id,
            p1_xp=p1_xp,
            p2_xp=p2_xp,
            summary=summary
        )
        return finalized
