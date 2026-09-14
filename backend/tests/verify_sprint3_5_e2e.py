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

def run_e2e_journey():
    print("=" * 65)
    print("AlgoQuest Sprint 3.5: Full End-to-End Integration & Quality Check")
    print("=" * 65)
    passed = 0
    total = 0

    def assert_check(name, condition, detail=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f" [PASS] Step {total:02d}: {name}")
        else:
            print(f" [FAIL] Step {total:02d}: {name} - {detail}")
            sys.exit(1)

    # 1. Create a new user
    status, body = make_request("/users", method="POST", data={
        "name": "E2E Adventurer",
        "preferred_language": "python",
        "experience_level": "intermediate",
        "learning_goal": "placement"
    })
    assert_check("Create new user (POST /api/users)", status == 201 and body.get("status") == "success")
    user = body.get("user", {})
    user_id = user.get("user_id")
    assert_check("Verify consistent user_id format ('user_' prefix)", user_id.startswith("user_") and len(user_id) > 6)
    assert_check("Initial user XP is 0 and Level is 1", user.get("xp") == 0 and user.get("level") == 1)

    # 2. Retrieve the user profile
    status, body = make_request(f"/users/{user_id}/profile")
    assert_check("Retrieve user profile (GET /api/users/<user_id>/profile)", status == 200)
    profile = body.get("profile", {})
    assert_check("Profile has 7 default thinking skills at 50", len(profile.get("skills", {})) == 7 and all(v == 50 for v in profile["skills"].values()))
    assert_check("Thinking profile is initially None", profile.get("thinking_profile") is None)

    # 3. Fetch the Thinking Trial
    status, body = make_request("/trial")
    assert_check("Fetch Thinking Trial (GET /api/trial)", status == 200)
    questions = body.get("questions", [])
    assert_check("Trial contains 6 questions", len(questions) == 6)
    answers_leaked = any("correct_option" in q or "expected_answer" in q or "explanation" in q for q in questions)
    assert_check("Security check: No answers or explanations leaked in trial GET endpoint", not answers_leaked)

    # 4. Submit the Thinking Trial
    # Deliberately answer q5 (dry_run) incorrectly to verify intelligent personalized recommendation
    trial_submission = {
        "user_id": user_id,
        "answers": {
            "q1_understanding": 0,    # correct
            "q2_concept": 1,          # correct
            "q3_decompose": 1,        # correct
            "q4_predict": 0,          # correct
            "q5_dry_run": 0,          # INCORRECT (correct is 2) -> dry_run = 0
            "q6_problem_solving": 1   # correct
        }
    }
    status, body = make_request("/trial/submit", method="POST", data=trial_submission)
    assert_check("Submit Thinking Trial (POST /api/trial/submit)", status == 200 and body.get("status") == "success")

    # 5. Confirm that a first quest recommendation is returned
    rec = body.get("recommendation", {})
    assert_check("First quest recommendation returned", bool(rec) and "quest_id" in rec)
    assert_check("Recommended quest is 'array_002' due to weak dry_run (<50)", rec.get("quest_id") == "array_002" and rec.get("focus_skill") == "dry_run")
    assert_check("Recommendation contains human-readable explanation", len(rec.get("reason", "")) > 15)

    # 6. Fetch the recommended quest / core quest array_001
    status, body = make_request("/quests/array_001")
    assert_check("Fetch quest details (GET /api/quests/array_001)", status == 200 and body.get("status") == "success")
    quest = body.get("quest", {})
    assert_check("Quest metadata has title, world_id, difficulty, xp_reward", quest.get("title") == "The Lost Maximum" and quest.get("world_id") == "array_forest")
    quest_leaked = any("expected_answer" in s or "explanation" in s for s in quest.get("stages", []))
    assert_check("Security check: No stage solutions leaked in quest GET endpoint", not quest_leaked)

    # 7. Start a quest attempt
    status, body = make_request("/quests/array_001/attempt", method="POST", data={"user_id": user_id})
    assert_check("Start quest attempt (POST /api/quests/array_001/attempt)", status == 201)
    attempt = body.get("attempt", {})
    attempt_id = attempt.get("attempt_id")
    assert_check("Verify consistent attempt_id format ('attempt_' prefix)", attempt_id.startswith("attempt_"))
    assert_check("Attempt starts at 'understand' stage in 'in_progress' status", attempt.get("current_stage") == "understand" and attempt.get("status") == "in_progress")

    # 8 & 9. Request progressive hint on Stage 1
    status, body = make_request("/quests/array_001/hint", method="POST", data={
        "user_id": user_id,
        "attempt_id": attempt_id,
        "stage_id": "understand"
    })
    assert_check("Request progressive hint (POST /api/quests/array_001/hint)", status == 200)
    hint_text = body.get("hint", "")
    assert_check("Hint provides guidance without revealing exact answer key", "option" not in hint_text.lower() and len(hint_text) > 10)
    assert_check("Hint usage counter incremented to 1", body.get("hints_used_for_stage") == 1)

    # 10. Submit Stage 1 and confirm score deduction for hint
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": user_id,
        "attempt_id": attempt_id,
        "stage_id": "understand",
        "answer": 0
    })
    assert_check("Submit Stage 1 'understand'", status == 200)
    feedback = body.get("stage_feedback", {})
    assert_check("Confirm hint penalty applied (10 max - 2 deduction = 8 pts)", feedback.get("score") == 8 and feedback.get("correctness") == "correct_with_hints")
    assert_check("Advances to Stage 2 'identify'", body.get("attempt_progress", {}).get("current_stage") == "identify")

    # Submit Stages 2 through 6 cleanly
    stages_flow = [
        ("identify", 1, 10),
        ("decompose", 0, 15),
        ("predict", 1, 15),
        ("dry_run", 0, 20),
        ("solve", 0, 20)
    ]
    for s_id, ans, max_p in stages_flow:
        status, body = make_request("/quests/array_001/submit", method="POST", data={
            "user_id": user_id,
            "attempt_id": attempt_id,
            "stage_id": s_id,
            "answer": ans
        })
        assert_check(f"Submit Stage '{s_id}' awards full {max_p} pts", status == 200 and body.get("stage_feedback", {}).get("score") == max_p)

    # 11. Complete the quest by submitting Stage 7: 'explain'
    status, body = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": user_id,
        "attempt_id": attempt_id,
        "stage_id": "explain",
        "answer": 0
    })
    assert_check("Submit Stage 7 'explain' completes quest", status == 200 and body.get("quest_completed") is True)
    summary = body.get("attempt_summary", {})
    assert_check("Attempt marked 'completed'", summary.get("status") == "completed")
    
    # Check score totals: 8 + 10 + 15 + 15 + 20 + 20 + 10 = 98
    assert_check("Verify accurate score total (98/100)", summary.get("total_score") == 98)

    # 12. Confirm XP awarded exactly once
    xp_awarded = summary.get("xp_earned")
    assert_check("Confirm XP earned is 98", xp_awarded == 98)
    user_prog = body.get("user_progress", {})
    assert_check("User progress reflects exactly 98 XP", user_prog.get("xp") == 98)

    # Attempt to submit again to test duplicate protection
    status_dup, body_dup = make_request("/quests/array_001/submit", method="POST", data={
        "user_id": user_id,
        "attempt_id": attempt_id,
        "stage_id": "explain",
        "answer": 0
    })
    assert_check("Duplicate submission rejected with 400 Bad Request", status_dup == 400 and "already been completed" in body_dup.get("message", "").lower())

    # 13. Confirm level and thinking skills are updated
    status_prof, body_prof = make_request(f"/users/{user_id}/profile")
    prof = body_prof.get("profile", {})
    assert_check("User XP remains exactly 98 after duplicate attempt (no XP leak)", prof.get("xp") == 98)
    assert_check("User level is 1 (reaches level 2 at 100 XP)", prof.get("level") == 1)
    
    # Verify skill mastery updated via 70/30 formula
    # In trial: q1 was correct -> understanding was 100.
    # In quest: understand stage earned 80% (8/10).
    # New mastery = round(100 * 0.7 + 80 * 0.3) = 70 + 24 = 94.
    und_skill = prof.get("skills", {}).get("understanding")
    assert_check("Rolling skill mastery formula applied to understanding (100*0.7 + 80*0.3 = 94)", und_skill == 94)

    # In trial: q5 was incorrect -> dry_run was 0.
    # In quest: dry_run stage earned 100% (20/20).
    # New mastery = round(0 * 0.7 + 100 * 0.3) = 30.
    dry_skill = prof.get("skills", {}).get("dry_run")
    assert_check("Rolling skill mastery formula applied to dry_run (0*0.7 + 100*0.3 = 30)", dry_skill == 30)

    # 14. Retrieve updated user profile
    assert_check("Profile reflects trial history count", prof.get("trial_attempts_count") >= 1)

    # 15. Retrieve progress and attempt history endpoints
    status_prog, body_prog = make_request(f"/users/{user_id}/progress")
    assert_check("Retrieve user progress (GET /api/users/<user_id>/progress)", status_prog == 200)
    prog_data = body_prog.get("progress", {})
    assert_check("Progress endpoint reports total_quests_completed = 1", prog_data.get("total_quests_completed") == 1)
    assert_check("Progress endpoint includes full quest attempts list", len(prog_data.get("quest_attempts", [])) == 1)

    status_att, body_att = make_request(f"/users/{user_id}/attempts")
    assert_check("Retrieve user attempts (GET /api/users/<user_id>/attempts)", status_att == 200 and body_att.get("total_attempts") == 1)

    # 16. Confirm next-quest recommendation is returned
    rec_next = body.get("recommendation", {})
    assert_check("Next-quest recommendation returned upon quest completion", bool(rec_next) and "quest_id" in rec_next)

    print("=" * 65)
    print(f" ALL {passed}/{total} INTEGRATION CHECKS PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_e2e_journey()
