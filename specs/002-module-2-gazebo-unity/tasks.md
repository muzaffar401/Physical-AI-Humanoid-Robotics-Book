---
description: "Task list for Module 2: The Digital Twin (Gazebo & Unity)"
---

# Tasks: Module 2 - The Digital Twin (Gazebo & Unity)

**Input**: Design documents from `/specs/002-module-2-gazebo-unity/`
**Prerequisites**: plan.md, spec.md (3 learning journeys)

**Organization**: Tasks are grouped by learning journey to enable independent implementation and testing of each educational path.

## Format: `[ID] [P?] [Journey] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[LJ#]**: Which learning journey this task belongs to (LJ1, LJ2, LJ3)
- Include exact file paths in descriptions

## Path Conventions

- **Educational Content**: `book_frontend/docs/module-2/` (chapter markdown files)
- **Assets**: `book_frontend/docs/assets/module-2/` (code examples, diagrams, images)
- **Documentation**: `specs/002-module-2-gazebo-unity/` (research, data model, contracts)
- **Tests**: `tests/content/` and `tests/code_examples/`

---

## Phase 1: Setup (Project Infrastructure)

**Purpose**: Initialize module structure and configuration

- [ ] T001 Create module directory structure at book_frontend/docs/module-2/
- [ ] T002 Create assets directory structure at book_frontend/docs/assets/module-2/ with subdirs (code/, diagrams/, images/)
- [ ] T003 [P] Create _category_.json for Docusaurus sidebar configuration
- [ ] T004 [P] Create module index file at book_frontend/docs/module-2/index.md
- [ ] T005 [P] Create test directory structure at tests/content/ and tests/code_examples/

---

## Phase 2: Foundational (Design Documents & Prerequisites)

**Purpose**: Core planning documents that MUST be complete before ANY learning journey content

**⚠️ CRITICAL**: No chapter writing can begin until this phase is complete

- [ ] T006 Create research.md with Gazebo Fortress vs Garden decision, ros_gz_bridge patterns, pedagogy sequencing
- [ ] T007 Create data-model.md with chapter structure, Bloom's taxonomy objectives, and dependencies
- [ ] T008 Create quickstart.md with prerequisites, Gazebo installation, ros_gz packages setup, workspace verification
- [ ] T009 [P] Create contracts/chapter-2-2-spawn-robot.md for URDF spawning example
- [ ] T010 [P] Create contracts/chapter-2-3-lidar-plugin-example.md for LiDAR sensor integration
- [ ] T011 [P] Create contracts/chapter-2-5-ros-gz-bridge-config.md for topic bridging example
- [ ] T012 [P] Create contracts/chapter-2-6-obstacle-avoidance.md for closed-loop control example
- [ ] T013 [P] Create reusable partial at book_frontend/docs/_partials/gazebo-install.md for installation instructions
- [ ] T014 [P] Create reusable partial at book_frontend/docs/_partials/troubleshooting-common-errors.md for Gazebo/ROS 2 issues

**Checkpoint**: Foundation documents ready - learning journey content implementation can now begin in parallel

---

## Phase 3: Learning Journey 1 - Physics Simulation with Gazebo (Priority: P1) 🎯 MVP

**Goal**: Learners can spawn URDF robots in Gazebo, apply forces, observe physics (gravity, collisions, friction), and simulate humanoid joint controllers

**Independent Test**: Spawn a wheeled robot URDF in Gazebo, apply motor commands via `/cmd_vel` topic, observe realistic motion with physics, inspect contact forces in Gazebo GUI

### Chapter 2.1: Introduction to Digital Twins

- [ ] T015 [LJ1] Write chapter-2-1-introduction.md with digital twin definition, real-world examples, module overview
- [ ] T016 [LJ1] Add learning objectives for Chapter 2.1 (Remember: define digital twin, Understand: explain benefits)
- [ ] T017 [P] [LJ1] Create gazebo-architecture.svg diagram showing Gazebo components (physics engine, sensors, rendering)
- [ ] T018 [LJ1] Add hands-on exercise: Install Gazebo Fortress and verify with `gz sim --version`
- [ ] T019 [LJ1] Add chapter summary and transition to Chapter 2.2

### Chapter 2.2: Spawning Robots in Gazebo

- [ ] T020 [LJ1] Write chapter-2-2-spawning-robots.md covering URDF to Gazebo workflow
- [ ] T021 [LJ1] Add learning objectives (Apply: spawn URDF in Gazebo, Analyze: compare URDF vs SDF)
- [ ] T022 [P] [LJ1] Create code example at book_frontend/docs/assets/module-2/code/chapter-2-2/simple_robot.urdf
- [ ] T023 [P] [LJ1] Create spawn_robot.launch.py launch file example
- [ ] T024 [P] [LJ1] Create urdf-to-gazebo-flow.svg diagram showing spawning workflow
- [ ] T025 [LJ1] Add guided walkthrough: Spawn wheeled robot from Module 1, observe in Gazebo
- [ ] T026 [LJ1] Add exercise 1: Modify robot URDF to change wheel size, respawn, observe changes
- [ ] T027 [LJ1] Add exercise 2: Apply forces to wheels via `/cmd_vel` topic, observe motion
- [ ] T028 [LJ1] Add milestone validation: Learner can spawn URDF and apply forces

### Chapter 2.4: Building Worlds with Obstacles

- [ ] T029 [LJ1] Write chapter-2-4-building-worlds.md covering SDF world files, obstacles, slopes
- [ ] T030 [LJ1] Add learning objectives (Create: build warehouse world with obstacles)
- [ ] T031 [P] [LJ1] Create code example at book_frontend/docs/assets/module-2/code/chapter-2-4/warehouse_world.sdf
- [ ] T032 [P] [LJ1] Create world-with-obstacles.svg diagram showing collision detection concept
- [ ] T033 [LJ1] Add guided walkthrough: Create empty world, add box obstacles, spawn robot
- [ ] T034 [LJ1] Add exercise 1: Create world with slope, observe robot behavior on incline
- [ ] T035 [LJ1] Add exercise 2: Drive robot into wall, inspect contact forces in Gazebo GUI
- [ ] T036 [LJ1] Add milestone validation: Learner observes collision detection and contact forces

### Physics Simulation Assets

- [ ] T037 [P] [LJ1] Create physics-forces-diagram.svg showing F=ma with different robot masses
- [ ] T038 [P] [LJ1] Create screenshot gazebo-empty-world.webp for Chapter 2.1
- [ ] T039 [P] [LJ1] Create screenshot robot-collision-demo.webp for Chapter 2.4
- [ ] T040 [P] [LJ1] Create humanoid URDF example at book_frontend/docs/assets/module-2/code/chapter-2-2/humanoid_simple.urdf
- [ ] T041 [P] [LJ1] Create code validation test at tests/code_examples/test_chapter_2_2_urdf.py

**Checkpoint**: Learning Journey 1 complete - learners can spawn robots, apply forces, observe physics

---

## Phase 4: Learning Journey 2 - Sensor Simulation (LiDAR, Cameras, IMU) (Priority: P1)

**Goal**: Learners can attach sensor plugins (LiDAR, depth camera, IMU) to robots in Gazebo, visualize sensor data in RViz2, and implement basic obstacle detection

**Independent Test**: Attach LiDAR plugin to Gazebo robot, visualize scan data in RViz2, subscribe to scan topic in ROS 2 node, implement obstacle detection (if obstacle <1m, publish stop command)

### Chapter 2.3: Sensors and Gazebo Plugins

- [ ] T042 [LJ2] Write chapter-2-3-gazebo-plugins.md covering sensor plugins (LiDAR, cameras, IMU)
- [ ] T043 [LJ2] Add learning objectives (Apply: attach LiDAR plugin, Create: custom sensor configuration)
- [ ] T044 [P] [LJ2] Create code example at book_frontend/docs/assets/module-2/code/chapter-2-3/robot_with_lidar.urdf
- [ ] T045 [P] [LJ2] Create lidar_subscriber.py ROS 2 node example
- [ ] T046 [P] [LJ2] Create sensor-plugin-lifecycle.svg diagram showing plugin initialization and data flow
- [ ] T047 [LJ2] Add LiDAR section: 2D laser scanner plugin, `/scan` topic, LaserScan message type
- [ ] T048 [LJ2] Add guided walkthrough: Attach LiDAR to wheeled robot, visualize in RViz2
- [ ] T049 [LJ2] Add exercise 1: Modify LiDAR parameters (FOV, range), observe scan changes
- [ ] T050 [LJ2] Add depth camera section: 3D point cloud plugin, `/camera/depth/points` topic
- [ ] T051 [P] [LJ2] Create robot_with_depth_camera.urdf example
- [ ] T052 [LJ2] Add exercise 2: Attach depth camera, visualize point cloud in RViz2
- [ ] T053 [LJ2] Add IMU section: orientation quaternion, angular velocity, `/imu/data` topic
- [ ] T054 [P] [LJ2] Create robot_with_imu.urdf example
- [ ] T055 [LJ2] Add exercise 3: Attach IMU, tilt robot in Gazebo, observe orientation changes
- [ ] T056 [LJ2] Add obstacle detection section: Read LiDAR data, detect obstacles, publish stop command
- [ ] T057 [P] [LJ2] Create simple_obstacle_detector.py code example
- [ ] T058 [LJ2] Add exercise 4: Implement obstacle avoidance (if obstacle <1m, turn robot)
- [ ] T059 [LJ2] Add milestone validation: Learner implements working obstacle detection node

### Sensor Simulation Assets

- [ ] T060 [P] [LJ2] Create lidar-scan-visualization.svg diagram showing scan rays and obstacles
- [ ] T061 [P] [LJ2] Create depth-camera-pointcloud.svg diagram showing 3D point cloud concept
- [ ] T062 [P] [LJ2] Create imu-orientation-axes.svg diagram showing IMU coordinate frame
- [ ] T063 [P] [LJ2] Create screenshot rviz2-lidar-scan.webp showing RViz2 with LaserScan display
- [ ] T064 [P] [LJ2] Create screenshot rviz2-pointcloud.webp for depth camera visualization
- [ ] T065 [P] [LJ2] Create code validation test at tests/code_examples/test_chapter_2_3_lidar.py

**Checkpoint**: Learning Journey 2 complete - learners can integrate sensors and process sensor data

---

## Phase 5: Learning Journey 3 - Gazebo-ROS 2 Integration (ros_gz_bridge) (Priority: P2)

**Goal**: Learners understand ros_gz_bridge for translating between Gazebo (Ignition Transport) and ROS 2 (DDS), configure bidirectional topic bridges, and debug bridge misconfigurations

**Independent Test**: Write ros_gz_bridge configuration that bridges custom topic from Gazebo to ROS 2, verify with `ros2 topic list`, subscribe in ROS 2 node

### Chapter 2.5: ros_gz_bridge Integration

- [ ] T066 [LJ3] Write chapter-2-5-ros-gz-bridge.md covering Ignition Transport vs DDS, bridge configuration
- [ ] T067 [LJ3] Add learning objectives (Analyze: debug bridge misconfigurations, Apply: configure bridge)
- [ ] T068 [P] [LJ3] Create ros-gz-bridge-flow.svg diagram showing ROS 2 ↔ Gazebo message translation
- [ ] T069 [LJ3] Add bridge fundamentals: Why bridging is needed, topic name mapping, message type compatibility
- [ ] T070 [LJ3] Add guided walkthrough: Bridge `/cmd_vel` from ROS 2 to Gazebo for teleop control
- [ ] T071 [P] [LJ3] Create bridge_cmd_vel.yaml configuration example
- [ ] T072 [P] [LJ3] Create bridge_launch.py launch file with ros_gz_bridge node
- [ ] T073 [LJ3] Add exercise 1: Configure bridge for `/scan` topic (Gazebo → ROS 2)
- [ ] T074 [LJ3] Add debugging section: Topic name mismatches, message type incompatibilities, `ros2 topic info`
- [ ] T075 [LJ3] Add exercise 2: Diagnose and fix topic name mismatch (`/lidar/scan` vs `/scan`)
- [ ] T076 [LJ3] Add bidirectional bridging: Commands from ROS 2, sensor data to ROS 2
- [ ] T077 [LJ3] Add exercise 3: Create launch file that bridges multiple topics (cmd_vel, scan, imu)
- [ ] T078 [LJ3] Add milestone validation: Learner can configure and debug custom topic bridges

### Chapter 2.6: Closed-Loop Control (Sense-Plan-Act)

- [ ] T079 [LJ3] Write chapter-2-6-closed-loop.md covering perception-control integration
- [ ] T080 [LJ3] Add learning objectives (Create: obstacle avoidance algorithm, Evaluate: test control loop)
- [ ] T081 [P] [LJ3] Create sense-plan-act-loop.svg diagram showing closed-loop architecture
- [ ] T082 [LJ3] Add closed-loop concept: Read sensors → make decisions → command actuators
- [ ] T083 [LJ3] Add guided walkthrough: Integrate LiDAR subscriber with cmd_vel publisher
- [ ] T084 [P] [LJ3] Create obstacle_avoidance.py complete example at book_frontend/docs/assets/module-2/code/chapter-2-6/
- [ ] T085 [P] [LJ3] Create obstacle_avoidance_launch.py that starts Gazebo, robot, bridge, and control node
- [ ] T086 [LJ3] Add exercise 1: Test obstacle avoidance in warehouse world from Chapter 2.4
- [ ] T087 [LJ3] Add exercise 2: Modify control logic to turn left/right based on scan sectors
- [ ] T088 [LJ3] Add exercise 3: Add state machine (exploring, avoiding, stopped)
- [ ] T089 [LJ3] Add milestone validation: Robot autonomously navigates warehouse without collisions

### Integration Assets

- [ ] T090 [P] [LJ3] Create bridge-topic-mapping.svg diagram showing topic remapping examples
- [ ] T091 [P] [LJ3] Create screenshot gazebo-rviz2-side-by-side.webp showing synchronized views
- [ ] T092 [P] [LJ3] Create screenshot obstacle-avoidance-demo.webp showing robot avoiding walls
- [ ] T093 [P] [LJ3] Create code validation test at tests/code_examples/test_chapter_2_6_obstacle.py

**Checkpoint**: Learning Journey 3 complete - learners can bridge topics and implement closed-loop control

---

## Phase 6: Optional Content & Mini-Project

**Purpose**: Advanced content (Unity) and integrative mini-project

### Chapter 2.7: Unity for High-Fidelity Rendering (Optional)

- [ ] T094 [P] Write chapter-2-7-unity-optional.md covering Unity + ROS integration
- [ ] T095 [P] Add learning objectives (Evaluate: compare Gazebo vs Unity trade-offs)
- [ ] T096 [P] Add Unity setup: Unity Hub, ROS-TCP-Connector package installation
- [ ] T097 [P] Add guided walkthrough: Import humanoid model in Unity, connect to ROS 2
- [ ] T098 [P] Create unity-ros-architecture.svg diagram showing Unity ↔ ROS communication
- [ ] T099 [P] Add exercise: Create simple HRI scenario (robot responds to voice commands visualized in Unity)
- [ ] T100 [P] Create screenshot unity-hri-scene.webp showing photorealistic humanoid in Unity

### Chapter 2.8: Mini-Project - Autonomous Warehouse Robot

- [ ] T101 Write chapter-2-8-mini-project.md with integrative project requirements
- [ ] T102 Add project goal: Wheeled robot autonomously navigates warehouse, avoids obstacles, reaches goal
- [ ] T103 Add requirements: Use LiDAR for perception, ros_gz_bridge for integration, closed-loop control
- [ ] T104 Add assessment rubric: Physics accuracy (20%), sensor integration (30%), bridge config (20%), control logic (30%)
- [ ] T105 [P] Create mini_project_world.sdf with warehouse layout, goal markers, obstacles
- [ ] T106 [P] Create mini_project_starter.py template with TODOs for learners
- [ ] T107 Add success criteria: Robot reaches goal in <2 minutes without collisions
- [ ] T108 Add extension challenges: Multiple goals, dynamic obstacles, path optimization
- [ ] T109 Create project-architecture-diagram.svg showing all components (Gazebo, RViz2, bridge, nodes)

**Checkpoint**: All module content complete - learners have end-to-end simulation skills

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Content validation, quality assurance, and documentation

### Documentation & Index

- [ ] T110 [P] Write comprehensive module index at book_frontend/docs/module-2/index.md with overview, prerequisites, learning goals
- [ ] T111 [P] Add module navigation links to all chapter files (Previous/Next chapter)
- [ ] T112 [P] Create module summary in index: What learners will achieve, time estimate (12 hours)
- [ ] T113 [P] Add "How to use this module" section with recommended sequence and optional paths

### Content Validation

- [ ] T114 [P] Create test_markdown_lint.py to validate CommonMark syntax with Vale
- [ ] T115 [P] Create test_links.py to check all internal and external links
- [ ] T116 [P] Create test_accessibility.py to verify WCAG 2.1 AA compliance (alt text, headings, contrast)
- [ ] T117 Run Vale linting on all chapter markdown files (book_frontend/docs/module-2/*.md)
- [ ] T118 Run markdown-link-check on all chapter files
- [ ] T119 Verify all images have descriptive alt text (<200KB file size)
- [ ] T120 Validate all code examples are syntactically correct (Python, bash, URDF, SDF)

### Code Example Testing

- [ ] T121 [P] Run test_chapter_2_2_urdf.py to validate URDF files with check_urdf
- [ ] T122 [P] Run test_chapter_2_3_lidar.py to test LiDAR plugin examples
- [ ] T123 [P] Run test_chapter_2_6_obstacle.py to validate obstacle avoidance logic
- [ ] T124 Test all launch files can start without errors (gz sim headless mode)
- [ ] T125 Verify all ROS 2 Python nodes can be executed (import checks, syntax validation)

### Docusaurus Build & Performance

- [ ] T126 Run Docusaurus build and verify no errors
- [ ] T127 Verify page load time <3s for all module pages
- [ ] T128 Compress images to <200KB (use WebP format for screenshots)
- [ ] T129 Verify all SVG diagrams render correctly across browsers

### Final Review

- [ ] T130 Review all learning objectives are addressed in chapter content
- [ ] T131 Verify chapter dependencies are correct (2.1→2.2→2.3→2.5→2.6)
- [ ] T132 Check all exercises have clear instructions and expected outcomes
- [ ] T133 Validate milestone tests align with learning journey goals
- [ ] T134 Run quickstart.md validation to ensure installation instructions work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all learning journeys
- **Learning Journeys (Phase 3-5)**: All depend on Foundational phase completion
  - LJ1 (Physics Simulation - P1): Can start after Foundational
  - LJ2 (Sensor Simulation - P1): Can start after Foundational (independent from LJ1)
  - LJ3 (ros_gz_bridge - P2): Should start after LJ1 and LJ2 (uses sensors from LJ2)
- **Optional & Project (Phase 6)**: Depends on desired learning journeys (Chapter 2.8 requires LJ1+LJ2+LJ3)
- **Polish (Phase 7)**: Depends on all content chapters being complete

### Learning Journey Dependencies

- **LJ1 (Physics Simulation)**: Independent - can start after Foundational
- **LJ2 (Sensor Simulation)**: Independent - can start after Foundational (parallel with LJ1)
- **LJ3 (ros_gz_bridge Integration)**: Depends on LJ1 (needs spawned robots) and LJ2 (bridges sensor topics)

### Within Each Learning Journey

- Chapter writing before diagrams/code (content drives assets)
- Diagrams marked [P] can be created in parallel
- Code examples marked [P] can be created in parallel
- Exercises follow guided walkthroughs
- Milestone validation at end of each learning journey

### Parallel Opportunities

- All Setup tasks (T001-T005) can run in parallel
- All Foundational contracts (T009-T012) can run in parallel after T006-T008
- All Foundational partials (T013-T014) can run in parallel
- Once Foundational completes:
  - LJ1 (Physics) and LJ2 (Sensors) can be developed in parallel
  - Within each LJ: diagrams and code examples marked [P] can run in parallel
- Chapter 2.7 (Unity) can be developed independently in parallel with other content
- All Polish tasks (T110-T134) marked [P] can run in parallel after content is complete

---

## Parallel Example: Learning Journey 1 (Physics Simulation)

```bash
# After Chapter 2.2 content is written, launch all assets together:
Task: "Create simple_robot.urdf"
Task: "Create spawn_robot.launch.py"
Task: "Create urdf-to-gazebo-flow.svg diagram"
Task: "Create humanoid_simple.urdf example"

# After Chapter 2.4 content is written, launch all assets together:
Task: "Create warehouse_world.sdf"
Task: "Create world-with-obstacles.svg diagram"
Task: "Create robot-collision-demo.webp screenshot"
```

---

## Implementation Strategy

### MVP First (Learning Journey 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all journeys)
3. Complete Phase 3: Learning Journey 1 (Physics Simulation)
4. **STOP and VALIDATE**: Test all Chapter 2.1, 2.2, 2.4 content independently
5. Deploy/demo if ready (learners can now spawn robots and understand physics)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add LJ1 (Physics) → Test independently → Deploy/Demo (MVP!)
3. Add LJ2 (Sensors) → Test independently → Deploy/Demo
4. Add LJ3 (ros_gz_bridge) → Test independently → Deploy/Demo
5. Add Chapter 2.8 (Mini-Project) → Complete module

### Parallel Team Strategy

With multiple content creators:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Creator A: LJ1 (Physics Simulation) - Chapters 2.1, 2.2, 2.4
   - Creator B: LJ2 (Sensor Simulation) - Chapter 2.3
   - Creator C: Research/diagrams for LJ1 and LJ2
3. After LJ1 + LJ2 complete:
   - Creator A+B: LJ3 (ros_gz_bridge Integration) - Chapters 2.5, 2.6
   - Creator C: Chapter 2.7 (Unity, optional)
4. All creators: Chapter 2.8 (Mini-Project) integration and polish

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [LJ#] label maps task to specific learning journey for traceability
- Each learning journey should be independently completable and testable
- Focus on educational quality: clear learning objectives, hands-on exercises, milestone validation
- All code examples must be tested and runnable (tests in Phase 7)
- Commit after each chapter or logical group of assets
- Stop at any checkpoint to validate learning journey independently
- Accessibility (WCAG 2.1 AA) is non-negotiable - all images need alt text, proper heading hierarchy

---

## Task Count Summary

- **Total Tasks**: 134
- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 9 tasks
- **Phase 3 (LJ1 - Physics)**: 27 tasks
- **Phase 4 (LJ2 - Sensors)**: 24 tasks
- **Phase 5 (LJ3 - Integration)**: 28 tasks
- **Phase 6 (Optional/Project)**: 16 tasks
- **Phase 7 (Polish)**: 25 tasks

**Parallel Opportunities**: 47 tasks marked [P] can run in parallel (35% of total)

**Independent Test Criteria**:
- LJ1: Spawn URDF, apply forces, observe physics and collisions
- LJ2: Attach sensors, visualize in RViz2, implement obstacle detection
- LJ3: Configure ros_gz_bridge, implement closed-loop control

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (Learning Journey 1 - Physics Simulation)
