import json
from pathlib import Path

STAGE_ORDER = ["understand", "identify", "decompose", "predict", "dry_run", "solve", "explain"]

STAGE_SKILL_MAP = {
    "understand": "understanding",
    "identify": "concept_recognition",
    "decompose": "decomposition",
    "predict": "prediction",
    "dry_run": "dry_run",
    "solve": "problem_solving",
    "explain": "explanation"
}

BASE_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class QuestService:
    """Manages Worlds, Quests, Stage progressions, deterministic evaluation, and hints."""

    @classmethod
    def get_stage_order(cls):
        return list(STAGE_ORDER)

    @classmethod
    def get_next_stage(cls, current_stage):
        """Returns the next stage identifier or 'completed' if at the final stage."""
        if current_stage not in STAGE_ORDER:
            return None
        idx = STAGE_ORDER.index(current_stage)
        if idx + 1 < len(STAGE_ORDER):
            return STAGE_ORDER[idx + 1]
        return "completed"

    @classmethod
    def load_worlds(cls):
        """Loads all world configurations."""
        worlds_path = BASE_DATA_DIR / "worlds" / "worlds.json"
        if not worlds_path.exists():
            return []
        with open(worlds_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def get_world(cls, world_id):
        """Retrieves a single world by ID."""
        worlds = cls.load_worlds()
        for w in worlds:
            if w.get("world_id") == world_id:
                return w
        return None

    @classmethod
    def load_quests(cls):
        """Loads all quest configurations."""
        quests_path = BASE_DATA_DIR / "quests" / "array_quests.json"
        if not quests_path.exists():
            return []
        with open(quests_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def get_quest(cls, quest_id, sanitize=True):
        """
        Retrieves a quest by ID.
        If sanitize=True, strips expected answers and explanations from stages.
        """
        quests = cls.load_quests()
        quest = None
        for q in quests:
            if q.get("quest_id") == quest_id:
                quest = dict(q)
                break

        if not quest:
            return None

        if sanitize and "stages" in quest:
            sanitized_stages = []
            for s in quest["stages"]:
                sanitized_stages.append({
                    "stage_id": s["stage_id"],
                    "name": s["name"],
                    "skill_dimension": s["skill_dimension"],
                    "type": s["type"],
                    "prompt": s["prompt"],
                    "code_snippet": s.get("code_snippet"),
                    "options": s.get("options", []),
                    "max_points": s.get("max_points", 10),
                    "hints_available": len(s.get("hints", []))
                })
            quest["stages"] = sanitized_stages

        return quest

    @classmethod
    def get_stage_hint(cls, quest, stage_id, current_hint_count):
        """
        Returns progressive hint for the given stage without revealing full answer.
        current_hint_count: how many hints the user has ALREADY consumed for this stage.
        """
        raw_stages = quest.get("stages", [])
        stage = next((s for s in raw_stages if s.get("stage_id") == stage_id), None)
        if not stage:
            return None, False

        hints = stage.get("hints", [])
        if not hints:
            return "Take your time and review the problem constraints and variable states carefully.", False

        if current_hint_count < len(hints):
            hint_text = hints[current_hint_count]
            has_more = (current_hint_count + 1) < len(hints)
            return hint_text, has_more
        else:
            return hints[-1] + " (All hints for this stage have been unlocked.)", False

    @classmethod
    def evaluate_stage(cls, quest, stage_id, answer, hints_used_count=0):
        """
        Deterministically evaluates stage answers.
        Returns:
            dict containing score, max_score, correctness, feedback, next_stage
        """
        raw_stages = quest.get("stages", [])
        stage = next((s for s in raw_stages if s.get("stage_id") == stage_id), None)
        if not stage:
            return None

        max_points = stage.get("max_points", 10)
        expected = stage.get("expected_answer")
        explanation = stage.get("explanation", "Stage completed.")

        is_correct = False
        # Normalize comparison
        if isinstance(expected, int):
            try:
                is_correct = int(answer) == expected
            except (ValueError, TypeError):
                # Fallback check for string match or solve snippet
                if isinstance(answer, str) and stage_id == "solve":
                    is_correct = "num > max_val" in answer.lower() or "max_val = num" in answer.lower()
                else:
                    is_correct = False
        else:
            is_correct = str(answer).strip().lower() == str(expected).strip().lower()

        if is_correct:
            # Hint penalty: 2 points per hint used, down to floor of 20% max points
            penalty = min(hints_used_count * 2, int(max_points * 0.8))
            earned_points = max(int(max_points * 0.2), max_points - penalty)
            correctness = "perfect" if hints_used_count == 0 else "correct_with_hints"
            feedback = explanation
        else:
            earned_points = 0
            correctness = "incorrect"
            feedback = "That answer was not correct. Analyze the problem constraints, re-check your assumptions, or request a progressive hint."

        next_stage = cls.get_next_stage(stage_id)

        return {
            "stage_id": stage_id,
            "score": earned_points,
            "max_score": max_points,
            "correctness": correctness,
            "feedback": feedback,
            "skill_dimension": stage.get("skill_dimension", STAGE_SKILL_MAP.get(stage_id)),
            "next_stage": next_stage
        }
