import sys
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
    print("=" * 60)
    print("AlgoQuest Sprint 3 Verification Suite")
    print("=" * 60)
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

    # 2. Fetch Worlds
    status, body = make_request("/worlds")
    assert_test("Fetch worlds returns 200 OK", status == 200)
    worlds = body.get("worlds", [])
    assert_test("At least one world exists", len(worlds) >= 1)
    array_forest = next((w for w in worlds if w.get("world_id") == "array_forest"), None)
    assert_test("Array Forest world exists in catalog", array_forest is not None)

    # 3. Fetch Specific World
    status, body = make_request("/worlds/array_forest")
    assert_test("Fetch array_forest returns 200 OK", status == 200)
    world = body.get("world", {})
    assert_test("Array Forest lists quests", len(world.get("quests", [])) == 4)

    # 4. Fetch Nonexistent World
    status, body = make_request("/worlds/unknown_world_999")
    assert_test("Fetch unknown world returns 404", status == 404)

    # 5. Fetch array_001
    status, body = make_request("/quests/array_001")
    assert_test("Fetch quest array_001 returns 200 OK", status == 200)
    quest = body.get("quest", {})
    assert_test("Quest has 7 stages", len(quest.get("stages", [])) == 7)
    
    # Verify answers and explanations are NOT leaked
    leaked = any("expected_answer" in s or "explanation" in s for s in quest.get("stages", []))
    assert_test("Quest definition does not leak expected answers or explanations", not leaked)

    # 6. Fetch Nonexistent Quest
    status, body = make_request("/quests/unknown_quest_999")
    assert_test("Fetch unknown quest returns 404", status == 404)

    # 7. Create User for Quest Attempt
    status, body = make_request("/users", method="POST", data={"name": "Aria Stark", "preferred_language": "python"})
    assert_test("Create user for attempt returns 201", status == 201)
    aria_id = body.get("user", {}).get("user_id")

    # 8. Start Attempt Validation
    status, body = make_request("/quests/array_001/attempt", method="POST", data={})
    assert_test("Start attempt without user_id returns 400", status == 400)

    status, body = make_request("/quests/array_001/attempt", method="POST", data={"user_id": "nonexistent_user_999"})
    assert_test("Start attempt with invalid user_id returns 404", status == 404)

    status, body = make_request("/quests/nonexistent_quest_999/attempt", method="POST", data={"user_id": aria_id})
    assert_test("Start attempt with invalid quest_id returns 404", status == 404)

    # 9. Start Valid Attempt
    status, body = make_request("/quests/array_001/attempt", method="POST", data={"user_id": aria_id})
    assert_test("Start valid attempt returns 201 Created", status == 201)
    attempt = body.get("attempt", {})
    attempt_id = attempt.get("attempt_id")
    assert_test("Attempt begins at 'understand' stage", attempt.get("current_stage") == "understand")
    assert_test("Attempt status is 'in_progress'", attempt.get("status") == "in_progress")

    # 10. Hint Validation
    # Another user
    status, body = make_request("/users", method="POST", data={"name": "Jon Snow"})
    jon_id = body.get("user", {}).get("user_id")

    status, body = make_request("/quests/array_001/hint", method="POST", data={
        "user_id": jon_id,
        "attempt_id": attempt_id,
        "stage_id": "understand"
    })
    assert_test("Request hint from wrong user returns 403 Forbidden", status == 403)

    status, body = make_request("/quests/array_001/hint", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "dry_run"
    })
    assert_test("Request hint for out-of-order stage returns 400", status == 400)

    # Request legitimate hint for current stage ("understand")
    status, body = make_request("/quests/array_001/hint", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "understand"
    })
    assert_test("Request valid hint returns 200 OK", status == 200)
    assert_test("Hint returned progressive text", len(body.get("hint", "")) > 5)
    assert_test("Hint tracks hints used count", body.get("hints_used_for_stage") == 1)

    # 11. Submit Validation: Out of Order
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "decompose",
        "answer": 0
    })
    assert_test("Submit out-of-order stage returns 400", status == 400)

    # 12. Submit Stage 1: "understand" (10 max pts, 1 hint used -> 8 pts)
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "understand",
        "answer": 0
    })
    assert_test("Submit stage 1 'understand' returns 200 OK", status == 200)
    assert_test("Stage feedback earned points with hint penalty", body.get("stage_feedback", {}).get("score") == 8)
    assert_test("Advances current stage to 'identify'", body.get("attempt_progress", {}).get("current_stage") == "identify")

    # 13. Re-submit or hint on already completed stage
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "understand",
        "answer": 0
    })
    assert_test("Duplicate stage submit returns 400", status == 400)

    status, body = make_request("/quests/array_001/hint", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "understand"
    })
    assert_test("Hint on already completed stage returns 400", status == 400)

    # 14. Step through remaining stages 2 through 6
    # Stage 2: identify (expected 1, max 10 pts)
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "identify",
        "answer": 1
    })
    assert_test("Submit stage 2 'identify' returns 200 OK", status == 200 and body.get("attempt_progress", {}).get("current_stage") == "decompose")

    # Stage 3: decompose (expected 0, max 15 pts)
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "decompose",
        "answer": 0
    })
    assert_test("Submit stage 3 'decompose' returns 200 OK", status == 200 and body.get("attempt_progress", {}).get("current_stage") == "predict")

    # Stage 4: predict (expected 1, max 15 pts)
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "predict",
        "answer": 1
    })
    assert_test("Submit stage 4 'predict' returns 200 OK", status == 200 and body.get("attempt_progress", {}).get("current_stage") == "dry_run")

    # Stage 5: dry_run (expected 0, max 20 pts)
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "dry_run",
        "answer": 0
    })
    assert_test("Submit stage 5 'dry_run' returns 200 OK", status == 200 and body.get("attempt_progress", {}).get("current_stage") == "solve")

    # Stage 6: solve (expected 0 or snippet, max 20 pts)
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "solve",
        "answer": 0
    })
    assert_test("Submit stage 6 'solve' returns 200 OK", status == 200 and body.get("attempt_progress", {}).get("current_stage") == "explain")

    # 15. Submit Final Stage 7: explain (expected 0, max 10 pts) -> Triggers Completion
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "explain",
        "answer": 0
    })
    assert_test("Submit stage 7 'explain' completes quest", status == 200 and body.get("quest_completed") is True)
    summary = body.get("attempt_summary", {})
    assert_test("Attempt marked completed", summary.get("status") == "completed")
    assert_test("Calculates total score (98 with 1 hint penalty)", summary.get("total_score") == 98)
    assert_test("Awards scaled XP (98 XP)", summary.get("xp_earned") == 98)
    user_prog = body.get("user_progress", {})
    assert_test("User progress records earned XP", user_prog.get("xp") == 98)
    assert_test("Next quest recommendation provided", "recommendation" in body and body["recommendation"].get("quest_id") is not None)

    # 16. Duplicate Completion Protection
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "explain",
        "answer": 0
    })
    assert_test("Duplicate completion attempt returns 400", status == 400 and "already been completed" in body.get("message", "").lower())

    # Hint after completion
    status, body = make_request("/quests/array_001/hint", method="POST", data={
        "user_id": aria_id,
        "attempt_id": attempt_id,
        "stage_id": "explain"
    })
    assert_test("Hint request after completion returns 400", status == 400 and "already been completed" in body.get("message", "").lower())

    # 17. Level Up Verification: Complete a second quest attempt to cross 100 XP -> Level 2
    status, body = make_request("/quests/array_001/attempt", method="POST", data={"user_id": aria_id})
    att2_id = body.get("attempt", {}).get("attempt_id")
    # Quickly submit 7 stages on attempt 2
    answers = [0, 1, 0, 1, 0, 0, 0]
    stages = ["understand", "identify", "decompose", "predict", "dry_run", "solve", "explain"]
    for s_name, ans in zip(stages, answers):
        status, body = make_request("/quests/array_001/submit", method="POST", data={
            "user_id": aria_id,
            "attempt_id": att2_id,
            "stage_id": s_name,
            "answer": ans
        })
    assert_test("Second quest completion reaches 198 XP", body.get("user_progress", {}).get("xp") == 198)
    assert_test("User levels up to Level 2 (100+ XP)", body.get("user_progress", {}).get("level") == 2)

    # 18. Retrieve Updated User Profile
    status, body = make_request(f"/users/{aria_id}/profile")
    assert_test("User profile reflects level 2 and 198 XP", status == 200 and body.get("profile", {}).get("level") == 2 and body.get("profile", {}).get("xp") == 198)

    print("=" * 60)
    print(f" ALL {passed}/{total} TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
