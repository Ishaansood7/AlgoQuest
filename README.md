# AlgoQuest — Backend Engine

> A gamified DSA learning platform powered by a 7-stage reasoning loop, deterministic skill scoring, and intelligent quest recommendations.

---

## Architecture & Flow

```text
1. User Onboarding ───► POST /api/users
                             │
                             ▼
2. Thinking Trial   ───► GET /api/trial
                             │
                             ▼
3. Submit Answers   ───► POST /api/trial/submit
                             │
                             ├──► Deterministic Scoring (7 Dimensions)
                             └──► Personalized First Quest Recommendation
                                     │
                                     ▼
4. World & Quests   ───► GET /api/worlds / GET /api/quests/<quest_id>
                             │
                             ▼
5. Quest Attempt    ───► POST /api/quests/<quest_id>/attempt
                             │
    ┌────────────────────────┴──────────────────────┐
    ▼                                               ▼
POST /api/quests/<quest_id>/hint        POST /api/quests/<quest_id>/submit
(Progressive hint, -2 pts deduction)    (Advances stage 1 through 7)
    │                                               │
    └───────────────────────┬───────────────────────┘
                            ▼
6. Quest Completion: All 7 Stages Finished
   ├──► Total Score & Percentage
   ├──► Scaled XP Awarded (Level = 1 + XP // 100)
   ├──► Rolling Skill Mastery Update (70% old + 30% attempt)
   └──► Next Quest Recommendation (Prevent Duplicate XP)
```

---

## 7-Stage Learning Framework

Every quest guides the learner through 7 sequential reasoning stages:

| Stage # | Stage Name | Target Skill | Max Points | Description |
|---|---|---|---|---|
| **1** | `understand` | `understanding` | 10 | Problem goal, input/output contracts, and constraints. |
| **2** | `identify` | `concept_recognition` | 10 | Recognizing the underlying algorithm/pattern. |
| **3** | `decompose` | `decomposition` | 15 | Breaking the solution into clear, ordered sub-steps. |
| **4** | `predict` | `prediction` | 15 | Mental simulation and output/state prediction. |
| **5** | `dry_run` | `dry_run` | 20 | Tracing pointer and loop variables step-by-step. |
| **6** | `solve` | `problem_solving` | 20 | Core algorithmic logic & assignment expression. |
| **7** | `explain` | `explanation` | 10 | Time & space complexity trade-offs and rationale. |
| **Total** | | | **100** | |

> [!NOTE]
> **MVP Solve Stage Scope**: For the 24-hour hackathon MVP, the `solve` stage evaluates structured solution input, pattern selection, and code snippets deterministically without running an arbitrary code execution sandbox.

---

## Setup & Installation

### 1. Prerequisites
- Python 3.11 or 3.12
- `git`

### 2. Environment Setup
```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in `backend/`:
```bash
# Server configuration
PORT=5000
FLASK_ENV=development
SECRET_KEY=algoquest-hackathon-secret-key

# MongoDB Atlas Configuration (Optional)
# If left empty, backend operates in graceful In-Memory mock mode
MONGO_URI=
DB_NAME=algoquest
```

---

## Running the Server

```powershell
cd backend
.\venv\Scripts\python.exe app.py
```
Server runs on `http://127.0.0.1:5000` with CORS enabled.

---

## Scoring, XP & Mastery Rules

1. **Stage Scoring**:
   - Each stage has a fixed point value totaling 100 points per quest.
   - Using hints deducts **2 points per hint** used for that stage (down to a minimum floor of 20% max points).
2. **XP & Leveling**:
   - $\text{XP Earned} = \text{round}(\text{Quest Max XP} \times \frac{\text{Total Score}}{100})$
   - $\text{Level} = 1 + (\text{Total User XP} // 100)$ (Level 1: 0–99 XP, Level 2: 100–199 XP, etc.)
   - Duplicate completion protection prevents re-awarding XP on completed attempts.
3. **Skill Mastery Update**:
   - Rolling formula blending historical competency with latest performance:
     $$\text{New Skill} = \text{round}(\text{Old Skill} \times 0.70 + \text{Stage \%} \times 0.30)$$

---

## API Reference

### Health & User APIs

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health and database connectivity status. |
| `POST` | `/api/users` | Creates a new user with baseline skills (50 each). |
| `GET` | `/api/users/<user_id>` | Retrieves user details. |
| `GET` | `/api/users/<user_id>/profile` | Rich profile with XP, level, streak, skills, and trial history. |
| `GET` | `/api/users/<user_id>/progress` | Aggregated user progress, completed quest count, and attempts. |
| `GET` | `/api/users/<user_id>/attempts` | Full list of quest attempts for the user. |

### Thinking Trial APIs

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/trial` | Fetches 6 objective assessment questions (answers stripped). |
| `POST` | `/api/trial/submit` | Evaluates answers, calculates skill scores, and recommends first quest. |

### AI Coach APIs (Optional & Resilient)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/ai/hint` | Socratic, progressive hints (Level 1 $\to$ 2 $\to$ 3). Falls back if API key is unset. |
| `POST` | `/api/ai/explain` | Contextual algorithmic explanation of concepts or mistake patterns. |

### Battle System / Duel Mode APIs

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/battles` | Initiates a 1v1 duel challenge against a friend or `algo_bot`. |
| `GET` | `/api/battles/<battle_id>` | Retrieves duel status, participant states, and scores. |
| `POST` | `/api/battles/<battle_id>/join` | Player 2 joins an open challenge. |
| `POST` | `/api/battles/<battle_id>/submit` | Submits answers and timing; auto-resolves winner when both finish. |
| `GET` | `/api/users/<user_id>/battle-history` | Match history with win/loss statistics. |

### World & Quest APIs

#### 1. List Worlds
- **`GET /api/worlds`**
- **Response `200 OK`**:
```json
{
  "status": "success",
  "total_worlds": 1,
  "worlds": [
    {
      "world_id": "array_forest",
      "name": "Array Forest",
      "theme": "nature_and_pointers",
      "description": "Master pointers, traversals, and running state techniques.",
      "total_quests": 4,
      "unlocked": true
    }
  ]
}
```

#### 2. Get World Details
- **`GET /api/worlds/<world_id>`**
- **Response `200 OK`**:
```json
{
  "status": "success",
  "world": {
    "world_id": "array_forest",
    "name": "Array Forest",
    "quests": [
      { "quest_id": "array_001", "title": "The Lost Maximum", "difficulty": "beginner", "xp_reward": 100 }
    ]
  }
}
```

#### 3. Get Quest
- **`GET /api/quests/<quest_id>`**
- **Response `200 OK`** (expected answers & explanations stripped for client security):
```json
{
  "status": "success",
  "quest": {
    "quest_id": "array_001",
    "title": "The Lost Maximum",
    "world_id": "array_forest",
    "concept": "Finding the maximum value in an array",
    "difficulty": "beginner",
    "learning_objective": "Master single-pass linear traversal...",
    "xp_reward": 100,
    "stages": [
      {
        "stage_id": "understand",
        "name": "Understand the Goal",
        "type": "multiple_choice",
        "prompt": "What is the primary objective and return value of this problem?",
        "options": [ ... ],
        "max_points": 10,
        "hints_available": 2
      }
    ]
  }
}
```

#### 4. Start Quest Attempt
- **`POST /api/quests/<quest_id>/attempt`**
- **Request Body**:
```json
{
  "user_id": "user_a1b2c3d4"
}
```
- **Response `201 Created`**:
```json
{
  "status": "success",
  "message": "Quest attempt initialized successfully",
  "attempt": {
    "attempt_id": "attempt_f7e6d5c4",
    "user_id": "user_a1b2c3d4",
    "quest_id": "array_001",
    "current_stage": "understand",
    "completed_stages": [],
    "status": "in_progress",
    "started_at": "2026-09-14T14:40:00Z"
  }
}
```

#### 5. Request Progressive Hint
- **`POST /api/quests/<quest_id>/hint`**
- **Request Body**:
```json
{
  "user_id": "user_a1b2c3d4",
  "attempt_id": "attempt_f7e6d5c4",
  "stage_id": "understand"
}
```
- **Response `200 OK`**:
```json
{
  "status": "success",
  "quest_id": "array_001",
  "stage_id": "understand",
  "hint": "Review the problem objective: what value needs to be retrieved from the stones?",
  "hints_used_for_stage": 1,
  "has_more_hints": true,
  "hint_penalty_notice": "Each hint used deducts 2 points from this stage's score (min 20% floor)."
}
```

#### 6. Submit Stage Answer
- **`POST /api/quests/<quest_id>/submit`**
- **Request Body**:
```json
{
  "user_id": "user_a1b2c3d4",
  "attempt_id": "attempt_f7e6d5c4",
  "stage_id": "understand",
  "answer": 0
}
```
- **Mid-Quest Response `200 OK` (Stage 1..6)**:
```json
{
  "status": "success",
  "quest_completed": false,
  "stage_feedback": {
    "stage_id": "understand",
    "score": 8,
    "max_score": 10,
    "correctness": "correct_with_hints",
    "feedback": "The problem specifically asks to identify the single largest number in the array.",
    "next_stage": "identify"
  },
  "attempt_progress": {
    "attempt_id": "attempt_f7e6d5c4",
    "current_stage": "identify",
    "completed_stages": ["understand"],
    "stage_scores": { "understand": 8 }
  }
}
```
- **Completion Response `200 OK` (Stage 7 - `explain`)**:
```json
{
  "status": "success",
  "message": "Quest completed successfully! Mastery updated.",
  "quest_completed": true,
  "stage_feedback": { ... },
  "attempt_summary": {
    "attempt_id": "attempt_f7e6d5c4",
    "status": "completed",
    "total_score": 98,
    "percentage": 98.0,
    "xp_earned": 98,
    "completed_stages": ["understand", "identify", "decompose", "predict", "dry_run", "solve", "explain"]
  },
  "user_progress": {
    "xp": 98,
    "level": 1,
    "skills": {
      "understanding": 64,
      "concept_recognition": 65,
      "decomposition": 65,
      "prediction": 65,
      "dry_run": 65,
      "problem_solving": 65,
      "explanation": 65
    }
  },
  "recommendation": {
    "quest_id": "array_001",
    "title": "The Lost Maximum",
    "world": "array_forest"
  }
}
```

#### 7. AI Coach: Socratic Contextual Hint
- **`POST /api/ai/hint`**
- **Request Body**:
```json
{
  "user_id": "user_a1b2c3d4",
  "quest_id": "array_001",
  "stage_id": "understand",
  "hints_used": 0
}
```
- **Response `200 OK`**:
```json
{
  "status": "success",
  "message": "Focus on the end goal: what single numerical value needs to be extracted from the array?",
  "source": "fallback",
  "quest_id": "array_001",
  "stage_id": "understand",
  "hint_level": 1,
  "next_hint_available": true
}
```

#### 8. AI Coach: Contextual Concept Explanation
- **`POST /api/ai/explain`**
- **Request Body**:
```json
{
  "user_id": "user_a1b2c3d4",
  "quest_id": "array_001",
  "stage_id": "identify",
  "user_answer": "Binary search on unsorted array"
}
```
- **Response `200 OK`**:
```json
{
  "status": "success",
  "explanation": "For unsorted data, linear scan O(N) is optimal because every element must be inspected at least once.",
  "source": "fallback",
  "quest_id": "array_001",
  "stage_id": "identify"
}
```

#### 9. Create 1v1 Battle Challenge
- **`POST /api/battles`**
- **Request Body**:
```json
{
  "user_id": "user_a1b2c3d4",
  "quest_id": "array_001",
  "opponent_id": "algo_bot"
}
```
- **Response `201 Created`**:
```json
{
  "status": "success",
  "message": "Battle challenge created successfully",
  "battle": {
    "battle_id": "battle_e5f6a7b8",
    "quest_id": "array_001",
    "status": "in_progress",
    "player1": { "user_id": "user_a1b2c3d4", "name": "Alice", "submitted": false },
    "player2": { "user_id": "algo_bot", "name": "AlgoBot [AI Rival]", "submitted": true, "score": 85 }
  }
}
```

#### 10. Submit Battle Answers & Resolve Winner
- **`POST /api/battles/<battle_id>/submit`**
- **Request Body**:
```json
{
  "user_id": "user_a1b2c3d4",
  "answers": { "understand": 0, "identify": 1, "decompose": 0, "predict": 1, "dry_run": 0, "solve": 0, "explain": 0 },
  "time_taken_seconds": 12
}
```
- **Response `200 OK`**:
```json
{
  "status": "success",
  "message": "Battle answers submitted successfully",
  "performance": {
    "accuracy": 100,
    "speed_bonus": 19,
    "total_score": 119
  },
  "battle_completed": true,
  "battle": {
    "battle_id": "battle_e5f6a7b8",
    "status": "completed",
    "winner_id": "user_a1b2c3d4",
    "xp_awarded": { "player1": 50, "player2": 15 },
    "summary": "Alice claimed victory (119 vs 85)!"
  }
}
```

---

## Running Verification Suites

To run all automated verification tests:

```powershell
cd backend
# Sprint 2 tests (25 assertions)
.\venv\Scripts\python.exe tests/verify_sprint2.py

# Sprint 3 tests (45 assertions)
.\venv\Scripts\python.exe tests/verify_sprint3.py
```
**All 70 combined assertions pass with 100% success.**
