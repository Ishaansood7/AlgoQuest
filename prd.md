# Coding Adventure Platform PRD

_Converted from `Coding_Adventure_Platform_PRD.pdf`. Page order is preserved._

Coding Adventure Platform - PRD
Product Requirements Document (PRD)

## 1. Product Overview

Product Name
Working Name:
Coding Adventure Platform
Final name:
TBD
Product Type
Game-based interactive DSA learning and coding platform.
Product Vision
Build an interactive coding adventure that teaches beginner programmers
how to think through programming problems
,
rather than simply teaching them how to memorize algorithms or solve more questions.
The platform combines:

1.  Adventure-based DSA learning
2.  Reasoning and dry-run practice
3.  AI-powered adaptive guidance
4.  Competitive coding battles
5.  Cross-platform coding progress tracking
    Product Tagline
    Don’t just solve the problem. Learn how to think through it.
    Core Value Proposition
    Traditional coding platforms primarily measure:
    “Did you solve the problem?”
    This platform additionally measures:
    “How did you think through the problem?”

## 2. Problem Statement

Beginner programmers often know basic programming syntax but struggle when they encounter unfamiliar DSA problems.
The difficulty is not always a lack of knowledge of a particular algorithm.
Common difficulties include:
Understanding what a problem is actually asking
Identifying the relevant concept
Breaking a large problem into smaller steps
Knowing what variables or information need to be tracked
Predicting how an algorithm will behave
Dry-running code
Handling edge cases

---

<!-- Page 2 -->

Moving from an idea to executable code
Explaining why a solution works
Becoming dependent on hints or AI-generated solutions
Knowing what to practice next
Existing platforms are generally optimized around:
Learn concept → solve problem → submit → accepted/rejected.
This creates a gap between
knowing programming concepts
and
being able to independently reason through unfamiliar
problems
.

## 3. Product Hypothesis

If programming practice is transformed into an interactive adventure where learners are explicitly trained through:
Understand → Identify → Decompose → Predict → Dry Run → Solve → Explain → Review
then beginners can develop problem-solving skills more deliberately than through answer-oriented practice alone.
The product should therefore treat
reasoning as a first-class learning outcome
.

## 4. Target Users

Primary User
BCA/CS college students
Students who:
Know basic programming syntax
Have little or moderate DSA experience
Understand individual concepts but struggle to solve unfamiliar problems
Prepare for placements, internships, exams or competitive programming
Need structured practice
Often rely on tutorials, solutions or AI when stuck
Secondary Users
Absolute programming beginners
Students transitioning from basic programming to DSA
Competitive-programming beginners
Self-learners
Students preparing for coding interviews

## 5. User Persona

Example Persona
Name:
Rahul
Age:
19–22
Background:
BCA/CS student
Rahul knows:
Java/Python basics
loops
arrays
functions

---

<!-- Page 3 -->

basic OOP
But when given:
“Find the maximum element in an array”
he can understand the syntax but may struggle to formulate the complete approach independently.
Typical behavior:
Read problem
↓
Try to code immediately
↓
Get stuck
↓
Search solution
↓
Copy/understand solution
↓
Submit
↓
Forget later
The platform should transform this into:
Read problem
↓
Understand
↓
Identify
↓
Break down
↓
Predict
↓
Dry run
↓
Code
↓
Test
↓
Explain
↓
Remember

## 6. Product Goals

Primary Goals

1.  Teach DSA through active problem-solving.
2.  Improve analytical thinking.
3.  Improve problem decomposition.
4.  Improve prediction and dry-running skills.
5.  Reduce dependence on immediate solutions.
6.  Provide personalized learning paths.
7.  Make DSA practice engaging through adventure mechanics.
8.  Measure
    how
    a learner solves problems.
9.  Encourage independent problem solving.
10. Make practice more consistent.
    Secondary Goals
11. Enable coding battles.
12. Track coding activity across external platforms.
13. Recommend the next best learning activity.
14. Create a persistent learner profile.

---

<!-- Page 4 -->

## 7. Non-Goals

The initial product will NOT attempt to:
Replace LeetCode/GFG/CodeChef/HackerRank.
Support every DSA topic.
Provide a complete programming course.
Build a full-scale competitive programming judge.
Integrate every coding platform in real time.
Build a social network.
Build a complex virtual economy.
Provide unrestricted AI-generated solutions.
Support every programming language in the MVP.

## 8. Product Pillars

The product consists of three primary pillars.
CODING ADVENTURE
│
┌────────────────┼────────────────┐
↓ ↓ ↓
LEARN COMPETE GROW
│ │ │
Adventure Code Battles Progress Hub
│ │ │
└────────────────┼────────────────┘
↓
LEARNER MODEL
↓
NEXT BEST ACTION
Pillar 1 — Learn
Adventure-based DSA learning.
Pillar 2 — Compete
User vs Bot and eventually User vs User coding battles.
Pillar 3 — Grow
Track learning and external coding-platform activity.

## 9. Core Learning Loop

Every important learning interaction should reinforce:
UNDERSTAND
↓
IDENTIFY
↓
DECOMPOSE
↓
PREDICT
↓
DRY RUN
↓
SOLVE
↓
EXPLAIN

---

<!-- Page 5 -->

↓
REVIEW
↓
MASTER
↓
UNLOCK
This loop is the central product mechanic.

## 10. First-Time User Experience

Flow
Welcome
↓
Onboarding
↓
Thinking Trial
↓
Thinking Profile
↓
Personalized Starting Path
↓
Adventure

## 11. Onboarding

The onboarding should be short.
Information collected

1.  Programming experience
2.  DSA experience
3.  Preferred programming language
4.  Learning goal
5.  Approximate confidence level
    Example goals
    Learn DSA
    Prepare for placements
    Improve problem solving
    Competitive programming
    Build coding consistency

## 12. Thinking Trial

The system should avoid calling this a traditional test.
Name
Thinking Trial
Duration
Approximately 5–10 minutes.
Purpose
Measure the learner’s initial reasoning ability.

---

<!-- Page 6 -->

Skills measured
Skill
Measurement
Problem Understanding
Can the learner identify what is being asked?
Concept Recognition
Can they identify the relevant concept?
Decomposition
Can they break the problem into steps?
Prediction
Can they predict state/output?
Dry Run
Can they manually execute the logic?
Solving
Can they produce a basic solution?
Explanation
Can they explain the approach?

## 13. Thinking Trial Example

Problem:
Find the maximum element in an array.
Instead of immediately asking for code:
Step 1 — Understand
“What are we actually trying to find?”
Step 2 — Identify
“What information do we need to keep track of?”
Step 3 — Decompose
“Which steps should the program perform?”
Step 4 — Predict
Given:
[4, 8, 2, 9]
What happens to the current maximum after each element?
Step 5 — Dry Run
The learner manually executes the algorithm.
Step 6 — Code
The learner writes the solution.
Step 7 — Explain
“Why does this approach work?”

## 14. Thinking Profile

After the trial, the learner receives a profile.
Example:
YOUR THINKING PROFILE

---

<!-- Page 7 -->

Understanding 82%
Concept Recognition 61%
Decomposition 74%
Prediction 88%
Dry Run 55%
Independent Solving 47%
Explanation 69%
The system then generates one primary insight.
Example:
Your concepts are stronger than your execution.
You understand what to use, but your dry-run accuracy is holding you back.
Then:
Recommended next step:
Complete two guided dry-run quests.

## 15. Adventure World

The learning experience is structured as an adventure.
WORLD
↓
REGION
↓
QUEST
↓
CHALLENGE
↓
BOSS
Example World
DSA Realm
Array Forest
String City
Stack Castle
Linked List Bridge
⛰
Recursion Mountain
Algorithm Kingdom
MVP
Only
Array Forest
needs to be implemented.

## 16. Array Forest

The first learning region.
Possible areas:
Array Forest
│
├── Traversal Trail
├── Maximum Valley
├── Search Path
├── Frequency Village

---

<!-- Page 8 -->

├── Two-Pointer River
└── Array Guardian

## 17. Quest Types

The platform supports five major quest types.

## 1. Concept Quest

Teaches a concept.

## 2. Prediction Quest

Learner predicts what the algorithm/code will do.

## 3. Dry Run Quest

Learner manually traces execution.

## 4. Problem Quest

Learner independently solves a programming problem.

## 5. Boss Quest

Combines multiple skills with minimal guidance.

## 18. Quest Structure

Every standard problem quest follows:
Problem
↓
Understand
↓
Identify
↓
Decompose
↓
Predict
↓
Dry Run
↓
Code
↓
Test
↓
Explain
↓
Score
↓
Reward
Not every quest must contain every stage, but the system should support the complete structure.

## 19. Quest Example — “The Lost Maximum”

Story
The Array Forest guardian has lost track of the largest value.
The learner must find it.

---

<!-- Page 9 -->

Stage 1 — Understand
“What is the problem asking you to find?”
Stage 2 — Identify
“What information must your algorithm remember while scanning the array?”
Stage 3 — Decompose
Learner selects:
Start
↓
Take first value
↓
Compare with next value
↓
Update maximum if needed
↓
Continue
↓
Return maximum
Stage 4 — Predict
Input:
[4, 7, 2, 9, 5]
Learner predicts:
4 → 7 → 7 → 9 → 9
Stage 5 — Dry Run
Interactive table:
Step
Current Element
Maximum
1
4
4
2
7
7
3
2
7
4
9
9
5
5
9
Stage 6 — Code
Learner writes code.
Stage 7 — Test
Normal case + edge case.
Stage 8 — Explain
“Why is your algorithm guaranteed to find the maximum?”

## 20. Visual Interaction

---

<!-- Page 10 -->

Visualizations should not simply show animations.
The learner should
predict before seeing the result
.
Core mechanic:
PREDICT
↓
REVEAL
↓
COMPARE
↓
EXPLAIN
↓
TRY AGAIN
Example:
The robot asks:
“What will
max
contain after this iteration?”
The learner chooses an answer.
Only then does the system animate the next step.

## 21. Dry-Run Engine

The dry-run interface should allow users to manipulate:
variables
array indices
current element
pointers
loop iterations
conditions
output
Example:
i = 2
current = 7
max = 9
What happens next?
The learner chooses or enters the next state.

## 22. AI Robot Companion

The robot is the learner’s companion throughout the adventure.
Responsibilities

1.  Explain
2.  Guide
3.  Diagnose
4.  Encourage
    The robot should
    not
    behave like an unrestricted ChatGPT clone.

---

<!-- Page 11 -->

## 23. Hint Ladder

Hints should progressively reveal information.
Level 0
No hint
Level 1
Gentle nudge
Level 2
Directional hint
Level 3
Detailed guidance
Level 4
Concept explanation
Level 5
Worked solution
Example:
Level 1
“Before thinking about the code, what information needs to survive each iteration?”
Level 2
“Think about the largest value you’ve seen so far.”
Level 3
“Maintain a variable representing the largest value encountered.”
Level 4
Explanation of the traversal/max concept.
Level 5
Full worked solution.

## 24. AI Design Principle

AI should increase thinking, not replace thinking.
AI should primarily:
simplify confusing wording
explain terminology
provide hints
diagnose mistakes
explain errors
suggest the next step

---

<!-- Page 12 -->

recommend prerequisite practice
Full solutions should be the
last resort
.

## 25. Adaptive Assistance

The robot should reduce assistance as the learner improves.
Example:
Beginner:
“Let’s break this problem into three smaller steps.”
Intermediate:
“Which part of the problem are you uncertain about?”
Advanced:
“You’ve solved similar problems before. What’s the invariant here?”
Eventually:
“No hints this time. You’ve got this.”

## 26. Reasoning/Mastery Engine

The platform maintains a learner model.
SkillProfile
│
├── Understanding
├── Concept Recognition
├── Decomposition
├── Prediction
├── Dry Run
├── Solving
├── Explanation
└── Hint Dependency
Each skill has a score from 0–100.

## 27. Mastery Calculation

Mastery should consider:
correctness
difficulty
independence
repeated performance
reasoning quality
hint usage
improvement after mistakes

---

<!-- Page 13 -->

Example:
Correct + independent
→ High mastery contribution
Correct + heavy hints
→ Moderate mastery contribution
Incorrect → retry → correct
→ Learning/improvement contribution

## 28. Recommendation Engine

The system identifies the learner’s weakest relevant skill.
Example:
Dry Run = 48%
Decomposition = 72%
Prediction = 86%
Recommendation:
Your next quest should focus on dry-running.
For MVP, simple rule-based recommendations are sufficient.
Example:
IF dryRun < 50
→ recommend Dry Run Quest
IF decomposition < 50
→ recommend Decomposition Quest
IF prediction < 50
→ recommend Prediction Quest

## 29. Boss Quests

Bosses test whether the learner can transfer their skills independently.
Normal quest:
Guidance
↓
Practice
↓
Hints
Boss:
Problem
↓
Think independently
↓
Solve
↓
Explain
Boss evaluates
Understanding

---

<!-- Page 14 -->

Concept recognition
Decomposition
Prediction
Dry run
Coding
Explanation
Hint dependency

## 30. Gamification

Gamification should reward meaningful learning behavior.
The product separates:
XP
Activity/progression.
Mastery
Actual learning.
Rating
Competitive performance.
Streak
Consistency.

## 31. XP

Example starting values:
Action
XP
Complete quest
50
Correct prediction
15
Complete dry run
20
Solve challenge
50
Explain solution
20
Complete boss
150
Win bot battle
75
Win PvP battle
100
Values can be balanced after testing.

## 32. Anti-Grinding

Repeatedly completing the same easy quest should not generate unlimited XP.
Therefore:
XP is primarily awarded for meaningful learning and improvement.

---

<!-- Page 15 -->

Repeated practice can still improve mastery without creating an XP exploit.

## 33. Levels

Levels represent adventure progression.
Example:
Level 1 → 0 XP
Level 2 → 250 XP
Level 3 → 600 XP
Level 4 → 1,000 XP
Level 5 → 1,500 XP
The exact curve will be tuned during implementation.

## 34. Unlock System

Unlocks should depend on
mastery
, not only XP.
Example:
Pointer Valley unlocks when Array Traversal mastery reaches 70%.
This prevents grinding easy quests to unlock advanced content.

## 35. Streak System

Two streaks are maintained.
Learning Streak
Activity on the platform.
Coding Streak
Coding activity across supported external platforms.
Example:
Learning Streak
12 days
External Coding
LeetCode
15
GFG
8
CodeChef
6
HackerRank
3
Breaking a streak should not delete mastery or progress.

## 36. Badges

Badges represent meaningful behaviors.
Examples:
First Thought

---

<!-- Page 16 -->

Complete first prediction.
Dry Runner
Complete 10 dry runs.
Decomposer
Successfully decompose 10 problems.
Independent Thinker
Solve 5 challenges without hints.
⚔ First Blood
Win first coding battle.
Boss Slayer
Complete first boss quest.

## 37. Code Battles

The second major product pillar.
Two modes:
CODE ARENA
│
├── User vs Bot
└── User vs User

## 38. User vs Bot

Flow:
Match
↓
Problem
↓
Think Phase
↓
Prediction
↓
Code
↓
Submit
↓
Bot Submission
↓
Result
For MVP, only one bot difficulty is required.
Future levels:
Beginner Bot
Challenger Bot
Expert Bot
Boss Bot

## 39. User vs User

---

<!-- Page 17 -->

Both players receive the same challenge.
Player A ──┐
├── Same Problem
Player B ──┘
↓
Think
↓
Code
↓
Submit
↓
Result
This is P1 for the hackathon.

## 40. Battle Scoring

Speed should not dominate because the product is about thinking.
Suggested scoring:
Component
Weight
Correctness
40%
Reasoning
25%
Dry Run
15%
Efficiency
10%
Speed
10%

## 41. Think Rating

Competitive performance is represented by a separate rating.
Example:
Level 8
Think Rating: 1284
17 Wins
8 Losses
XP and Think Rating must remain separate.

## 42. Coding Progress Hub

The third product pillar tracks external coding activity.
Potential platforms:
LeetCode
GeeksforGeeks
CodeChef
HackerRank
Dashboard information
External Coding

---

<!-- Page 18 -->

LeetCode
12
GFG
8
CodeChef
5
HackerRank
3
Problems solved
Weekly activity
Topic distribution
Current streak

## 43. Progress Hub Philosophy

The Progress Hub should not simply become another statistics dashboard.
It should answer:
“What should I do next?”
Example:
You solved:
Arrays 27
Strings 11
Linked List 2
Your weak area:
Dry Run
Recommended:
Complete 2 guided dry-run quests
before attempting medium two-pointer problems.

## 44. External Platform Integration Strategy

Because reliable public APIs are not guaranteed across all platforms, external integrations are not part of the MVP critical path.
MVP
Use:
seeded/demo data
manually entered usernames
mock platform activity
Future
Implement isolated connectors:
LeetCode Connector
GFG Connector
CodeChef Connector
HackerRank Connector
All connectors map into one internal structure:
ExternalProgress
│
├── platform
├── problemsSolved
├── streak
├── topics
├── difficulty
├── activity
└── lastActive

---

<!-- Page 19 -->

## 45. Dashboard

The dashboard should answer four questions immediately:

1. Where am I?
   Current world/region/quest.
2. How am I doing?
   Mastery and progression.
3. What am I weak at?
   Reasoning profile.
4. What should I do next?
   Personalized recommendation.

## 46. Example Dashboard

GOOD MORNING, ISHAAN
Level 8
12 Day Learning Streak
Think Rating 1284
CURRENT ADVENTURE
Array Forest
82% Mastery
REASONING
Understanding 84%
Decomposition 71%
Prediction 91%
Dry Run 58%
Solving 66%
────────────────────────
NEXT QUEST
The Pointer Path
Recommended because:
Your dry-run accuracy is lower than
your other reasoning skills.
[START QUEST]

## 47. Navigation

Recommended primary navigation:
Home
Adventure
⚔
Arena
Progress
Profile
Robot/help remains accessible globally.

---

<!-- Page 20 -->

## 48. User Profile

Profile should show:
Player level
XP
Think Rating
Learning streak
Mastery
Reasoning profile
Strongest skill
Weakest skill
Badges
Completed regions
Battle record
External coding activity

## 49. Data Model

Core entities:
User
│
├── Profile
├── SkillProfile
├── Progress
├── Streaks
├── Achievements
├── Battles
└── ExternalPlatformData
Quest:
Quest
│
├── id
├── title
├── region
├── type
├── difficulty
├── concept
├── problem
├── reasoningSteps
├── predictionData
├── dryRunData
├── testCases
├── hints
└── rewards
Attempt:
Attempt
│
├── userId
├── questId
├── answers
├── code
├── correctness
├── hintsUsed
├── time
├── reasoningScore
├── masteryGain
└── timestamp

---

<!-- Page 21 -->

## 50. Content-Driven Quest Architecture

One of the most important technical requirements:
Developers should be able to create a new quest primarily by adding structured content rather than rewriting React
components.
Example conceptual structure:
The frontend renders the appropriate interaction from the quest definition.

## 51. Technical Requirements

Frontend
Recommended:
React
Vite
JavaScript
CSS/Tailwind
React Router
Frontend responsibilities
Adventure map
Quest UI
Interactive visualizations
Prediction interface
Dry-run interface
Code editor
Battle interface
Dashboard
Profile
Progress Hub

## 52. Backend

{
"id"
:
"array-max-01"
,
"title"
:
"The Lost Maximum"
,
"type"
:
"problem"
,
"topic"
:
"arrays"
,
"difficulty"
:
"beginner"
,
"steps"
:
[
"understand"
,
"identify"
,
"decompose"
,
"predict"
,
"dryRun"
,
"code"
,
"explain"
]
,
"hints"
:
[
"..."
,
"..."
,
"..."
]
}

---

<!-- Page 22 -->

A lightweight backend is sufficient for the MVP.
Responsibilities:
user data
quest progress
mastery
attempts
battle results
streaks
profile data
The MVP should avoid unnecessary backend complexity.

## 53. AI Layer

AI should be isolated from the core learning engine.
Application
│
├── Deterministic Quest Engine
│
├── Mastery Engine
│
└── AI Tutor
│
├── Simplify
├── Hint
├── Diagnose
└── Explain
If AI fails during the demo, the core learning experience must still work.

## 54. Code Execution

The platform eventually requires a sandboxed code execution environment.
For the 24-hour MVP:
Preferred approach
Use a limited set of predefined coding challenges and a simple judging mechanism.
The system does not need to support arbitrary competitive-programming infrastructure.
The bot can also use predetermined solutions/results for the demo.

## 55. MVP Scope — 24 Hours

The MVP must demonstrate one complete vertical slice.
DEMO
│
┌──────────┼──────────┐
↓ ↓ ↓
THINKING ARRAY CODE
TRIAL FOREST BATTLE
│ │ │
└──────────┼──────────┘
↓
LEARNER MODEL
↓
RECOMMENDATION

---

<!-- Page 23 -->

Must Have
Onboarding
Thinking Trial
Thinking Profile
Array Forest
2–3 quests
Prediction interaction
Dry-run interaction
Coding challenge
Robot hints
Mastery calculation
Dashboard
One User vs Bot battle
Basic XP/level
Basic streak
Basic badges
Demo Progress Hub

## 56. Should Have

Boss quest
More XP mechanics
richer badges
battle history
external platform mock data
improved visualizations
user profile

## 57. Could Have

User vs User
real LeetCode integration
GFG integration
CodeChef integration
HackerRank integration
advanced AI personalization
matchmaking
leaderboards
multiple worlds

## 58. Won’t Have in MVP

Full social network
Real-time multiplayer infrastructure
Complete competitive programming judge
All DSA topics
All programming languages
Complex economy
Advanced recommendation AI
Production-grade integrations with every external coding platform

## 59. Critical User Journey

---

<!-- Page 24 -->

The hackathon demo should tell one story.
Scene 1
Student knows Java but struggles with DSA.
Scene 2
Student completes the Thinking Trial.
Scene 3
System discovers:
“Your dry-run ability needs improvement.”
Scene 4
Student enters Array Forest.
Scene 5
They complete:
The Lost Maximum
Scene 6
Student predicts algorithm behavior.
Scene 7
Student performs an interactive dry run.
Scene 8
Robot provides a contextual hint after the student struggles.
Scene 9
Student writes the solution.
Scene 10
Mastery profile updates.
Dry Run
54% → 63%
Scene 11
Student enters the Code Arena.
Scene 12
Student battles the bot.
Scene 13
Progress Hub displays external coding activity.
Scene 14
Platform recommends the next challenge.
Final message:
“We don’t just track whether you solved the problem. We track how you learned to solve it.”

---

<!-- Page 25 -->

## 60. Success Metrics

Learning Metrics
Improvement in Thinking Trial vs later performance
Prediction accuracy
Dry-run accuracy
Decomposition accuracy
Independent solve rate
Hint dependency
Explanation quality
Engagement Metrics
Daily active learners
Learning streak retention
Quest completion rate
Return rate
Boss completion rate
Product Metrics
Recommendation acceptance rate
Battle participation
External platform tracking usage
Average session duration

## 61. Key Product KPIs for Hackathon Demo

The judges should be able to see:
KPI 1
Reasoning improvement
Dry Run
54% → 68%
KPI 2
Reduced hint dependency
5 hints → 2 hints
KPI 3
Independent solving
Guided → Semi-guided → Independent
These demonstrate educational impact better than:
“The user earned 500 XP.”

---

<!-- Page 26 -->

## 62. Risks

Risk
Impact
Mitigation
AI unavailable
High
Deterministic fallback hints
Code execution complexity
High
Limited MVP judge
External APIs unavailable
Medium
Seeded/demo data
Too many features
High
Strict vertical slice
Gamification becomes distracting
Medium
Reward learning actions
Users rely on AI
High
Progressive hints
Visualizations become passive
Medium
Prediction-first interactions
Multiplayer takes too long
High
User vs Bot first

## 63. Product Principles

Principle 1 — Thinking before coding
Don’t immediately ask the learner to write code.
Principle 2 — Predict before reveal
The learner should actively reason before seeing the animation/output.
Principle 3 — Hints before answers
AI should scaffold rather than replace thinking.
Principle 4 — Reward learning
XP should reward meaningful actions.
Principle 5 — Failure is data
Incorrect answers should identify the learner’s weakness.
Principle 6 — Mastery over grinding
Progression should depend on demonstrated understanding.
Principle 7 — Speed is secondary
Especially in educational battles.
Principle 8 — Every game mechanic must have a learning purpose.

## 64. Competitive Differentiation

Platform
Primary Strength
LeetCode
Problem practice
GeeksforGeeks
DSA content + practice
CodeChef
Competitive programming
CodeCombat
Game-based coding
VisuAlgo
Algorithm visualization
Duolingo
Gamified learning

---

<!-- Page 27 -->

Coding Adventure
Platform
Reasoning-first DSA learning + adaptive scaffolding + adventure + competition + progress
intelligence
The product should therefore
not
position itself simply as:
“Duolingo for DSA.”
Instead:
“An adventure game that trains you to think like a programmer.”

## 65. Unique Selling Proposition

Primary USP
A DSA learning platform that measures and trains the reasoning process behind solving a problem—not just the
final answer.
Supporting USPs

## 1. Reasoning-first learning

Understand → Decompose → Predict → Dry Run → Solve.

## 2. Adaptive AI companion

Hints become less explicit as the learner improves.

## 3. Adventure progression

Concepts become explorable regions and quests.

## 4. Reasoning profile

The system identifies
how
the learner struggles.

## 5. Integrated coding journey

Learning activity + competitive battles + external coding progress.

## 66. Product Architecture

┌─────────────────────────────────────────────┐
│ FRONTEND │
│ │
│ Onboarding │ Adventure │ Arena │ Progress │
│ │ Dashboard │ Profile │
└──────────────────────┬──────────────────────┘
↓
┌─────────────────────────────────────────────┐
│ LEARNING ENGINE │
│ │
│ Quest Engine │
│ Reasoning Engine │
│ Mastery Engine │
│ Recommendation Engine │
│ Battle Scoring │
│ Progress Engine │
└───────────────┬─────────────────────────────┘
│
┌────────┴────────┐
↓ ↓

---

<!-- Page 28 -->

┌──────────────┐ ┌───────────────┐
│ AI TUTOR │ │ DATA LAYER │
│ │ │ │
│ Hints │ │ Users │
│ Explain │ │ Quests │
│ Diagnose │ │ Attempts │
│ Simplify │ │ Battles │
└──────────────┘ │ Mastery │
│ Streaks │
│ Platforms │
└───────────────┘

## 67. Future Roadmap

Phase 1 — Hackathon MVP
Thinking Trial

- Array Forest
- Reasoning Engine
- AI Hints
- Bot Battle
- Progress Dashboard
  Phase 2 — Product Beta
  More DSA regions
- Bosses
- User vs User
- Real coding execution
- Real platform tracking
  Phase 3 — Intelligent Learning Platform
  Adaptive curriculum
- Advanced learner model
- Spaced repetition
- Personalized problem generation
- Advanced AI tutor
- Real-time multiplayer
  Phase 4 — Coding Learning Ecosystem
  DSA
- Competitive Programming
- Placement Preparation
- Interview Simulation
- Community
- Mentorship

  ***

<!-- Page 29 -->

## 68. Final Product Definition

A game-based interactive DSA learning platform for beginner programmers that teaches problem-solving as a
sequence of reasoning skills—understanding, concept recognition, decomposition, prediction, dry-running,
solving and explanation. Learners progress through an adventure world with an adaptive AI companion that
provides progressively reduced scaffolding, while a reasoning profile tracks how independently they solve
problems and recommends the next best challenge. The platform also adds coding battles and cross-platform
coding progress tracking to create a unified coding-learning journey.

## 69. One-Line Pitch

Don’t just solve the problem. Learn how to think through it. 70. 30-Second Pitch
“Most coding platforms tell you whether your answer is right or wrong. Our platform goes one step deeper—it teaches and
measures how you think. Students enter an adventure world where every DSA problem becomes a quest. Before coding, they
must understand the problem, break it down, predict the algorithm and dry-run it. An AI robot provides hints without
immediately giving the answer. The system builds a reasoning profile showing where the learner struggles and recommends
what they should practice next. Then they can test themselves through coding battles and track their broader coding
progress. So instead of just asking
‘Did you solve it?’
, we ask
‘Did you learn how to solve it?’
”
