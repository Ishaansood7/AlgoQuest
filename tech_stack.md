# Algorithmic Arcade TechStack Document

_Converted from `Algorithmic_Arcade_TechStack_Document.pdf`. Page order is preserved._

Algorithmic Arcade
Technical Stack & Architecture Document
Project: Algorithmic Arcade — A DSA Problem-Solving Adventure
Version: 1.0
Date: September 2026
Target: Hackathon MVP
Constraint: 24 Hours / Team of 4

## 1. Technical Overview

Algorithmic Arcade is a web-based gamified DSA learning platform designed around an interactive reasoning
loop:
Understand → Decompose → Predict → Dry Run → Solve → Explain → Review
The technical architecture is intentionally lightweight.
The MVP should prioritize:
rapid development,
reliable interactions,
simple deployment,
persistent learner progress,
controlled AI usage,
reusable quest components,
and minimal infrastructure complexity.
The architecture consists of four major layers:
•
•
•
•
•
•
•

---

<!-- Page 2 -->

┌──────────────────────────────────────────────┐
│ USER / BROWSER │
└──────────────────────┬───────────────────────┘
│
▼
┌──────────────────────────────────────────────┐
│ FRONTEND APPLICATION │
│ HTML + CSS + JavaScript │
│ │
│ World │ Quest │ Prediction │ Dry Run │ Code │
└──────────────────────┬───────────────────────┘
│
┌────────┴────────┐
▼ ▼
┌─────────────────────┐ ┌─────────────────────┐
│ FIREBASE │ │ PYTHON FLASK │
│ │ │ │
│ Progress / Database │ │ AI API Integration │
│ Authentication │ │ Simplification │
│ Duel Synchronization│ │ Hint Generation │
└─────────────────────┘ └──────────┬──────────┘
│
▼
┌─────────────────┐
│ AI SERVICE │
└─────────────────┘

---

<!-- Page 3 -->

## 2. Technology Stack

Layer Technology Purpose
Frontend HTML5 Application structure
Styling CSS3 UI, responsive layouts, game-world styling
Frontend Logic JavaScript Quest engine, interactions, state
management
Backend Python Server-side logic
Backend
Framework Flask API layer and AI integration
Database Firebase User progress and application data
Real-time DatabaseFirestore Duel Mode synchronization
AI External AI API Problem simplification and staged hints
Quest Content JSON / JavaScript Objects Quest definitions and content
Code Execution MVP-controlled execution
approach Evaluate learner submissions
Hosting Lightweight web hosting Deployment of frontend/backend
Version Control Git + GitHub Source control and collaboration
The hackathon problem statement explicitly identifies HTML, CSS, JavaScript, Python/Flask, and Firebase
as the intended technical direction.

---

<!-- Page 4 -->

## 3. Frontend

3.1 HTML5
HTML will provide the structural foundation of the application.
Responsibilities
Landing page.
World map.
Region/quest screens.
Problem statement.
Problem simplifier interface.
Prediction interface.
Dry-run table.
Coding interface.
Explanation input.
Mastery screen.
Robot dialogue interface.

## 4. CSS3

CSS will control the visual identity of Algorithmic Arcade.
Responsibilities
Game-world interface.
Quest cards.
Buttons.
Progress bars.
Cards and panels.
State tables.
Robot companion UI.
Success/failure states.
Responsive layouts.
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

<!-- Page 5 -->

Animations and transitions where useful.
Design Principle
The interface should feel like an adventure game while remaining easy enough for a beginner to understand.
Visual complexity should not interfere with the learning process.

## 5. JavaScript

JavaScript is the primary client-side application logic.
It will handle:
navigation,
quest progression,
prediction interactions,
dry-run state,
coding challenge interactions,
test cases,
hint progression,
mastery calculations,
UI state,
Firebase communication,
and optional Duel Mode interactions.

## 6. Quest Engine

The quest engine is one of the most important architectural components.
Instead of hardcoding every quest separately, quests should follow a reusable structure.
Conceptually:
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

<!-- Page 6 -->

Quest
│
├── Metadata
│ ├── id
│ ├── title
│ ├── region
│ └── difficulty
│
├── Problem
│ ├── statement
│ ├── simplifiedStatement
│ └── vocabulary
│
├── Decomposition
│ └── prompts
│
├── Prediction
│ └── states
│
├── Dry Run
│ └── executionStates
│
├── Coding
│ ├── starterCode
│ ├── testCases
│ └── edgeCases
│
├── Explanation
│ └── prompt
│
└── Mastery
└── scoringRules
This allows a second or third quest to reuse the same application engine.
The research recommends representing quest content as JSON or JavaScript objects because this makes
content easier to author and debug.

## 7. Quest Content Format

A simplified quest object may conceptually look like:

---

<!-- Page 7 -->

quest
├── id
├── title
├── region
├── difficulty
├── problem
├── simplifiedProblem
├── decomposition
├── predictionStates
├── dryRunStates
├── codingChallenge
├── testCases
├── edgeCases
├── explanationPrompt
└── masteryRules
The actual implementation format can be JSON or JavaScript objects.

## 8. Prediction Engine

The Prediction Engine is a core product differentiator.
It should allow the learner to predict the next state before the system reveals it.
Example
Current State
i = 1
max = 5
current = 7
Question:
What will max become?
○ 5
○ 7
○ 3
○ I don't know
After submission:

---

<!-- Page 8 -->

Your Prediction: 7
Correct State: 7
✓ Correct Prediction
The system then records the result.
Data Recorded
prediction attempt,
expected value,
learner response,
correctness,
timestamp,
prediction accuracy.

## 9. Dry-Run Engine

The dry-run system represents algorithm execution as explicit states.
Example:
Step 0
i = 0
current = 5
max = 5
↓
Step 1
i = 1
current = 7
max = 7
↓
Step 2
i = 2
current = 3
max = 7
The research specifically recommends reusable visualization components with explicit state rather than
relying on complex animation.
•
•
•
•
•
•

---

<!-- Page 9 -->

## 10. Robot Companion

The Robot Companion is the AI-assisted coaching interface.
Its responsibilities include:
simplifying terminology,
giving hints,
guiding the learner,
explaining mistakes,
recommending prerequisite learning,
providing quest feedback.
The robot must not become an unrestricted answer generator.

## 11. Hint Architecture

The hint system should follow a controlled ladder.
Learner Gets Stuck
│
▼
Level 1 — Nudge
│
▼
Level 2 — Direction
│
▼
Level 3 — Structure
│
▼
Level 4 — Explanation
│
▼
Level 5 — Full Solution
For the hackathon MVP:
Levels 1–3 are required.
•
•
•
•
•
•

---

<!-- Page 10 -->

The problem statement explicitly defines the MVP robot ladder as:
nudge → direction → structure.

## 12. Backend

Python + Flask
Flask will act as the lightweight backend API.
Primary Responsibilities
Receive AI requests.
Send constrained prompts to the AI service.
Return AI-generated simplifications.
Return staged hints.
Keep AI credentials away from the browser.
Provide a simple API boundary between frontend and AI services.
Example API Structure
POST /api/simplify
POST /api/hint
POST /api/explain
GET /api/health
The exact endpoint set may be reduced during the hackathon depending on implementation needs.

## 13. AI Integration

AI should be treated as a supporting service.

1.
2.
3.
4.
5.
6.

---

<!-- Page 11 -->

AI Features
Problem Simplification
Input:
Original problem
Output:
Simplified explanation
Hint Generation
Input:
Problem
Current learning stage
Learner state
Hint level
Output:
Controlled hint
The source problem statement specifies constrained single-shot AI calls for simplification and staged hints.

## 14. AI Safety / Learning Guardrails

The AI must not immediately provide the complete solution.
Required behavior
For Hint Level 1:
Give a conceptual nudge.
Do not provide an algorithm.
Do not provide code.
For Hint Level 2:

---

<!-- Page 12 -->

Suggest a direction.
Do not provide complete implementation.
For Hint Level 3:
Provide structural guidance.
Still avoid complete code.
This preserves the reasoning-first philosophy.

## 15. Firebase

Firebase will provide persistent application data.
Responsibilities
User progress.
Quest completion.
Mastery data.
Session statistics.
Duel Mode synchronization.
The hackathon problem statement explicitly identifies Firebase for progress storage and real-time Duel Mode
synchronization.

## 16. Firestore Data Structure

A conceptual structure:
•
•
•
•
•

---

<!-- Page 13 -->

users/
{userId}/
profile
progress
quests/
{questId}
status
timeTaken
predictionAccuracy
hintsUsed
codingResult
mastery
sessions/
{sessionId}
startedAt
completedAt
score
Duel Mode can maintain a separate challenge document.
duels/
{duelId}
player1
player2
progress1
progress2
score1
score2
status
This is a conceptual schema; exact Firebase structure can be simplified for the MVP.

## 17. Authentication

Authentication is not the central learning feature.
For the hackathon MVP, authentication should remain lightweight.
Possible implementation:
Firebase Authentication.
Anonymous authentication.
Simple email-based authentication.
•
•
•

---

<!-- Page 14 -->

The exact authentication method is an implementation decision and is not specified in the source documents.
If authentication threatens the 24-hour MVP timeline, the team should prioritize the learning experience and
progress persistence over complex account functionality.

## 18. Coding Execution

The learner must eventually submit code and test it.
The PRD requires:
normal test case,
edge case,
coding result.
However, the provided source documents do not specify a particular code-execution technology or sandbox
architecture.
Therefore, this component should be treated as an implementation decision.
Hackathon Recommendation
Use a controlled execution approach appropriate to the chosen supported language.
Avoid building a custom code-execution sandbox from scratch during the 24-hour hackathon.

## 19. Duel Mode Architecture

Duel Mode is a P1 feature.
Concept:
•
•
•

---

<!-- Page 15 -->

Player A
│
▼
Quest Progress ───────┐
│
▼
Firestore
▲
│
Quest Progress ───────┘
▲
│
Player B
Firestore synchronizes:
progress,
player status,
score,
completion state.
Proposed scoring
Score =
Speed

- Accuracy

* Hints
  This scoring model is explicitly proposed in the problem statement.

## 20. Mastery Engine

The Mastery Engine converts learning behavior into progress.
Inputs:
•
•
•
•

---

<!-- Page 16 -->

Prediction Accuracy
Hints Used
Coding Result
Completion
Time Taken
Output:
Mastery Score
The exact scoring formula should be kept configurable rather than hardcoded throughout the application.

## 21. Example Mastery Object

mastery
├── predictionAccuracy
├── hintsUsed
├── codingPassed
├── edgeCasePassed
├── timeTaken
└── masteryScore
This makes the mastery system reusable across quests.

## 22. Recommended Application Structure

A simple project structure:

---

<!-- Page 17 -->

algorithmic-arcade/
│
├── frontend/
│ ├── index.html
│ ├── css/
│ │ ├── style.css
│ │ └── responsive.css
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
│ └── assets/
│ ├── robot/
│ ├── regions/
│ └── icons/
│
├── backend/
│ ├── app.py
│ ├── routes/
│ │ ├── simplify.py
│ │ └── hints.py
│ │
│ ├── services/
│ │ └── ai_service.py
│ │
│ └── config.py
│
├── data/
│ ├── quests/
│ │ ├── lost_maximum.json
│ │ └── quest_02.json
│ │
│ └── dry-runs/
│
├── README.md
└── .gitignore
This structure is intentionally simple enough for rapid hackathon development.

---

<!-- Page 18 -->

## 23. Data Flow — Complete Quest

Learner
│
▼
Select Quest
│
▼
Load Quest Data
│
▼
Problem Statement
│
▼
AI Simplifier
│
▼
Problem Understanding
│
▼
Decomposition
│
▼
Prediction Engine
│
▼
Dry-Run Engine
│
▼
Coding Challenge
│
▼
Test Cases
│
▼
Explanation
│
▼
Mastery Engine
│
▼
Firebase
│
▼
Progress Screen

---

<!-- Page 19 -->

## 24. Frontend State Management

The application should maintain a central quest state.
Conceptually:
questState
│
├── currentQuest
├── currentStep
├── predictionResults
├── dryRunProgress
├── hintsUsed
├── codingStatus
├── explanation
├── startTime
└── mastery
Possible quest states:
PROBLEM
↓
SIMPLIFY
↓
DECOMPOSE
↓
PREDICT
↓
DRY_RUN
↓
CODE
↓
EXPLAIN
↓
REVIEW
↓
COMPLETE

## 25. Performance Requirements

The MVP should feel responsive on normal laptops.

---

<!-- Page 20 -->

Requirements
Quest transitions should be fast.
Local interactions should not require unnecessary API requests.
Prediction and dry-run interactions should execute locally where possible.
Firebase writes should be limited to meaningful progress events.
AI calls should occur only when needed.

## 26. Reliability Requirements

The core quest should remain functional if optional services fail.
If AI fails
The system should use predefined fallback:
simplification,
hints.
If Firebase temporarily fails
The current session should continue locally where practical and synchronize later if implementation permits.
If external integrations fail
The core learning experience must remain unaffected.
This follows the research recommendation that the core product should remain useful even when external
platform integrations are unavailable.

## 27. Security Considerations

For the MVP:
API keys must never be exposed in frontend JavaScript.
AI requests should go through Flask.
Firebase credentials/configuration should follow the platform's recommended client configuration.
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

<!-- Page 21 -->

User data should not be unnecessarily collected.
AI prompts should avoid sending unnecessary personal information.
The project should not build unnecessary security infrastructure during the hackathon.

## 28. Deployment Architecture

Recommended conceptual deployment:
INTERNET
│
┌──────────┴──────────┐
│ │
▼ ▼
Frontend Hosting Flask Backend
│ │
│ ▼
│ AI Service
│
▼
Firebase
│
▼
Firestore
The exact hosting provider is not specified in the source documents and can be selected based on the team's
existing familiarity.

## 29. Technology Selection Rationale

HTML/CSS/JavaScript
Chosen because the team can rapidly build and demonstrate a browser-based interactive experience without
introducing a large framework dependency.
Python/Flask
Chosen for a lightweight backend and straightforward AI API integration.
•
•

---

<!-- Page 22 -->

Firebase
Chosen for rapid implementation of:
persistence,
user progress,
and real-time synchronization.
JSON / JavaScript Objects
Chosen for rapid quest authoring and reusable content.
AI API
Used selectively for capabilities where natural-language adaptation is useful.
The source research similarly recommends a simple frontend, minimal backend, simple hosted database,
reusable visualization components, and constrained AI rather than overbuilding infrastructure.

## 30. Technology Priorities for 24-Hour MVP

Must Work
Frontend
↓
Quest Engine
↓
Prediction
↓
Dry Run
↓
Coding
↓
Mastery
↓
Firebase
•
•
•

---

<!-- Page 23 -->

Should Work
Frontend
↓
Flask
↓
AI Simplifier
↓
Robot Hints
Optional
Firestore
↓
Duel Mode
Future
External Coding Platforms
↓
Progress Normalization
↓
Personalized Recommendations

---

<!-- Page 24 -->

## 31. MVP Technical Priority Matrix

Component Priority Reason
HTML/CSS/JS frontend P0 Core application
Quest engine P0 Core learning system
Prediction engine P0 Major differentiator
Dry-run engine P0 Major learner pain point
Mastery engine P0 Progress measurement
Firebase P0 Progress persistence
Flask backend P0 AI integration
AI simplifier P0 Beginner assistance
Robot hints P0 Guided learning
Coding execution P0 Complete quest
Second quest P1 Content expansion
Duel Mode P1 Competition
Boss challenge P2 Advanced challenge
External integrations P2 Future roadmap
Large question bank P2 Future scale

---

<!-- Page 25 -->

## 32. Technical Risks

Risk — Over-engineering
Solution: Keep the backend minimal.
Risk — AI latency
Solution: Use AI only for simplification/hints and provide fallback content.
Risk — Firebase complexity
Solution: Use a simple schema and write only required progress data.
Risk — Coding execution complexity
Solution: Use an existing controlled execution approach rather than building a custom sandbox.
Risk — UI consumes development time
Solution: Build the complete learning loop before polishing visual details.
Risk — Too many features
Solution: Freeze P0 features early.

## 33. Definition of Technical Completion

The MVP is technically complete when:
The application loads successfully.
A learner can enter Array Forest.
The learner can start The Lost Maximum.
Quest data loads correctly.
Problem simplification works or has a fallback.
Decomposition can be completed.
•
•
•
•
•
•

---

<!-- Page 26 -->

Prediction can be submitted and evaluated.
Dry-run states can be traversed.
Hints can be requested progressively.
Code can be tested.
Normal and edge cases can be evaluated.
Explanation can be submitted.
Mastery statistics are calculated.
Progress is saved to Firebase.
The final mastery screen is displayed.

## 34. Recommended Build Order

The implementation order should be:

## 1. Application Shell

↓

## 2. Array Forest

↓

## 3. Quest Engine

↓

## 4. The Lost Maximum

↓

## 5. Prediction

↓

## 6. Dry Run

↓

## 7. Coding

↓

## 8. Mastery

↓

## 9. Firebase

↓

## 10. Robot Hints

↓

## 11. AI Simplifier

↓

## 12. Second Quest

↓

## 13. Duel Mode

This follows the research recommendation to build:
Array Forest → one excellent quest → prediction → dry run → robot hints → mastery → boss/tracker.
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

## 35. Final Technical Architecture Decision

Algorithmic Arcade should use a lightweight, modular web architecture.
Core Stack
Frontend: HTML + CSS + JavaScript
Backend: Python + Flask
Database: Firebase / Firestore
AI: Constrained AI API calls
Quest Data: JSON / JavaScript objects
Version Control: Git + GitHub
Architecture Principle
Keep the infrastructure simple and make the learning interaction sophisticated.
The technical complexity should be concentrated in the quest engine, prediction system, dry-run
experience, hint ladder, and mastery model, because these directly create the product's differentiation.
The research explicitly recommends avoiding unnecessary infrastructure and prioritizing a complete vertical
slice over a large ecosystem.

---

<!-- Page 28 -->

## 36. Final Stack Summary

ALGORITHMIC ARCADE
│
▼
┌─────────────────┐
│ HTML / CSS │
│ JavaScript │
└────────┬────────┘
│
┌────────────┼────────────┐
│ │ │
▼ ▼ ▼
Quest Engine Prediction Dry Run
│ │ │
└────────────┼────────────┘
│
▼
Mastery Engine
│
┌────────┴────────┐
│ │
▼ ▼
Firebase Flask/Python
│ │
│ ▼
│ AI API
│ │
└─────────────────┘
│
▼
Learner Progress
Technical North Star:
Build the smallest reliable technical system capable of delivering the complete reasoning-first DSA
learning loop.
The goal of the hackathon is not to demonstrate how much technology the team can integrate. It is to
demonstrate that the technology can turn DSA reasoning into an interactive, measurable learning
experience.
