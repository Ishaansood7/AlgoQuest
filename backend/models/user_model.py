import uuid
import threading
from datetime import datetime, timezone
from db import get_db, Database

# Thread-safe in-memory stores for fallback / offline mode
_LOCK = threading.Lock()
_IN_MEMORY_USERS = {}
_IN_MEMORY_TRIALS = {}

DEFAULT_SKILLS = {
    "understanding": 50,
    "concept_recognition": 50,
    "decomposition": 50,
    "prediction": 50,
    "dry_run": 50,
    "problem_solving": 50,
    "explanation": 50
}

class UserModel:
    """Manages User entity persistence with transparent MongoDB/In-Memory fallback."""

    @staticmethod
    def _now_iso():
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def _is_mongo_active(cls):
        return Database.get_status().get("connected", False)

    @classmethod
    def create(cls, data):
        """Creates a new user with default skills, XP, and streaks."""
        user_id = data.get("user_id") or f"user_{uuid.uuid4().hex[:8]}"
        now = cls._now_iso()

        # Merge initial skills if custom provided, else defaults
        skills = {**DEFAULT_SKILLS, **(data.get("skills") or {})}

        user_doc = {
            "user_id": user_id,
            "name": data.get("name", "").strip(),
            "preferred_language": data.get("preferred_language", "python").strip().lower(),
            "experience_level": data.get("experience_level", "beginner").strip().lower(),
            "learning_goal": data.get("learning_goal", "placement").strip().lower(),
            "xp": int(data.get("xp", 0)),
            "level": int(data.get("level", 1)),
            "learning_streak": int(data.get("learning_streak", 1)),
            "skills": skills,
            "thinking_profile": None,
            "created_at": now,
            "updated_at": now
        }

        db = get_db()
        if cls._is_mongo_active() and db is not None:
            db.users.update_one({"user_id": user_id}, {"$set": user_doc}, upsert=True)
        else:
            with _LOCK:
                _IN_MEMORY_USERS[user_id] = dict(user_doc)

        return user_doc

    @classmethod
    def get_by_id(cls, user_id):
        """Fetches a user by user_id."""
        db = get_db()
        if cls._is_mongo_active() and db is not None:
            user = db.users.find_one({"user_id": user_id}, {"_id": 0})
            return user
        else:
            with _LOCK:
                user = _IN_MEMORY_USERS.get(user_id)
                return dict(user) if user else None

    @classmethod
    def update_skills_and_profile(cls, user_id, new_skills, thinking_profile=None):
        """Updates user skills and stores the resulting thinking profile."""
        now = cls._now_iso()
        update_fields = {
            "skills": new_skills,
            "updated_at": now
        }
        if thinking_profile is not None:
            update_fields["thinking_profile"] = thinking_profile

        db = get_db()
        if cls._is_mongo_active() and db is not None:
            result = db.users.update_one(
                {"user_id": user_id},
                {"$set": update_fields}
            )
            return result.matched_count > 0
        else:
            with _LOCK:
                user = _IN_MEMORY_USERS.get(user_id)
                if not user:
                    return False
                user["skills"] = new_skills
                if thinking_profile is not None:
                    user["thinking_profile"] = thinking_profile
                user["updated_at"] = now
                return True

    @classmethod
    def record_trial(cls, trial_record):
        """Saves a thinking trial attempt."""
        db = get_db()
        if cls._is_mongo_active() and db is not None:
            db.trials.insert_one(dict(trial_record))
        else:
            user_id = trial_record.get("user_id")
            with _LOCK:
                if user_id not in _IN_MEMORY_TRIALS:
                    _IN_MEMORY_TRIALS[user_id] = []
                _IN_MEMORY_TRIALS[user_id].append(dict(trial_record))
        return True

    @classmethod
    def get_user_trials(cls, user_id):
        """Fetches all trial attempts for a user."""
        db = get_db()
        if cls._is_mongo_active() and db is not None:
            trials = list(db.trials.find({"user_id": user_id}, {"_id": 0}))
            return trials
        else:
            with _LOCK:
                return list(_IN_MEMORY_TRIALS.get(user_id, []))

    @classmethod
    def award_xp_and_skills(cls, user_id, xp_gain, skill_updates=None):
        """
        Awards XP, updates level, and adjusts skill dimensions using gradual mastery formula:
        new_mastery = round(old_mastery * 0.7 + attempt_pct * 0.3)
        """
        now = cls._now_iso()
        user = cls.get_by_id(user_id)
        if not user:
            return None

        new_xp = user.get("xp", 0) + int(xp_gain)
        # Level formula: Level 1 at 0-99 XP, Level 2 at 100-199 XP, etc.
        new_level = 1 + (new_xp // 100)

        updated_skills = dict(user.get("skills", DEFAULT_SKILLS))
        if skill_updates and isinstance(skill_updates, dict):
            for dim, attempt_pct in skill_updates.items():
                if dim in updated_skills:
                    old_val = updated_skills[dim]
                    # 70% retention, 30% new performance weight
                    new_val = round((old_val * 0.7) + (float(attempt_pct) * 0.3))
                    # Clamp between 0 and 100
                    updated_skills[dim] = max(0, min(100, new_val))

        update_fields = {
            "xp": new_xp,
            "level": new_level,
            "skills": updated_skills,
            "updated_at": now
        }

        db = get_db()
        if cls._is_mongo_active() and db is not None:
            db.users.update_one({"user_id": user_id}, {"$set": update_fields})
        else:
            with _LOCK:
                if user_id in _IN_MEMORY_USERS:
                    _IN_MEMORY_USERS[user_id].update(update_fields)

        # Return updated user state
        updated_user = cls.get_by_id(user_id)
        return updated_user
