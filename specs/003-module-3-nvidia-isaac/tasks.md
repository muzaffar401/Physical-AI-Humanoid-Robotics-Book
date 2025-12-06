---
description: "Task list for Module 3: The AI-Robot Brain (NVIDIA Isaac)"
---

# Tasks: Module 3 - The AI-Robot Brain (NVIDIA Isaac)

**Input**: Design documents from `/specs/003-module-3-nvidia-isaac/`
**Prerequisites**: plan.md, spec.md (4 learning journeys)

**Organization**: Tasks are grouped by learning journey to enable independent implementation and testing of each educational path.

## Format: `[ID] [P?] [Journey] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[LJ#]**: Which learning journey this task belongs to (LJ1, LJ2, LJ3, LJ4)
- Include exact file paths in descriptions

## Path Conventions

- **Educational Content**: `book_frontend/docs/module-3/` (chapter markdown files)
- **Assets**: `book_frontend/docs/assets/module-3/` (code examples, USD scenes, diagrams, images)
- **Documentation**: `specs/003-module-3-nvidia-isaac/` (research, data model, contracts)
- **Tests**: `tests/content/` and `tests/code_examples/`

---

## Phase 1: Setup (Project Infrastructure)

**Purpose**: Initialize module structure and configuration

- [ ] T001 Create module directory structure at book_frontend/docs/module-3/
- [ ] T002 Create assets directory structure at book_frontend/docs/assets/module-3/ with subdirs (code/, usd_scenes/, diagrams/, images/)
- [ ] T003 [P] Create _category_.json for Docusaurus sidebar configuration
- [ ] T004 [P] Create module index file at book_frontend/docs/module-3/index.md
- [ ] T005 [P] Create test directory structure for Module 3 validation

---

## Phase 2: Foundational (Design Documents & Prerequisites)

**Purpose**: Core planning documents that MUST be complete before ANY learning journey content

**⚠️ CRITICAL**: No chapter writing can begin until this phase is complete

- [ ] T006 Create research.md with Isaac Sim version decision (2023.1.0+), Docker vs native Isaac ROS, synthetic data formats, Nav2 humanoid tuning
- [ ] T007 Create data-model.md with chapter structure, Bloom's taxonomy objectives, dependencies (3.1→3.2→3.3→3.5, 3.7-3.8 require 3.5)
- [ ] T008 Create quickstart.md with GPU requirements (RTX 2060+ min, RTX 3070+ recommended), NVIDIA driver/CUDA setup, Omniverse installation, Docker Isaac ROS setup
- [ ] T009 [P] Create contracts/chapter-3-2-humanoid-scene.md for Isaac Sim humanoid robot scene example
- [ ] T010 [P] Create contracts/chapter-3-4-synthetic-data-generation.md for domain randomization and dataset export
- [ ] T011 [P] Create contracts/chapter-3-5-isaac-ros-vslam.md for cuVSLAM integration example
- [ ] T012 [P] Create contracts/chapter-3-7-nav2-navigation.md for Nav2 path planning with humanoid
- [ ] T013 [P] Create reusable partial at book_frontend/docs/_partials/isaac-installation.md for Omniverse and Isaac Sim setup
- [ ] T014 [P] Create reusable partial at book_frontend/docs/_partials/gpu-troubleshooting.md for CUDA/GPU driver issues

**Checkpoint**: Foundation documents ready - learning journey content implementation can now begin

---

## Phase 3: Learning Journey 1 - Isaac Sim Photorealistic Digital Twin (Priority: P1) 🎯 MVP

**Goal**: Learners can launch Isaac Sim, load humanoid robots with sensors, run photorealistic simulations, and publish sensor data to ROS 2 topics

**Independent Test**: Launch Isaac Sim, load humanoid with camera, run simulation, subscribe to `/camera/image_raw` in ROS 2 (RViz2), see real-time camera images streaming

### Chapter 3.1: Introduction to NVIDIA Isaac Platform

- [ ] T015 [LJ1] Write chapter-3-1-introduction.md with Isaac platform overview, Isaac Sim vs Gazebo comparison, Omniverse ecosystem
- [ ] T016 [LJ1] Add learning objectives (Remember: define Isaac Sim/USD, Understand: explain GPU acceleration benefits)
- [ ] T017 [P] [LJ1] Create isaac-platform-architecture.svg diagram showing Isaac Sim + Isaac ROS + Nav2 integration
- [ ] T018 [LJ1] Add hands-on exercise: Install NVIDIA Omniverse Launcher and Isaac Sim
- [ ] T019 [LJ1] Add GPU requirements section with VRAM recommendations (6GB min, 8GB+ recommended)
- [ ] T020 [LJ1] Add chapter summary and transition to Chapter 3.2

### Chapter 3.2: Simulating Humanoid Robots in Isaac Sim

- [ ] T021 [LJ1] Write chapter-3-2-simulating-humanoids.md covering Isaac Sim UI, USD scene graph, robot import
- [ ] T022 [LJ1] Add learning objectives (Apply: import URDF/USD robot, Analyze: navigate Isaac Sim interface)
- [ ] T023 [P] [LJ1] Create USD scene at book_frontend/docs/assets/module-3/usd_scenes/warehouse_environment.usd
- [ ] T024 [P] [LJ1] Create USD humanoid robot at book_frontend/docs/assets/module-3/usd_scenes/humanoid_simple.usd
- [ ] T025 [P] [LJ1] Create isaac-sim-ui-overview.svg diagram showing stage, viewport, property panels
- [ ] T026 [LJ1] Add guided walkthrough: Launch Isaac Sim, load warehouse environment, navigate 3D viewport
- [ ] T027 [LJ1] Add exercise 1: Import humanoid URDF, position in scene, enable physics, run simulation (robot falls)
- [ ] T028 [LJ1] Add exercise 2: Add ground plane, rerun simulation, observe physics-accurate landing
- [ ] T029 [LJ1] Add milestone validation: Robot appears in scene with physics enabled

### Chapter 3.3: Sensors and ROS 2 Integration

- [ ] T030 [LJ1] Write chapter-3-3-sensors-ros2.md covering camera prims, depth sensors, LiDAR, ROS 2 bridge
- [ ] T031 [LJ1] Add learning objectives (Apply: attach camera to robot, Create: configure ROS 2 bridge for sensors)
- [ ] T032 [P] [LJ1] Create Python script at book_frontend/docs/assets/module-3/code/chapter-3-3/add_camera_sensor.py
- [ ] T033 [P] [LJ1] Create Isaac ROS bridge configuration example
- [ ] T034 [P] [LJ1] Create sensor-data-flow.svg diagram showing Isaac Sim → ROS 2 topic publishing
- [ ] T035 [LJ1] Add camera sensor section: RGB camera prim, resolution, FOV, sensor preview
- [ ] T036 [LJ1] Add guided walkthrough: Attach camera to humanoid head, enable Camera Sensor Preview
- [ ] T037 [LJ1] Add exercise 1: Configure camera intrinsics (640x480, 90° FOV), preview in Isaac UI
- [ ] T038 [LJ1] Add depth sensor section: Depth camera, point cloud output, `/camera/depth` topic
- [ ] T039 [P] [LJ1] Create depth camera setup example
- [ ] T040 [LJ1] Add exercise 2: Add depth camera, run simulation, visualize depth map
- [ ] T041 [LJ1] Add ROS 2 bridge section: Enable Isaac ROS bridge extension, configure topics
- [ ] T042 [LJ1] Add guided walkthrough: Enable bridge, run `ros2 topic list`, see `/camera/image_raw`
- [ ] T043 [LJ1] Add exercise 3: Subscribe to camera topic in RViz2, verify real-time streaming
- [ ] T044 [LJ1] Add milestone validation: Camera images stream to ROS 2 at >30 FPS

### Isaac Sim Assets

- [ ] T045 [P] [LJ1] Create screenshot isaac-sim-warehouse.webp showing photorealistic warehouse scene
- [ ] T046 [P] [LJ1] Create screenshot isaac-sim-camera-preview.webp showing sensor preview panel
- [ ] T047 [P] [LJ1] Create screenshot rviz2-isaac-camera.webp showing RViz2 with Isaac camera feed
- [ ] T048 [P] [LJ1] Create usd-scene-graph.svg diagram explaining USD prims and hierarchy
- [ ] T049 [P] [LJ1] Create code validation test at tests/code_examples/test_chapter_3_2_usd.py

**Checkpoint**: Learning Journey 1 complete - learners can simulate humanoids in photorealistic environments with ROS 2 integration

---

## Phase 4: Learning Journey 2 - Synthetic Data Generation (Priority: P2)

**Goal**: Learners can generate synthetic training datasets (images, segmentation masks, bounding boxes) using domain randomization for AI model training

**Independent Test**: Configure Isaac Sim to capture 1000 images with semantic segmentation masks in randomized environments, export in COCO format

### Chapter 3.4: Synthetic Data and Domain Randomization

- [ ] T050 [LJ2] Write chapter-3-4-synthetic-data.md covering ground-truth data, domain randomization, dataset export
- [ ] T051 [LJ2] Add learning objectives (Create: generate synthetic dataset, Evaluate: assess label quality)
- [ ] T052 [P] [LJ2] Create domain-randomization-concept.svg diagram showing varying lighting/textures/poses
- [ ] T053 [LJ2] Add synthetic data fundamentals: Why synthetic data, sim-to-real gap, annotation formats (COCO, KITTI)
- [ ] T054 [LJ2] Add guided walkthrough: Enable Semantic Segmentation render in Isaac Sim viewport
- [ ] T055 [LJ2] Add exercise 1: Configure class IDs for objects (humanoid=1, floor=2, obstacles=3), visualize segmentation
- [ ] T056 [LJ2] Add bounding box section: 2D and 3D bounding boxes, automatic annotation
- [ ] T057 [P] [LJ2] Create Python script at book_frontend/docs/assets/module-3/code/chapter-3-4/export_coco_annotations.py
- [ ] T058 [LJ2] Add exercise 2: Enable bounding box writer, capture 100 images with COCO JSON annotations
- [ ] T059 [LJ2] Add domain randomization section: Randomize lighting (HDR environment maps), textures, object poses
- [ ] T060 [P] [LJ2] Create Replicator script at book_frontend/docs/assets/module-3/code/chapter-3-4/randomization_script.py
- [ ] T061 [LJ2] Add guided walkthrough: Write Replicator script that randomizes 5 parameters, run automated capture
- [ ] T062 [LJ2] Add exercise 3: Generate 1000 images with randomized scenes, verify diversity visually
- [ ] T063 [LJ2] Add dataset export section: Organize images and annotations, validate with visualization script
- [ ] T064 [P] [LJ2] Create visualization script at book_frontend/docs/assets/module-3/code/chapter-3-4/visualize_annotations.py
- [ ] T065 [LJ2] Add exercise 4: Visualize sample images with overlaid bounding boxes and segmentation masks
- [ ] T066 [LJ2] Add milestone validation: Successfully export 1000-image dataset with accurate annotations

### Synthetic Data Assets

- [ ] T067 [P] [LJ2] Create screenshot semantic-segmentation-view.webp showing color-coded segmentation
- [ ] T068 [P] [LJ2] Create screenshot bounding-box-annotations.webp with 2D boxes overlaid
- [ ] T069 [P] [LJ2] Create synthetic-data-pipeline.svg diagram showing capture → randomization → export flow
- [ ] T070 [P] [LJ2] Create sample COCO JSON snippet for documentation

**Checkpoint**: Learning Journey 2 complete - learners can generate AI training datasets from simulation

---

## Phase 5: Learning Journey 3 - Isaac ROS GPU-Accelerated Perception (Priority: P1)

**Goal**: Learners can deploy Isaac ROS nodes for real-time VSLAM and depth estimation, leveraging GPU acceleration for <10ms latency perception

**Independent Test**: Launch Isaac ROS Visual SLAM node, feed stereo camera images from Isaac Sim, observe 6DOF pose published to `/visual_slam/pose` at >30 Hz

### Chapter 3.5: Isaac ROS Installation and Architecture

- [ ] T071 [LJ3] Write chapter-3-5-isaac-ros-intro.md covering Isaac ROS packages, CUDA/TensorRT, Docker setup
- [ ] T072 [LJ3] Add learning objectives (Understand: explain GPU acceleration benefits, Apply: install Isaac ROS)
- [ ] T073 [P] [LJ3] Create isaac-ros-architecture.svg diagram showing ROS 2 node → CUDA kernel → TensorRT inference
- [ ] T074 [LJ3] Add Isaac ROS overview: GEMs (GPU-accelerated nodes), comparison with CPU perception
- [ ] T075 [LJ3] Add installation section: Docker method (recommended) vs native apt install
- [ ] T076 [P] [LJ3] Create Docker setup script at book_frontend/docs/assets/module-3/code/chapter-3-5/isaac_ros_docker_setup.sh
- [ ] T077 [LJ3] Add guided walkthrough: Pull Isaac ROS Docker image from NGC, run container with GPU support
- [ ] T078 [LJ3] Add exercise 1: Verify Isaac ROS installation with `ros2 pkg list | grep isaac_ros`
- [ ] T079 [LJ3] Add GPU requirements verification: Check CUDA version, TensorRT installation
- [ ] T080 [LJ3] Add milestone validation: Isaac ROS Docker container running with GPU access confirmed

### Chapter 3.6: Visual SLAM with cuVSLAM

- [ ] T081 [LJ3] Write chapter-3-6-visual-slam.md covering VSLAM concepts, cuVSLAM node, pose estimation
- [ ] T082 [LJ3] Add learning objectives (Apply: launch cuVSLAM, Analyze: compare GPU vs CPU VSLAM performance)
- [ ] T083 [P] [LJ3] Create vslam-concept.svg diagram showing feature tracking, pose estimation, map building
- [ ] T084 [LJ3] Add VSLAM fundamentals: Visual odometry, loop closure, why cameras vs LiDAR
- [ ] T085 [LJ3] Add cuVSLAM section: Stereo vs monocular mode, camera calibration requirements
- [ ] T086 [P] [LJ3] Create launch file at book_frontend/docs/assets/module-3/code/chapter-3-6/cuVSLAM_launch.py
- [ ] T087 [LJ3] Add guided walkthrough: Launch Isaac Sim with stereo cameras, start cuVSLAM node
- [ ] T088 [LJ3] Add exercise 1: Observe `/visual_slam/pose` topic, verify 30+ Hz publish rate
- [ ] T089 [LJ3] Add TF visualization section: cuVSLAM publishes TF transforms (odom → camera_link)
- [ ] T090 [LJ3] Add exercise 2: Visualize TF tree in RViz2, see robot trajectory as it moves in Isaac Sim
- [ ] T091 [LJ3] Add performance comparison: Run cuVSLAM (GPU) vs ORB-SLAM3 (CPU), measure latency
- [ ] T092 [P] [LJ3] Create benchmark script at book_frontend/docs/assets/module-3/code/chapter-3-6/vslam_benchmark.py
- [ ] T093 [LJ3] Add exercise 3: Record latency data, create comparison table (GPU: ~10ms, CPU: ~50ms)
- [ ] T094 [LJ3] Add milestone validation: cuVSLAM running at >30 Hz with accurate pose estimation

### Chapter 3.X: Depth Estimation with Isaac ROS

- [ ] T095 [P] [LJ3] Write chapter section on Isaac ROS depth estimation (DNN-based stereo depth)
- [ ] T096 [P] [LJ3] Add DNN depth model: ESS (Efficient Stereo Separation), TensorRT optimization
- [ ] T097 [P] [LJ3] Create depth estimation example at book_frontend/docs/assets/module-3/code/chapter-3-6/depth_estimation.py
- [ ] T098 [P] [LJ3] Add exercise: Run depth estimation on Isaac Sim stereo images, visualize depth maps in RViz2

### Isaac ROS Assets

- [ ] T099 [P] [LJ3] Create screenshot cuVSLAM-trajectory.webp showing RViz2 with robot path overlay
- [ ] T100 [P] [LJ3] Create gpu-acceleration-diagram.svg showing CPU vs GPU processing pipeline
- [ ] T101 [P] [LJ3] Create isaac-ros-performance-chart.svg with latency comparison (GPU vs CPU)
- [ ] T102 [P] [LJ3] Create code validation test at tests/code_examples/test_chapter_3_6_docker.py

**Checkpoint**: Learning Journey 3 complete - learners can deploy GPU-accelerated perception pipelines

---

## Phase 6: Learning Journey 4 - Autonomous Navigation with Nav2 (Priority: P2)

**Goal**: Learners can configure Nav2 for humanoid robots, create occupancy grid maps, send navigation goals, and observe collision-free path planning

**Independent Test**: Send navigation goal to humanoid in Isaac Sim via RViz2, watch Nav2 compute path, observe autonomous navigation with obstacle avoidance

### Chapter 3.7: Nav2 Fundamentals for Humanoids

- [ ] T103 [LJ4] Write chapter-3-7-nav2-fundamentals.md covering Nav2 architecture, costmaps, planners
- [ ] T104 [LJ4] Add learning objectives (Understand: explain Nav2 components, Apply: configure Nav2 for humanoid)
- [ ] T105 [P] [LJ4] Create nav2-architecture.svg diagram showing map server, planners, controllers, costmaps
- [ ] T106 [LJ4] Add Nav2 overview: Behavior Trees, action servers, recovery behaviors
- [ ] T107 [LJ4] Add humanoid-specific challenges: Non-circular footprint, balance constraints, limited maneuverability
- [ ] T108 [P] [LJ4] Create Nav2 config file at book_frontend/docs/assets/module-3/code/chapter-3-7/humanoid_nav2_params.yaml
- [ ] T109 [LJ4] Add guided walkthrough: Create 2D occupancy grid map of Isaac Sim warehouse
- [ ] T110 [LJ4] Add exercise 1: Launch Nav2 with map server, visualize map in RViz2
- [ ] T111 [LJ4] Add footprint configuration: Define humanoid footprint (0.3m x 0.6m rectangular)
- [ ] T112 [LJ4] Add exercise 2: Tune costmap inflation radius for humanoid size
- [ ] T113 [LJ4] Add milestone validation: Nav2 stack running with humanoid-specific configuration

### Chapter 3.8: Path Planning and Obstacle Avoidance

- [ ] T114 [LJ4] Write chapter-3-8-path-planning.md covering global/local planners, dynamic obstacles, replanning
- [ ] T115 [LJ4] Add learning objectives (Create: send navigation goals, Evaluate: test obstacle avoidance)
- [ ] T116 [P] [LJ4] Create path-planning-concept.svg diagram showing global path (A*) vs local trajectory (DWB)
- [ ] T117 [LJ4] Add global planner section: NavFn vs Smac Planner for grid-based planning
- [ ] T118 [LJ4] Add guided walkthrough: Send "Nav2 Goal" in RViz2, observe green path line
- [ ] T119 [LJ4] Add exercise 1: Send goal across warehouse, watch humanoid navigate autonomously
- [ ] T120 [LJ4] Add local planner section: DWB (Dynamic Window Approach) for trajectory following
- [ ] T121 [LJ4] Add exercise 2: Place dynamic obstacle in path, observe Nav2 replanning
- [ ] T122 [LJ4] Add integration with VSLAM: Use cuVSLAM for localization instead of AMCL
- [ ] T123 [P] [LJ4] Create integrated launch file at book_frontend/docs/assets/module-3/code/chapter-3-8/nav2_vslam_launch.py
- [ ] T124 [LJ4] Add exercise 3: Run Nav2 with cuVSLAM localization, no pre-made map (SLAM mode)
- [ ] T125 [LJ4] Add milestone validation: Humanoid navigates to goal avoiding obstacles autonomously

### Navigation Assets

- [ ] T126 [P] [LJ4] Create screenshot nav2-rviz-goal.webp showing RViz2 with goal pose and planned path
- [ ] T127 [P] [LJ4] Create screenshot humanoid-navigating.webp showing robot in motion with costmap overlay
- [ ] T128 [P] [LJ4] Create costmap-layers.svg diagram showing static map, obstacle layer, inflation layer
- [ ] T129 [P] [LJ4] Create code validation test at tests/code_examples/test_chapter_3_8_nav2.py

**Checkpoint**: Learning Journey 4 complete - learners have end-to-end autonomous navigation

---

## Phase 7: Mini-Project and Integration

**Purpose**: Integrative mini-project combining all learning journeys

### Chapter 3.9: Mini-Project - Autonomous Warehouse Assistant

- [ ] T130 Write chapter-3-9-mini-project.md with comprehensive project requirements
- [ ] T131 Add project goal: Humanoid robot patrols warehouse, detects objects with Isaac ROS, navigates to inspection points
- [ ] T132 Add requirements: Isaac Sim scene, cuVSLAM for localization, Nav2 for path planning, synthetic data collection
- [ ] T133 Add assessment rubric: Simulation quality (15%), VSLAM accuracy (25%), Navigation success (30%), Dataset quality (20%), Integration (10%)
- [ ] T134 [P] Create warehouse_patrol.usd scene at book_frontend/docs/assets/module-3/usd_scenes/
- [ ] T135 [P] Create mini_project_starter.py template with TODOs
- [ ] T136 Add success criteria: Robot visits 5 waypoints, collects 500 synthetic images, avoids obstacles
- [ ] T137 Add extension challenges: Object detection with Isaac ROS, multi-floor navigation, dynamic replanning
- [ ] T138 Create end-to-end-architecture.svg showing all Module 3 components integrated

**Checkpoint**: Complete mini-project demonstrates mastery of Isaac platform

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Content validation, quality assurance, and documentation

### Documentation & Index

- [ ] T139 [P] Write comprehensive module index at book_frontend/docs/module-3/index.md
- [ ] T140 [P] Add GPU requirements warning in index (RTX 2060+ minimum, performance expectations)
- [ ] T141 [P] Add module navigation links to all chapter files
- [ ] T142 [P] Add "How to use this module" with LJ1+LJ3 as critical path (can skip LJ2+LJ4 initially)

### Content Validation

- [ ] T143 [P] Create test_markdown_lint.py for Vale linting
- [ ] T144 [P] Create test_links.py for link checking
- [ ] T145 [P] Create test_accessibility.py for WCAG 2.1 AA compliance
- [ ] T146 Run Vale linting on all Module 3 chapters
- [ ] T147 Run markdown-link-check on all chapter files
- [ ] T148 Verify all images have alt text and <200KB file size
- [ ] T149 Validate all Python code examples (syntax, imports)
- [ ] T150 Verify all USD scenes can load in Isaac Sim without errors

### Isaac-Specific Testing

- [ ] T151 [P] Test all USD scenes in Isaac Sim headless mode (CI-friendly)
- [ ] T152 [P] Validate Docker examples with nvidia-docker runtime
- [ ] T153 [P] Test Nav2 configuration files with `nav2_bringup`
- [ ] T154 Verify all Isaac ROS examples work with mocked data (for CI without GPU)
- [ ] T155 Test cuVSLAM launch file with sample rosbag data

### Docusaurus Build & Performance

- [ ] T156 Run Docusaurus build and verify no errors
- [ ] T157 Verify page load time <3s (Module 3 has larger assets)
- [ ] T158 Compress all screenshot images to <200KB (WebP format)
- [ ] T159 Verify all SVG diagrams render correctly

### Final Review

- [ ] T160 Review all learning objectives are addressed
- [ ] T161 Verify chapter dependencies (3.1→3.2→3.3→3.5, 3.7-3.8 require 3.5)
- [ ] T162 Check all exercises have GPU considerations noted (may run slower on lower-end GPUs)
- [ ] T163 Validate milestone tests align with learning journey goals
- [ ] T164 Run quickstart.md validation (Omniverse install, GPU driver setup)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all learning journeys
- **Learning Journeys (Phase 3-6)**: All depend on Foundational phase completion
  - LJ1 (Isaac Sim - P1): Can start after Foundational
  - LJ2 (Synthetic Data - P2): Depends on LJ1 (needs Isaac Sim working)
  - LJ3 (Isaac ROS - P1): Can start after Foundational (parallel with LJ1, but uses LJ1 camera data)
  - LJ4 (Nav2 - P2): Depends on LJ3 (uses cuVSLAM for localization)
- **Mini-Project (Phase 7)**: Depends on LJ1 + LJ3 minimum (LJ2+LJ4 optional but recommended)
- **Polish (Phase 8)**: Depends on all content chapters being complete

### Learning Journey Dependencies

- **LJ1 (Isaac Sim)**: Independent - foundational for all Isaac work
- **LJ2 (Synthetic Data)**: Depends on LJ1 (uses Isaac Sim scenes)
- **LJ3 (Isaac ROS)**: Depends on LJ1 (needs camera data from Isaac Sim)
- **LJ4 (Nav2)**: Depends on LJ1 + LJ3 (needs simulation environment and VSLAM)

### Critical Path for MVP

Minimum viable module: LJ1 (Isaac Sim) + LJ3 (Isaac ROS VSLAM)
- Learners get photorealistic simulation + GPU-accelerated perception
- Can skip synthetic data (LJ2) and navigation (LJ4) initially

### Within Each Learning Journey

- Chapter writing before USD scenes/diagrams/code
- USD scenes marked [P] can be created in parallel
- Diagrams marked [P] can be created in parallel
- Code examples marked [P] can be created in parallel
- Exercises follow guided walkthroughs
- Milestone validation at end of each learning journey

### Parallel Opportunities

- All Setup tasks (T001-T005) can run in parallel
- All Foundational contracts (T009-T012) can run in parallel
- All Foundational partials (T013-T014) can run in parallel
- Once Foundational completes:
  - LJ1 (Isaac Sim) can start immediately
  - LJ3 (Isaac ROS) can start in parallel (uses sample data initially, integrates with LJ1 later)
- Within each LJ: USD scenes, diagrams, code examples marked [P] can run in parallel
- All Polish tasks marked [P] can run in parallel after content complete

---

## Parallel Example: Learning Journey 1 (Isaac Sim)

```bash
# After Chapter 3.2 content is written, launch all assets together:
Task: "Create warehouse_environment.usd"
Task: "Create humanoid_simple.usd"
Task: "Create isaac-sim-ui-overview.svg"
Task: "Create screenshot isaac-sim-warehouse.webp"

# After Chapter 3.3 content is written, launch all assets together:
Task: "Create add_camera_sensor.py script"
Task: "Create Isaac ROS bridge config"
Task: "Create sensor-data-flow.svg diagram"
Task: "Create screenshot rviz2-isaac-camera.webp"
```

---

## Implementation Strategy

### MVP First (LJ1 + LJ3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: Learning Journey 1 (Isaac Sim)
4. Complete Phase 5: Learning Journey 3 (Isaac ROS VSLAM)
5. **STOP and VALIDATE**: Learners can simulate robots and run GPU perception
6. Deploy/demo (core Isaac value delivered)

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add LJ1 (Isaac Sim) → Test independently → Deploy/Demo (MVP!)
3. Add LJ3 (Isaac ROS) → Test independently → Deploy/Demo
4. Add LJ2 (Synthetic Data) → Test independently → Deploy/Demo
5. Add LJ4 (Nav2) → Test independently → Deploy/Demo
6. Add Chapter 3.9 (Mini-Project) → Complete module

### Parallel Team Strategy

With multiple content creators:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Creator A: LJ1 (Isaac Sim) - Chapters 3.1, 3.2, 3.3
   - Creator B: LJ3 (Isaac ROS) - Chapters 3.5, 3.6
   - Creator C: Research, GPU requirements documentation, USD scene creation
3. After LJ1 complete:
   - Creator A: LJ2 (Synthetic Data) - Chapter 3.4
   - Creator B: LJ4 (Nav2) - Chapters 3.7, 3.8
4. All creators: Chapter 3.9 (Mini-Project) integration and polish

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [LJ#] label maps task to specific learning journey
- **GPU Requirements**: All Isaac Sim and Isaac ROS tasks assume RTX 2060+ GPU
- Tests use Isaac Sim headless mode and mocked Isaac ROS data for CI (no GPU required)
- USD scenes should be tested in Isaac Sim to verify they load correctly
- Docker examples are preferred over native install for reproducibility
- All code examples must include GPU memory usage notes (large scenes require 8GB+ VRAM)
- Accessibility: All Isaac Sim screenshots need descriptive alt text explaining what's shown

---

## Task Count Summary

- **Total Tasks**: 164
- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 9 tasks
- **Phase 3 (LJ1 - Isaac Sim)**: 35 tasks
- **Phase 4 (LJ2 - Synthetic Data)**: 21 tasks
- **Phase 5 (LJ3 - Isaac ROS)**: 32 tasks
- **Phase 6 (LJ4 - Nav2)**: 27 tasks
- **Phase 7 (Mini-Project)**: 9 tasks
- **Phase 8 (Polish)**: 26 tasks

**Parallel Opportunities**: 56 tasks marked [P] can run in parallel (34% of total)

**Hardware Requirements**:
- Minimum: RTX 2060 (6GB VRAM), 32GB RAM, 500GB SSD
- Recommended: RTX 3070+ (8GB+ VRAM), 32GB RAM, 1TB NVMe SSD

**Independent Test Criteria**:
- LJ1: Launch Isaac Sim, load humanoid, stream camera to ROS 2 at 30+ FPS
- LJ2: Generate 1000-image dataset with semantic segmentation in COCO format
- LJ3: Run cuVSLAM at 30+ Hz with <10ms latency on GPU
- LJ4: Humanoid navigates autonomously to goal with obstacle avoidance

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (LJ1) + Phase 5 (LJ3) = Isaac Sim + GPU-accelerated perception
