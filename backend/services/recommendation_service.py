class RecommendationService:
    """Rule-based recommendation engine for personalized quest selection."""

    @classmethod
    def recommend_first_quest(cls, skill_scores):
        """
        Recommends the initial quest based on thinking profile skills:
        - If dry_run < 50 -> dry_run quest
        - Else if decomposition < 60 -> decomposition quest
        - Else if understanding < 60 -> problem-understanding quest
        - Else -> first Array Forest quest
        """
        dry_run = skill_scores.get("dry_run", 50)
        decomposition = skill_scores.get("decomposition", 50)
        understanding = skill_scores.get("understanding", 50)

        if dry_run < 50:
            return {
                "quest_id": "array_002",
                "world": "array_forest",
                "title": "The Step-by-Step Tracker",
                "difficulty": "beginner",
                "focus_skill": "dry_run",
                "reason": "Your dry-run tracing score was below 50. This quest trains stepping through loop iterations and pointer tracking."
            }
        elif decomposition < 60:
            return {
                "quest_id": "array_003",
                "world": "array_forest",
                "title": "Divide and Conquer Roots",
                "difficulty": "beginner",
                "focus_skill": "decomposition",
                "reason": "Your decomposition score was below 60. This quest trains breaking complex requirements into bite-sized logical steps."
            }
        elif understanding < 60:
            return {
                "quest_id": "array_004",
                "world": "array_forest",
                "title": "The Riddle of the Constraints",
                "difficulty": "beginner",
                "focus_skill": "understanding",
                "reason": "Your problem understanding score was below 60. This quest sharpens constraint identification and edge-case awareness."
            }
        else:
            return {
                "quest_id": "array_001",
                "world": "array_forest",
                "title": "The Lost Maximum",
                "difficulty": "beginner",
                "focus_skill": "problem_solving",
                "reason": "Strong baseline across core reasoning dimensions! You are ready to enter Array Forest and begin The Lost Maximum."
            }
