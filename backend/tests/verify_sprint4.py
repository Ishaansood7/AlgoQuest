import sys
from pathlib import Path

# Ensure backend root is in sys.path for direct service imports
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:5000/api"

def make_request(path, method="GET", data=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data is not None else None

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            resp_body = json.loads(resp.read().decode("utf-8"))
            return status, resp_body
    except urllib.error.HTTPError as e:
        err_body = json.loads(e.read().decode("utf-8"))
        return e.code, err_body

def run_tests():
    print("=" * 65)
    print("AlgoQuest Sprint 4: AI Coach & Contextual Explanations Suite")
    print("=" * 65)
    passed = 0
    total = 0

    def assert_test(name, condition, detail=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f" [PASS] {name}")
        else:
            print(f" [FAIL] {name} - {detail}")
            sys.exit(1)

    # 1. Health check intact
    status, body = make_request("/health")
    assert_test("Health check responds 200 OK", status == 200 and body.get("status") == "success")

    # 2. Create user for AI context
    status, body = make_request("/users", method="POST", data={"name": "Ada Lovelace", "preferred_language": "python"})
    assert_test("Create user for AI Coach tests", status == 201)
    ada_id = body.get("user", {}).get("user_id")

    # 3. Missing API key / Fallback Hint Level 1 (Conceptual Nudge)
    status, body = make_request("/ai/hint", method="POST", data={
        "user_id": ada_id,
        "quest_id": "array_001",
        "stage_id": "understand",
        "hints_used": 0
    })
    assert_test("AI hint returns 200 OK without API key", status == 200 and body.get("status") == "success")
    assert_test("Source is fallback when API key unset", body.get("source") == "fallback")
    assert_test("Hint level is 1", body.get("hint_level") == 1)
    assert_test("Next hint available is True", body.get("next_hint_available") is True)
    assert_test("Message provides conceptual nudge", "numerical value" in body.get("message", "").lower() or "maximum" in body.get("message", "").lower())

    # 4. Progressive Hint Level 2 (Structural Direction)
    status, body = make_request("/ai/hint", method="POST", data={
        "user_id": ada_id,
        "quest_id": "array_001",
        "stage_id": "understand",
        "hints_used": 1
    })
    assert_test("Level 2 hint returns 200 OK", status == 200)
    assert_test("Hint level is 2", body.get("hint_level") == 2)
    assert_test("Level 2 message provides structural direction", "maximum value itself" in body.get("message", "").lower())
    assert_test("Next hint available is True for level 2", body.get("next_hint_available") is True)

    # 5. Progressive Hint Level 3 (Small Example / Pattern)
    status, body = make_request("/ai/hint", method="POST", data={
        "user_id": ada_id,
        "quest_id": "array_001",
        "stage_id": "understand",
        "hints_used": 2
    })
    assert_test("Level 3 hint returns 200 OK", status == 200)
    assert_test("Hint level is 3", body.get("hint_level") == 3)
    assert_test("Next hint available is False for level 3", body.get("next_hint_available") is False)
    assert_test("Level 3 message provides example", "example" in body.get("message", "").lower())

    # 6. Progressive Hint Level > 3 (All hints unlocked)
    status, body = make_request("/ai/hint", method="POST", data={
        "user_id": ada_id,
        "quest_id": "array_001",
        "stage_id": "understand",
        "hints_used": 3
    })
    assert_test("Level > 3 hint returns capped message", status == 200 and "unlocked" in body.get("message", "").lower())

    # 7. Fallback Contextual Explanation
    status, body = make_request("/ai/explain", method="POST", data={
        "user_id": ada_id,
        "quest_id": "array_001",
        "stage_id": "identify",
        "user_answer": "Binary search on unsorted array"
    })
    assert_test("AI explain returns 200 OK", status == 200 and body.get("status") == "success")
    assert_test("Explanation source is fallback", body.get("source") == "fallback")
    assert_test("Explanation provides educational rationale", "linear" in body.get("explanation", "").lower() or "unsorted" in body.get("explanation", "").lower())

    # 8. Validation: Missing quest_id or stage_id
    status, body = make_request("/ai/hint", method="POST", data={"stage_id": "understand"})
    assert_test("Missing quest_id returns 400", status == 400 and "quest_id" in body.get("message", "").lower())

    status, body = make_request("/ai/hint", method="POST", data={"quest_id": "array_001"})
    assert_test("Missing stage_id returns 400", status == 400 and "stage_id" in body.get("message", "").lower())

    # 9. Validation: Invalid stage_id
    status, body = make_request("/ai/hint", method="POST", data={"quest_id": "array_001", "stage_id": "magic_stage"})
    assert_test("Invalid stage_id returns 400", status == 400 and "invalid stage_id" in body.get("message", "").lower())

    # 10. Validation: Unknown quest_id
    status, body = make_request("/ai/hint", method="POST", data={"quest_id": "unknown_quest_999", "stage_id": "understand"})
    assert_test("Unknown quest_id returns 404", status == 404 and "not found" in body.get("message", "").lower())

    # 11. Validation: Unknown user_id
    status, body = make_request("/ai/hint", method="POST", data={"quest_id": "array_001", "stage_id": "understand", "user_id": "unknown_user_999"})
    assert_test("Unknown user_id returns 404", status == 404 and "not found" in body.get("message", "").lower())

    # 12. Safety & Privacy: Excessively long input rejection (> 1000 chars)
    long_input = "A" * 1050
    status, body = make_request("/ai/hint", method="POST", data={
        "quest_id": "array_001",
        "stage_id": "understand",
        "user_answer": long_input
    })
    assert_test("User answer > 1000 chars returns 400", status == 400 and "exceeds maximum" in body.get("message", "").lower())

    status, body = make_request("/ai/explain", method="POST", data={
        "quest_id": "array_001",
        "stage_id": "understand",
        "user_answer": long_input
    })
    assert_test("Explain answer > 1000 chars returns 400", status == 400 and "exceeds maximum" in body.get("message", "").lower())

    # 13. Provider failure / simulated exception resilience test (Direct Unit Check)
    from services.ai_service import AIService
    from config import Config

    # Force simulated failure
    original_api_key = Config.AI_API_KEY
    Config.AI_API_KEY = "invalid_simulated_key_that_fails"
    Config.AI_ENABLED = True
    
    # Should safely catch exception and return fallback without crashing
    res = AIService.generate_hint("array_001", "dry_run", hints_used=0)
    assert_test("AI service recovers gracefully on simulated API failure", res.get("source") == "fallback" and "Think about" in res.get("message"))
    
    res_exp = AIService.generate_explanation("array_001", "dry_run")
    assert_test("AI explain recovers gracefully on simulated API failure", res_exp.get("source") == "fallback")

    # Restore config
    Config.AI_API_KEY = original_api_key

    print("=" * 65)
    print(f" ALL {passed}/{total} SPRINT 4 AI TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
