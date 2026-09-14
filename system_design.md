# Algorithmic Arcade System Architecture

_Converted from `Algorithmic_Arcade_System_Architecture.pdf`. Page order is preserved._

Algorithmic Arcade
System Architecture Document
Project: Algorithmic Arcade — A DSA Problem-Solving Adventure
Version: 1.0
Platform: Web Application
Architecture Style: Lightweight Client–Server Architecture
Primary Stack: HTML5, CSS3, JavaScript, Python + Flask, Firebase / Firestore
MVP Focus: Array Forest — The Lost Maximum

## 1. Architecture Overview

Algorithmic Arcade is designed as a lightweight web application where the frontend manages the interactive
learning experience, the Flask backend manages AI-related operations, and Firebase/Firestore stores learner
progress and multiplayer state.
The architecture intentionally avoids unnecessary infrastructure because the project is being developed within
a 24-hour hackathon.
The primary architecture is:

---

<!-- Page 2 -->

┌─────────────────────┐
│ USER │
│ Browser │
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│ FRONTEND │
│ HTML / CSS / JS │
│ │
│ • Adventure Map │
│ • Quest Engine │
│ • Prediction │
│ • Dry Run │
│ • Code Interface │
│ • Robot UI │
│ • Mastery UI │
└───────┬───────┬─────┘
│ │
AI │ │ Progress
Request │ │
▼ ▼
┌──────────────┐ ┌──────────────┐
│ Flask Backend│ │ Firebase │
│ │ │ Firestore │
│ AI Gateway │ │ │
└──────┬───────┘ │ • Users │
│ │ • Progress │
▼ │ • Quests │
┌──────────────┐ │ • Duels │
│ External AI │ └──────────────┘
│ API │
└──────────────┘

## 2. Architectural Goals

The architecture should:
Be implementable within 24 hours.
Keep the frontend lightweight.
Support the complete learning loop.
Allow reusable quest components.
Keep AI calls controlled.
Persist learner progress.
Support future Duel Mode.
•
•
•
•
•
•
•

---

<!-- Page 3 -->

Avoid unnecessary backend complexity.
Allow additional DSA regions to be added later.
Keep the core learning experience functional even if optional services fail.

## 3. Architectural Principles

3.1 Lightweight First
The MVP does not require a large distributed backend. A simple:
Browser → Flask → AI API
architecture is sufficient for AI functionality.
3.2 Frontend-Driven Learning Experience
Most interactions are deterministic and should be handled on the client. Examples:
prediction validation
dry-run progression
quest navigation
XP calculation
local quest state
UI feedback
This reduces backend dependency.
3.3 Backend as a Controlled AI Gateway
The frontend should not directly expose AI API credentials. Instead:
Frontend
│
│ AI Request
▼
Flask
│
│ Authenticated API Request
▼
AI Provider
•
•
•
•
•
•
•
•
•

---

<!-- Page 4 -->

The Flask server acts as the controlled gateway.
3.4 Database for Persistent State
Firebase/Firestore is responsible for persistent application data such as:
user progress
quest completion
mastery
scores
Duel Mode state
3.5 Content-Driven Quest Architecture
Quest content should be stored separately from the core quest engine. Instead of hardcoding every quest into
the interface:
Quest Engine + Quest Data
This allows new quests to be added without rebuilding the entire application.

## 4. High-Level Architecture

The system can be divided into five major layers:
┌─────────────────────────────────────────────┐
│ PRESENTATION │
│ HTML / CSS / JavaScript │
├─────────────────────────────────────────────┤
│ APPLICATION LOGIC │
│ Quest Engine / Mastery / Progress │
├─────────────────────────────────────────────┤
│ DATA / CONTENT │
│ JSON / JS Quest Data │
├─────────────────────────────────────────────┤
│ BACKEND SERVICES │
│ Flask │
├─────────────────────────────────────────────┤
│ EXTERNAL / CLOUD │
│ Firebase + External AI API │
└─────────────────────────────────────────────┘
•
•
•
•
•

---

<!-- Page 5 -->

## 5. Major System Components

5.1 Frontend
The frontend is responsible for the learner-facing experience.
Responsibilities
rendering screens
navigation
quest progression
prediction interactions
dry-run visualization
code interface
Robot interaction
progress display
mastery display
Duel UI

## 6. Frontend Architecture

The frontend can be logically divided into:
•
•
•
•
•
•
•
•
•
•

---

<!-- Page 6 -->

Frontend
│
├── App Shell
│
├── Navigation
│
├── Adventure Map
│
├── Region System
│
├── Quest Engine
│ ├── Understanding
│ ├── Decomposition
│ ├── Prediction
│ ├── Dry Run
│ ├── Coding
│ ├── Explanation
│ └── Review
│
├── Robot Companion
│
├── Mastery System
│
├── Progress System
│
└── Duel Mode

## 7. Quest Engine

The Quest Engine is the core application component. Its responsibility is to control the learner's current
position within a quest. Conceptually:
Quest Engine
│
├── currentQuest
├── currentStage
├── attempts
├── hints
├── predictions
├── dryRunState
├── codeState
└── completionState
The engine determines what the learner should see at each stage.

---

<!-- Page 7 -->

## 8. Quest State Machine

Each quest operates as a state machine.
┌─────────────┐
│ START │
└──────┬──────┘
▼
┌─────────────┐
│ UNDERSTAND │
└──────┬──────┘
▼
┌─────────────┐
│ DECOMPOSE │
└──────┬──────┘
▼
┌─────────────┐
│ PREDICT │
└──────┬──────┘
▼
┌─────────────┐
│ DRY RUN │
└──────┬──────┘
▼
┌─────────────┐
│ SOLVE │
└──────┬──────┘
▼
┌─────────────┐
│ EXPLAIN │
└──────┬──────┘
▼
┌─────────────┐
│ REVIEW │
└──────┬──────┘
▼
┌─────────────┐
│ COMPLETE │
└─────────────┘
The learner should not normally skip stages during the initial learning experience.

## 9. Quest Content Architecture

Quest content should be represented as structured data. Conceptually:

---

<!-- Page 8 -->

Quest
│
├── id
├── title
├── region
├── difficulty
├── description
├── problem
├── simplifiedProblem
├── concepts
├── decompositionSteps
├── predictionSteps
├── dryRunStates
├── testCases
├── hints
└── masteryRules
Example conceptual structure:
Lost Maximum
│
├── Problem
│
├── Objective
│
├── Array
│
├── Expected Result
│
├── Decomposition
│
├── Prediction
│
├── Dry Run
│
├── Coding Tests
│
└── Hint Ladder
This allows the same Quest Engine to run different problems.

## 10. Problem Understanding Architecture

The problem-understanding component contains two sources of information:

---

<!-- Page 9 -->

Original Problem
│
├───────────────┐
│ │
▼ ▼
Original Text AI Simplifier
│
▼
Beginner Explanation
The AI simplifier should be optional. If the AI service is unavailable, the quest should still contain a predefined
explanation for the MVP quest.

## 11. AI Architecture

AI functionality should be routed through Flask.
FRONTEND
│
│ POST /api/ai/\*
▼
┌──────────────┐
│ Flask Server │
└──────┬───────┘
│
Prompt Construction
│
▼
External AI API
│
▼
Structured Response
│
▼
FRONTEND
The AI layer should support two primary MVP operations:
Problem Simplification
Progressive Hints

1.
2.

---

<!-- Page 10 -->

## 12. AI API Responsibilities

Possible backend endpoints:
POST /api/ai/simplify
POST /api/ai/hint
/api/ai/simplify
Input: _ problem _ difficulty _ learnerLevel
Output: _ simplifiedExplanation _ importantTerms
/api/ai/hint
Input: _ problem _ currentStage _ hintLevel _ learnerState
Output: _ hint
The backend should not expose the AI provider's credentials to the browser.

## 13. AI Hint Architecture

The hint system should maintain a controlled ladder.
Learner requests help
│
▼
Current Hint Level
│
▼
┌─────────────────────┐
│ Level 1 — Nudge │
└─────────┬───────────┘
│
▼
┌─────────────────────┐
│ Level 2 — Direction │
└─────────┬───────────┘
│
▼
┌─────────────────────┐
│ Level 3 — Structure │
└─────────────────────┘
•
•

---

<!-- Page 11 -->

The frontend tracks the hint level. The backend/AI should receive the current level and generate only an
appropriately scoped response.

## 14. AI Safety / Learning Guardrails

The system should prevent the Robot from immediately solving the problem. The prompt structure should
communicate:
You are a DSA learning coach.
Current learner stage: Prediction Current hint level: 1
Do: - guide the learner - simplify terminology - ask a useful question
Do not: - provide the final code - reveal the complete algorithm - skip the learner's current reasoning
step
These guardrails protect the core learning objective.

## 15. Prediction Engine

Prediction is handled primarily on the frontend.
Flow:

---

<!-- Page 12 -->

Quest Data
│
▼
Prediction State
│
▼
Learner Input
│
▼
Validation
│
┌──┴───────┐
│ │
Correct Wrong
│ │
▼ ▼
Reward Feedback
The engine records: _ prediction value _ expected value _ correctness _ attempts \* prediction accuracy

## 16. Dry-Run Engine

The Dry-Run Engine maintains a sequence of algorithm states. For example:
Input Array:
[4, 9, 2, 7]
States:
Step 1
current = 4
max = 4
Step 2
current = 9
max = 9
Step 3
current = 2
max = 9
Step 4
current = 7
max = 9

---

<!-- Page 13 -->

The interface exposes one state at a time. The engine controls: _ current index _ current value _ tracked
variables _ expected state _ learner prediction _ completion

## 17. Coding Architecture

The coding stage should receive the problem and relevant context from the quest.
Quest
│
├── Problem
├── Constraints
├── Examples
└── Test Cases
│
▼
Code Interface
│
▼
User Code
│
▼
Controlled Execution
│
▼
Test Results
The exact code execution implementation is intentionally kept as an implementation decision within the MVP
because the source architecture documents do not specify a particular execution engine. The architecture
should therefore avoid making a custom sandbox a dependency for the core product.

## 18. Test Case Architecture

A quest should contain:
Test Cases
│
├── Normal Case
├── Edge Case
└── Additional Case

---

<!-- Page 14 -->

The learner should first solve the normal case and then verify their reasoning against an edge case. This
reinforces transfer rather than memorization.

## 19. Mastery Engine

The Mastery Engine converts learner activity into measurable progress.
Inputs: _ Prediction Accuracy _ Dry Run Performance _ Coding Result _ Time Taken _ Hints Used _ Attempts \*
Explanation
Conceptual flow:
Learner Activity
│
▼
Performance Data
│
▼
Mastery Engine
│
├── Prediction
├── Dry Run
├── Coding
├── Independence
└── Speed
│
▼
Mastery Result

## 20. Mastery Calculation

A conceptual mastery model can be:
Mastery =
Prediction Performance

- Dry Run Performance
- Coding Performance
- Independence
- Explanation

---

<!-- Page 15 -->

The exact numerical weighting can be tuned during implementation. The important architectural principle is
that mastery should not depend solely on accepted code.

## 21. Progress Architecture

Progress is stored in Firebase/Firestore. Conceptually:
User
│
└── Progress
│
├── Regions
│ └── Array Forest
│
├── Quests
│ └── Lost Maximum
│
└── Mastery
Quest progress can contain: _ questId _ status _ predictionAccuracy _ dryRunAccuracy _ codingStatus _
hintsUsed _ attempts _ timeTaken _ score _ mastery \* completedAt

## 22. Firebase / Firestore Architecture

The database can be structured conceptually as:
users/
{userId}/
profile
progress/
quests/
{questId}
mastery/
{skillId}
duels/
{duelId}

---

<!-- Page 16 -->

The exact Firestore collection structure can be simplified during implementation if required by hackathon time.

## 23. User Authentication

Authentication is not the central learning feature. Possible MVP approaches include: _ lightweight Firebase
authentication _ anonymous authentication \* minimal user identity for demo purposes
The architecture should avoid spending significant hackathon time on complex authentication flows.

## 24. Duel Mode Architecture

Duel Mode is an optional P1 component. It uses Firestore to synchronize shared progress.
Player A
│
▼
Firebase
▲
│
Player B
Each player's state may contain: _ playerId _ progress _ accuracy _ hintsUsed _ time _ score _ status
The shared Duel document can contain: _ duelId _ questId _ playerA _ playerB _ status _ startTime _ result

---

<!-- Page 17 -->

## 25. Duel Data Flow

Player A completes stage
│
▼
Firestore
│
▼
Shared Duel State
│
▼
Player B UI
This allows the progress bar to update without building a complex real-time game server.

## 26. Data Flow — Normal Quest

The normal quest flow is:
User
│
▼
Frontend
│
├── Load Quest Data
│
▼
Quest Engine
│
├── Understand
├── Decompose
├── Predict
├── Dry Run
├── Solve
├── Explain
└── Review
│
▼
Mastery Engine
│
▼
Firestore
│
▼
Progress Saved

---

<!-- Page 18 -->

## 27. Data Flow — AI Simplification

User clicks "Simplify"
│
▼
Frontend
│
│ Problem
▼
Flask `/api/ai/simplify`
│
▼
External AI API
│
▼
Simplified Explanation
│
▼
Frontend
│
▼
Problem Understanding UI

---

<!-- Page 19 -->

## 28. Data Flow — Hint Request

User clicks Hint
│
▼
Current Quest State
│
▼
Current Hint Level
│
▼
Flask
│
▼
AI API
│
▼
Hint
│
▼
Robot Companion
│
▼
User

## 29. Data Flow — Quest Completion

Quest Activity
│
▼
Performance Metrics
│
▼
Mastery Engine
│
├── Score
├── Mastery
├── XP
└── Skill Progress
│
▼
Firestore
│
▼
Completion Screen

---

<!-- Page 20 -->

## 30. Failure Handling

The architecture should prevent optional services from breaking the learning experience.
AI Failure
If the AI API fails:
AI Request
│
▼
Failure
│
▼
Predefined Hint / Explanation
The user should see:
"Robot is temporarily unavailable. Try the built-in hint."
Firebase Failure
The frontend can maintain temporary local state during the active quest.
Active Quest
│
▼
Local State
│
├── Firebase available → Save
│
└── Firebase unavailable → Temporary state
Code Execution Failure
Display a controlled error message instead of terminating the quest.

---

<!-- Page 21 -->

## 31. Security Architecture

The main security considerations are:
API Keys: AI credentials must remain on the Flask server.
Firebase Rules: Firestore security rules should restrict users from modifying arbitrary users' progress.
Input Validation: Flask should validate AI requests before forwarding them.
Prompt Control: The backend should restrict AI behavior to the intended learning functions.
Client Trust: Important persistent data should not rely solely on client-provided values where integrity
matters.

## 32. Performance Architecture

The application is intentionally lightweight. Performance principles:
minimize unnecessary backend calls
load quest content locally where practical
reuse UI components
avoid large animation assets
make AI calls only when requested
avoid unnecessary database writes
AI calls should be single-shot and constrained wherever possible.

## 33. Project Structure

A practical project structure is:
•
•
•
•
•
•
•
•
•
•
•

---

<!-- Page 22 -->

algorithmic-arcade/
│
├── frontend/
│ │
│ ├── index.html
│ ├── css/
│ │ ├── style.css
│ │ └── components.css
│ │
│ ├── js/
│ │ ├── app.js
│ │ ├── questEngine.js
│ │ ├── prediction.js
│ │ ├── dryRun.js
│ │ ├── mastery.js
│ │ ├── firebase.js
│ │ └── ui.js
│ │
│ ├── data/
│ │ └── quests.json
│ │
│ └── assets/
│ ├── images/
│ └── icons/
│
├── backend/
│ │
│ ├── app.py
│ ├── routes/
│ │ └── ai.py
│ ├── services/
│ │ └── ai_service.py
│ └── config.py
│
├── README.md
├── requirements.txt
└── .gitignore
The final structure can be simplified further if required by the team's implementation style.

---

<!-- Page 23 -->

## 34. Module Responsibilities

Module Responsibility
app.js Application initialization
questEngine.js Quest state and progression
prediction.js Prediction validation
dryRun.js Dry-run state management
mastery.js Performance/mastery calculation
firebase.js Database interaction
ui.js Shared UI functions
quests.json Quest content
app.py Flask application
ai.py AI endpoints
ai_service.py AI provider interaction
config.py Backend configuration

## 35. API Architecture

The minimum backend API can be:
/api/ai/simplify
/api/ai/hint
Optional future APIs: _ /api/quests _ /api/progress _ /api/duels _ /api/tracker
However, the MVP should avoid creating endpoints that are unnecessary for the actual demo.
•
•

---

<!-- Page 24 -->

## 36. Example AI Request

Conceptual request:
POST /api/ai/hint
Request:
{
"problem": "...",
"stage": "PREDICT",
"hintLevel": 1
}
Response:
{
"hint": "Think about the value you need to keep track of."
}
The exact request/response format can be adjusted during implementation.

## 37. Architecture for Future DSA Regions

The architecture should allow new regions without changing the core Quest Engine.
Quest Engine
│
├── Array Forest
│
├── String City
│
├── Stack Castle
│
├── Linked List Bridge
│
├── Recursion Mountain
│
└── Algorithm Kingdom

---

<!-- Page 25 -->

Each region provides quest data while the engine provides the common learning mechanics.

## 38. External Platform Tracker

The research proposes a future multi-platform tracker for platforms such as: _ LeetCode _ GeeksforGeeks _
CodeChef _ HackerRank
This should not be a dependency of the MVP. Future architecture:
External Platforms
│
├── LeetCode Connector
├── GFG Connector
├── CodeChef Connector
└── HackerRank Connector
│
▼
Normalization Layer
│
▼
User Profile
│
▼
Recommendation Engine
For the hackathon, seeded/demo data can represent this concept.

## 39. Deployment Architecture

The expected deployment is lightweight:

---

<!-- Page 26 -->

INTERNET
│
┌──────────┴──────────┐
│ │
▼ ▼
Frontend Host Flask Host
│ │
│ ▼
│ External AI
│
▼
Browser
│
└──────────────┐
▼
Firebase
The exact hosting provider is not mandated by the architecture. 40. 24-Hour Architecture Priorities
Hours 0–2
repository setup
frontend structure
Flask setup
Firebase setup
define quest data model
Hours 2–5
application shell
adventure map
Array Forest
quest navigation
Hours 5–10
Quest Engine
Lost Maximum
understanding stage
•
•
•
•
•
•
•
•
•
•
•
•

---

<!-- Page 27 -->

decomposition stage
Hours 10–14
prediction engine
dry-run engine
state visualization
Hours 14–17
Robot UI
hint ladder
mastery
progress
Hours 17–19
coding stage
boss/second quest if feasible
optional Duel
Hours 19–21
integration
testing
failure handling
Hours 21–23
deployment
demo preparation
screenshots
backup
Hours 23–24
final testing
pitch rehearsal
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•
•

---

<!-- Page 28 -->

## 41. Architecture Risk Analysis

Risk Impact Mitigation
AI API failure High Built-in hints/fallback content
Firebase configuration issues Medium Local active-session state
Coding execution complexity High Use controlled existing approach
Too much backend work High Keep Flask focused on AI
Large content scope High One polished quest
Excessive animation Medium State-table interaction
AI reveals solution High Hint-level guardrails
Deployment failure High Early deployment
Duel complexity Medium Keep as P1

## 42. Architecture Trade-Offs

Why not a large backend? Because most MVP interactions are client-side and a complex backend
increases development time.
Why Flask? The project already specifies Python/Flask for AI calls, making it a simple AI gateway.
Why Firebase? It provides a lightweight persistence layer and supports the planned Duel
synchronization.
Why JSON quest content? It separates educational content from application logic and makes adding
quests easier.
Why not live external integrations? They add reliability and API-policy risk without contributing to the
core demo.
•
•
•
•
•

---

<!-- Page 29 -->

## 43. MVP Architecture Boundary

The following components are inside the core MVP: _ ✓ Frontend _ ✓ Quest Engine _ ✓ Array Forest _ ✓
Lost Maximum _ ✓ Prediction _ ✓ Dry Run _ ✓ Robot Hint Ladder _ ✓ AI Simplifier _ ✓ Basic Coding _ ✓
Mastery _ ✓ Firebase Progress
The following are outside the core MVP: _ ○ Multiple DSA regions _ ○ Large question bank _ ○ Four live
external integrations _ ○ Advanced algorithm animation _ ○ Complex multiplayer infrastructure \* ○ Full
recommendation engine

## 44. Architecture Acceptance Criteria

The architecture is considered implementation-ready when:
Frontend
application loads successfully
Adventure Map is accessible
Array Forest is accessible
quest state can progress
Quest Engine
stages execute in the intended order
learner state persists during the quest
incorrect actions produce feedback
Prediction
answers can be validated
accuracy can be recorded
Dry Run
states can be displayed sequentially
learner can move between states
AI
simplification endpoint works
•
•
•
•
•
•
•
•
•
•
•
•

---

<!-- Page 30 -->

hint endpoint works
API credentials remain server-side
fallback exists
Database
user progress can be saved
quest completion can be retrieved
Mastery
performance data produces a result
completion screen displays meaningful metrics
Reliability
AI failure does not destroy the quest
database failure does not immediately destroy active progress

## 45. Complete Architecture

The complete MVP architecture can be represented as:
•
•
•
•
•
•
•
•
•

---

<!-- Page 31 -->

USER
│
▼
┌───────────────────┐
│ BROWSER │
│ │
│ HTML / CSS / JS │
└─────────┬─────────┘
│
┌──────┴───────┐
│ │
▼ ▼
Quest Engine Firebase
│ │
┌────────────┼────────────┐ │
│ │ │ │
▼ ▼ ▼ │
Prediction Dry Run Mastery
│ │ │
└────────────┼────────────┘
│
▼
Robot Companion
│
│ AI Request
▼
┌─────────────┐
│ Flask │
│ AI Gateway │
└──────┬──────┘
│
▼
┌─────────────┐
│ External AI │
│ API │
└─────────────┘

## 46. Final Architectural Principle

The architecture exists to support one central product principle:
The system should teach the learner how to think before it helps them write code.
Therefore:

---

<!-- Page 32 -->

Architecture
↓
Quest Engine
↓
Learning Loop
↓
Understand
↓
Decompose
↓
Predict
↓
Dry Run
↓
Solve
↓
Explain
↓
Review
↓
Mastery
The most important architectural component is consequently not the AI service, database, or game layer. It is
the Quest Engine + Learning State Model, because that is what converts Algorithmic Arcade from a normal
coding-practice website into a structured problem-solving learning system.

## 47. Final Architecture Statement

Algorithmic Arcade uses a lightweight client–server architecture in which the browser manages the interactive
learning journey, Flask provides a controlled gateway to AI capabilities, and Firebase/Firestore provides
persistent progress and optional multiplayer synchronization.
The architecture is deliberately optimized for the 24-hour hackathon:
Simple infrastructure + reusable quest engine + measurable learning interactions + controlled AI +
persistent progress
The MVP is therefore capable of demonstrating the complete product thesis through one polished vertical
slice:

---

<!-- Page 33 -->

Array Forest → The Lost Maximum → Understand → Decompose → Predict → Dry Run → Solve →
Explain → Review → Mastery
This architecture can later scale into multiple DSA regions, richer visualizations, multiplayer challenges, and
external coding-platform tracking without requiring the fundamental learning engine to be redesigned.
