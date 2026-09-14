import json
from pathlib import Path
from models.user_model import DEFAULT_SKILLS

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "trials" / "thinking_trial.json"

class ScoringService:
    """Evaluates thinking trials and computes skill breakdown deterministically."""

    @classmethod
    def load_questions(cls):
        """Loads raw thinking trial questions from data store."""
        if not DATA_PATH.exists():
            return []
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def get_client_questions(cls):
        """Returns questions stripped of answers and explanations for client safety."""
        questions = cls.load_questions()
        sanitized = []
        for q in questions:
            sanitized.append({
                "id": q["id"],
                "skill_dimension": q["skill_dimension"],
                "question": q["question"],
                "code_snippet": q.get("code_snippet"),
                "options": q["options"]
            })
        return sanitized

    @classmethod
    def evaluate_trial(cls, user_answers, current_skills=None):
        """
        Evaluates submitted answers deterministically.
        user_answers: dict of { question_id: selected_option_index }
        """
        questions = cls.load_questions()
        if not questions:
            raise RuntimeError("Thinking trial questions not found.")

        # Baseline skills from existing user or system defaults
        baseline_skills = dict(current_skills or DEFAULT_SKILLS)
        
        dimension_points = {}
        dimension_counts = {}
        question_evaluations = []
        total_questions = len(questions)
        correct_count = 0

        for q in questions:
            qid = q["id"]
            dim = q["skill_dimension"]
            correct_opt = q["correct_option"]
            submitted = user_answers.get(qid)

            is_correct = False
            if submitted is not None:
                try:
                    is_correct = int(submitted) == int(correct_opt)
                except (ValueError, TypeError):
                    is_correct = False

            if is_correct:
                correct_count += 1
                points = 100
            else:
                points = 0

            dimension_points[dim] = dimension_points.get(dim, 0) + points
            dimension_counts[dim] = dimension_counts.get(dim, 0) + 1

            question_evaluations.append({
                "question_id": qid,
                "dimension": dim,
                "submitted_option": submitted,
                "correct_option": correct_opt,
                "is_correct": is_correct,
                "explanation": q.get("explanation")
            })

        # Calculate final score for each dimension
        skill_scores = {}
        for dim, default_val in DEFAULT_SKILLS.items():
            if dim in dimension_counts and dimension_counts[dim] > 0:
                skill_scores[dim] = round(dimension_points[dim] / dimension_counts[dim])
            else:
                # For dimensions not directly tested in objective questions (e.g. explanation),
                # calibrate from baseline or problem-solving/understanding average
                if dim == "explanation":
                    und = skill_scores.get("understanding", default_val)
                    prob = skill_scores.get("problem_solving", default_val)
                    skill_scores[dim] = round((und + prob) / 2)
                else:
                    skill_scores[dim] = default_val

        overall_score = round(sum(skill_scores.values()) / len(skill_scores))

        # Determine Strengths & Improvement Areas
        sorted_by_score = sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)
        strengths = [dim for dim, score in sorted_by_score if score >= 70]
        if not strengths:
            # Fallback to top 2
            strengths = [dim for dim, _ in sorted_by_score[:2]]

        improvement_areas = [dim for dim, score in sorted_by_score if score < 60]
        if not improvement_areas:
            # Fallback to bottom 2
            improvement_areas = [dim for dim, _ in sorted_by_score[-2:]]

        return {
            "correct_answers": correct_count,
            "total_questions": total_questions,
            "accuracy_percentage": round((correct_count / total_questions) * 100, 1),
            "overall_score": overall_score,
            "skill_scores": skill_scores,
            "strengths": strengths,
            "improvement_areas": improvement_areas,
            "breakdown": question_evaluations
        }
