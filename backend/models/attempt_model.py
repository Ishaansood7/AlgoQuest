import uuid
import threading
from datetime import datetime, timezone
from db import get_db, Database

_LOCK = threading.Lock()
_IN_MEMORY_ATTEMPTS = {}

class AttemptModel:
    """Manages Quest Attempt persistence with dual-mode MongoDB / In-Memory support."""

    @staticmethod
    def _now_iso():
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def _is_mongo_active(cls):
        return Database.get_status().get("connected", False)

    @classmethod
    def create(cls, user_id, quest_id):
        """Initializes a new quest attempt starting at 'understand' stage."""
        attempt_id = f"attempt_{uuid.uuid4().hex[:8]}"
        now = cls._now_iso()

        attempt_doc = {
            "attempt_id": attempt_id,
            "user_id": user_id,
            "quest_id": quest_id,
            "started_at": now,
            "completed_at": None,
            "current_stage": "understand",
            "completed_stages": [],
            "stage_answers": {},
            "stage_scores": {},
            "hints_used": {},
            "total_score": 0,
            "percentage": 0.0,
            "xp_earned": 0,
            "status": "in_progress"
        }

        db = get_db()
        if cls._is_mongo_active() and db is not None:
            db.attempts.insert_one(dict(attempt_doc))
        else:
            with _LOCK:
                _IN_MEMORY_ATTEMPTS[attempt_id] = dict(attempt_doc)

        return attempt_doc

    @classmethod
    def get_by_id(cls, attempt_id):
        """Fetches an attempt by attempt_id."""
        db = get_db()
        if cls._is_mongo_active() and db is not None:
            attempt = db.attempts.find_one({"attempt_id": attempt_id}, {"_id": 0})
            return attempt
        else:
            with _LOCK:
                attempt = _IN_MEMORY_ATTEMPTS.get(attempt_id)
                return dict(attempt) if attempt else None

    @classmethod
    def record_hint(cls, attempt_id, stage_id):
        """Increments and returns the count of hints used for a specific stage."""
        attempt = cls.get_by_id(attempt_id)
        if not attempt:
            return 0

        hints_used = dict(attempt.get("hints_used", {}))
        current_count = hints_used.get(stage_id, 0) + 1
        hints_used[stage_id] = current_count

        db = get_db()
        if cls._is_mongo_active() and db is not None:
            db.attempts.update_one(
                {"attempt_id": attempt_id},
                {"$set": {"hints_used": hints_used}}
            )
        else:
            with _LOCK:
                if attempt_id in _IN_MEMORY_ATTEMPTS:
                    _IN_MEMORY_ATTEMPTS[attempt_id]["hints_used"] = hints_used

        return current_count

    @classmethod
    def update_stage_progress(cls, attempt_id, stage_id, answer, score, next_stage):
        """Records completed stage answer and score, and advances current_stage."""
        attempt = cls.get_by_id(attempt_id)
        if not attempt:
            return None

        completed_stages = list(attempt.get("completed_stages", []))
        if stage_id not in completed_stages:
            completed_stages.append(stage_id)

        stage_answers = dict(attempt.get("stage_answers", {}))
        stage_answers[stage_id] = answer

        stage_scores = dict(attempt.get("stage_scores", {}))
        stage_scores[stage_id] = score

        update_fields = {
            "completed_stages": completed_stages,
            "stage_answers": stage_answers,
            "stage_scores": stage_scores,
            "current_stage": next_stage
        }

        db = get_db()
        if cls._is_mongo_active() and db is not None:
            db.attempts.update_one({"attempt_id": attempt_id}, {"$set": update_fields})
        else:
            with _LOCK:
                if attempt_id in _IN_MEMORY_ATTEMPTS:
                    _IN_MEMORY_ATTEMPTS[attempt_id].update(update_fields)

        return cls.get_by_id(attempt_id)

    @classmethod
    def mark_completed(cls, attempt_id, total_score, percentage, xp_earned):
        """Finalizes the attempt marking status as completed."""
        now = cls._now_iso()
        update_fields = {
            "status": "completed",
            "completed_at": now,
            "current_stage": "completed",
            "total_score": int(total_score),
            "percentage": float(percentage),
            "xp_earned": int(xp_earned)
        }

        db = get_db()
        if cls._is_mongo_active() and db is not None:
            db.attempts.update_one({"attempt_id": attempt_id}, {"$set": update_fields})
        else:
            with _LOCK:
                if attempt_id in _IN_MEMORY_ATTEMPTS:
                    _IN_MEMORY_ATTEMPTS[attempt_id].update(update_fields)

        return cls.get_by_id(attempt_id)

    @classmethod
    def get_by_user_id(cls, user_id):
        """Retrieves all quest attempts for a user."""
        db = get_db()
        if cls._is_mongo_active() and db is not None:
            attempts = list(db.attempts.find({"user_id": user_id}, {"_id": 0}))
            return attempts
        else:
            with _LOCK:
                return [dict(a) for a in _IN_MEMORY_ATTEMPTS.values() if a.get("user_id") == user_id]
