# Algorithmic Arcade Design Document

_Converted from `Algorithmic_Arcade_Design_Document.pdf`. Page order is preserved._

Algorithmic Arcade
Design Document
Project: Algorithmic Arcade — A DSA Problem-Solving Adventure
Document Type: Product & System Design Document
Version: 1.0
Platform: Web Application
Primary Theme: EdTech / Gamified Programming Education
MVP Focus: Beginner DSA Problem-Solving
Initial Region: Array Forest

## 1. Design Overview

Algorithmic Arcade is designed as a game-like learning environment for beginner programmers who
understand basic programming syntax but struggle when faced with unfamiliar DSA problems.
The design focuses on the mental process that occurs between reading a problem and writing code.
Instead of immediately asking the learner to solve a coding problem, the system guides them through:
Understand → Decompose → Predict → Dry Run → Solve → Explain → Review
The product therefore behaves less like a traditional coding-practice website and more like a guided
adventure where each problem-solving skill becomes part of gameplay.
The MVP concentrates on one polished learning region, Array Forest, and one complete quest, The Lost
Maximum.

---

<!-- Page 2 -->

## 2. Design Principles

2.1 Learning Before Coding
The interface should not immediately present a large code editor.
The learner first interacts with the problem through understanding, prediction, and reasoning activities.
2.2 Active Participation
Animations should not simply show the learner what happens.
The learner should be asked to:
predict
choose
identify
arrange
explain
dry-run
solve
The system should make the learner think before revealing information.
2.3 Progressive Assistance
The Robot Companion should provide assistance gradually.
The learner should never receive the complete solution simply because they made one mistake.
The preferred assistance sequence is:
Nudge → Direction → Structure → Explanation → Solution
The MVP may expose the first three levels, while later levels can be added.
•
•
•
•
•
•
•

---

<!-- Page 3 -->

2.4 Minimal Cognitive Overload
The interface should introduce one learning action at a time.
Instead of showing:
problem statement
code editor
hints
leaderboard
XP
statistics
animations
all at once, the experience should reveal information progressively.
2.5 Game Mechanics Must Support Learning
XP, levels, badges and progression should reinforce learning behavior.
For example:
accurate prediction → reward
completing dry run → reward
solving with fewer hints → better mastery
explaining the solution → mastery evidence
Gamification should not become the objective itself.

## 3. Design Goals

The design should achieve the following:
Make DSA feel approachable to beginners.
Break complex problem-solving into smaller actions.
Make invisible reasoning measurable.
Provide immediate but controlled feedback.
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

1.
2.
3.
4.

---

<!-- Page 4 -->

Encourage independent problem solving.
Make progress visually understandable.
Create a memorable game-like experience within the 24-hour hackathon scope.

## 4. Target User

Primary User
A college student who:
knows basic programming syntax
has learned variables, loops and arrays
can write simple programs
struggles with unfamiliar DSA questions
often searches for solutions immediately
has difficulty identifying which concept to use
struggles with dry runs
User Mindset
Typical experience:
"Mujhe syntax aata hai, but question dekhte hi samajh nahi aata ki start kaha se karu."
Algorithmic Arcade is designed specifically around this gap.

## 5. Experience Architecture

The application is divided into several conceptual layers. 5. 6. 7.
•
•
•
•
•
•
•

---

<!-- Page 5 -->

ALGORITHMIC ARCADE
│
┌──────┴──────┐
│ Adventure │
│ Map │
└──────┬──────┘
│
┌──────▼──────┐
│ Region │
│ Array Forest │
└──────┬──────┘
│
┌──────▼──────┐
│ Quest │
│ Lost Maximum │
└──────┬──────┘
│
┌──────────────────┼──────────────────┐
│ │ │
▼ ▼ ▼
Understand Predict Dry Run
│ │ │
└──────────────────┼──────────────────┘
│
┌──────▼──────┐
│ Solve │
└──────┬──────┘
│
┌──────▼──────┐
│ Explain │
└──────┬──────┘
│
┌──────▼──────┐
│ Review │
└─────────────┘

## 6. Information Architecture

The MVP consists of the following major screens:

---

<!-- Page 6 -->

Landing Page
│
▼
Adventure Map
│
▼
Array Forest
│
▼
Quest Introduction
│
▼
Problem Understanding
│
▼
Prediction
│
▼
Dry Run
│
▼
Coding
│
▼
Explanation
│
▼
Quest Results
│
▼
Mastery / Progress
Optional:
Array Forest
│
└── Duel Mode

## 7. Visual Design Direction

7.1 Overall Style
The visual language should feel like:

---

<!-- Page 7 -->

Coding platform + adventure game + educational dashboard
The interface should avoid looking like a conventional LMS.
Instead of traditional menus such as:
Courses → Modules → Lessons → Exercises
the learner should encounter:
World → Region → Quest → Challenge → Boss
7.2 Visual Hierarchy
Each screen should have:
Primary Area
The current learning activity.
Secondary Area
Contextual information, such as:
progress
objective
current stage
XP
Support Area
Robot Companion and hints.
The learner's current task must always dominate the screen.
•
•
•
•

---

<!-- Page 8 -->

## 8. Global Interface

A consistent top-level interface should contain:
┌─────────────────────────────────────────────────────────┐
│ Algorithmic Arcade Quest Progress XP Profile │
├─────────────────────────────────────────────────────────┤
│ │
│ CURRENT ACTIVITY │
│ │
│ │
│ │
├─────────────────────────────────────────────────────────┤
│ Robot Companion Help/Hints │
└─────────────────────────────────────────────────────────┘
The exact visual implementation can be adapted to the final frontend.

## 9. Landing / Entry Screen

Purpose
Introduce the product and establish the adventure metaphor.
Main Elements
Algorithmic Arcade logo
short value proposition
Start Adventure button
brief explanation
optional existing-user continuation
Primary CTA
Start Adventure
•
•
•
•
•

---

<!-- Page 9 -->

Supporting message:
Learn DSA by learning how to think, not just what to code.

## 10. Adventure Map

The Adventure Map is the main navigation hub.
Possible world structure:
ALGORITHMIC ARCADE
🏰
Algorithm Kingdom
│
┌────────┴────────┐
│ │
Array Forest String City
│
┌──────┼──────┐
│ │ │
Quest Quest Quest
│
Lost Maximum
For the MVP, only Array Forest needs to be fully interactive.
Other regions can appear locked.

## 11. Array Forest Design

Array Forest introduces fundamental array problem-solving skills.
Potential quest progression:

---

<!-- Page 10 -->

Array Forest
│
├── Quest 1: Lost Maximum
│
├── Quest 2: Array Explorer
│
└── Quest 3: Hidden Pattern
Only the first quest needs to be fully polished for the MVP.
Locked quests communicate future progression without requiring implementation.

## 12. Quest Card Design

Each quest should communicate:
Quest name
difficulty
skill
estimated time
completion state
mastery status
Example:
┌─────────────────────────────────┐
│ 🌲 THE LOST MAXIMUM │
│ │
│ Find the largest element │
│ in the mysterious array. │
│ │
│ Skill: Array Traversal │
│ Difficulty: ⭐ │
│ │
│ [ START QUEST ] │
└─────────────────────────────────┘
•
•
•
•
•
•

---

<!-- Page 11 -->

## 13. Quest Experience

Each quest follows a controlled sequence.
Quest Start
│
▼
Understand
│
▼
Decompose
│
▼
Predict
│
▼
Dry Run
│
▼
Solve
│
▼
Explain
│
▼
Review
The learner should not be forced to navigate between unrelated pages.
The experience should feel like one continuous quest.

## 14. Problem Understanding Screen

Objective
Ensure the learner understands what the problem is asking before thinking about implementation.
The screen should show:
original problem
simplified explanation
important terms
expected output
•
•
•
•

---

<!-- Page 12 -->

optional Robot assistance
Example:
┌─────────────────────────────────────────────┐
│ WHAT IS THE QUEST ASKING? │
│ │
│ Find the largest number in the array. │
│ │
│ In simple words: │
│ Look at all numbers and remember the │
│ biggest number you have seen so far. │
│ │
│ [ I UNDERSTAND ] [ ASK ROBOT ] │
└─────────────────────────────────────────────┘
The AI Problem Simplifier should be constrained to explanation rather than solution generation.

## 15. Decomposition Screen

The learner identifies the smaller actions required to solve the problem.
Example:
What do you need to do?
Possible choices:
Look at every element
Keep track of the largest value
Compare current value with largest
Print the final largest value
The system can allow the learner to arrange or select the relevant steps.
This makes decomposition a measurable learning action.
•
•
•
•
•

---

<!-- Page 13 -->

## 16. Prediction Screen

Prediction is one of the key differentiating interactions.
The system presents an array and asks the learner to predict what the algorithm's tracking variable will
become.
Example:
Array:
[ 4 ] [ 9 ] [ 2 ] [ 7 ]
Start:
max = 4
After seeing 9, what will max be?
[ 4 ] [ 9 ] [ 2 ] [ 7 ]
Your prediction:
┌─────────┐
│ 9 │
└─────────┘
[ CHECK ]
The learner receives immediate feedback.
Prediction accuracy can contribute to mastery.

## 17. Dry-Run Interface

The dry-run screen is the central interactive learning component.
Instead of showing only an animation, the system should expose the changing state.
Example:

---

<!-- Page 14 -->

Step Element Current Max
1 4 4
2 9 9
3 2 9
4 7 9
The current step should be visually emphasized.
Controls:
[ Previous ] [ Next ] [ Auto Run ]
Optional:
Predict next state
This allows the learner to understand how the algorithm changes state over time.

## 18. Coding Screen

After the learner understands and dry-runs the algorithm, the system introduces coding.
The coding screen contains:

---

<!-- Page 15 -->

┌─────────────────────────────────────────────┐
│ THE LOST MAXIMUM │
├─────────────────────────────────────────────┤
│ Problem │
│ Find the maximum element of an array. │
│ │
│ Hint: Think about what you tracked in │
│ the dry run. │
├─────────────────────────────────────────────┤
│ │
│ CODE EDITOR │
│ │
│ // Write your solution │
│ │
│ │
├─────────────────────────────────────────────┤
│ [ Run ] [ Hint ] │
└─────────────────────────────────────────────┘
The exact code-execution technology is intentionally kept lightweight for the hackathon MVP.

## 19. Robot Companion

The Robot is a persistent learning companion.
Its role is:
Coach, not answer machine.
The Robot should be visually identifiable but should not dominate the interface.
Possible personality:
encouraging
slightly playful
concise
beginner-friendly
Example:
•
•
•
•

---

<!-- Page 16 -->

🤖 "You're close. Don't think about the whole array at once. Ask yourself: what information do I need to
remember while scanning it?"

## 20. Hint Ladder

The hint system should progressively reduce the learner's uncertainty.
Level 1 — Nudge
"What value are you trying to keep track of?"
Level 2 — Direction
"You need to compare each element with the largest value you've seen so far."
Level 3 — Structure
"Start with a variable for the current maximum, then traverse the array and update it when a larger value
appears."
Level 4 — Explanation
Explain the algorithm in more detail.
Level 5 — Solution
Reveal the solution only when appropriate.
The MVP should prioritize the first three levels.

---

<!-- Page 17 -->

## 21. Quest State Model

Every quest should maintain a state.
Conceptually:
QuestState
problem
currentStage
predictionAttempts
predictionAccuracy
dryRunProgress
hintsUsed
codeAttempts
completed
score
mastery
Example:
{
currentStage: "DRY_RUN",
predictionAccuracy: 0.75,
hintsUsed: 1,
codeAttempts: 2,
completed: false
}
This state controls what the learner sees next.

---

<!-- Page 18 -->

## 22. Quest State Machine

START
│
▼
UNDERSTAND
│
▼
DECOMPOSE
│
▼
PREDICT
│
▼
DRY_RUN
│
▼
SOLVE
│
▼
EXPLAIN
│
▼
REVIEW
│
▼
COMPLETE
If the learner requests help:
Any Stage
│
▼
Robot Hint
│
▼
Same Stage
A hint should not automatically move the learner forward.

## 23. Mastery Design

The product should track more than whether the final code was accepted.

---

<!-- Page 19 -->

Possible mastery dimensions:
Dimension Measurement
Understanding Problem interpretation
Decomposition Correct logical steps
Prediction Prediction accuracy
Dry Run State-tracking performance
Coding Correctness
Independence Hints used
Speed Time taken
Explanation Ability to explain reasoning
The resulting profile can represent how the learner solved the problem, not simply whether they solved it.

## 24. Quest Completion Screen

After completion:
┌──────────────────────────────────────────┐
│ QUEST COMPLETE! 🎉 │
│ │
│ THE LOST MAXIMUM │
│ │
│ Prediction 80% │
│ Dry Run 100% │
│ Coding ✓ │
│ Hints Used 1 │
│ Time 04:32 │
│ │
│ +120 XP │
│ │
│ [ CONTINUE ] │
└──────────────────────────────────────────┘

---

<!-- Page 20 -->

The feedback should highlight learning behavior.

## 25. Mastery Dashboard

The dashboard should answer:
"Am I actually getting better at solving problems?"
Example:
MY MASTERY
Arrays ████████░░ 80%
Prediction ███████░░░ 70%
Dry Run █████████░ 90%
Problem Understanding ██████░░░░ 60%
Hints Independence ████████░░ 80%
For the MVP, these can be calculated from the current quest and a small set of stored progress data.

## 26. Gamification Design

The MVP should use lightweight gamification.
Possible elements:
XP
Earned from meaningful actions.
Quest Completion
Unlocks additional content.

---

<!-- Page 21 -->

Mastery
Represents learning quality.
Region Progress
Shows progress through Array Forest.
Badges
Optional if implementation time allows.
Example:
🧠
Prediction Pro Successfully predicted 5 algorithm states.

## 27. Duel Mode Design

Duel Mode is a P1 feature.
It should be an asynchronous 1v1 experience rather than a technically complex real-time multiplayer game.
Basic flow:
Player A ──┐
├── Shared Quest
Player B ──┘
│
▼
Progress Comparison
│
▼
Result
The progress bar can show:
ISHaan ████████░░ 80%
Opponent ██████░░░░ 60%
The score should consider:

---

<!-- Page 22 -->

Speed + Accuracy − Hints
This prevents simply rushing through the challenge from being the only winning strategy.

## 28. Data Design

The design assumes a lightweight Firebase/Firestore-backed progress model.
Conceptually:
users
│
├── profile
├── progress
│ ├── regions
│ ├── quests
│ └── mastery
│
└── duels
Quest progress may contain:
questId
status
predictionAccuracy
dryRunAccuracy
timeTaken
hintsUsed
attempts
score
completedAt

## 29. AI Interaction Design

AI should be used only where it provides clear educational value.

---

<!-- Page 23 -->

AI Problem Simplifier
Input:
Original problem
Output:
Beginner-friendly explanation
AI Robot Hint
Input:
Problem + current stage + learner state
Output:
Controlled hint appropriate to the current level
AI should not automatically generate the final solution.

## 30. AI Guardrails

The AI layer should:
avoid immediately revealing answers
use beginner-friendly language
explain unfamiliar terminology
remain focused on the current problem
provide hints appropriate to the learner's stage
avoid unnecessary advanced concepts
•
•
•
•
•
•

---

<!-- Page 24 -->

The frontend should also maintain the hint level rather than relying entirely on the AI to decide how much
information to reveal.

## 31. Responsive Design

The primary target is a laptop/desktop browser because the MVP is intended for hackathon demonstration
and coding interaction.
However, the interface should remain usable on smaller screens.
Priority:
Desktop / Laptop
↓
Tablet
↓
Mobile
The coding and dry-run interfaces should receive special attention because they contain information-dense
components.

## 32. Accessibility Considerations

The interface should aim to provide:
readable typography
sufficient contrast
keyboard-accessible controls
clear button labels
non-color-only feedback
understandable error messages
consistent navigation
For the MVP, accessibility should be incorporated into the UI rather than treated as a separate feature.
•
•
•
•
•
•
•

---

<!-- Page 25 -->

## 33. Error & Feedback Design

Errors should teach rather than punish.
Instead of:
❌ Wrong Answer
prefer:
Not quite. Your prediction changed too early. Look at which element has actually been processed at this
step.
For coding:
Your code doesn't produce the expected result for this test case. Try checking how you update the
maximum.
The Robot can provide a hint without immediately exposing the solution.

## 34. Empty / Loading / Failure States

Important states include:
AI Loading
🤖 Thinking...

---

<!-- Page 26 -->

AI Failure
Robot connection failed. You can continue using the built-in hints.
Firebase Failure
The quest should ideally remain usable locally and save progress when the connection becomes available.
Code Execution Failure
Display a clear error instead of crashing the quest.

## 35. Animation Strategy

Animation should be purposeful.
Useful animations:
character movement between regions
quest unlock
array traversal
current-state highlighting
XP/progress updates
successful completion
Avoid excessive animation because the MVP has only 24 hours and the research explicitly prioritizes
meaningful interaction over decorative game mechanics.

## 36. Component Design

Suggested reusable UI components:
•
•
•
•
•
•

---

<!-- Page 27 -->

App
│
├── Header
├── AdventureMap
│ ├── RegionCard
│ └── QuestCard
│
├── QuestEngine
│ ├── ProblemPanel
│ ├── DecompositionPanel
│ ├── PredictionPanel
│ ├── DryRunPanel
│ ├── CodePanel
│ ├── ExplanationPanel
│ └── ReviewPanel
│
├── RobotCompanion
│ └── HintPanel
│
├── ProgressBar
├── MasteryCard
├── XPDisplay
└── DuelPanel
The exact component structure can evolve during implementation.

---

<!-- Page 28 -->

## 37. Design-to-Technology Mapping

Design Element Technical Implementation
Adventure Map HTML/CSS/JavaScript
Quest Engine JavaScript state management
Quest Content JSON / JS objects
Prediction JavaScript validation
Dry Run Reusable state-table component
Coding Controlled execution approach
Robot Flask + AI API
Progress Firebase / Firestore
Duel Firestore synchronization
Authentication Firebase or lightweight MVP approach
Version Control Git/GitHub

## 38. MVP Screen Priority

P0 — Must Have
Landing page
Adventure map
Array Forest
Quest introduction
Problem simplifier
Prediction

1.
2.
3.
4.
5.
6.

---

<!-- Page 29 -->

Dry run
Coding
Robot hint ladder
Quest completion
Basic mastery/progress
P1 — If Time Allows
Second quest
Duel Mode
Better progression system
More detailed mastery dashboard
P2 — Future
Boss challenges
Additional regions
External coding-platform tracker
Larger quest library
Advanced visualizations

## 39. Critical Design Decisions

Decision 1 — One Excellent Quest Over Many Average Quests
The MVP should prioritize:
one complete, polished learning experience
over a large question bank. 7. 8. 9. 10. 11.

1.
2.
3.
4.
5.
6.
7.
8.
9.

---

<!-- Page 30 -->

Decision 2 — Interaction Over Decoration
The core demo should visibly demonstrate:
Problem → Prediction → Dry Run → Hint → Code → Mastery
This is more important than elaborate game graphics.
Decision 3 — Robot as Coach
The Robot should guide thinking rather than replace it.
Decision 4 — State-Based Dry Run
A structured state table is preferred for the MVP over complex animated algorithm visualizations.
Decision 5 — Seeded Data Over Risky Integrations
External platform tracking should not become a dependency for the core experience.

## 40. Complete User Journey

The intended experience is:

---

<!-- Page 31 -->

START
│
▼
Welcome to Arcade
│
▼
Adventure Map
│
▼
Array Forest
│
▼
The Lost Maximum
│
▼
"What is asked?"
│
▼
Decompose
│
▼
"What should we track?"
│
▼
Predict
│
▼
Interactive Dry Run
│
▼
Write Code
│
┌────────┴────────┐
│ │
Correct Wrong
│ │
│ Robot Hint
│ │
└────────┬────────┘
▼
Explain
│
▼
Quest Review
│
▼
Mastery + XP
│
▼
Unlock Next Quest

---

<!-- Page 32 -->

## 41. Design Success Criteria

The design is successful if a first-time user can:
Understand what Algorithmic Arcade is within seconds.
Enter Array Forest without instruction.
Understand the purpose of the quest.
Interact with the problem before coding.
Make and receive feedback on a prediction.
Perform a visible dry run.
Request a progressive hint.
Write and test code.
See how their reasoning affected their performance.
Understand what they should improve next.

## 42. Hackathon Demo Design

The strongest demo should not begin by explaining every feature.
Instead:
Step 1
Show the problem:
"Find the maximum element."
Step 2
Ask the audience:
"Most coding platforms would now say: write code."

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.

---

<!-- Page 33 -->

Step 3
Show Algorithmic Arcade asking:
"Before coding—what do you think the maximum tracker becomes?"
Step 4
Perform the dry run.
Step 5
Intentionally make a mistake.
Step 6
Ask the Robot for a hint.
Step 7
Write the code.
Step 8
Show the mastery result.
The final message should be:
We don't just measure whether you solved the problem. We measure how you learned to solve
it.

## 43. Design Differentiator

The visual adventure is not the primary differentiator.
The important design decision is converting traditionally invisible cognitive actions into interactive product
actions.

---

<!-- Page 34 -->

Traditional Coding Platform
Read → Code → Submit → Accepted/Wrong
Algorithmic Arcade
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
Master
This is the central design philosophy of the product.

## 44. Future Design Expansion

Once the core learning system is validated, additional regions can be designed around different DSA
concepts:
Coding Village
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
Each region should preserve the same underlying learning loop while introducing domain-specific interactions.

---

<!-- Page 35 -->

The world can therefore expand without changing the fundamental learning architecture.

## 45. Final Design Summary

Algorithmic Arcade should feel like an adventure game on the surface and a structured problem-solving
trainer underneath.
Its design is built around one central idea:
The hardest part of DSA for beginners is often not writing the code—it is knowing what to think
about before writing it.
Therefore, the product should make those normally invisible steps visible and interactive.
The MVP should deliver one exceptionally polished vertical slice:
Array Forest → The Lost Maximum → Understand → Decompose → Predict → Dry Run → Solve
→ Explain → Review → Mastery
Everything else should support this experience rather than distract from it.
The design priority for the 24-hour hackathon is therefore:
Meaningful interaction > Game decorationLearning feedback > XPOne polished quest > Large
content libraryGuided thinking > Instant AI answersReliable MVP > Risky integrations
Core Design Statement:
Algorithmic Arcade turns the hidden mental steps of DSA problem-solving into an interactive
adventure.
