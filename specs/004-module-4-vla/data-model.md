# Data Model: Module 4 - Vision-Language-Action (VLA)

**Feature**: Module 4 - VLA
**Date**: 2025-12-01
**Purpose**: Defines content structure, learning objectives taxonomy, chapter dependencies, and assessment criteria

## Content Structure

### Module 4 Overview

- **Module Number**: 4
- **Module Title**: Vision-Language-Action (VLA)
- **Total Duration**: 10 hours over 3-4 weeks
- **Chapter Count**: 9 chapters
- **Learning Journeys**: 4 (LJ1-LJ4)
- **Mini-Project**: 1 (integrative VLA system)

---

## Chapter Structure

### Chapter 4.1: Introduction to Vision-Language-Action

**Learning Journey**: LJ1 (Voice-to-Text)
**Duration**: 1 hour
**Prerequisites**: Module 1 complete (ROS 2 fundamentals), Module 2 OR 3 complete (simulation)

**Learning Objectives** (Bloom's Taxonomy):
- **Remember**: Define Vision-Language-Action (VLA) paradigm and its three components
- **Understand**: Explain how VLA enables natural human-robot interaction vs traditional programming
- **Understand**: Describe the VLA pipeline flow (Voice → Language Understanding → Visual Grounding → Action Execution)

**Topics**:
- What is VLA? (Definition, real-world examples: Everyday Robots, Tesla Optimus, Google RT-2)
- Why VLA matters (Natural interaction, adaptability, common-sense reasoning)
- Module roadmap (4 learning journeys, technologies: Whisper, GPT-4/Claude, CLIP, ROS 2)
- Prerequisites review (ROS 2 pub/sub from Module 1, Nav2 from Module 3, API keys)

**Deliverables**:
- Chapter content (introduction.md)
- VLA pipeline overview diagram (SVG)
- Hands-on preview walkthrough (what learners will build by module end)

**Dependencies**: None (foundational chapter)

---

### Chapter 4.2: Speech-to-Text with Whisper

**Learning Journey**: LJ1 (Voice-to-Text)
**Duration**: 2 hours
**Prerequisites**: Chapter 4.1

**Learning Objectives** (Bloom's Taxonomy):
- **Understand**: Explain how automatic speech recognition (ASR) works and why Whisper is state-of-the-art
- **Apply**: Transcribe audio using OpenAI Whisper API and local Whisper models
- **Apply**: Compare API-based vs local Whisper (latency, cost, accuracy trade-offs)
- **Create**: Build ROS 2 WhisperNode that publishes transcriptions to `/voice_command` topic

**Topics**:
- ASR fundamentals (acoustic model, language model, decoder)
- Whisper architecture (encoder-decoder Transformer, multilingual, robust to noise)
- Whisper API usage (OpenAI API, costs, latency)
- Local Whisper deployment (openai-whisper, faster-whisper, GPU acceleration)
- ROS 2 integration (WhisperNode, audio capture, topic publishing)

**Code Examples**:
- `whisper_api_basic.py` - Simple API transcription
- `whisper_local_basic.py` - Local model transcription
- `whisper_ros_node.py` - ROS 2 node with `/voice_command` publishing

**Exercises**:
1. Test Whisper with different accents and languages (verify accuracy)
2. Compare API vs local latency on same audio clip (measure and tabulate)
3. Implement streaming transcription (continuous listening, not single-shot)

**Assessment**:
- **Milestone**: Voice commands published to ROS 2 topic with <2s latency, verified with `ros2 topic echo`

**Dependencies**: Chapter 4.1 (VLA overview), Module 1 Chapter 1.2 (ROS 2 pub/sub)

---

### Chapter 4.3: Wake-Word Detection and Audio Processing

**Learning Journey**: LJ1 (Voice-to-Text)
**Duration**: 1.5 hours
**Prerequisites**: Chapter 4.2

**Learning Objectives** (Bloom's Taxonomy):
- **Understand**: Explain why wake-word detection is needed (reduce false triggers)
- **Apply**: Integrate Porcupine wake-word detection ("Hey Robot")
- **Analyze**: Tune audio preprocessing (noise reduction, VAD) to improve transcription accuracy

**Topics**:
- Wake-word detection fundamentals (keyword spotting vs continuous recognition)
- Porcupine setup (API key, wake-word models, callback integration)
- Audio preprocessing (noise reduction with `noisereduce`, Voice Activity Detection)
- Audio pipeline architecture (Mic → Preprocess → Wake-word → Whisper → ROS 2)

**Code Examples**:
- `porcupine_wake_word.py` - Porcupine integration
- `audio_preprocessing.py` - Noise reduction and VAD utilities

**Exercises**:
1. Test wake-word in noisy environment (background music), verify triggering
2. Apply noise reduction before Whisper, compare transcription accuracy (with/without)

**Assessment**:
- **Milestone**: Wake-word detection working with <500ms latency, only post-wake speech transcribed

**Dependencies**: Chapter 4.2 (Whisper integration), audio capture infrastructure

---

### Chapter 4.4: LLMs for Cognitive Planning

**Learning Journey**: LJ2 (LLM Task Planning)
**Duration**: 2.5 hours
**Prerequisites**: Chapter 4.1 (can be done parallel with LJ1 chapters 4.2-4.3)

**Learning Objectives** (Bloom's Taxonomy):
- **Understand**: Explain how LLMs perform common-sense reasoning for robot task planning
- **Understand**: Compare GPT-4 vs Claude 3 (costs, context limits, safety guardrails)
- **Apply**: Design prompts for robot planning (system message, few-shot examples, JSON output schema)
- **Create**: Build LLMPlannerNode that subscribes to `/voice_command`, publishes to `/action_plan`
- **Evaluate**: Validate LLM output (check action primitives, required fields, safety)

**Topics**:
- LLM capabilities (reasoning, task decomposition, natural language understanding)
- GPT-4 vs Claude comparison (API costs, context windows, latency, safety)
- Prompt engineering (system message: robot capabilities, few-shot examples, output format)
- Action primitives (navigate, grasp, place, search, wait)
- Handling ambiguity (clarifying questions when command unclear)
- Error handling (LLM hallucination, invalid actions, safety validation)

**Code Examples**:
- `robot_planner_system.txt` - System prompt template
- `planning_examples.json` - Few-shot examples
- `action_primitives.py` - Action definitions and validators
- `llm_planner_node.py` - ROS 2 node (voice → LLM → action plan)
- `plan_validator.py` - Safety and feasibility checks

**Exercises**:
1. Test LLM with 5 different commands, verify valid action sequences generated
2. Send ambiguous command ("Bring me that"), verify LLM asks clarification
3. Validate LLM output (all actions in primitives list, required fields present)
4. Send unsafe command ("Fly to the moon"), verify LLM refuses or flags as infeasible

**Assessment**:
- **Milestone**: LLM generates valid action plans for 90%+ of test commands, handles ambiguity, refuses unsafe commands

**Dependencies**: Chapter 4.1 (VLA overview), API keys setup (OpenAI OR Anthropic)

---

### Chapter 4.5: Visual Grounding with CLIP

**Learning Journey**: LJ3 (Visual Grounding)
**Duration**: 2 hours
**Prerequisites**: Chapter 4.4 (needs LLM output to know what to look for)

**Learning Objectives** (Bloom's Taxonomy):
- **Understand**: Explain vision-language models and CLIP's contrastive learning approach
- **Apply**: Use CLIP to match text queries ("red box") to image regions (zero-shot detection)
- **Apply**: Compare CLIP vs OWL-ViT for object detection (accuracy, speed, complexity trade-offs)
- **Create**: Build visual grounding node that detects objects based on text descriptions

**Topics**:
- Vision-language models (multimodal embeddings, text-image similarity)
- CLIP fundamentals (contrastive pre-training, zero-shot classification)
- Sliding window approach (divide image into grid, run CLIP on patches, find best match)
- OWL-ViT alternative (open-vocabulary object detector, better localization)
- Performance considerations (CPU vs GPU, latency, accuracy)

**Code Examples**:
- `clip_basic_example.py` - Query CLIP with text, get similarity scores
- `clip_object_detector.py` - Sliding window object detection
- `owlvit_example.py` - OWL-ViT alternative (optional, GPU recommended)

**Exercises**:
1. Test CLIP with 10 object descriptions, measure accuracy (% correct detections)
2. Detect "blue cup" in cluttered scene with multiple objects
3. Compare CLIP vs OWL-ViT (accuracy, speed, GPU requirements)

**Assessment**:
- **Milestone**: CLIP correctly identifies target objects in 80%+ of test images

**Dependencies**: Chapter 4.4 (LLM generates object descriptions), Module 3 camera integration (RGB images)

---

### Chapter 4.6: 3D Pose Estimation and Action Primitives

**Learning Journey**: LJ3 (Visual Grounding)
**Duration**: 1.5 hours
**Prerequisites**: Chapter 4.5 (CLIP object detection)

**Learning Objectives** (Bloom's Taxonomy):
- **Apply**: Compute 3D object positions from bounding box + depth data
- **Apply**: Publish detected object poses to TF (`/detected_object` frame)
- **Create**: Map LLM actions to ROS 2 primitives (navigate → Nav2 goal, grasp → gripper command)
- **Evaluate**: Test end-to-end voice → visual grounding → navigation workflow

**Topics**:
- Depth-based 3D localization (bounding box → depth → 3D position in camera frame)
- Camera intrinsics and projection (pixel coordinates → 3D world coordinates)
- TF integration (publish detected object frames, transform to robot base frame)
- Action primitive mapping (LLM "navigate to red box" → visual grounding → Nav2 goal)

**Code Examples**:
- `depth_to_3d.py` - Utility functions for depth-based 3D position
- `visual_grounding_node.py` - ROS 2 node (image + text query → 3D pose)
- `action_executor.py` - Interprets LLM plans, calls visual grounding, sends Nav2 goals

**Exercises**:
1. Detect "red box" with CLIP, use depth camera to get 3D coordinates, publish to TF
2. Use `/object_pose` as Nav2 goal, navigate robot to detected object in simulation
3. End-to-end test: voice "Go to the blue cup" → LLM plan → visual grounding → navigation

**Assessment**:
- **Milestone**: Robot autonomously navigates to visually detected objects (voice command → autonomous action)

**Dependencies**: Chapter 4.5 (CLIP detection), Module 3 Nav2 (navigation), RGB-D camera (depth data)

---

### Chapter 4.7: VLA Pipeline Integration with State Machines

**Learning Journey**: LJ4 (End-to-End VLA Pipeline)
**Duration**: 2 hours
**Prerequisites**: Chapters 4.2 (Voice), 4.4 (LLM), 4.5 (Vision), 4.6 (Action Primitives)

**Learning Objectives** (Bloom's Taxonomy):
- **Understand**: Explain why state machines are needed for complex robot workflows
- **Apply**: Implement custom state machine for VLA (Listen → Plan → Ground → Execute)
- **Create**: Build VLA orchestrator node using py_trees behavior tree
- **Evaluate**: Test full VLA pipeline with simple commands in simulation

**Topics**:
- State machine fundamentals (states, transitions, events)
- py_trees behavior trees (sequence nodes, fallback nodes, decorators)
- VLA state machine structure (IDLE → LISTENING → PLANNING → GROUNDING → NAVIGATING → EXECUTING → SUCCESS/ERROR)
- Component integration (chain WhisperNode, LLMPlannerNode, VisualGroundingNode, ActionExecutor)
- Behavior tree visualization (py_trees_ros_viewer)

**Code Examples**:
- `vla_behavior_tree.py` - py_trees VLA orchestration
- `vla_orchestrator_node.py` - State machine managing transitions

**Exercises**:
1. Implement simple state machine chaining Whisper → LLM → visual grounding
2. Launch full VLA stack, give voice command, observe state transitions in logs
3. Test end-to-end command "Pick up the wrench" in Isaac Sim or Gazebo

**Assessment**:
- **Milestone**: Full VLA pipeline executes successfully for simple commands (voice → autonomous action completion)

**Dependencies**: All Learning Journeys 1-3 complete (integrates all components)

---

### Chapter 4.8: Error Recovery and Robustness

**Learning Journey**: LJ4 (End-to-End VLA Pipeline)
**Duration**: 1.5 hours
**Prerequisites**: Chapter 4.7 (VLA pipeline)

**Learning Objectives** (Bloom's Taxonomy):
- **Analyze**: Identify common VLA failure modes (speech errors, LLM hallucination, perception failure, navigation blocked)
- **Create**: Implement recovery strategies (confirmation prompts, LLM replan, perception fallback, navigation retry)
- **Evaluate**: Test error recovery for 3+ failure types (demonstrate robustness)

**Topics**:
- Common failure modes (speech misrecognition, LLM hallucination, object not found, navigation blocked)
- Speech confirmation (confirm transcription with user: "Did you say X?")
- LLM validation (check plan feasibility given environment, reject impossible actions)
- Perception fallback (object moved or occluded → trigger LLM replan)
- Navigation recovery (path blocked → Nav2 failure → report to user or replan)
- Graceful degradation (if all retries fail, return to start and report)

**Code Examples**:
- `confirmation_handler.py` - User feedback loop for speech confirmation
- `plan_feasibility_checker.py` - Validates LLM plans against environment state
- `perception_fallback.py` - Triggers LLM replan on perception failure
- `navigation_recovery.py` - Retry and fallback strategies for Nav2

**Exercises**:
1. Intentionally misrecognize command, verify confirmation prompt triggers
2. LLM plans to navigate through wall, validator rejects and asks for replan
3. Move object mid-task, verify robot detects absence and triggers replan
4. Block robot's path, verify it detects Nav2 failure and reports or replans

**Assessment**:
- **Milestone**: VLA pipeline recovers from at least 3 failure types (speech, planning, perception, navigation)

**Dependencies**: Chapter 4.7 (VLA pipeline), error handling requires functional baseline system

---

### Chapter 4.9: Mini-Project - Voice-Controlled Humanoid Assistant

**Learning Journey**: Integrative (all LJ1-4)
**Duration**: 2 hours
**Prerequisites**: All chapters 4.1-4.8 complete

**Learning Objectives** (Bloom's Taxonomy):
- **Create**: Implement complete VLA system for fetch-and-deliver tasks in simulated home environment
- **Evaluate**: Assess VLA system performance across 5 test scenarios (80%+ success rate required)

**Project Description**:
Learners build a voice-controlled humanoid that responds to fetch-and-deliver commands in a simulated home (Gazebo or Isaac Sim). Robot must use Whisper for voice, GPT-4/Claude for planning, CLIP for object detection, and Nav2 for navigation. System must recover from at least 2 error types.

**Requirements**:
- Whisper voice input (API or local)
- LLM task planning (GPT-4 or Claude)
- CLIP visual grounding for object detection
- Nav2 navigation to objects
- Error recovery (speech confirmation, perception fallback)

**Test Scenarios** (5 commands):
1. "Bring me the red mug from the kitchen"
2. "Find the blue book"
3. "Put the wrench on the table"
4. "Search for the green box"
5. "Get the yellow cup from the living room"

**Success Criteria**:
- Complete 4 out of 5 tasks (80%+ success rate)
- Recover from 2+ error types (demonstrate robustness)
- Execution time <60s per command (voice → task completion)

**Assessment Rubric** (100 points):
- Speech accuracy (15%): Whisper correctly transcribes 5/5 commands
- Plan quality (20%): LLM generates valid, efficient action sequences
- Visual grounding (20%): CLIP detects target objects in 4/5 scenarios
- Navigation (20%): Robot navigates to target locations without collision
- Error recovery (15%): Demonstrates recovery from 2+ failure types
- Integration (10%): All components communicate via ROS 2, pipeline executes smoothly

**Extension Challenges** (optional):
- Multi-object tasks ("Bring the red mug and blue book")
- Multi-turn dialogue (user provides clarification when asked)
- Custom action primitives (open drawer, press button)

**Deliverables**:
- Complete VLA system code
- Test results table (success/failure for each scenario, execution times)
- Video demo (3-5 minutes showing successful task and error recovery)

**Dependencies**: All chapters 4.1-4.8 (integrates all VLA components)

---

## Chapter Dependency Graph

```
4.1 (Introduction - Foundational)
  ├─→ 4.2 (Whisper - LJ1)
  │    └─→ 4.3 (Wake-Word - LJ1)
  │
  └─→ 4.4 (LLM Planning - LJ2, parallel with LJ1)
       └─→ 4.5 (CLIP - LJ3, requires LLM output)
            └─→ 4.6 (3D Pose - LJ3)

4.2 + 4.4 + 4.5 + 4.6 (all LJ1-3 complete)
  └─→ 4.7 (VLA Integration - LJ4)
       └─→ 4.8 (Error Recovery - LJ4)
            └─→ 4.9 (Mini-Project - Integrative)
```

**Critical Path**: 4.1 → 4.2 → 4.4 → 4.5 → 4.6 → 4.7 → 4.8 → 4.9
**Parallel Opportunities**: LJ1 (4.2-4.3) can develop in parallel with LJ2 (4.4) after 4.1 completes

---

## Learning Objectives Summary (Bloom's Taxonomy)

### Remember (Knowledge)
- Define VLA paradigm (4.1)
- List action primitives (4.4)

### Understand (Comprehension)
- Explain ASR and Whisper architecture (4.2)
- Describe LLM reasoning capabilities (4.4)
- Explain CLIP contrastive learning (4.5)
- Explain state machine purpose (4.7)

### Apply (Application)
- Transcribe audio with Whisper (4.2)
- Integrate wake-word detection (4.3)
- Design LLM prompts for planning (4.4)
- Use CLIP for object detection (4.5)
- Compute 3D poses from depth (4.6)
- Implement state machines (4.7)

### Analyze (Analysis)
- Compare Whisper API vs local (4.2)
- Compare GPT-4 vs Claude (4.4)
- Tune audio preprocessing (4.3)
- Identify VLA failure modes (4.8)

### Create (Synthesis)
- Build WhisperNode ROS 2 integration (4.2)
- Build LLMPlannerNode (4.4)
- Build visual grounding node (4.5-4.6)
- Build VLA orchestrator (4.7)
- Implement error recovery (4.8)
- Build complete VLA system (4.9)

### Evaluate (Evaluation)
- Validate LLM plans (4.4)
- Test visual grounding accuracy (4.5)
- Assess VLA system performance (4.9)

---

## Assessment Criteria

### Formative Assessment (During Learning)

**Chapter Quizzes** (multiple choice, 5-10 questions each):
- **Passing Score**: 80%
- **Topics**: ASR fundamentals, LLM capabilities, CLIP architecture, state machines, error recovery
- **Purpose**: Check conceptual understanding before hands-on exercises

**Guided Exercises** (hands-on coding tasks):
- **Completion Required**: 100% (all exercises must be attempted)
- **Success Criteria**: Code runs without errors, meets functional requirements
- **Purpose**: Build skills incrementally (Whisper → LLM → CLIP → integration)

**Milestone Validations** (end of each learning journey):
- **LJ1**: Voice commands published to ROS 2 with <2s latency
- **LJ2**: LLM generates valid plans for 90%+ test commands
- **LJ3**: CLIP detects objects in 80%+ test images
- **LJ4**: VLA pipeline recovers from 3+ failure types

### Summative Assessment (Module Completion)

**Mini-Project** (Chapter 4.9):
- **Required**: Yes (must complete to finish module)
- **Passing Score**: 70/100 points (see rubric above)
- **Deliverables**: Working VLA system, test results, video demo
- **Time Limit**: 2 hours for implementation + testing

---

## Content Quality Standards

### Markdown Quality
- **Heading Hierarchy**: Use H2 for sections, H3 for subsections (no H1 in chapters)
- **Line Length**: Max 120 characters per line
- **Code Blocks**: Fenced with language identifiers (```python, ```bash)
- **Lists**: Use `-` for unordered, `1.` for ordered

### Accessibility (WCAG 2.1 AA)
- **Images**: All images must have descriptive alt text
- **Code Contrast**: Ensure syntax highlighting has sufficient contrast
- **Headings**: Logical hierarchy (no skipped levels)
- **Links**: Descriptive link text (avoid "click here")

### Code Examples
- **Testing**: All code examples must run without errors (tested with API mocks)
- **API Keys**: NO hardcoded API keys (use `.env` files, document in quickstart.md)
- **Comments**: Explain complex logic, avoid obvious comments
- **Length**: Max 200 lines per example (longer → split into modules)

### Media Guidelines
- **Image Format**: WebP for screenshots, SVG for diagrams
- **Image Size**: <200KB per image (compress with tools)
- **Diagram Style**: Consistent color scheme (primary: blue #0066CC, secondary: green #00AA44)
- **Alt Text**: Describe diagram content and purpose (accessibility)

---

## Metadata for Each Chapter

Each chapter markdown file includes YAML front matter:

```yaml
---
id: chapter-4-X-title
title: "Chapter Title"
sidebar_label: "4.X Title"
sidebar_position: X
description: "Brief chapter description for SEO and sidebar"
keywords: [vla, whisper, gpt4, claude, clip, ros2]
learning_journey: "LJ1" # or LJ2, LJ3, LJ4, Integrative
duration: "2 hours"
difficulty: "intermediate"
prerequisites:
  - "module-1-complete"
  - "chapter-4-X-previous"
objectives:
  - "Apply: Transcribe audio with Whisper"
  - "Create: Build ROS 2 WhisperNode"
milestone: "Voice commands published to ROS 2 with <2s latency"
---
```

---

## External Dependencies (from Other Modules)

### From Module 1 (ROS 2 Fundamentals)
- **Chapter 1.2**: Publishers and subscribers (for `/voice_command`, `/action_plan` topics)
- **Chapter 1.4**: Services (optional, for LLM API calls as service requests)
- **Chapter 1.6**: RViz2 visualization (for visualizing TF frames of detected objects)

### From Module 2 (Gazebo) OR Module 3 (Isaac Sim)
- **Simulation Environment**: Testing ground for VLA pipeline
- **Camera Sensors**: RGB and depth cameras for visual grounding
- **Robot Model**: Humanoid with gripper for manipulation tasks
- **Navigation Stack**: Nav2 for autonomous navigation to detected objects

### Provides to Module 5 (Capstone)
- **Voice Interface**: Natural language command input for complex tasks
- **Cognitive Planning**: LLM-based task decomposition
- **Visual Grounding**: Connecting language to perception
- **Error Recovery**: Robust execution with fallback strategies

---

**Status**: ✅ Data model complete - chapter structure, dependencies, and assessment criteria defined
**Next**: Create contracts/ (code specifications for each chapter's code examples)
