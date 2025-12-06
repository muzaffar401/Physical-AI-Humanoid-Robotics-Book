# Feature Specification: Module 4 - Vision-Language-Action (VLA)

**Feature Branch**: `004-module-4-vla`
**Created**: 2025-11-30
**Status**: Draft

## Module Information

- **Module Number**: 4
- **Module Title**: Vision-Language-Action (VLA)
- **Estimated Duration**: 10 hours over 3-4 weeks
- **Prerequisites**:
  - **Module 1 complete** (ROS 2 fundamentals)
  - **Module 2 OR 3 complete** (simulation environment - Gazebo OR Isaac Sim)
  - Python programming
  - **API keys**: OpenAI API (for GPT/Whisper) OR Anthropic API (for Claude)
  - Basic understanding of LLMs and prompt engineering (helpful but not required)
- **Target Audience**: AI/ML engineers and roboticists who completed prior modules and want to integrate large language models (LLMs) with robot control for natural language interaction

## Module Description

The convergence of Vision, Language, and Action (VLA) represents the frontier of Physical AI. This module teaches you to build robots that understand human speech ("Clean the room"), see their environment (computer vision), reason about tasks (LLM-based planning), and execute actions (ROS 2 motor commands). You'll integrate OpenAI Whisper for speech-to-text, GPT-4/Claude for cognitive planning, and perception models for visual grounding.

Unlike previous modules that focused on individual capabilities (motion, perception, navigation), VLA is about orchestration: chaining voice → language understanding → visual perception → task planning → robot action. By module's end, you'll have a humanoid robot that accepts voice commands like "Bring me the red box," plans a sequence of actions (navigate to box, grasp, navigate to human, release), and executes them autonomously.

**Key Focus**: Voice-to-text (Whisper), LLM-based task planning (GPT-4/Claude), visual grounding (CLIP, object detection), action primitives (pick, place, navigate), and closed-loop execution with error recovery.

## Learning Journeys

### Learning Journey 1: Voice-to-Text with OpenAI Whisper (Priority: P1)

**Narrative**: Learners begin by understanding automatic speech recognition (ASR) and why Whisper is state-of-the-art (robust to accents, noise, 99 languages). They install Whisper (local or API-based), record audio via microphone, transcribe it to text, and publish transcripts to a ROS 2 topic (`/voice_command`). Next, they add wake-word detection (listen for "Hey Robot") to avoid processing all speech. Finally, they handle streaming transcription (real-time, not batch) for responsive voice interaction.

**Why this priority**: Voice input is the entry point for VLA. Without reliable speech-to-text, the entire pipeline fails. P1 because it's foundational.

**Independent Validation**: Learner can speak a command ("Move forward 2 meters"), have Whisper transcribe it accurately, publish the transcript to `/voice_command` topic, and subscribe in another ROS 2 node to verify reception.

**Learning Milestones**:
1. **Given** Whisper installed (local model or OpenAI API), **When** recording 5-second audio clip and transcribing, **Then** learner gets accurate text transcript
2. **Given** microphone input streaming, **When** running real-time Whisper in ROS 2 node, **Then** transcriptions publish to `/voice_command` topic with <2 second latency
3. **Given** wake-word detection enabled (using Porcupine or custom), **When** speaking "Hey Robot, go to the kitchen," **Then** only "go to the kitchen" transcribed and published (wake-word stripped)
4. **Given** noisy environment (background music, multiple speakers), **When** speaking command, **Then** Whisper still transcribes primary speaker accurately (robustness test)

---

### Learning Journey 2: LLM-Based Task Planning (Priority: P1)

**Narrative**: After receiving a voice command text, the robot needs to plan actions. LLMs excel at common-sense reasoning and can decompose high-level commands into action primitives. Learners create a prompt template that describes robot capabilities (navigate, pick, place, search) and the environment (rooms, objects). They send commands like "Bring me the blue cup from the kitchen" to GPT-4/Claude, parse the LLM's response (a sequence of actions in JSON or structured text), and validate the plan. Next, they handle edge cases (object not found, ambiguous commands) via clarifying questions and LLM retries.

**Why this priority**: LLM planning is the "cognitive brain" of VLA. Without it, robots can only execute fixed scripts, not adapt to new commands. P1 because it's core to the VLA concept.

**Independent Validation**: Learner can send a natural language command to an LLM (via API), receive a structured action plan (e.g., JSON array of actions), parse it in Python, and convert each action into corresponding ROS 2 messages (nav goals, gripper commands).

**Learning Milestones**:
1. **Given** command "Pick up the red box," **When** sending to LLM with prompt describing robot's capabilities, **Then** LLM returns plan: `[{"action": "navigate", "target": "red box"}, {"action": "grasp", "object": "red box"}]`
2. **Given** ambiguous command "Bring me that," **When** LLM detects insufficient context, **Then** LLM asks clarifying question: "Which object do you mean?" (via text-to-speech or screen output)
3. **Given** plan with 5 steps, **When** parsing LLM JSON output, **Then** learner extracts each action and maps to ROS 2 primitives (navigate → Nav2 goal, grasp → gripper topic)
4. **Given** execution failure (object not found), **When** reporting error to LLM, **Then** LLM generates alternative plan (e.g., search other rooms)

---

### Learning Journey 3: Visual Grounding - Connecting Language to Perception (Priority: P2)

**Narrative**: When LLM plans to "navigate to the red box," the robot must identify the red box in camera images. This is visual grounding: mapping language descriptions to visual regions. Learners use CLIP (OpenAI's vision-language model) to match text queries ("red box") with image regions, or integrate object detection models (YOLO, OWL-ViT) with language-based post-filtering. They estimate object 3D positions using depth data, publish object poses to TF, and use them as Nav2 goals. Finally, they handle occlusions and multi-object scenes (e.g., "the red box on the left table").

**Why this priority**: P2 because it builds on LLM planning (need to know what to look for) and perception from Module 3 (camera, depth). Not foundational, but essential for real-world VLA.

**Independent Validation**: Learner can send text query "red box" with an RGB-D image to a visual grounding node, receive 3D coordinates of the red box in robot's frame, and use those coordinates to navigate the robot to the object in simulation.

**Learning Milestones**:
1. **Given** RGB image with multiple objects, **When** querying CLIP with "red box," **Then** learner identifies the bounding box region with highest similarity score
2. **Given** object bounding box and depth image, **When** computing 3D position, **Then** learner publishes object pose to TF (e.g., `/red_box` frame)
3. **Given** command "go to the red box," **When** LLM + visual grounding active, **Then** robot autonomously navigates to red box using detected 3D position as Nav2 goal
4. **Given** occluded object (partially hidden behind another), **When** visual grounding runs, **Then** learner detects ambiguity and triggers LLM fallback (ask user or reposition)

---

### Learning Journey 4: End-to-End VLA Pipeline with Error Recovery (Priority: P2)

**Narrative**: Learners integrate all components (Whisper, LLM, perception, Nav2, gripper control) into a single pipeline orchestrated by a state machine or behavior tree. They handle common failure modes: speech misrecognition (confirmation prompts), LLM hallucination (validate plans against environment), perception failures (object not visible), navigation failures (path blocked). They implement retry logic, user confirmation ("Did you mean X?"), and graceful degradation (if navigation fails, return to start and report).

**Why this priority**: P2 because it's integration work building on LJ1-3. Not a new concept, but critical for robustness.

**Independent Validation**: Learner can give voice command "Bring the blue cup to me," watch robot execute full pipeline (transcribe → plan → locate cup → navigate → grasp → navigate back → release), and demonstrate recovery from at least one failure (e.g., cup moved mid-task, robot replans).

**Learning Milestones**:
1. **Given** full VLA pipeline, **When** speaking "Pick up the wrench," **Then** robot transcribes, plans, locates wrench visually, navigates, and grasps without human intervention
2. **Given** misrecognized speech ("Pick up the bench" instead of "wrench"), **When** robot confirms via text-to-speech ("Did you mean bench?"), **Then** user corrects and robot retries
3. **Given** object moved during execution, **When** robot reaches expected location and doesn't see object, **Then** LLM generates replan (search nearby or ask user)
4. **Given** navigation failure (path blocked), **When** Nav2 reports failure, **Then** robot publishes failure status, LLM suggests alternative (e.g., "Path blocked, please clear area")

---

## Core Concepts & Dependencies

**Core Concepts** (Key terminology):
- **VLA (Vision-Language-Action)**: AI paradigm where robots perceive via vision, understand commands via language models, and execute actions, enabling natural human-robot interaction
- **ASR (Automatic Speech Recognition)**: Technology that converts spoken language into text, enabling voice interfaces for robots
- **OpenAI Whisper**: State-of-the-art ASR model (encoder-decoder Transformer) trained on 680k hours of multilingual data, robust to accents and noise
- **Wake-Word Detection**: Technique to activate speech recognition only when specific phrase ("Hey Robot") is spoken, reducing false transcriptions
- **LLM (Large Language Model)**: AI model trained on vast text corpora (GPT-4, Claude, LLaMA) capable of common-sense reasoning, task planning, and natural language understanding
- **Prompt Engineering**: Designing text prompts for LLMs to elicit desired outputs (e.g., action plans), including system messages, few-shot examples, and output format specs
- **Visual Grounding**: Mapping language descriptions ("red box") to visual regions (bounding boxes, pixels) in images, connecting language and perception
- **CLIP (Contrastive Language-Image Pre-training)**: OpenAI's vision-language model that learns aligned representations of images and text, enabling zero-shot image classification via text queries
- **Action Primitives**: Basic, reusable robot actions (navigate, grasp, place, search) that can be composed into complex tasks
- **State Machine**: Control flow model where system transitions between discrete states (listening, planning, executing, error) based on events

**Within-Module Dependencies**: Chapter 4.1 (Introduction) is foundational → Chapters 4.2-4.3 (Speech) are independent → Chapter 4.4 (LLM) independent of speech → Chapter 4.5 (Visual grounding) requires understanding of LLM output → Chapter 4.6 (Action primitives) builds on Module 3 (Nav2) → Chapter 4.7 (Integration) requires Chapters 4.2, 4.4, 4.5, 4.6 → Chapter 4.8 (Error handling) requires 4.7 → Chapter 4.9 (mini-project integrates all).

**Cross-Module Dependencies**:
- **Requires from Module 1**: Chapter 1.2 (pub/sub for voice commands, LLM plans published to topics), Chapter 1.4 (services, could use for LLM API calls)
- **Requires from Module 2 OR 3**: Simulated environment for testing VLA pipeline (Gazebo OR Isaac Sim), camera sensors, perception (object detection from Module 3, or basic vision from Module 2), navigation (Nav2 from Module 3)
- **Provides for Module 5 (Capstone)**: Complete VLA pipeline (voice → plan → act), visual grounding for object identification, error recovery mechanisms

**External Dependencies**:
- **Software**: OpenAI API OR Anthropic API (GPT-4-turbo/Claude 3, requires API key, paid usage ~$0.01-$0.10 per command), Whisper (OpenAI API OR local via `pip install openai-whisper`), CLIP (`pip install openai-clip`, PyTorch-based, GPU recommended), Wake-word detection (Porcupine by Picovoice, free tier available, OR Snowboy, open-source)
- **Hardware**: Microphone (any USB mic or laptop mic), GPU recommended for CLIP and local Whisper (RTX 2060+), 16GB+ RAM (LLM API calls are light, but local models require memory if used)
- **External Accounts**: OpenAI Account OR Anthropic Account (requires credit card), Picovoice Account (optional, for Porcupine wake-word, free tier includes 3 wake-words)

## Out of Scope

- **End-to-End Neural VLA Policies** (RT-1, RT-2): Policies trained on millions of robot demonstrations to directly map images + language → actions. Rationale: Requires massive datasets and specialized training infrastructure; LLM-based planning is more accessible for learners.
- **Multimodal LLMs for Direct Vision** (GPT-4V, PaLM-E): LLMs that directly process images, not just text. Rationale: Emerging capability (GPT-4V released late 2023); API costs are high; we use CLIP for visual grounding instead.
- **Text-to-Speech (TTS)**: Robot speaking responses back to user. Rationale: Valuable for UX, but not core to VLA pipeline; can be added as enhancement (e.g., pyttsx3, Google TTS).
- **Advanced Manipulation** (Dexterous Grasping, Bimanual): Complex gripper control, fine motor skills. Rationale: Manipulation is deep topic (could be its own module); VLA focuses on orchestration, not low-level control.
- **Safety and Ethics**: Ensuring robots don't execute harmful commands. Rationale: Critical for deployment, but beyond educational scope; briefly mentioned in error handling (LLM should refuse unsafe commands).
- **Multi-Turn Dialogue**: Back-and-forth conversations for clarification ("Which room?" "The kitchen"). Rationale: Adds complexity (dialogue state tracking); focus is single-command execution.
- **Sim-to-Real for VLA**: Transferring VLA policies from simulation to real robots. Rationale: Requires real hardware; book is simulation-focused.

---

## Planning Note

This is a concise specification (~180 lines) focused on learning outcomes, core concepts, and dependencies. For detailed chapter structure, code examples, and assessment designs, refer to:
- Detailed overlay: `.specify/templates/educational-content/modules/module-4-vla.md`
- Reference spec: `specs/001-module-1-ros2/spec.md`

Use this spec for `/sp.plan` to design implementation approach, then `/sp.tasks` to generate actionable task breakdown.
