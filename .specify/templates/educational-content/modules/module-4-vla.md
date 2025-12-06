# Module 4 Overlay: Vision-Language-Action (VLA)

**Instructions**: Combine this with `base-module-prompt.md` to create the complete
Module 4 specification prompt.

---

## Module Information (PRE-FILLED)

- **Module Number**: 4
- **Module Title**: Vision-Language-Action (VLA)
- **Estimated Duration**: 10 hours over 3-4 weeks
- **Prerequisites**:
  - **Module 1 complete** (ROS 2 fundamentals)
  - **Module 2 or 3 complete** (simulation environment - Gazebo OR Isaac Sim)
  - Python programming
  - **API keys**: OpenAI API (for GPT/Whisper) OR Anthropic API (for Claude)
  - Basic understanding of LLMs and prompt engineering (helpful but not required)
- **Target Audience**: AI/ML engineers and roboticists who completed prior modules
  and want to integrate large language models (LLMs) with robot control for natural
  language interaction

## Module Description (PRE-FILLED)

The convergence of Vision, Language, and Action (VLA) represents the frontier of
Physical AI. This module teaches you to build robots that understand human speech
("Clean the room"), see their environment (computer vision), reason about tasks
(LLM-based planning), and execute actions (ROS 2 motor commands). You'll integrate
OpenAI Whisper for speech-to-text, GPT-4/Claude for cognitive planning, and
perception models for visual grounding.

Unlike previous modules that focused on individual capabilities (motion, perception,
navigation), VLA is about orchestration: chaining voice → language understanding →
visual perception → task planning → robot action. By module's end, you'll have a
humanoid robot that accepts voice commands like "Bring me the red box," plans a
sequence of actions (navigate to box, grasp, navigate to human, release), and
executes them autonomously.

**Key Focus**: Voice-to-text (Whisper), LLM-based task planning (GPT-4/Claude),
visual grounding (CLIP, object detection), action primitives (pick, place, navigate),
and closed-loop execution with error recovery.

## Module Learning Goals (PRE-FILLED)

1. **Understand**: How Large Language Models (LLMs) can be used for robot task
   planning by translating natural language commands into structured action sequences
2. **Apply**: Integrate OpenAI Whisper for real-time speech recognition, send voice
   transcripts to LLMs, and parse LLM outputs into ROS 2 action commands
3. **Analyze**: Evaluate trade-offs between different VLA architectures (end-to-end
   neural policies vs LLM-based planners vs hybrid approaches) for robustness and
   interpretability
4. **Create**: Implement a complete voice-to-action pipeline where a humanoid robot
   receives a voice command, uses vision to identify objects/locations, plans a task
   sequence with LLM, and executes actions with error handling

---

## Learning Journeys (PRE-FILLED)

### Learning Journey 1: Voice-to-Text with OpenAI Whisper (Priority: P1)

**Narrative**: Learners begin by understanding automatic speech recognition (ASR)
and why Whisper is state-of-the-art (robust to accents, noise, 99 languages). They
install Whisper (local or API-based), record audio via microphone, transcribe it to
text, and publish transcripts to a ROS 2 topic (`/voice_command`). Next, they add
wake-word detection (listen for "Hey Robot") to avoid processing all speech. Finally,
they handle streaming transcription (real-time, not batch) for responsive voice
interaction.

**Why this priority**: Voice input is the entry point for VLA. Without reliable
speech-to-text, the entire pipeline fails. P1 because it's foundational.

**Independent Validation**: Learner can speak a command ("Move forward 2 meters"),
have Whisper transcribe it accurately, publish the transcript to `/voice_command`
topic, and subscribe in another ROS 2 node to verify reception.

**Learning Milestones**:
1. **Given** Whisper installed (local model or OpenAI API), **When** recording 5-
   second audio clip and transcribing, **Then** learner gets accurate text transcript
2. **Given** microphone input streaming, **When** running real-time Whisper in ROS 2
   node, **Then** transcriptions publish to `/voice_command` topic with <2 second
   latency
3. **Given** wake-word detection enabled (using Porcupine or custom), **When**
   speaking "Hey Robot, go to the kitchen," **Then** only "go to the kitchen"
   transcribed and published (wake-word stripped)
4. **Given** noisy environment (background music, multiple speakers), **When**
   speaking command, **Then** Whisper still transcribes primary speaker accurately
   (robustness test)

### Learning Journey 2: LLM-Based Task Planning (Priority: P1)

**Narrative**: After receiving a voice command text, the robot needs to plan actions.
LLMs excel at common-sense reasoning and can decompose high-level commands into
action primitives. Learners create a prompt template that describes robot capabilities
(navigate, pick, place, search) and the environment (rooms, objects). They send
commands like "Bring me the blue cup from the kitchen" to GPT-4/Claude, parse the
LLM's response (a sequence of actions in JSON or structured text), and validate the
plan. Next, they handle edge cases (object not found, ambiguous commands) via
clarifying questions and LLM retries.

**Why this priority**: LLM planning is the "cognitive brain" of VLA. Without it,
robots can only execute fixed scripts, not adapt to new commands. P1 because it's
core to the VLA concept.

**Independent Validation**: Learner can send a natural language command to an LLM
(via API), receive a structured action plan (e.g., JSON array of actions), parse it
in Python, and convert each action into corresponding ROS 2 messages (nav goals,
gripper commands).

**Learning Milestones**:
1. **Given** command "Pick up the red box," **When** sending to LLM with prompt
   describing robot's capabilities, **Then** LLM returns plan: `[{"action":
   "navigate", "target": "red box"}, {"action": "grasp", "object": "red box"}]`
2. **Given** ambiguous command "Bring me that," **When** LLM detects insufficient
   context, **Then** LLM asks clarifying question: "Which object do you mean?" (via
   text-to-speech or screen output)
3. **Given** plan with 5 steps, **When** parsing LLM JSON output, **Then** learner
   extracts each action and maps to ROS 2 primitives (navigate → Nav2 goal, grasp →
   gripper topic)
4. **Given** execution failure (object not found), **When** reporting error to LLM,
   **Then** LLM generates alternative plan (e.g., search other rooms)

### Learning Journey 3: Visual Grounding - Connecting Language to Perception
(Priority: P2)

**Narrative**: When LLM plans to "navigate to the red box," the robot must identify
the red box in camera images. This is visual grounding: mapping language descriptions
to visual regions. Learners use CLIP (OpenAI's vision-language model) to match text
queries ("red box") with image regions, or integrate object detection models (YOLO,
OWL-ViT) with language-based post-filtering. They estimate object 3D positions using
depth data, publish object poses to TF, and use them as Nav2 goals. Finally, they
handle occlusions and multi-object scenes (e.g., "the red box on the left table").

**Why this priority**: P2 because it builds on LLM planning (need to know what to
look for) and perception from Module 3 (camera, depth). Not foundational, but
essential for real-world VLA.

**Independent Validation**: Learner can send text query "red box" with an RGB-D
image to a visual grounding node, receive 3D coordinates of the red box in robot's
frame, and use those coordinates to navigate the robot to the object in simulation.

**Learning Milestones**:
1. **Given** RGB image with multiple objects, **When** querying CLIP with "red box,"
   **Then** learner identifies the bounding box region with highest similarity score
2. **Given** object bounding box and depth image, **When** computing 3D position,
   **Then** learner publishes object pose to TF (e.g., `/red_box` frame)
3. **Given** command "go to the red box," **When** LLM + visual grounding active,
   **Then** robot autonomously navigates to red box using detected 3D position as
   Nav2 goal
4. **Given** occluded object (partially hidden behind another), **When** visual
   grounding runs, **Then** learner detects ambiguity and triggers LLM fallback
   (ask user or reposition)

### Learning Journey 4: End-to-End VLA Pipeline with Error Recovery (Priority: P2)

**Narrative**: Learners integrate all components (Whisper, LLM, perception, Nav2,
gripper control) into a single pipeline orchestrated by a state machine or behavior
tree. They handle common failure modes: speech misrecognition (confirmation prompts),
LLM hallucination (validate plans against environment), perception failures (object
not visible), navigation failures (path blocked). They implement retry logic, user
confirmation ("Did you mean X?"), and graceful degradation (if navigation fails,
return to start and report).

**Why this priority**: P2 because it's integration work building on LJ1-3. Not a new
concept, but critical for robustness.

**Independent Validation**: Learner can give voice command "Bring the blue cup to
me," watch robot execute full pipeline (transcribe → plan → locate cup → navigate →
grasp → navigate back → release), and demonstrate recovery from at least one failure
(e.g., cup moved mid-task, robot replans).

**Learning Milestones**:
1. **Given** full VLA pipeline, **When** speaking "Pick up the wrench," **Then**
   robot transcribes, plans, locates wrench visually, navigates, and grasps without
   human intervention
2. **Given** misrecognized speech ("Pick up the bench" instead of "wrench"), **When**
   robot confirms via text-to-speech ("Did you mean bench?"), **Then** user corrects
   and robot retries
3. **Given** object moved during execution, **When** robot reaches expected location
   and doesn't see object, **Then** LLM generates replan (search nearby or ask user)
4. **Given** navigation failure (path blocked), **When** Nav2 reports failure, **Then**
   robot publishes failure status, LLM suggests alternative (e.g., "Path blocked,
   please clear area")

---

## Suggested Chapter Structure (TEMPLATES)

### Chapter 4.1: Introduction to Vision-Language-Action Models
- **Learning Objectives**: Understand VLA concept, compare VLA architectures (end-
  to-end neural, LLM-based, hybrid), explain why VLA enables general-purpose robots
- **Content**: VLA history (from fixed scripts to learned policies to LLM planners),
  real-world VLA systems (RT-1, PaLM-E, VoxPoser), architecture trade-offs
- **Hands-On**: Survey existing VLA demos (videos, papers), design VLA architecture
  for a specific task
- **Assessment**: Written comparison of end-to-end vs LLM-based VLA for home robotics

### Chapter 4.2: Speech Recognition with OpenAI Whisper
- **Learning Objectives**: Install Whisper, transcribe audio to text, integrate with
  ROS 2, handle streaming input
- **Content**: ASR overview, Whisper model architecture (encoder-decoder Transformer),
  API vs local deployment trade-offs
- **Hands-On**: Record audio, transcribe with Whisper, publish transcripts to ROS 2
  topic
- **Assessment**: Build voice command node that transcribes and publishes to
  `/voice_command` with <2s latency

### Chapter 4.3: Wake-Word Detection and Voice Activity Detection
- **Learning Objectives**: Implement wake-word detection (Porcupine, Snowboy), filter
  silence using VAD, reduce false activations
- **Content**: Wake-word vs full transcription, VAD (Voice Activity Detection), edge
  cases (false positives, missed wake-words)
- **Hands-On**: Add "Hey Robot" wake-word, only transcribe after wake-word detected
- **Assessment**: Test with 10 commands, verify wake-word detection accuracy >90%

### Chapter 4.4: Large Language Models for Robot Task Planning
- **Learning Objectives**: Design prompts for LLMs describing robot capabilities,
  parse LLM outputs into action sequences, handle failures
- **Content**: Prompt engineering for robotics, action primitives (navigate, pick,
  place), output parsing (JSON, structured text), retries and error handling
- **Hands-On**: Send commands to GPT-4/Claude, parse action plans, validate against
  environment
- **Assessment**: LLM generates valid plans for 5 diverse commands (navigation,
  manipulation, search)

### Chapter 4.5: Visual Grounding - Language to Vision
- **Learning Objectives**: Use CLIP for open-vocabulary object detection, compute 3D
  object positions from depth, publish to TF
- **Content**: CLIP architecture (vision-text contrastive learning), visual grounding
  techniques, depth-based 3D localization
- **Hands-On**: Query "red box" in camera image, get bounding box, compute 3D pose,
  publish to TF
- **Assessment**: Detect 3 objects by text query, verify 3D positions <10cm error in
  simulation

### Chapter 4.6: Action Primitives and Motion Planning
- **Learning Objectives**: Define action primitives (navigate, grasp, place, search),
  map to ROS 2 (Nav2, gripper control), sequence actions
- **Content**: Motion planning for manipulation (MoveIt if time), gripper control
  (position, force), action chaining
- **Hands-On**: Implement "navigate to X" and "grasp Y" primitives, chain them in
  sequence
- **Assessment**: Execute 3-step plan (navigate → grasp → navigate back) autonomously

### Chapter 4.7: End-to-End VLA Pipeline Integration
- **Learning Objectives**: Orchestrate VLA components with state machine or behavior
  tree, handle async execution, debug inter-component failures
- **Content**: State machine design (SMACH, py_trees), ROS 2 action servers for long-
  running tasks, logging and debugging
- **Hands-On**: Build state machine: Voice → LLM → Perception → Navigation → Action
- **Assessment**: Full pipeline executes 2 commands end-to-end without human
  intervention

### Chapter 4.8: Error Handling and Robustness
- **Learning Objectives**: Identify failure modes (speech errors, LLM hallucinations,
  perception failures, action failures), implement retries and fallbacks
- **Content**: Failure taxonomy, confirmation prompts, graceful degradation, user
  feedback
- **Hands-On**: Add retry logic for perception failures, user confirmation for
  ambiguous commands
- **Assessment**: Demonstrate recovery from 3 failure types (misheard command, object
  not found, navigation blocked)

### Chapter 4.9: Module 4 Mini-Project - Voice-Controlled Room Cleanup
- **Project**: Humanoid receives voice command "Clean the room," identifies objects
  on floor using vision, picks them up, and places them in designated bin
- **Requirements**: Full VLA pipeline, object detection, manipulation primitives, Nav2
  navigation
- **Assessment**: Robot cleans room with 3+ objects, handles at least one error (e.g.,
  object too heavy, asks for help)

---

## Core Concepts & Terminology (PRE-FILLED)

- **Term**: VLA (Vision-Language-Action)
- **Definition**: AI paradigm where robots perceive via vision, understand commands
  via language models, and execute actions, enabling natural human-robot interaction
- **Analogy**: Like a human assistant who sees, listens, understands, and acts
- **First Introduced**: Chapter 4.1
- **Related Terms**: LLM, Whisper, Visual Grounding, Action Primitives

---

- **Term**: ASR (Automatic Speech Recognition)
- **Definition**: Technology that converts spoken language into text, enabling voice
  interfaces for robots
- **Analogy**: Like dictation software (Google Voice Typing, Siri), but for robots
- **First Introduced**: Chapter 4.2
- **Related Terms**: Whisper, Wake-Word Detection, VAD

---

- **Term**: OpenAI Whisper
- **Definition**: State-of-the-art ASR model (encoder-decoder Transformer) trained on
  680k hours of multilingual data, robust to accents and noise
- **Analogy**: Like GPT for speech—general-purpose, multilingual, open-source
- **First Introduced**: Chapter 4.2
- **Related Terms**: ASR, Speech-to-Text, Transformer

---

- **Term**: Wake-Word Detection
- **Definition**: Technique to activate speech recognition only when specific phrase
  ("Hey Robot") is spoken, reducing false transcriptions
- **Analogy**: Like "Hey Siri" or "Alexa"—device listens only after wake phrase
- **First Introduced**: Chapter 4.3
- **Related Terms**: Porcupine, Snowboy, VAD, Hotword

---

- **Term**: LLM (Large Language Model)
- **Definition**: AI model trained on vast text corpora (GPT-4, Claude, LLaMA) capable
  of common-sense reasoning, task planning, and natural language understanding
- **Analogy**: Like a very knowledgeable assistant who can plan and reason
- **First Introduced**: Chapter 4.4
- **Related Terms**: GPT-4, Claude, Prompt Engineering, Task Planning

---

- **Term**: Prompt Engineering
- **Definition**: Designing text prompts for LLMs to elicit desired outputs (e.g.,
  action plans), including system messages, few-shot examples, and output format specs
- **Analogy**: Like writing clear instructions for a human assistant
- **First Introduced**: Chapter 4.4
- **Related Terms**: LLM, System Prompt, Few-Shot Learning, Chain-of-Thought

---

- **Term**: Visual Grounding
- **Definition**: Mapping language descriptions ("red box") to visual regions (bounding
  boxes, pixels) in images, connecting language and perception
- **Analogy**: Like pointing—when someone says "that red box," you know which one
- **First Introduced**: Chapter 4.5
- **Related Terms**: CLIP, Object Detection, Referring Expression Comprehension

---

- **Term**: CLIP (Contrastive Language-Image Pre-training)
- **Definition**: OpenAI's vision-language model that learns aligned representations
  of images and text, enabling zero-shot image classification via text queries
- **Analogy**: Like a universal image search—describe what you want, CLIP finds it
- **First Introduced**: Chapter 4.5
- **Related Terms**: Visual Grounding, Embedding, Zero-Shot Classification

---

- **Term**: Action Primitives
- **Definition**: Basic, reusable robot actions (navigate, grasp, place, search) that
  can be composed into complex tasks
- **Analogy**: Like Lego blocks—simple pieces combine to build complex structures
- **First Introduced**: Chapter 4.6
- **Related Terms**: Motion Planning, Task Planning, Behavior Tree

---

- **Term**: State Machine
- **Definition**: Control flow model where system transitions between discrete states
  (listening, planning, executing, error) based on events
- **Analogy**: Like a flowchart—each box is a state, arrows are transitions
- **First Introduced**: Chapter 4.7
- **Related Terms**: SMACH (ROS state machine library), Behavior Tree, Finite State
  Machine (FSM)

---

[Continue with 2-3 more terms: Behavior Tree, Graceful Degradation, Hallucination
(LLM), Zero-Shot Learning]

---

## Cross-Module Dependencies (PRE-FILLED)

### Within-Module
- **Chapter 4.1** (Introduction) is foundational
- **Chapter 4.2-4.3** (Speech) are independent, can precede or follow LLM chapters
- **Chapter 4.4** (LLM) independent of speech (can use text commands for testing)
- **Chapter 4.5** (Visual grounding) requires understanding of LLM output (need to
  know what to look for)
- **Chapter 4.6** (Action primitives) builds on Module 3 (Nav2, manipulation)
- **Chapter 4.7** (Integration) requires Chapters 4.2, 4.4, 4.5, 4.6
- **Chapter 4.8** (Error handling) requires Chapter 4.7 (need integrated system to
  test failures)
- **Chapter 4.9** (Mini-Project) integrates all chapters

### Cross-Module

**What Module 4 Requires from Module 1**:
- **Chapter 1.2**: Pub/sub (voice commands, LLM plans published to topics)
- **Chapter 1.4**: Services (could use service for LLM API calls, though HTTP is more
  common)

**What Module 4 Requires from Module 2 OR Module 3**:
- **From Module 2 (Gazebo)**: Simulated environment for testing VLA pipeline, camera
  sensors
- **From Module 3 (Isaac)**: Perception (object detection, depth), navigation (Nav2),
  Isaac Sim for high-fidelity testing

**What Module 4 Provides for Module 5 (Capstone)**:
- Complete VLA pipeline (voice → plan → act)
- Visual grounding for object identification
- Error recovery mechanisms

### External Dependencies

**Software**:
- **OpenAI API** OR **Anthropic API** (for LLMs):
  - OpenAI: GPT-4-turbo, Whisper API (requires API key, paid usage)
  - Anthropic: Claude 3 Opus/Sonnet (requires API key)
  - Alternative: Local LLMs (LLaMA via Ollama, free but less capable)
- **Whisper** (ASR):
  - OpenAI API (easier setup, requires internet)
  - OR Local: `pip install openai-whisper` (requires PyTorch, CUDA for GPU
    acceleration)
- **CLIP**: `pip install openai-clip` (PyTorch-based, GPU recommended)
- **Wake-word detection** (optional):
  - **Porcupine** (Picovoice, free tier available)
  - OR **Snowboy** (open-source, less maintained)

**Hardware**:
- **Microphone**: Any USB mic or laptop mic (for voice input testing)
- **GPU recommended**: CLIP and local Whisper benefit from CUDA (RTX 2060+)
- **16GB+ RAM**: LLM API calls are light, but local models (if used) require memory

**External Accounts**:
- **OpenAI Account** (for GPT-4 and/or Whisper API): Requires credit card, ~$0.01-
  $0.10 per command depending on usage
- **Anthropic Account** (alternative for Claude): Similar pricing
- **Picovoice Account** (optional, for Porcupine wake-word): Free tier includes 3
  wake-words

---

## Out of Scope (PRE-FILLED)

### Explicitly NOT Covered in Module 4

- **End-to-End Neural VLA Policies** (RT-1, RT-2): Policies trained on millions of
  robot demonstrations to directly map images + language → actions
  - **Rationale**: Requires massive datasets and specialized training infrastructure;
    LLM-based planning is more accessible for learners

- **Multimodal LLMs for Direct Vision** (GPT-4V, PaLM-E): LLMs that directly process
  images, not just text
  - **Rationale**: Emerging capability (GPT-4V released late 2023); API costs are
    high; we use CLIP for visual grounding instead

- **Text-to-Speech (TTS)**: Robot speaking responses back to user
  - **Rationale**: Valuable for UX, but not core to VLA pipeline; can be added as
    enhancement (e.g., pyttsx3, Google TTS)

- **Advanced Manipulation** (Dexterous Grasping, Bimanual): Complex gripper control,
  fine motor skills
  - **Rationale**: Manipulation is deep topic (could be its own module); VLA focuses
    on orchestration, not low-level control

- **Safety and Ethics**: Ensuring robots don't execute harmful commands
  - **Rationale**: Critical for deployment, but beyond educational scope; briefly
    mentioned in error handling (LLM should refuse unsafe commands)

- **Multi-Turn Dialogue**: Back-and-forth conversations for clarification ("Which
  room?" "The kitchen")
  - **Rationale**: Adds complexity (dialogue state tracking); focus is single-command
    execution

- **Sim-to-Real for VLA**: Transferring VLA policies from simulation to real robots
  - **Rationale**: Requires real hardware; book is simulation-focused

**Overall Rationale**: Module 4 provides practical VLA skills using accessible tools
(Whisper, GPT-4/Claude, CLIP) for voice-controlled robots. Advanced topics (neural
VLA, multimodal LLMs, dexterous manipulation) deferred or excluded to maintain focus
on fundamentals.

---

**Module 4 Overlay Complete**
**Lines**: ~580
**Status**: Ready to combine with base-module-prompt.md for `/sp.specify`
