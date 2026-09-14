import uuid
import threading
from datetime import datetime, timezone
from db import get_db, Database

_LOCK = threading.Lock()
_IN_MEMORY_BATTLES = {}

class BattleModel:
    """Manages 1v1 Battle/Duel entities with dual-mode MongoDB / In-Memory support."""

    @staticmethod
    def _now_iso():
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def _is_mongo_active(cls):
        return Database.get_status().get("connected", False)

    @classmethod
    def create(cls, creator, quest_id, opponent=None):
        """Initializes a new battle challenge."""
        battle_id = f"battle_{uuid.uuid4().hex[:8]}"
        now = cls._now_iso()

        is_bot = bool(opponent and opponent.get("user_id") == "algo_bot")
        status = "in_progress" if (opponent or is_bot) else "waiting"

        player2_data = None
        if is_bot:
            player2_data = {
                "user_id": "algo_bot",
                "name": "AlgoBot [AI Rival]",
                "submitted": True, # bot submits dynamically
                "score": 85,
                "time_taken_seconds": 45,
                "answers": {}
            }
        elif opponent:
            player2_data = {
                "user_id": opponent["user_id"],
                "name": opponent["name"],
                "submitted": False,
                "score": 0,
                "time_taken_seconds": 0,
                "answers": {}
            }

        battle_doc = {
            "battle_id": battle_id,
            "quest_id": quest_id,
            "status": status,
            "created_at": now,
            "completed_at": None,
            "player1": {
                "user_id": creator["user_id"],
                "name": creator["name"],
                "submitted": False,
                "score": 0,
                "time_taken_seconds": 0,
                "answers": {}
            },
            "player2": player2_data,
            "winner_id": None,
            "xp_awarded": {},
            "summary": "Battle awaiting participants and submissions."
        }

        db = get_db()
        if cls._is_mongo_active() and db is not None:
            db.battles.insert_one(dict(battle_doc))
        else:
            with _LOCK:
                _IN_MEMORY_BATTLES[battle_id] = dict(battle_doc)

        return battle_doc

    @classmethod
    def get_by_id(cls, battle_id):
        """Fetches a battle by ID."""
        db = get_db()
        if cls._is_mongo_active() and db is not None:
            battle = db.battles.find_one({"battle_id": battle_id}, {"_id": 0})
            return battle
        else:
            with _LOCK:
                battle = _IN_MEMORY_BATTLES.get(battle_id)
                return dict(battle) if battle else None

    @classmethod
    def join(cls, battle_id, user):
        """Joins an open/waiting battle as Player 2."""
        battle = cls.get_by_id(battle_id)
        if not battle:
            return None

        player2_data = {
            "user_id": user["user_id"],
            "name": user["name"],
            "submitted": False,
            "score": 0,
            "time_taken_seconds": 0,
            "answers": {}
        }

        update_fields = {
            "player2": player2_data,
            "status": "in_progress",
            "summary": f"{user['name']} joined the duel! Both players may submit."
        }

        db = get_db()
        if cls._is_mongo_active() and db is not None:
            db.battles.update_one({"battle_id": battle_id}, {"$set": update_fields})
        else:
            with _LOCK:
                if battle_id in _IN_MEMORY_BATTLES:
                    _IN_MEMORY_BATTLES[battle_id].update(update_fields)

        return cls.get_by_id(battle_id)

    @classmethod
    def record_submission(cls, battle_id, user_id, answers, score, time_taken_seconds):
        """Records answers, score, and elapsed time for a player."""
        battle = cls.get_by_id(battle_id)
        if not battle:
            return None

        p1 = dict(battle.get("player1", {}))
        p2 = dict(battle.get("player2", {})) if battle.get("player2") else None

        update_fields = {}
        if p1.get("user_id") == user_id:
            p1["submitted"] = True
            p1["score"] = int(score)
            p1["time_taken_seconds"] = int(time_taken_seconds)
            p1["answers"] = answers
            update_fields["player1"] = p1
        elif p2 and p2.get("user_id") == user_id:
            p2["submitted"] = True
            p2["score"] = int(score)
            p2["time_taken_seconds"] = int(time_taken_seconds)
            p2["answers"] = answers
            update_fields["player2"] = p2
        else:
            return None

        db = get_db()
        if cls._is_mongo_active() and db is not None:
            db.battles.update_one({"battle_id": battle_id}, {"$set": update_fields})
        else:
            with _LOCK:
                if battle_id in _IN_MEMORY_BATTLES:
                    _IN_MEMORY_BATTLES[battle_id].update(update_fields)

        return cls.get_by_id(battle_id)

    @classmethod
    def finalize_battle(cls, battle_id, winner_id, p1_xp, p2_xp, summary):
        """Marks battle as completed with winner and awarded XP."""
        now = cls._now_iso()
        update_fields = {
            "status": "completed",
            "completed_at": now,
            "winner_id": winner_id,
            "xp_awarded": {
                "player1": int(p1_xp),
                "player2": int(p2_xp)
            },
            "summary": summary
        }

        db = get_db()
        if cls._is_mongo_active() and db is not None:
            db.battles.update_one({"battle_id": battle_id}, {"$set": update_fields})
        else:
            with _LOCK:
                if battle_id in _IN_MEMORY_BATTLES:
                    _IN_MEMORY_BATTLES[battle_id].update(update_fields)

        return cls.get_by_id(battle_id)

    @classmethod
    def get_user_battles(cls, user_id):
        """Retrieves match history for a user as Player 1 or Player 2."""
        db = get_db()
        if cls._is_mongo_active() and db is not None:
            battles = list(db.battles.find(
                {"$or": [{"player1.user_id": user_id}, {"player2.user_id": user_id}]},
                {"_id": 0}
            ).sort("created_at", -1))
            return battles
        else:
            with _LOCK:
                matched = [
                    dict(b) for b in _IN_MEMORY_BATTLES.values()
                    if b.get("player1", {}).get("user_id") == user_id
                    or (b.get("player2") and b.get("player2", {}).get("user_id") == user_id)
                ]
                matched.sort(key=lambda x: x.get("created_at", ""), reverse=True)
                return matched
