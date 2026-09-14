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
    print("AlgoQuest Sprint 2 Verification Suite")
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

    # 2. Validation error on creating user without name
    status, body = make_request("/users", method="POST", data={})
    assert_test("Create user without name returns 400", status == 400 and "name" in body.get("message", "").lower())

    # 3. Create valid user
    new_user_data = {
        "name": "Alex Hunter",
        "preferred_language": "python",
        "experience_level": "beginner",
        "learning_goal": "placement"
    }
    status, body = make_request("/users", method="POST", data=new_user_data)
    assert_test("Create user returns 201 Created", status == 201 and body.get("status") == "success")
    user = body.get("user", {})
    user_id = user.get("user_id")
    assert_test("User has generated unique user_id", bool(user_id) and user_id.startswith("user_"))
    assert_test("User default skills initialized with 7 dimensions", len(user.get("skills", {})) == 7)

    # 4. Retrieve user by ID
    status, body = make_request(f"/users/{user_id}")
    assert_test("Retrieve user by ID returns 200 OK", status == 200 and body.get("user", {}).get("name") == "Alex Hunter")

    # 5. Retrieve unknown user ID
    status, body = make_request("/users/unknown_user_999")
    assert_test("Retrieve unknown user returns 404", status == 404 and body.get("status") == "error")

    # 6. Get trial questions
    status, body = make_request("/trial")
    assert_test("Get trial questions returns 200 OK", status == 200)
    questions = body.get("questions", [])
    assert_test("Trial has 6 questions", len(questions) == 6)
    
    # Verify no correct_option or explanation is leaked in questions
    leaked = any("correct_option" in q or "explanation" in q for q in questions)
    assert_test("Trial questions do not leak answers or explanations", not leaked)

    # 7. Submit trial with invalid payload (missing user_id)
    status, body = make_request("/trial/submit", method="POST", data={"answers": {}})
    assert_test("Submit trial without user_id returns 400", status == 400)

    # 8. Submit trial for unknown user
    status, body = make_request("/trial/submit", method="POST", data={"user_id": "nonexistent_user", "answers": {}})
    assert_test("Submit trial for unknown user returns 404", status == 404)

    # 9. Submit trial answers - Scenario A: Weak dry-run (dry_run < 50)
    # Answers targeting dry_run incorrect (q5), but answering others correctly
    answers_weak_dryrun = {
        "q1_understanding": 0,    # correct -> 100
        "q2_concept": 1,          # correct -> 100
        "q3_decompose": 1,        # correct -> 100
        "q4_predict": 0,          # correct -> 100
        "q5_dry_run": 0,          # incorrect (correct is 2) -> dry_run = 0
        "q6_problem_solving": 1   # correct -> 100
    }
    status, body = make_request("/trial/submit", method="POST", data={
        "user_id": user_id,
        "answers": answers_weak_dryrun
    })
    assert_test("Submit trial returns 200 OK", status == 200 and body.get("status") == "success")
    skills = body.get("skill_scores", {})
    assert_test("Calculates score for each skill dimension", len(skills) == 7)
    assert_test("Identifies dry_run as improvement area", skills.get("dry_run") == 0)
    rec = body.get("recommendation", {})
    assert_test("Recommends dry-run quest when dry_run < 50", rec.get("focus_skill") == "dry_run" and rec.get("quest_id") == "array_002")
    assert_test("Recommendation includes clear reason", "reason" in rec and len(rec["reason"]) > 10)

    # 10. Check user profile reflects thinking profile and updated skills
    status, body = make_request(f"/users/{user_id}/profile")
    assert_test("Get profile returns 200 OK", status == 200)
    profile = body.get("profile", {})
    assert_test("Profile contains updated skills", profile.get("skills", {}).get("dry_run") == 0)
    assert_test("Profile contains thinking_profile", profile.get("thinking_profile") is not None)
    assert_test("Thinking profile records recommendation", profile.get("thinking_profile", {}).get("recommended_quest", {}).get("quest_id") == "array_002")

    # 11. Submit trial answers - Perfect trial -> array_001
    status, body = make_request("/users", method="POST", data={"name": "Sarah Connor", "preferred_language": "python"})
    sarah_id = body.get("user", {}).get("user_id")
    answers_perfect = {
        "q1_understanding": 0,
        "q2_concept": 1,
        "q3_decompose": 1,
        "q4_predict": 0,
        "q5_dry_run": 2,
        "q6_problem_solving": 1
    }
    status, body = make_request("/trial/submit", method="POST", data={
        "user_id": sarah_id,
        "answers": answers_perfect
    })
    assert_test("Perfect trial returns 100% accuracy", body.get("accuracy_percentage") == 100.0)
    assert_test("Perfect trial recommends array_001 (The Lost Maximum)", body.get("recommendation", {}).get("quest_id") == "array_001")

    # 12. Submit trial answers - Weak decomposition branch (decomposition < 60, dry_run >= 50)
    status, body = make_request("/users", method="POST", data={"name": "Decomp User"})
    decomp_uid = body.get("user", {}).get("user_id")
    answers_weak_decomp = {
        "q1_understanding": 0,
        "q2_concept": 1,
        "q3_decompose": 0,  # wrong (correct is 1) -> decomposition = 0
        "q4_predict": 0,
        "q5_dry_run": 2,    # correct -> dry_run = 100
        "q6_problem_solving": 1
    }
    status, body = make_request("/trial/submit", method="POST", data={
        "user_id": decomp_uid,
        "answers": answers_weak_decomp
    })
    rec = body.get("recommendation", {})
    assert_test("Recommends decomposition quest when decomposition < 60", rec.get("focus_skill") == "decomposition" and rec.get("quest_id") == "array_003")

    # 13. Submit trial answers - Weak understanding branch (understanding < 60, dry_run >= 50, decomposition >= 60)
    status, body = make_request("/users", method="POST", data={"name": "Understanding User"})
    und_uid = body.get("user", {}).get("user_id")
    answers_weak_und = {
        "q1_understanding": 2, # wrong (correct is 0) -> understanding = 0
        "q2_concept": 1,
        "q3_decompose": 1,     # correct -> decomposition = 100
        "q4_predict": 0,
        "q5_dry_run": 2,       # correct -> dry_run = 100
        "q6_problem_solving": 1
    }
    status, body = make_request("/trial/submit", method="POST", data={
        "user_id": und_uid,
        "answers": answers_weak_und
    })
    rec = body.get("recommendation", {})
    assert_test("Recommends understanding quest when understanding < 60", rec.get("focus_skill") == "understanding" and rec.get("quest_id") == "array_004")

    print("=" * 60)
    print(f" ALL {passed}/{total} TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
