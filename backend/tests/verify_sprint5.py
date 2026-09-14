import sys
from pathlib import Path

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
    print("AlgoQuest Sprint 5: Battle System / Duel Mode Suite")
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

    # 2. Create Users: Alice and Bob
    status, body = make_request("/users", method="POST", data={"name": "Alice Duelist"})
    assert_test("Create player 1 (Alice)", status == 201)
    alice_id = body.get("user", {}).get("user_id")

    status, body = make_request("/users", method="POST", data={"name": "Bob Challenger"})
    assert_test("Create player 2 (Bob)", status == 201)
    bob_id = body.get("user", {}).get("user_id")

    # 3. Create Battle Validations
    status, body = make_request("/battles", method="POST", data={"quest_id": "array_001"})
    assert_test("Create battle without user_id returns 400", status == 400)

    status, body = make_request("/battles", method="POST", data={"user_id": alice_id, "quest_id": "nonexistent_quest"})
    assert_test("Create battle with nonexistent quest returns 404", status == 404)

    status, body = make_request("/battles", method="POST", data={"user_id": alice_id, "quest_id": "array_001", "opponent_id": alice_id})
    assert_test("Challenging oneself returns 400", status == 400)

    # 4. Create Open Battle (waiting for opponent)
    status, body = make_request("/battles", method="POST", data={
        "user_id": alice_id,
        "quest_id": "array_001"
    })
    assert_test("Create open battle returns 201 Created", status == 201 and body.get("status") == "success")
    battle = body.get("battle", {})
    battle_id = battle.get("battle_id")
    assert_test("Battle has 'battle_' prefix", battle_id.startswith("battle_"))
    assert_test("Battle status is 'waiting'", battle.get("status") == "waiting")
    assert_test("Player 2 is initially None", battle.get("player2") is None)

    # 5. Fetch Battle by ID
    status, body = make_request(f"/battles/{battle_id}")
    assert_test("Fetch battle by ID returns 200 OK", status == 200 and body.get("battle", {}).get("battle_id") == battle_id)

    status, body = make_request("/battles/unknown_battle_999")
    assert_test("Fetch unknown battle returns 404", status == 404)

    # 6. Join Battle Validations
    status, body = make_request(f"/battles/{battle_id}/join", method="POST", data={"user_id": alice_id})
    assert_test("Creator joining own battle returns 400", status == 400)

    # Bob joins the battle
    status, body = make_request(f"/battles/{battle_id}/join", method="POST", data={"user_id": bob_id})
    assert_test("Opponent (Bob) joins battle returns 200 OK", status == 200)
    updated_battle = body.get("battle", {})
    assert_test("Battle status advances to 'in_progress'", updated_battle.get("status") == "in_progress")
    assert_test("Player 2 is Bob", updated_battle.get("player2", {}).get("user_id") == bob_id)

    # Another user tries to join when already full
    status, body = make_request("/users", method="POST", data={"name": "Charlie ThirdWheel"})
    charlie_id = body.get("user", {}).get("user_id")
    status, body = make_request(f"/battles/{battle_id}/join", method="POST", data={"user_id": charlie_id})
    assert_test("Third player joining full battle returns 400", status == 400)

    # 7. Submissions: Non-participant rejected
    status, body = make_request(f"/battles/{battle_id}/submit", method="POST", data={
        "user_id": charlie_id,
        "answers": {}
    })
    assert_test("Non-participant submission returns 403 Forbidden", status == 403)

    # Player 1 (Alice) submits perfect answers in 15 seconds
    alice_answers = {
        "understand": 0,
        "identify": 1,
        "decompose": 0,
        "predict": 1,
        "dry_run": 0,
        "solve": 0,
        "explain": 0
    }
    status, body = make_request(f"/battles/{battle_id}/submit", method="POST", data={
        "user_id": alice_id,
        "answers": alice_answers,
        "time_taken_seconds": 15
    })
    assert_test("Alice submits duel answers returns 200 OK", status == 200)
    perf = body.get("performance", {})
    assert_test("Alice gets 100 accuracy + 19 speed bonus = 119", perf.get("total_score") == 119)
    assert_test("Battle still waiting for Bob (battle_completed=False)", body.get("battle_completed") is False)

    # Duplicate submission rejected
    status, body = make_request(f"/battles/{battle_id}/submit", method="POST", data={
        "user_id": alice_id,
        "answers": alice_answers
    })
    assert_test("Alice duplicate submission returns 400", status == 400 and "already submitted" in body.get("message", "").lower())

    # Player 2 (Bob) submits partial answers in 30 seconds
    bob_answers = {
        "understand": 0,
        "identify": 1,
        "decompose": 0
    }
    status, body = make_request(f"/battles/{battle_id}/submit", method="POST", data={
        "user_id": bob_id,
        "answers": bob_answers,
        "time_taken_seconds": 30
    })
    assert_test("Bob submits duel answers returns 200 OK", status == 200)
    assert_test("Battle resolves automatically (battle_completed=True)", body.get("battle_completed") is True)
    final_b = body.get("battle", {})
    assert_test("Alice declared winner (119 vs 52)", final_b.get("winner_id") == alice_id)
    assert_test("Alice awarded 50 XP and Bob awarded 15 XP", final_b.get("xp_awarded", {}).get("player1") == 50 and final_b.get("xp_awarded", {}).get("player2") == 15)

    # 8. Battle Against algo_bot
    status, body = make_request("/battles", method="POST", data={
        "user_id": alice_id,
        "quest_id": "array_001",
        "opponent_id": "algo_bot"
    })
    assert_test("Create duel against algo_bot returns 201", status == 201)
    bot_battle = body.get("battle", {})
    bot_bid = bot_battle.get("battle_id")
    assert_test("Bot battle status is 'in_progress'", bot_battle.get("status") == "in_progress")
    assert_test("Player 2 is AlgoBot", bot_battle.get("player2", {}).get("user_id") == "algo_bot")

    # Alice submits against algo_bot
    status, body = make_request(f"/battles/{bot_bid}/submit", method="POST", data={
        "user_id": alice_id,
        "answers": alice_answers,
        "time_taken_seconds": 10
    })
    assert_test("Alice vs AlgoBot submission resolves immediately", status == 200 and body.get("battle_completed") is True)
    assert_test("Alice defeats AlgoBot (119 vs 85)", body.get("battle", {}).get("winner_id") == alice_id)

    # 9. Battle History
    status, body = make_request(f"/users/{alice_id}/battle-history")
    assert_test("Get battle history returns 200 OK", status == 200)
    assert_test("Alice has 2 completed battles", body.get("total_battles") == 2)
    assert_test("Alice has 2 victories", body.get("victories") == 2)
    assert_test("Battle history contains match records", len(body.get("battles", [])) == 2)

    status, body = make_request(f"/users/{bob_id}/battle-history")
    assert_test("Bob has 1 battle and 0 victories", body.get("total_battles") == 1 and body.get("victories") == 0)

    print("=" * 65)
    print(f" ALL {passed}/{total} SPRINT 5 BATTLE TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
