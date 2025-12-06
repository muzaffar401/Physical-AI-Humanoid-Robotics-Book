# Module 5 Overlay: Capstone Project - The Autonomous Humanoid

**Instructions**: Combine this with `base-module-prompt.md` to create the complete
Module 5 specification prompt.

---

## Module Information (PRE-FILLED)

- **Module Number**: 5
- **Module Title**: Capstone Project - The Autonomous Humanoid
- **Estimated Duration**: 8-12 hours over 2-3 weeks (self-paced project work)
- **Prerequisites**:
  - **ALL prior modules complete** (Modules 1-4)
  - Specifically:
    - Module 1: ROS 2 fundamentals
    - Module 2 OR 3: Simulation environment (Gazebo or Isaac Sim)
    - Module 3: Perception and navigation (if using Isaac)
    - Module 4: VLA pipeline (voice, LLM, visual grounding)
- **Target Audience**: All course participants ready to demonstrate mastery by
  integrating all learned skills into a complete autonomous system

## Module Description (PRE-FILLED)

The capstone project synthesizes everything learned across Modules 1-4 into a single
demonstration: an autonomous humanoid robot that receives a voice command, plans a
sequence of actions, navigates through an environment, manipulates objects, and
completes the task—all while handling errors gracefully.

**Example Capstone Scenario**: *"Hey Robot, clean the room."* The robot:
1. Transcribes voice command via Whisper (Module 4)
2. Plans task sequence via LLM: identify objects on floor, navigate to each, pick up,
   place in bin (Module 4)
3. Uses visual grounding to locate objects in camera view (Module 4)
4. Navigates to each object using Nav2 path planning (Module 3)
5. Grasps objects using manipulation primitives (Module 4)
6. Handles failures: object out of reach → ask for help, path blocked → replan

This module is project-based, not lecture-based. Learners choose from predefined
scenarios or propose custom projects that integrate at least 3 of the 4 prior modules.

**Key Focus**: Integration, system testing, debugging, error recovery, and
demonstrating a working end-to-end autonomous system.

## Module Learning Goals (PRE-FILLED)

1. **Integrate**: Combine ROS 2 fundamentals, simulation, perception, navigation, and
   VLA into a single coherent system with multiple interacting nodes
2. **Evaluate**: Test the autonomous system across multiple scenarios, identify
   failure modes, and measure performance metrics (task success rate, execution time,
   error recovery rate)
3. **Debug**: Diagnose and fix inter-component issues (topic mismatches, timing
   problems, perception failures, navigation deadlocks) using ROS 2 tools (rqt_graph,
   ros2 topic echo, rviz2)
4. **Present**: Document the capstone project with system architecture diagram, demo
   video, performance analysis, and reflection on lessons learned

---

## Learning Journeys (PRE-FILLED)

### Learning Journey 1: Project Scoping and Architecture Design (Priority: P1)

**Narrative**: Learners begin by selecting a capstone scenario (from provided options
or custom proposal). They define success criteria (e.g., "robot picks up 3 objects in
<5 minutes"), list required components (voice, LLM, perception, navigation,
manipulation), and design system architecture (nodes, topics, data flow). They create
a high-level architecture diagram showing how all modules integrate. This planning
phase prevents scope creep and ensures the project is achievable within 8-12 hours.

**Why this priority**: P1 because proper scoping is essential for capstone success.
Without it, learners may overcommit or build incompatible components.

**Independent Validation**: Learner produces a 1-page project proposal including:
scenario description, success criteria (measurable), list of ROS 2 nodes, architecture
diagram (nodes, topics, message flow), and timeline.

**Learning Milestones**:
1. **Given** capstone scenario options, **When** evaluating complexity and required
   modules, **Then** learner selects scenario matching their skill level and available
   time
2. **Given** chosen scenario, **When** defining success criteria, **Then** learner
   specifies measurable metrics (e.g., "90% object detection accuracy, <3 min task
   completion")
3. **Given** system requirements, **When** designing architecture, **Then** learner
   creates diagram showing all nodes (voice, LLM, perception, Nav2, gripper) and topic
   connections
4. **Given** architecture design, **When** reviewing with peers or instructor, **Then**
   learner identifies potential issues (bottlenecks, missing error handling) and
   revises design

### Learning Journey 2: Incremental Integration and Testing (Priority: P1)

**Narrative**: Rather than building the entire system at once, learners integrate
components incrementally, testing each addition. They start with voice → LLM (Module
4), verifying commands parse into plans. Next, they add perception (visual grounding),
testing object detection. Then navigation (Nav2), testing path planning. Finally,
manipulation (grasping), testing pick-and-place. At each step, they write integration
tests to catch regressions (e.g., "voice command 'pick up red box' generates correct
plan with red box coordinates").

**Why this priority**: P1 because incremental integration is the only feasible
approach for complex systems. Big-bang integration leads to debugging nightmares.

**Independent Validation**: Learner demonstrates the system at 4 integration
milestones: (1) voice + LLM only, (2) + perception, (3) + navigation, (4) + full
manipulation. Each milestone has passing tests.

**Learning Milestones**:
1. **Given** voice and LLM nodes, **When** speaking test commands ("go to kitchen"),
   **Then** learner verifies LLM output contains correct action plan
2. **Given** perception added, **When** querying "red box," **Then** learner verifies
   3D object pose published to TF within 0.1m error (in simulation ground truth)
3. **Given** navigation added, **When** setting Nav2 goal to detected object, **Then**
   robot navigates successfully without collisions (5/5 trials)
4. **Given** full system, **When** running end-to-end test ("pick up the cup"), **Then**
   robot completes task within success criteria (time, accuracy)

### Learning Journey 3: Error Handling and Robustness Testing (Priority: P2)

**Narrative**: Learners stress-test their system by introducing failures: speech
misrecognition (say "box" but Whisper hears "socks"), missing objects (command
"pick up wrench" but wrench not in scene), blocked paths (place obstacle in Nav2
path), and perception failures (poor lighting). For each failure mode, they implement
error detection (how to know failure occurred) and recovery (retry, ask for help,
abort gracefully). They measure robustness: out of 20 test runs, how many succeed?
How many fail gracefully vs crash?

**Why this priority**: P2 because error handling is essential for real-world systems,
but builds on a working baseline (LJ2 must work first).

**Independent Validation**: Learner documents 5 failure modes, implements error
handling for each, and demonstrates recovery in at least 3 scenarios (with video
evidence).

**Learning Milestones**:
1. **Given** intentional speech misrecognition, **When** LLM receives incorrect
   transcript, **Then** robot asks confirmation ("Did you mean X?") instead of
   executing wrong action
2. **Given** missing object scenario, **When** visual grounding fails to locate object,
   **Then** robot reports "Object not found" and asks user for guidance
3. **Given** blocked navigation path, **When** Nav2 fails to reach goal, **Then**
   robot retries once, then aborts and reports failure (no infinite loop)
4. **Given** 20 test runs with random failures injected, **When** analyzing results,
   **Then** learner achieves >70% success rate and 100% graceful degradation (no
   crashes)

### Learning Journey 4: Documentation and Presentation (Priority: P1)

**Narrative**: Learners document their capstone project for portfolio and peer review.
They create: (1) system architecture diagram (updated from LJ1 with actual
implementation), (2) demo video (3-5 min showing successful run + error recovery),
(3) performance report (success metrics, failure analysis, lessons learned), (4)
code repository with README (setup instructions, how to run). They present to peers
or record a narrated walkthrough explaining design decisions and challenges overcome.

**Why this priority**: P1 because documentation is essential for learning consolidation
and professional development. Also serves as course completion requirement.

**Independent Validation**: Learner submits complete documentation package (diagram,
video, report, repo) that allows another student to understand and reproduce the
project.

**Learning Milestones**:
1. **Given** final system, **When** creating architecture diagram, **Then** diagram
   accurately reflects all nodes, topics, and dependencies (verified by peer review)
2. **Given** working demo, **When** recording video, **Then** video shows at least
   one successful task completion and one error recovery scenario
3. **Given** test data, **When** writing performance report, **Then** report includes
   quantitative metrics (success rate, avg execution time, error breakdown) and
   qualitative analysis
4. **Given** code repository, **When** peer attempts to run project, **Then** they
   can set up and run within 30 minutes using README instructions

---

## Suggested Chapter Structure (TEMPLATES)

### Chapter 5.1: Capstone Project Overview and Scenario Selection
- **Learning Objectives**: Understand capstone requirements, evaluate scenario
  options, select project aligned with skills and interests
- **Content**: Capstone rubric (grading criteria), predefined scenarios (room cleanup,
  warehouse picking, search and rescue), custom proposal guidelines
- **Hands-On**: Review scenarios, select one OR propose custom project, draft 1-page
  proposal
- **Assessment**: Submit project proposal with scenario, success criteria, and
  architecture sketch

### Chapter 5.2: System Architecture Design
- **Learning Objectives**: Design multi-node ROS 2 system architecture, identify
  topic/service interfaces, plan error handling strategies
- **Content**: Architecture patterns (layered, pipeline, state machine), component
  diagram notation, interface definition
- **Hands-On**: Create detailed architecture diagram (use draw.io, Mermaid, or similar),
  define topic names and message types, list nodes and their responsibilities
- **Assessment**: Peer review of architecture (feedback on completeness, feasibility)

### Chapter 5.3: Incremental Integration - Voice and Planning
- **Learning Objectives**: Integrate voice (Whisper) and LLM planning, test in
  isolation, verify action plans generated correctly
- **Content**: Integration testing strategies, unit tests for ROS 2 nodes, logging
  best practices
- **Hands-On**: Implement voice → LLM pipeline, test with 10 sample commands, validate
  LLM outputs
- **Assessment**: Demonstrate voice command correctly parsed into action plan (5/5
  trials)

### Chapter 5.4: Incremental Integration - Perception
- **Learning Objectives**: Add visual grounding, test object detection accuracy,
  publish object poses to TF
- **Content**: Perception pipeline testing (precision, recall, false positives),
  coordinate frame validation
- **Hands-On**: Integrate CLIP/object detection, test with 5 objects, verify 3D pose
  accuracy
- **Assessment**: Object detection >80% precision/recall on test set of 10 objects

### Chapter 5.5: Incremental Integration - Navigation
- **Learning Objectives**: Integrate Nav2, test path planning to detected objects,
  tune costmap parameters
- **Content**: Nav2 debugging (rviz2 costmap visualization, path visualization),
  parameter tuning for humanoid footprint
- **Hands-On**: Send Nav2 goals from perception output, test navigation in 3 different
  environments
- **Assessment**: Robot navigates to objects without collisions (5/5 trials in simple
  environment)

### Chapter 5.6: Incremental Integration - Manipulation
- **Learning Objectives**: Add gripper control, test pick-and-place primitives,
  integrate with full pipeline
- **Content**: Manipulation testing (grasp success rate, positioning accuracy),
  action chaining
- **Hands-On**: Implement grasp primitive, chain with navigation (navigate → grasp),
  test on 3 objects
- **Assessment**: Successful grasp and transport of object from A to B

### Chapter 5.7: End-to-End System Testing
- **Learning Objectives**: Run full pipeline (voice → action), measure performance
  metrics, identify bottlenecks
- **Content**: End-to-end testing strategies, performance profiling (latency
  measurement), bottleneck identification
- **Hands-On**: Run 10 end-to-end tests, measure task completion time, log all
  failures
- **Assessment**: >60% success rate on 10-test suite, documented failure analysis

### Chapter 5.8: Error Handling and Robustness
- **Learning Objectives**: Implement error detection and recovery for 5 failure modes,
  test robustness
- **Content**: Failure mode taxonomy (perception, navigation, manipulation, planning),
  recovery strategies (retry, fallback, user intervention)
- **Hands-On**: Inject failures (remove objects, block paths, misrecognize speech),
  implement error handling
- **Assessment**: Demonstrate graceful recovery from 3 failure types (video evidence)

### Chapter 5.9: Documentation and Code Repository
- **Learning Objectives**: Document system architecture, create README with setup
  instructions, organize code repository
- **Content**: Technical documentation best practices, README structure, code
  organization
- **Hands-On**: Write comprehensive README, create architecture diagram, add inline
  code comments
- **Assessment**: Peer can clone repo and run system following README (<30 min setup)

### Chapter 5.10: Demo Video and Final Presentation
- **Learning Objectives**: Record demo video, prepare presentation slides, present
  project to peers/instructors
- **Content**: Demo video structure (intro, successful run, error recovery, results),
  presentation skills
- **Hands-On**: Record 3-5 min demo video, create 5-10 slide deck, present (live or
  recorded)
- **Assessment**: Complete documentation package submitted: diagram, video, report,
  repo, presentation

---

## Capstone Scenario Options (PRE-FILLED)

**Scenario 1: Room Cleanup Assistant**
- **Task**: Robot receives command "Clean the room," identifies objects on floor
  (toys, books, cups), picks each up, places in designated bin
- **Modules**: Voice (Module 4), LLM planning (Module 4), object detection (Module
  3/4), navigation (Module 3), manipulation (Module 4)
- **Success Criteria**: Pick up 3+ objects in <5 minutes, 80% success rate over 5 trials
- **Complexity**: Medium (standard scenario, good for most learners)

**Scenario 2: Warehouse Item Retrieval**
- **Task**: Robot receives command "Bring me item X from shelf Y," navigates warehouse,
  locates shelf using map, identifies item via visual grounding, retrieves and
  delivers to user
- **Modules**: Voice (Module 4), LLM + map reasoning (Module 4), navigation with
  large map (Module 3), object detection (Module 4), manipulation (Module 4)
- **Success Criteria**: Retrieve correct item 4/5 trials, <3 min per retrieval
- **Complexity**: High (requires multi-room navigation, precise manipulation)

**Scenario 3: Search and Rescue Simulation**
- **Task**: Robot receives command "Find survivors in building," autonomously explores
  unknown environment, detects human-shaped objects (mannequins or AR markers),
  reports locations, navigates to each and confirms visually
- **Modules**: Voice (Module 4), autonomous exploration (Module 3), object detection
  (Module 3/4), navigation/SLAM (Module 3)
- **Success Criteria**: Find 3/3 "survivors" in <10 min, build complete map
- **Complexity**: High (requires frontier exploration algorithm, multi-target planning)

**Scenario 4: Interactive Tour Guide**
- **Task**: Robot receives commands like "Take me to the cafeteria" or "Tell me about
  this room," navigates to locations, uses LLM to generate descriptions (e.g., room
  features from visual input), provides voice feedback via TTS (optional)
- **Modules**: Voice (Module 4), LLM for dialogue (Module 4), navigation (Module 3),
  visual scene understanding (Module 3/4)
- **Success Criteria**: Complete 3-stop tour, respond to 2 questions correctly
- **Complexity**: Medium-High (requires TTS for full experience, multi-turn dialogue)

**Scenario 5: Custom Proposal**
- **Requirements**: Must integrate at least 3 of 4 modules (ROS 2 assumed), must
  have measurable success criteria, must be achievable in 8-12 hours
- **Approval**: Submit proposal to instructor/peer group for feasibility review
- **Examples**: Barista robot (voice order, navigate to coffee machine, manipulate
  cups), Security patrol (autonomous patrol + anomaly detection), Pet care robot
  (fill water bowl, check food level)

---

## Core Concepts & Terminology (PRE-FILLED)

- **Term**: Capstone Project
- **Definition**: Culminating project that integrates knowledge and skills from all
  prior modules, demonstrating mastery of course material
- **Analogy**: Like a thesis or final exam, but hands-on and creative
- **First Introduced**: Chapter 5.1
- **Related Terms**: Integration, System Testing, End-to-End

---

- **Term**: Integration Testing
- **Definition**: Testing how multiple system components work together, identifying
  interface mismatches, timing issues, and emergent behaviors
- **Analogy**: Like a band rehearsal—each musician (component) may be skilled, but
  they must play together in sync
- **First Introduced**: Chapter 5.3
- **Related Terms**: Unit Testing (single node), End-to-End Testing, System Testing

---

- **Term**: Incremental Integration
- **Definition**: Strategy of adding components to a system one at a time, testing
  after each addition, to isolate issues
- **Analogy**: Like building with Legos—add one piece, verify it fits, then add next
- **First Introduced**: Chapter 5.2
- **Related Terms**: Big-Bang Integration (opposite, risky), Test-Driven Development

---

- **Term**: Graceful Degradation
- **Definition**: System behavior where failures are handled without crashes, often
  by reducing functionality or requesting help
- **Analogy**: Like a car in limp mode—still drivable, but slower/limited when
  engine fails
- **First Introduced**: Chapter 5.8
- **Related Terms**: Error Recovery, Fault Tolerance, Robustness

---

- **Term**: Failure Mode
- **Definition**: Specific way a system component can fail (e.g., speech
  misrecognition, object not found, navigation timeout)
- **Analogy**: Like different ways a car can break (flat tire, dead battery, engine
  failure)
- **First Introduced**: Chapter 5.8
- **Related Terms**: Error Handling, Recovery Strategy, Edge Case

---

- **Term**: System Architecture
- **Definition**: High-level design of a software system showing components (nodes),
  their interfaces (topics, services), and data flow
- **Analogy**: Like a building blueprint—shows rooms (components) and how they
  connect (hallways = topics)
- **First Introduced**: Chapter 5.2
- **Related Terms**: Component Diagram, Node Graph, Data Flow Diagram

---

## Cross-Module Dependencies (PRE-FILLED)

### Within-Module
- **Chapter 5.1-5.2** (Scoping, Architecture) are foundational
- **Chapters 5.3-5.6** (Incremental integration) must be done in sequence (voice →
  perception → navigation → manipulation), though order can vary by project
- **Chapter 5.7** (End-to-end testing) requires Chapters 5.3-5.6 complete
- **Chapter 5.8** (Error handling) requires Chapter 5.7 (need working system to test
  failures)
- **Chapters 5.9-5.10** (Documentation, presentation) are final steps, require full
  system

### Cross-Module

**What Module 5 Requires from ALL Prior Modules**:

- **From Module 1 (ROS 2)**:
  - Core pub/sub, services, nodes (foundation for all components)
  - ROS 2 tools (rqt_graph, rviz2, ros2 topic echo) for debugging

- **From Module 2 (Gazebo) OR Module 3 (Isaac)**:
  - Simulation environment for testing capstone
  - Sensor simulation (camera, depth, LiDAR)
  - Simulated humanoid robot model

- **From Module 3 (Isaac - if used)**:
  - Isaac ROS perception (VSLAM, object detection)
  - Nav2 navigation stack
  - Familiarity with Isaac Sim

- **From Module 4 (VLA)**:
  - Voice input (Whisper)
  - LLM task planning
  - Visual grounding (CLIP, object detection)
  - Action primitives (navigate, grasp, place)

**Module 5 is Pure Integration**: Does not introduce new concepts, only synthesizes
prior modules.

### External Dependencies

**Software**: All dependencies from Modules 1-4, specifically:
- ROS 2 Humble
- Gazebo OR Isaac Sim
- OpenAI/Anthropic API (for LLM)
- Whisper (local or API)
- Nav2, Isaac ROS (if Module 3 completed)
- CLIP (for visual grounding)

**Hardware**:
- Same as prior modules (GPU recommended for Isaac/CLIP)
- Microphone (for voice input)
- Sufficient compute for running full pipeline (16GB+ RAM)

**External Accounts**:
- Same as Module 4 (OpenAI/Anthropic API keys)

---

## Out of Scope (PRE-FILLED)

### Explicitly NOT Covered in Module 5

- **Real Hardware Deployment**: Capstone is simulation-only; deploying to physical
  humanoid robot requires additional steps (motor calibration, safety systems, sensor
  integration) beyond course scope
  - **Rationale**: Simulation allows all students to participate regardless of
    hardware access; real robots add variability and safety concerns

- **Scalability and Multi-Robot Coordination**: Single-robot capstone only
  - **Rationale**: Multi-robot systems add significant complexity; single-robot
    mastery is prerequisite

- **Production-Level Robustness**: Industrial-grade error handling (redundancy,
  fault tolerance, 99.9% uptime)
  - **Rationale**: Capstone demonstrates concepts; production deployment is
    professional engineering concern

- **Advanced LLM Techniques**: Fine-tuning LLMs for robotics, multi-agent LLM systems
  - **Rationale**: Module 4 covers prompt engineering; fine-tuning requires ML
    expertise and datasets beyond scope

- **Performance Optimization**: Real-time optimization (reducing latency to <10ms),
  code profiling
  - **Rationale**: Capstone focuses on functionality; optimization is important but
    secondary for educational project

**Overall Rationale**: Module 5 synthesizes prior modules into a working autonomous
system, demonstrating integration skills. Production deployment, hardware integration,
and advanced optimization are valuable but beyond educational scope.

---

## Assessment Rubric (PRE-FILLED)

### Project Proposal (10%)
- Scenario clearly defined: 3 pts
- Success criteria measurable: 3 pts
- Architecture diagram complete: 4 pts

### Technical Implementation (50%)
- Voice input working (Whisper integration): 8 pts
- LLM planning generates valid action sequences: 10 pts
- Perception (visual grounding) detects objects: 10 pts
- Navigation (Nav2) reaches goals without collisions: 10 pts
- Manipulation OR alternative action completes task: 10 pts
- (If not all components required by scenario, points redistributed)

### Error Handling and Robustness (15%)
- 3+ failure modes identified: 5 pts
- Error detection implemented for each: 5 pts
- Graceful recovery demonstrated for 2+ modes: 5 pts

### Documentation (15%)
- Architecture diagram (final): 3 pts
- README with setup instructions: 4 pts
- Code organization and comments: 3 pts
- Performance report (metrics, analysis): 5 pts

### Demo Video and Presentation (10%)
- Video shows successful task completion: 4 pts
- Video shows error recovery: 3 pts
- Presentation explains design decisions: 3 pts

**Total: 100 points**

**Passing Grade**: 70+ (demonstrates competency in integration and 3+ modules)
**Excellent Grade**: 85+ (robust system, excellent documentation, creative scenario)

---

**Module 5 Overlay Complete**
**Lines**: ~580
**Status**: Ready to combine with base-module-prompt.md for `/sp.specify`
