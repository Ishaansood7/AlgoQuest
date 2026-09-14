import json
import logging
import urllib.request
import urllib.error
from config import Config

logger = logging.getLogger("algoquest.ai")

# Progressive 3-tier deterministic fallback hints for array_001
STAGE_FALLBACK_HINTS = {
    "understand": {
        1: "Focus on the end goal: what single numerical value needs to be extracted from the array?",
        2: "Notice we are looking for the maximum value itself, not an index, count, or sorted sequence.",
        3: "Example: For stones [3, 7, 2], the goal is to return 7. Keep your focus on finding the single highest number."
    },
    "identify": {
        1: "The array is unsorted. Can you safely skip any elements without inspecting them?",
        2: "Because any element could be the largest, an optimal solution must inspect every element once in linear time.",
        3: "Pattern clue: A single linear pass O(N) holding a 'current champion' is both optimal and straightforward."
    },
    "decompose": {
        1: "What is your baseline reference point before you begin iterating through the array?",
        2: "First set current_max to the first element (arr[0]), then loop through the remaining elements from index 1 to N-1.",
        3: "Logical breakdown: 1. Initialize max to arr[0] -> 2. Compare each next element -> 3. Update if larger -> 4. Return max."
    },
    "predict": {
        1: "Trace each element one by one against the running maximum.",
        2: "Only count an update when the condition 'arr[i] > current_max' evaluates to strictly True.",
        3: "Trace for [3, 7, 2, 9, 5]: 7 > 3 (update #1), 2 > 7 (no), 9 > 7 (update #2), 5 > 9 (no). Exactly 2 updates occur."
    },
    "dry_run": {
        1: "Think about what the maximum variable was holding right before element 9 was encountered at index 3.",
        2: "After index 2, current_max held 7. When inspecting index 3 (value 9), compare 9 against 7.",
        3: "State transition: Before = 7. Condition 9 > 7 is True. After = 9."
    },
    "solve": {
        1: "What conditional comparison determines if you have encountered a new maximum?",
        2: "You need a strictly greater-than comparison (`>`), followed by storing that new value into `max_val`.",
        3: "Core code pattern: `if num > max_val: max_val = num`."
    },
    "explain": {
        1: "How many times does the algorithm loop through an array of size N?",
        2: "Visiting each element once takes O(N) time. How much auxiliary memory is allocated?",
        3: "Complexity analysis: O(N) time because each element is inspected once. O(1) auxiliary space because only one tracking variable is retained."
    }
}

STAGE_FALLBACK_EXPLANATIONS = {
    "understand": "Understanding constraints and return types prevents off-by-one errors and incorrect algorithm selection.",
    "identify": "For unsorted data, linear scan O(N) is optimal because every element must be inspected at least once.",
    "decompose": "Decomposing algorithms into initialization, invariant loop, and return step ensures clean, bug-free implementation.",
    "predict": "Mental execution tracing strengthens loop invariant verification and catches edge case anomalies early.",
    "dry_run": "Step-by-step state tracing confirms that variables update only when their transition conditions are met.",
    "solve": "The core assignment `max_val = num` guarantees that the variable always reflects the largest number seen up to the current iteration.",
    "explain": "A single linear pass requires O(N) operations and maintaining one scalar variable uses O(1) space, making this optimal in time and space."
}

class AIService:
    """Provides contextual, Socratic AI coaching with deterministic fallback support."""

    @classmethod
    def _call_gemini_api(cls, system_prompt, user_prompt):
        """Calls Google Gemini REST API using urllib (zero extra dependencies)."""
        api_key = Config.AI_API_KEY
        if not api_key:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{Config.AI_MODEL_NAME}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{system_prompt}\n\nUser Question:\n{user_prompt}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 250
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=Config.AI_TIMEOUT_SECONDS) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
        return None

    @classmethod
    def get_fallback_hint(cls, stage_id, hint_level):
        """Returns deterministic stage hint according to progressive level."""
        stage_hints = STAGE_FALLBACK_HINTS.get(stage_id, {})
        if not stage_hints:
            return (
                "Review the stage instructions carefully, analyze the current variable state, and consider the algorithmic invariant.",
                False
            )

        if hint_level in stage_hints:
            hint_text = stage_hints[hint_level]
            has_more = (hint_level + 1) in stage_hints
            return hint_text, has_more
        else:
            return stage_hints.get(3, "All hints unlocked.") + " (All progressive hints for this stage have been unlocked.)", False

    @classmethod
    def generate_hint(cls, quest_id, stage_id, user_answer=None, hints_used=0, user_lang="python"):
        """
        Generates Socratic pedagogical hint with progressive tiers.
        Returns:
            dict with message, source, stage_id, hint_level, next_hint_available
        """
        # Calculate next hint level (1, 2, 3...)
        hint_level = int(hints_used) + 1
        level_label = {1: "conceptual nudge", 2: "structural direction", 3: "example & pattern"}.get(hint_level, "deep hint")

        # Check if AI is configured and enabled
        if Config.AI_ENABLED and Config.AI_API_KEY:
            try:
                system_prompt = (
                    "You are the AlgoQuest AI Coach, an expert DSA tutor for beginners. "
                    "Follow these strict pedagogical guardrails:\n"
                    "1. Never give the exact answer or reveal option letters/numbers.\n"
                    "2. Use Socratic questioning and progressive clues.\n"
                    f"3. This is hint level {hint_level} ({level_label}).\n"
                    f"4. Keep response under 3 sentences. Be encouraging and clear.\n"
                    f"5. Focus strictly on reasoning stage '{stage_id}' for quest '{quest_id}'."
                )
                user_prompt = f"The learner is on stage '{stage_id}'. "
                if user_answer:
                    user_prompt += f"Their current thought/answer is: '{str(user_answer)[:200]}'. "
                user_prompt += f"Please provide a level {hint_level} hint."

                ai_response = cls._call_gemini_api(system_prompt, user_prompt)
                if ai_response:
                    has_more = hint_level < 3
                    return {
                        "message": ai_response,
                        "source": "ai",
                        "quest_id": quest_id,
                        "stage_id": stage_id,
                        "hint_level": hint_level,
                        "next_hint_available": has_more
                    }
            except Exception as err:
                logger.warning(f"AI API request failed: {err}. Reverting to deterministic fallback.")

        # Deterministic fallback path
        fallback_msg, has_more = cls.get_fallback_hint(stage_id, hint_level)
        return {
            "message": fallback_msg,
            "source": "fallback",
            "quest_id": quest_id,
            "stage_id": stage_id,
            "hint_level": hint_level,
            "next_hint_available": has_more
        }

    @classmethod
    def generate_explanation(cls, quest_id, stage_id, user_answer=None, question_context=None, user_lang="python"):
        """
        Explains concepts or why an approach works/fails.
        Returns:
            dict with explanation, source, quest_id, stage_id
        """
        if Config.AI_ENABLED and Config.AI_API_KEY:
            try:
                system_prompt = (
                    "You are the AlgoQuest AI Coach. Explain why an algorithmic concept works or why a mistake occurs. "
                    "Be beginner-friendly, concise, and educational. Under 4 sentences."
                )
                user_prompt = f"Quest: '{quest_id}', Stage: '{stage_id}'. "
                if question_context:
                    user_prompt += f"Context: '{str(question_context)[:200]}'. "
                if user_answer:
                    user_prompt += f"User answer: '{str(user_answer)[:200]}'. "
                user_prompt += "Explain the core takeaway."

                ai_response = cls._call_gemini_api(system_prompt, user_prompt)
                if ai_response:
                    return {
                        "explanation": ai_response,
                        "source": "ai",
                        "quest_id": quest_id,
                        "stage_id": stage_id
                    }
            except Exception as err:
                logger.warning(f"AI explanation call failed: {err}. Reverting to fallback.")

        # Deterministic fallback explanation
        explanation = STAGE_FALLBACK_EXPLANATIONS.get(
            stage_id,
            "Carefully verifying edge cases and running state invariants ensures algorithmic correctness."
        )
        return {
            "explanation": explanation,
            "source": "fallback",
            "quest_id": quest_id,
            "stage_id": stage_id
        }
