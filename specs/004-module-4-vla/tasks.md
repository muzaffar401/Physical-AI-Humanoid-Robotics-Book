---
description: "Task list for Module 4: Vision-Language-Action (VLA)"
---

# Tasks: Module 4 - Vision-Language-Action (VLA)

**Input**: Design documents from `/specs/004-module-4-vla/`
**Prerequisites**: plan.md, spec.md (4 learning journeys)

**Organization**: Tasks are grouped by learning journey to enable independent implementation and testing of each VLA component.

## Format: `[ID] [P?] [Journey] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[LJ#]**: Which learning journey this task belongs to (LJ1, LJ2, LJ3, LJ4)
- Include exact file paths in descriptions

## Path Conventions

- **Educational Content**: `book_frontend/docs/module-4/` (chapter markdown files)
- **Assets**: `book_frontend/docs/assets/module-4/` (code examples, diagrams, prompt templates, images)
- **Documentation**: `specs/004-module-4-vla/` (research, data model, contracts)
- **Tests**: `tests/content/` and `tests/code_examples/`

---

## Phase 1: Setup (Project Infrastructure)

**Purpose**: Initialize module structure and configuration

- [X] T001 Create module directory structure at book_frontend/docs/module-4/
- [X] T002 Create assets directory structure at book_frontend/docs/assets/module-4/ with subdirs (code/, prompts/, diagrams/, images/)
- [X] T003 [P] Create _category_.json for Docusaurus sidebar configuration
- [X] T004 [P] Create module index file at book_frontend/docs/module-4/index.md
- [X] T005 [P] Create test directory structure for Module 4 validation

---

## Phase 2: Foundational (Design Documents & Prerequisites)

**Purpose**: Core planning documents that MUST be complete before ANY learning journey content

**⚠️ CRITICAL**: No chapter writing can begin until this phase is complete

- [X] T006 Create research.md with Whisper API vs local decision, GPT-4 vs Claude comparison, CLIP vs OWL-ViT, wake-word library (Porcupine), state machine frameworks (py_trees)
- [X] T007 Create data-model.md with chapter structure, Bloom's taxonomy objectives, dependencies (4.1→4.2-4.3, 4.4, 4.5 requires 4.4, 4.7 requires 4.2+4.4+4.5+4.6)
- [X] T008 Create quickstart.md with API keys setup (.env), microphone requirements, GPU optional (for CLIP), both GPT-4 and Claude examples
- [X] T009 [P] Create contracts/chapter-4-2-whisper-ros-node.md for speech-to-text ROS 2 integration
- [X] T010 [P] Create contracts/chapter-4-4-llm-task-planner.md for LLM-based action planning
- [X] T011 [P] Create contracts/chapter-4-5-visual-grounding.md for CLIP-based object detection
- [X] T012 [P] Create contracts/chapter-4-7-vla-pipeline.md for end-to-end integration
- [X] T013 [P] Create reusable partial at book_frontend/docs/_partials/api-keys-setup.md for OpenAI/Anthropic configuration
- [X] T014 [P] Create reusable partial at book_frontend/docs/_partials/llm-safety-guidelines.md for ethical AI usage

**Checkpoint**: Foundation documents ready - learning journey content implementation can now begin

---

## Phase 3: Learning Journey 1 - Voice-to-Text with OpenAI Whisper (Priority: P1) 🎯 MVP

**Goal**: Learners can capture microphone audio, transcribe with Whisper (API or local), publish transcripts to ROS 2 `/voice_command` topic with <2s latency

**Independent Test**: Speak command "Move forward 2 meters," Whisper transcribes, publishes to `/voice_command`, another ROS 2 node receives transcript

### Chapter 4.1: Introduction to Vision-Language-Action

- [X] T015 [LJ1] Write chapter-4-1-introduction.md with VLA paradigm overview, real-world examples (Everyday Robots, Tesla Optimus), module roadmap
- [X] T016 [LJ1] Add learning objectives (Remember: define VLA, Understand: explain voice → vision → action flow)
- [X] T017 [P] [LJ1] Create vla-pipeline-overview.svg diagram showing Whisper → LLM → CLIP → Robot actions
- [X] T018 [LJ1] Add hands-on preview: Complete VLA demo walkthrough (what learners will build)
- [X] T019 [LJ1] Add prerequisite review: Module 1 pub/sub, Module 2/3 simulation, API key requirements
- [X] T020 [LJ1] Add chapter summary and transition to Chapter 4.2

### Chapter 4.2: Speech-to-Text with Whisper

- [X] T021 [LJ1] Write chapter-4-2-speech-to-text.md covering ASR fundamentals, Whisper model, API vs local
- [X] T022 [LJ1] Add learning objectives (Apply: transcribe audio with Whisper, Create: ROS 2 voice input node)
- [X] T023 [P] [LJ1] Create whisper-architecture.svg diagram showing encoder-decoder Transformer
- [X] T024 [LJ1] Add Whisper fundamentals: Why Whisper (99 languages, noise robust), model sizes (tiny, base, small, medium, large)
- [X] T025 [LJ1] Add API-based approach: OpenAI Whisper API, cost (~$0.006/minute), latency (~1-2s)
- [X] T026 [P] [LJ1] Create code example at book_frontend/docs/assets/module-4/code/chapter-4-2/whisper_api_basic.py
- [X] T027 [LJ1] Add guided walkthrough: Record 5-second audio, send to Whisper API, print transcript
- [X] T028 [LJ1] Add exercise 1: Test Whisper with different accents (record in various languages), verify accuracy
- [X] T029 [LJ1] Add local Whisper approach: `pip install openai-whisper`, GPU acceleration (faster-whisper)
- [X] T030 [P] [LJ1] Create code example at book_frontend/docs/assets/module-4/code/chapter-4-2/whisper_local_basic.py
- [X] T031 [LJ1] Add exercise 2: Compare API vs local latency and accuracy on same audio clip
- [X] T032 [LJ1] Add ROS 2 integration: Create WhisperNode that publishes to `/voice_command` (String message)
- [X] T033 [P] [LJ1] Create whisper_ros_node.py at book_frontend/docs/assets/module-4/code/chapter-4-2/
- [X] T034 [LJ1] Add guided walkthrough: Run WhisperNode, speak into mic, verify topic with `ros2 topic echo /voice_command`
- [X] T035 [LJ1] Add exercise 3: Implement streaming transcription (continuously listen, not single-shot)
- [X] T036 [LJ1] Add milestone validation: Voice commands published to ROS 2 with <2s latency

### Chapter 4.3: Wake-Word Detection and Audio Processing

- [ ] T037 [LJ1] Write chapter-4-3-wake-word.md covering wake-word detection, audio filtering, noise reduction
- [ ] T038 [LJ1] Add learning objectives (Apply: integrate wake-word, Analyze: tune audio preprocessing)
- [ ] T039 [P] [LJ1] Create wake-word-flow.svg diagram showing audio stream → wake-word detector → Whisper
- [ ] T040 [LJ1] Add wake-word fundamentals: Why needed (reduce false triggers), libraries (Porcupine, Snowboy, Pocketsphinx)
- [ ] T041 [LJ1] Add Porcupine integration: Free tier setup, "Hey Robot" wake-word, callback on detection
- [ ] T042 [P] [LJ1] Create porcupine_wake_word.py example at book_frontend/docs/assets/module-4/code/chapter-4-3/
- [ ] T043 [LJ1] Add guided walkthrough: Run wake-word node, say "Hey Robot, turn left," only "turn left" transcribed
- [ ] T044 [LJ1] Add exercise 1: Test in noisy environment (background music), verify wake-word still triggers
- [ ] T045 [LJ1] Add audio preprocessing: Noise reduction (noisereduce library), VAD (Voice Activity Detection)
- [ ] T046 [P] [LJ1] Create audio_preprocessing.py utility functions
- [ ] T047 [LJ1] Add exercise 2: Apply noise reduction before Whisper, compare transcription accuracy
- [ ] T048 [LJ1] Add milestone validation: Wake-word detection working with <500ms latency

### Voice-to-Text Assets

- [ ] T049 [P] [LJ1] Create screenshot microphone-setup.webp showing USB mic and audio levels
- [ ] T050 [P] [LJ1] Create screenshot ros-voice-command-topic.webp showing RViz2 or rqt with /voice_command
- [ ] T051 [P] [LJ1] Create audio-pipeline-diagram.svg showing mic → preprocessing → wake-word → Whisper → ROS 2
- [ ] T052 [P] [LJ1] Create code validation test at tests/code_examples/test_chapter_4_2_whisper.py (mocked Whisper API)

**Checkpoint**: Learning Journey 1 complete - learners have robust voice input to ROS 2

---

## Phase 4: Learning Journey 2 - LLM-Based Task Planning (Priority: P1)

**Goal**: Learners can send natural language commands to GPT-4/Claude, receive structured action plans (JSON), parse plans, and convert to ROS 2 messages

**Independent Test**: Send "Pick up the red box" to LLM, receive plan `[{action: navigate, target: red box}, {action: grasp, object: red box}]`, parse and map to ROS 2

### Chapter 4.4: LLMs for Cognitive Planning

- [ ] T053 [LJ2] Write chapter-4-4-llm-planning.md covering LLM capabilities, prompt engineering, action decomposition
- [ ] T054 [LJ2] Add learning objectives (Understand: explain LLM reasoning, Create: design prompts for robot planning)
- [ ] T055 [P] [LJ2] Create llm-planning-flow.svg diagram showing command → prompt → LLM → JSON plan → action executor
- [ ] T056 [LJ2] Add LLM fundamentals: GPT-4 vs Claude 3, API costs (~$0.01-$0.10/command), context limits (8k-100k tokens)
- [ ] T057 [LJ2] Add prompt engineering: System message (robot capabilities), few-shot examples, output format (JSON schema)
- [ ] T058 [P] [LJ2] Create prompt template at book_frontend/docs/assets/module-4/prompts/robot_planner_system.txt
- [ ] T059 [P] [LJ2] Create few-shot examples at book_frontend/docs/assets/module-4/prompts/planning_examples.json
- [ ] T060 [LJ2] Add guided walkthrough: Send "Bring me the blue cup" to GPT-4 with prompt, inspect JSON response
- [ ] T061 [LJ2] Add exercise 1: Test with 5 different commands, verify LLM generates valid action sequences
- [ ] T062 [LJ2] Add action primitives: Define robot vocabulary (navigate, grasp, place, search, wait)
- [ ] T063 [P] [LJ2] Create action_primitives.py with primitive definitions and validators
- [ ] T064 [LJ2] Add exercise 2: Validate LLM output (all actions in primitives list, required fields present)
- [ ] T065 [LJ2] Add ROS 2 integration: LLMPlannerNode subscribes to `/voice_command`, publishes to `/action_plan`
- [ ] T066 [P] [LJ2] Create llm_planner_node.py at book_frontend/docs/assets/module-4/code/chapter-4-4/
- [ ] T067 [LJ2] Add guided walkthrough: Chain WhisperNode → LLMPlannerNode, verify plans published
- [ ] T068 [LJ2] Add milestone validation: LLM generates valid action plans for 90%+ of test commands

### Chapter 4.4B: Handling Ambiguity and Errors

- [ ] T069 [LJ2] Add section on ambiguous commands: "Bring me that" → LLM asks clarifying question
- [ ] T070 [P] [LJ2] Create clarification prompt template at book_frontend/docs/assets/module-4/prompts/clarification_template.txt
- [ ] T071 [LJ2] Add exercise 3: Test ambiguous commands, verify LLM requests more information
- [ ] T072 [LJ2] Add error handling: Invalid actions, contradictory plans, impossible requests
- [ ] T073 [P] [LJ2] Create plan_validator.py with safety and feasibility checks
- [ ] T074 [LJ2] Add exercise 4: Send "Fly to the moon," verify LLM refuses or flags as infeasible
- [ ] T075 [LJ2] Add GPT-4 vs Claude comparison: Test same commands with both models, compare plan quality
- [ ] T076 [P] [LJ2] Create comparison table for documentation
- [ ] T077 [LJ2] Add milestone validation: LLM handles ambiguity and refuses unsafe commands

### LLM Planning Assets

- [ ] T078 [P] [LJ2] Create screenshot gpt4-response-example.webp showing API response with JSON plan
- [ ] T079 [P] [LJ2] Create action-primitive-taxonomy.svg showing action types and parameters
- [ ] T080 [P] [LJ2] Create prompt-engineering-diagram.svg showing system + few-shot + user prompt structure
- [ ] T081 [P] [LJ2] Create code validation test at tests/code_examples/test_chapter_4_4_llm_mock.py (mocked API)

**Checkpoint**: Learning Journey 2 complete - learners have LLM-based cognitive planning

---

## Phase 5: Learning Journey 3 - Visual Grounding (Priority: P2)

**Goal**: Learners can match text queries ("red box") to image regions using CLIP, compute 3D object poses from depth data, and publish to TF for navigation

**Independent Test**: Send "red box" with RGB-D image to visual grounding node, receive 3D coordinates, navigate robot to object in simulation

### Chapter 4.5: Visual Grounding with CLIP

- [ ] T082 [LJ3] Write chapter-4-5-visual-grounding.md covering vision-language models, CLIP, object localization
- [ ] T083 [LJ3] Add learning objectives (Apply: use CLIP for object detection, Create: 3D pose estimation from depth)
- [ ] T084 [P] [LJ3] Create visual-grounding-concept.svg diagram showing text query + image → CLIP → bounding box + depth → 3D pose
- [ ] T085 [LJ3] Add CLIP fundamentals: Contrastive learning, zero-shot classification, text-image similarity scores
- [ ] T086 [LJ3] Add basic CLIP usage: Query "red box" against image patches, find highest similarity region
- [ ] T087 [P] [LJ3] Create clip_basic_example.py at book_frontend/docs/assets/module-4/code/chapter-4-5/
- [ ] T088 [LJ3] Add guided walkthrough: Load image with red/blue/green boxes, query CLIP with "red box," visualize result
- [ ] T089 [LJ3] Add exercise 1: Test CLIP with 10 object descriptions, measure accuracy (% correct detections)
- [ ] T090 [LJ3] Add sliding window approach: Divide image into grid, run CLIP on each patch, find best match
- [ ] T091 [P] [LJ3] Create clip_object_detector.py with sliding window implementation
- [ ] T092 [LJ3] Add exercise 2: Detect "blue cup" in cluttered scene with multiple objects
- [ ] T093 [LJ3] Add alternative: OWL-ViT (open-vocabulary object detector), comparison with CLIP
- [ ] T094 [P] [LJ3] Create owlvit_example.py (optional, for learners with GPUs)
- [ ] T095 [LJ3] Add milestone validation: CLIP correctly identifies target objects in 80%+ of test images

### Chapter 4.6: 3D Pose Estimation and Action Primitives

- [ ] T096 [LJ3] Write chapter section on depth-based 3D localization
- [ ] T097 [LJ3] Add depth integration: Given bounding box + depth image, compute 3D position in camera frame
- [ ] T098 [P] [LJ3] Create depth_to_3d.py utility functions at book_frontend/docs/assets/module-4/code/chapter-4-6/
- [ ] T099 [LJ3] Add guided walkthrough: Detect "red box" with CLIP, use depth camera to get 3D coordinates
- [ ] T100 [LJ3] Add exercise 1: Publish detected object pose to TF (`/detected_object` frame)
- [ ] T101 [LJ3] Add ROS 2 integration: VisualGroundingNode subscribes to `/camera/image` and `/camera/depth`, publishes to `/object_pose`
- [ ] T102 [P] [LJ3] Create visual_grounding_node.py at book_frontend/docs/assets/module-4/code/chapter-4-6/
- [ ] T103 [LJ3] Add exercise 2: Use `/object_pose` as Nav2 goal, navigate robot to detected object
- [ ] T104 [LJ3] Add action primitive integration: Map LLM action "navigate to red box" → visual grounding → Nav2 goal
- [ ] T105 [P] [LJ3] Create action_executor.py that interprets LLM plans and calls visual grounding
- [ ] T106 [LJ3] Add exercise 3: End-to-end test - voice "Go to the blue cup" → LLM plan → visual grounding → navigation
- [ ] T107 [LJ3] Add milestone validation: Robot autonomously navigates to visually detected objects

### Visual Grounding Assets

- [ ] T108 [P] [LJ3] Create screenshot clip-detection-example.webp showing image with bounding boxes and similarity scores
- [ ] T109 [P] [LJ3] Create screenshot rviz-detected-object-tf.webp showing TF frame for detected object
- [ ] T110 [P] [LJ3] Create depth-to-3d-diagram.svg showing pixel coordinates → depth → 3D transform
- [ ] T111 [P] [LJ3] Create code validation test at tests/code_examples/test_chapter_4_5_clip.py

**Checkpoint**: Learning Journey 3 complete - learners connect language to visual perception

---

## Phase 6: Learning Journey 4 - End-to-End VLA Pipeline with Error Recovery (Priority: P2)

**Goal**: Learners integrate all VLA components (Whisper → LLM → CLIP → Nav2/Gripper) with state machine orchestration and error recovery

**Independent Test**: Voice "Bring the blue cup to me" → full pipeline execution (transcribe → plan → locate → navigate → grasp → return) with recovery from 1+ failures

### Chapter 4.7: VLA Pipeline Integration with State Machines

- [ ] T112 [LJ4] Write chapter-4-7-vla-integration.md covering state machine orchestration, component integration
- [ ] T113 [LJ4] Add learning objectives (Create: implement VLA state machine, Evaluate: test full pipeline)
- [ ] T114 [P] [LJ4] Create vla-state-machine.svg diagram showing states (Listening, Planning, Executing, Error, Success)
- [ ] T115 [LJ4] Add state machine fundamentals: Why needed (manage complex flows), libraries (py_trees, SMACH, custom)
- [ ] T116 [LJ4] Add py_trees approach: Behavior tree for VLA (sequence nodes, fallback nodes, decorators)
- [ ] T117 [P] [LJ4] Create vla_behavior_tree.py at book_frontend/docs/assets/module-4/code/chapter-4-7/
- [ ] T118 [LJ4] Add guided walkthrough: Define VLA states - Listen → Plan → Ground → Navigate → Execute → Report
- [ ] T119 [LJ4] Add exercise 1: Implement simple state machine that chains Whisper → LLM → visual grounding
- [ ] T120 [LJ4] Add component integration: Connect all ROS 2 nodes (WhisperNode, LLMPlannerNode, VisualGroundingNode, ActionExecutor)
- [ ] T121 [P] [LJ4] Create vla_orchestrator_node.py that manages state transitions
- [ ] T122 [LJ4] Add guided walkthrough: Launch full VLA stack, give voice command, observe state transitions in logs
- [ ] T123 [LJ4] Add exercise 2: Test end-to-end command "Pick up the wrench" in Isaac Sim or Gazebo
- [ ] T124 [LJ4] Add milestone validation: Full VLA pipeline executes successfully for simple commands

### Chapter 4.8: Error Recovery and Robustness

- [ ] T125 [LJ4] Write chapter-4-8-error-recovery.md covering failure modes, retry logic, graceful degradation
- [ ] T126 [LJ4] Add learning objectives (Analyze: identify failure modes, Create: implement recovery strategies)
- [ ] T127 [P] [LJ4] Create error-recovery-flowchart.svg showing failure detection → diagnosis → recovery action
- [ ] T128 [LJ4] Add common failure modes: Speech misrecognition, LLM hallucination, object not found, navigation failure
- [ ] T129 [LJ4] Add speech confirmation: After Whisper transcription, confirm with user ("Did you say X?")
- [ ] T130 [P] [LJ4] Create confirmation_handler.py for user feedback loop
- [ ] T131 [LJ4] Add exercise 1: Intentionally misrecognize command, verify confirmation prompt triggers
- [ ] T132 [LJ4] Add LLM validation: Check if planned actions are feasible given environment state
- [ ] T133 [P] [LJ4] Create plan_feasibility_checker.py that validates against known obstacles
- [ ] T134 [LJ4] Add exercise 2: LLM plans to navigate through wall, validator rejects and asks LLM for replan
- [ ] T135 [LJ4] Add perception failure handling: Object moved during execution, not visible, occluded
- [ ] T136 [P] [LJ4] Create perception_fallback.py that triggers LLM replan on perception failure
- [ ] T137 [LJ4] Add exercise 3: Move object mid-task, verify robot detects absence and triggers replan
- [ ] T138 [LJ4] Add navigation failure recovery: Path blocked → Nav2 fails → report to LLM → suggest alternative
- [ ] T139 [P] [LJ4] Create navigation_recovery.py with retry and fallback strategies
- [ ] T140 [LJ4] Add exercise 4: Block robot's path, verify it detects failure and reports to user or replans
- [ ] T141 [LJ4] Add graceful degradation: If all retries fail, return to start position and report failure to user
- [ ] T142 [LJ4] Add milestone validation: VLA pipeline recovers from at least 3 failure types

### VLA Integration Assets

- [ ] T143 [P] [LJ4] Create screenshot vla-full-demo.webp showing all ROS 2 nodes running (rqt_graph)
- [ ] T144 [P] [LJ4] Create screenshot state-machine-visualization.webp showing py_trees or SMACH GUI
- [ ] T145 [P] [LJ4] Create error-recovery-examples.svg showing before/after recovery scenarios
- [ ] T146 [P] [LJ4] Create code validation test at tests/code_examples/test_chapter_4_7_state_machine.py

**Checkpoint**: Learning Journey 4 complete - learners have robust, production-like VLA system

---

## Phase 7: Mini-Project and Integration

**Purpose**: Integrative mini-project demonstrating complete VLA capability

### Chapter 4.9: Mini-Project - Voice-Controlled Humanoid Assistant

- [ ] T147 Write chapter-4-9-mini-project.md with comprehensive VLA project requirements
- [ ] T148 Add project goal: Humanoid responds to voice commands for fetch-and-deliver tasks in simulated home
- [ ] T149 Add requirements: Whisper for voice, GPT-4/Claude for planning, CLIP for object detection, Nav2 for navigation
- [ ] T150 Add assessment rubric: Speech accuracy (15%), Plan quality (20%), Visual grounding (20%), Navigation (20%), Error recovery (15%), Integration (10%)
- [ ] T151 [P] Create home_environment.sdf (Gazebo) or home_scene.usd (Isaac Sim) at book_frontend/docs/assets/module-4/
- [ ] T152 [P] Create mini_project_vla_stack.py complete VLA system
- [ ] T153 Add success criteria: Complete 5 fetch tasks with 80%+ success rate, recover from 2+ error types
- [ ] T154 Add test scenarios: "Bring the red mug from kitchen," "Find the blue book," "Put the wrench on the table"
- [ ] T155 Add extension challenges: Multi-object tasks, multi-turn dialogue, custom action primitives (open drawer)
- [ ] T156 Create vla-complete-architecture.svg showing all Module 4 components integrated

**Checkpoint**: Complete mini-project demonstrates VLA mastery

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Content validation, quality assurance, and documentation

### Documentation & Index

- [ ] T157 [P] Write comprehensive module index at book_frontend/docs/module-4/index.md
- [ ] T158 [P] Add API keys warning in index (costs, rate limits, security best practices)
- [ ] T159 [P] Add module navigation links to all chapter files
- [ ] T160 [P] Add ethical AI guidelines section (don't execute unsafe commands, privacy considerations)

### Content Validation

- [ ] T161 [P] Create test_markdown_lint.py for Vale linting
- [ ] T162 [P] Create test_links.py for link checking
- [ ] T163 [P] Create test_accessibility.py for WCAG 2.1 AA compliance
- [ ] T164 Run Vale linting on all Module 4 chapters
- [ ] T165 Run markdown-link-check on all chapter files
- [ ] T166 Verify all images have alt text and <200KB file size
- [ ] T167 Validate all Python code examples (syntax, imports, no hardcoded API keys)
- [ ] T168 Verify all prompt templates use .env for API keys (no secrets in code)

### VLA-Specific Testing

- [ ] T169 [P] Test Whisper examples with mocked API responses (for CI without API keys)
- [ ] T170 [P] Test LLM planner with mocked GPT-4/Claude responses
- [ ] T171 [P] Test CLIP examples with sample images (no network required for CI)
- [ ] T172 Verify state machine examples can run in dry-run mode (no simulation needed)
- [ ] T173 Test all ROS 2 nodes can launch without API keys (graceful degradation)

### Docusaurus Build & Performance

- [ ] T174 Run Docusaurus build and verify no errors
- [ ] T175 Verify page load time <3s for all module pages
- [ ] T176 Compress all screenshot images to <200KB (WebP format)
- [ ] T177 Verify all SVG diagrams render correctly

### Final Review

- [ ] T178 Review all learning objectives are addressed
- [ ] T179 Verify chapter dependencies (4.1→4.2-4.3, 4.4, 4.5 requires 4.4, 4.7 requires 4.2+4.4+4.5+4.6)
- [ ] T180 Check all exercises have clear API cost estimates (transparency)
- [ ] T181 Validate milestone tests align with learning journey goals
- [ ] T182 Run quickstart.md validation (API keys, microphone, .env setup)
- [ ] T183 Verify both GPT-4 and Claude examples work (don't favor one API)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all learning journeys
- **Learning Journeys (Phase 3-6)**: All depend on Foundational phase completion
  - LJ1 (Voice-to-Text - P1): Can start after Foundational
  - LJ2 (LLM Planning - P1): Can start after Foundational (parallel with LJ1)
  - LJ3 (Visual Grounding - P2): Depends on LJ2 (needs LLM output to know what to look for)
  - LJ4 (VLA Pipeline - P2): Depends on LJ1 + LJ2 + LJ3 (integrates all)
- **Mini-Project (Phase 7)**: Depends on all LJ1-4 complete
- **Polish (Phase 8)**: Depends on all content chapters being complete

### Learning Journey Dependencies

- **LJ1 (Voice-to-Text)**: Independent - foundational for VLA
- **LJ2 (LLM Planning)**: Independent - can develop in parallel with LJ1
- **LJ3 (Visual Grounding)**: Depends on LJ2 (uses LLM-generated targets for grounding)
- **LJ4 (VLA Pipeline)**: Depends on LJ1 + LJ2 + LJ3 (orchestrates all components)

### Critical Path for MVP

Minimum viable module: LJ1 (Voice) + LJ2 (LLM Planning)
- Learners get voice-to-plan pipeline (no vision yet)
- Can test with pre-positioned objects (hardcoded positions instead of visual grounding)
- Add LJ3+LJ4 for complete VLA

### Within Each Learning Journey

- Chapter writing before code examples/diagrams
- Prompt templates marked [P] can be created in parallel
- Code examples marked [P] can be created in parallel
- Diagrams marked [P] can be created in parallel
- Exercises follow guided walkthroughs
- Milestone validation at end of each learning journey

### Parallel Opportunities

- All Setup tasks (T001-T005) can run in parallel
- All Foundational contracts (T009-T012) can run in parallel
- All Foundational partials (T013-T014) can run in parallel
- Once Foundational completes:
  - LJ1 (Voice) and LJ2 (LLM) can be developed in parallel
- Within each LJ: prompt templates, code examples, diagrams marked [P] can run in parallel
- All Polish tasks marked [P] can run in parallel after content complete

---

## Parallel Example: Learning Journey 2 (LLM Planning)

```bash
# After Chapter 4.4 content is written, launch all assets together:
Task: "Create robot_planner_system.txt prompt template"
Task: "Create planning_examples.json few-shot examples"
Task: "Create action_primitives.py"
Task: "Create llm_planner_node.py"
Task: "Create llm-planning-flow.svg diagram"

# After ambiguity section is written, launch all assets together:
Task: "Create clarification_template.txt"
Task: "Create plan_validator.py"
Task: "Create comparison table for GPT-4 vs Claude"
```

---

## Implementation Strategy

### MVP First (LJ1 + LJ2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: Learning Journey 1 (Voice-to-Text)
4. Complete Phase 4: Learning Journey 2 (LLM Planning)
5. **STOP and VALIDATE**: Voice commands → LLM action plans (no vision yet)
6. Deploy/demo (core VLA cognitive pipeline working)

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add LJ1 (Voice) → Test independently → Deploy/Demo
3. Add LJ2 (LLM) → Test independently → Deploy/Demo (MVP!)
4. Add LJ3 (Visual Grounding) → Test independently → Deploy/Demo
5. Add LJ4 (VLA Pipeline) → Test independently → Deploy/Demo
6. Add Chapter 4.9 (Mini-Project) → Complete module

### Parallel Team Strategy

With multiple content creators:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Creator A: LJ1 (Voice-to-Text) - Chapters 4.1, 4.2, 4.3
   - Creator B: LJ2 (LLM Planning) - Chapter 4.4
   - Creator C: Prompt templates, research on CLIP vs OWL-ViT
3. After LJ1 + LJ2 complete:
   - Creator A+C: LJ3 (Visual Grounding) - Chapters 4.5, 4.6
   - Creator B: LJ4 (VLA Pipeline) - Chapters 4.7, 4.8
4. All creators: Chapter 4.9 (Mini-Project) integration and polish

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [LJ#] label maps task to specific learning journey
- **API Keys Required**: All Whisper and LLM tasks need API keys (OpenAI or Anthropic)
- **Cost Transparency**: All exercises include estimated API costs (~$0.01-$0.50 per command)
- **Security**: NO hardcoded API keys in code - all examples use .env files
- **Mocking**: Tests use mocked API responses (no real API calls in CI)
- **GPU Optional**: CLIP works on CPU (slower), GPU recommended for real-time performance
- **Microphone Required**: All voice tasks need microphone access
- **Both LLMs Supported**: Examples provided for both GPT-4 and Claude (learner choice)
- Accessibility: All screenshots need descriptive alt text

---

## Task Count Summary

- **Total Tasks**: 183
- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 9 tasks
- **Phase 3 (LJ1 - Voice-to-Text)**: 38 tasks
- **Phase 4 (LJ2 - LLM Planning)**: 29 tasks
- **Phase 5 (LJ3 - Visual Grounding)**: 30 tasks
- **Phase 6 (LJ4 - VLA Pipeline)**: 35 tasks
- **Phase 7 (Mini-Project)**: 10 tasks
- **Phase 8 (Polish)**: 27 tasks

**Parallel Opportunities**: 64 tasks marked [P] can run in parallel (35% of total)

**API Requirements**:
- OpenAI API key (for Whisper + GPT-4) OR Anthropic API key (for Claude 3)
- Estimated cost for full module: $5-10 (includes all exercises)
- Free tier alternatives: Local Whisper (slower), open-source LLMs (lower quality)

**Hardware Requirements**:
- Microphone (any USB mic or laptop mic)
- GPU recommended for CLIP (RTX 2060+), but works on CPU
- 16GB+ RAM for local Whisper (if not using API)

**Independent Test Criteria**:
- LJ1: Voice commands published to ROS 2 with <2s latency
- LJ2: LLM generates valid action plans for 90%+ of test commands
- LJ3: CLIP detects target objects in 80%+ of test images
- LJ4: Full VLA pipeline executes with recovery from 3+ failure types

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (LJ1) + Phase 4 (LJ2) = Voice-to-Plan pipeline
