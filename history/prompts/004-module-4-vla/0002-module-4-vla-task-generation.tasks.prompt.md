---
id: 0002
title: Module 4 VLA Task Generation
stage: tasks
date: 2025-11-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 004-module-4-vla
branch: 004-module-4-vla
user: assistant
command: /sp.tasks
labels: ["educational-content", "vla", "whisper", "llm", "clip", "task-generation", "module-4"]
links:
  spec: specs/004-module-4-vla/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-module-4-vla/tasks.md
tests:
  - Task format validation (all tasks follow checklist format)
  - Learning journey mapping verified
  - Parallel opportunities identified (64 tasks)
  - API security validated (no hardcoded keys)
---

## Prompt

Execute `/sp.tasks` command for Module 4: Vision-Language-Action (VLA).

**Context**: Implementation plan completed (58 lines concise) with 4 learning journeys focused on voice-to-text (Whisper - P1), LLM task planning (GPT-4/Claude - P1), visual grounding (CLIP - P2), and end-to-end VLA pipeline with error recovery (P2).

**Task**: Generate actionable task breakdown following plan → tasks workflow, including:
- Tasks organized by learning journey for VLA component integration
- API security best practices (all examples use .env, no hardcoded keys)
- Cost transparency (API usage estimates in exercises)
- Both GPT-4 and Claude examples (learner choice)
- Prompt template creation and validation
- State machine orchestration for VLA pipeline
- Error recovery and robustness tasks
- MVP scope definition (LJ1 + LJ2 = Voice → LLM planning)

## Response snapshot

Created comprehensive task breakdown (183 tasks) for Module 4 educational content:

**Summary**: Tasks organized into 8 phases with multimodal AI integration:
- Phase 1 (Setup): 5 tasks - module structure with prompts/ subdirectory
- Phase 2 (Foundational): 9 tasks - research (Whisper API vs local, GPT-4 vs Claude), API keys setup, safety guidelines
- Phase 3 (LJ1 - Voice-to-Text): 38 tasks - Chapters 4.1, 4.2, 4.3 + Whisper integration + wake-word detection
- Phase 4 (LJ2 - LLM Planning): 29 tasks - Chapter 4.4 + prompt templates + action primitives + error handling
- Phase 5 (LJ3 - Visual Grounding): 30 tasks - Chapters 4.5, 4.6 + CLIP + depth-based 3D localization
- Phase 6 (LJ4 - VLA Pipeline): 35 tasks - Chapters 4.7, 4.8 + state machines + error recovery
- Phase 7 (Mini-Project): 10 tasks - Chapter 4.9 voice-controlled humanoid assistant
- Phase 8 (Polish): 27 tasks - content validation, mocked API testing, security audit

**Task Organization by Learning Journey**:
- LJ1 (Voice-to-Text - P1): 38 tasks covering Whisper API/local, wake-word detection, ROS 2 integration
- LJ2 (LLM Planning - P1): 29 tasks covering GPT-4/Claude, prompt engineering, action primitives, validation
- LJ3 (Visual Grounding - P2): 30 tasks covering CLIP, depth-based 3D poses, visual-language mapping
- LJ4 (VLA Pipeline - P2): 35 tasks covering state machines, error recovery, confirmation prompts, graceful degradation

**Parallel Opportunities**: 64 tasks (35%) marked [P] can run in parallel:
- All prompt templates (robot_planner_system.txt, clarification_template.txt, etc.)
- All code examples within a chapter (Whisper API, local, ROS node)
- All diagrams (vla-pipeline-overview, llm-planning-flow, error-recovery-flowchart)
- LJ1 (Voice) and LJ2 (LLM) can be developed in parallel (independent components)

**API Security & Cost Management**:
- NO hardcoded API keys in any code example (all use .env files)
- All exercises include cost estimates (~$0.01-$0.50 per command)
- Total module cost: $5-10 for all exercises (transparent upfront)
- Mocked API responses for CI testing (no real API calls in tests)
- Security audit task (T167) validates no secrets in code
- Free tier alternatives documented (local Whisper, open-source LLMs)

**Dependencies & Critical Path**:
- Setup (Phase 1) → Foundational (Phase 2) with API keys + safety docs - BLOCKS all
- LJ1 (Voice) and LJ2 (LLM) can be developed in parallel after Foundational
- LJ3 (Visual Grounding) depends on LJ2 (uses LLM-generated targets)
- LJ4 (VLA Pipeline) depends on LJ1 + LJ2 + LJ3 (orchestrates all)
- Mini-project depends on all learning journeys

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (LJ1) + Phase 4 (LJ2) = 81 tasks
- Delivers voice-to-plan pipeline (no vision yet)
- Learners speak commands → Whisper transcribes → GPT-4/Claude plans actions
- Can test with hardcoded object positions (add vision later)
- Demonstrates core VLA cognitive pipeline

**Checkpoints**:
- After Phase 3 (LJ1): Voice commands published to ROS 2 with <2s latency
- After Phase 4 (LJ2): LLM generates valid action plans for 90%+ of commands
- After Phase 5 (LJ3): CLIP detects objects in 80%+ of images, publishes 3D poses to TF
- After Phase 6 (LJ4): Full VLA pipeline with error recovery (speech confirmation, perception fallback, navigation retry)
- After Phase 8: Complete module with voice-controlled fetch-and-deliver demo

**Implementation Strategy**:
1. MVP-first: Complete LJ1 (Voice) + LJ2 (LLM) → deploy voice-to-plan → validate
2. Incremental: Add LJ3 (Visual Grounding) → add LJ4 (VLA Integration) → mini-project
3. Parallel team: Creator A (LJ1), Creator B (LJ2), Creator C (prompt templates + research)

**Ethical AI & Safety**:
- Reusable partial: docs/_partials/llm-safety-guidelines.md (Rule: refuse unsafe commands)
- LLM validation task (T072-T074): Ensure robots reject harmful instructions
- Cost transparency task (T180): All exercises include API cost estimates
- Privacy considerations in ethical guidelines (voice data handling)

## Outcome

- ✅ Impact: Task breakdown created for Module 4, ready for VLA implementation
- 🧪 Tests: Format validation passed, API security audit included, cost transparency verified
- 📁 Files: tasks.md (183 tasks, API-secure) in specs/004-module-4-vla/
- 🔁 Next prompts: Implement all modules (Modules 2, 3, 4 ready for development)
- 🧠 Reflection: VLA module task generation successfully integrated multimodal AI (voice → language → vision → action) with strong emphasis on API security, cost transparency, and error recovery. Critical additions: Mocked API testing strategy, both GPT-4 and Claude support, ethical AI guidelines, and state machine orchestration for robust execution.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS (task format, API security, cost documentation, error recovery)
- Prompt variant (if applicable): N/A (standard /sp.tasks with API security + cost emphasis)
- Next experiment (smallest change to try): Apply API security pattern (no hardcoded keys, mocked tests) to any future AI-integrated modules, ensure cost transparency is always included for paid APIs
