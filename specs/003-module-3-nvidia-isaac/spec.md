# Feature Specification: Module 3 - The AI-Robot Brain (NVIDIA Isaac)

**Feature Branch**: `003-module-3-nvidia-isaac`
**Created**: 2025-11-30
**Status**: Draft

## Module Information

- **Module Number**: 3
- **Module Title**: The AI-Robot Brain (NVIDIA Isaac™)
- **Estimated Duration**: 14 hours over 4-5 weeks
- **Prerequisites**:
  - **Module 1 complete** (ROS 2 fundamentals)
  - **Module 2 complete** (Gazebo simulation, sensors)
  - Python programming
  - **NVIDIA GPU recommended** (RTX 20-series or later for Isaac Sim)
  - Basic understanding of computer vision and SLAM concepts (helpful but not required)
- **Target Audience**: Developers and AI engineers who completed Modules 1-2 and want to leverage NVIDIA's AI-accelerated robotics platform for perception and navigation

## Module Description

NVIDIA Isaac is an end-to-end platform for AI-powered robotics, comprising Isaac Sim (photorealistic simulator with ray-traced rendering and physics), Isaac ROS (GPU-accelerated perception pipelines), and integrations with Nav2 (navigation stack). While Gazebo (Module 2) focuses on physics accuracy, Isaac Sim adds photorealism, synthetic data generation for training AI models, and NVIDIA Omniverse integration.

This module teaches you to simulate humanoid robots in Isaac Sim, generate synthetic training data (images, depth maps, segmentation masks), deploy Isaac ROS nodes for hardware-accelerated VSLAM (Visual SLAM) and object detection, and implement autonomous navigation using Nav2. By module's end, you'll have a simulated humanoid that can localize itself in an environment, plan paths to goals, and avoid obstacles—all running at real-time speeds on NVIDIA GPUs.

**Key Focus**: Isaac Sim photorealistic simulation, synthetic data generation, Isaac ROS perception pipelines (VSLAM, depth estimation), Nav2 path planning for bipedal humanoids, GPU acceleration.

## Learning Journeys

### Learning Journey 1: Isaac Sim - Photorealistic Digital Twin (Priority: P1)

**Narrative**: Learners begin by installing NVIDIA Omniverse and Isaac Sim, exploring the interface (stage, viewport, property panels). They import a humanoid robot (URDF or USD format), position it in a prebuilt environment (warehouse, hospital), and add virtual sensors (cameras, depth sensors, LiDAR). Next, they run simulation and visualize sensor outputs (RGB images, point clouds) in Isaac Sim's UI. Finally, they configure Isaac Sim to publish sensor data to ROS 2 topics, bridging the simulation to ROS 2 control nodes.

**Why this priority**: Isaac Sim is the foundation for all Module 3 work. Without it, learners cannot progress to synthetic data generation or Isaac ROS pipelines.

**Independent Validation**: Learner can launch Isaac Sim, load a humanoid robot with a camera attached, run the simulation, and subscribe to `/camera/image_raw` in ROS 2 (using RViz2 or `ros2 topic echo`) to see simulated camera images streaming in real-time.

**Learning Milestones**:
1. **Given** Isaac Sim installed, **When** launching and loading a prebuilt warehouse environment, **Then** learner can navigate the 3D viewport (pan, zoom, rotate) and inspect object properties
2. **Given** humanoid robot URDF/USD, **When** dragging into Isaac Sim stage, **Then** robot appears in scene with physics enabled (falls due to gravity if unsupported)
3. **Given** robot with camera prim attached, **When** running simulation and opening Camera Sensor Preview, **Then** learner sees real-time rendered camera view
4. **Given** Isaac ROS bridge enabled, **When** running `ros2 topic list`, **Then** learner sees `/camera/image_raw`, `/camera/depth`, etc., and can visualize in RViz2

---

### Learning Journey 2: Synthetic Data Generation for AI Training (Priority: P2)

**Narrative**: Real-world data collection for training perception models (object detection, segmentation, pose estimation) is time-consuming and expensive. Isaac Sim can generate millions of labeled images automatically. Learners start by enabling ground-truth data outputs (bounding boxes, semantic segmentation masks, instance masks). They configure randomization (lighting, textures, object poses) to create diverse datasets. Next, they export data in formats compatible with training frameworks (COCO, KITTI, custom). Finally, they understand domain randomization strategies to reduce sim-to-real gap.

**Why this priority**: Synthetic data is a key advantage of Isaac over Gazebo. However, it's P2 because basic simulation (LJ1) must work first, and not all use cases require AI training.

**Independent Validation**: Learner can configure Isaac Sim to capture 1000 images of a humanoid robot in randomized environments (varying lighting, backgrounds, object placements), with automatically generated semantic segmentation masks, and export the dataset in a structured format ready for training.

**Learning Milestones**:
1. **Given** Isaac Sim scene with objects, **When** enabling Semantic Segmentation render, **Then** learner sees color-coded segmentation masks in real-time viewport
2. **Given** object detection scenario, **When** enabling bounding box annotations, **Then** learner exports 2D/3D bounding boxes for all objects in scene in COCO JSON format
3. **Given** domain randomization script (lighting, textures), **When** running automated data capture, **Then** Isaac generates 1000+ diverse images without manual intervention
4. **Given** synthetic dataset, **When** visualizing sample images with overlaid annotations, **Then** learner verifies label quality (bounding boxes align with objects, segmentation masks accurate)

---

### Learning Journey 3: Isaac ROS - GPU-Accelerated Perception (Priority: P1)

**Narrative**: Traditional ROS 2 perception nodes run on CPU, limiting real-time performance. Isaac ROS offloads compute-intensive tasks (visual odometry, depth estimation, image segmentation) to NVIDIA GPUs using CUDA and TensorRT. Learners install Isaac ROS packages (from apt or Docker), launch Visual SLAM (cuVSLAM) on live camera feeds from Isaac Sim or real cameras, and observe pose estimation accuracy. They compare latency and accuracy with CPU-based alternatives (ORB-SLAM3), understanding when GPU acceleration justifies added complexity.

**Why this priority**: Isaac ROS is the "brain" that processes sensor data. P1 because it's essential for any AI-powered robotics application needing real-time perception.

**Independent Validation**: Learner can launch Isaac ROS Visual SLAM node, feed it stereo camera images from Isaac Sim, and observe real-time pose estimation (6DOF: position + orientation) published to `/visual_slam/pose` topic, with TF frames updated in RViz2.

**Learning Milestones**:
1. **Given** Isaac ROS installed (Docker or native), **When** launching `isaac_ros_visual_slam` node with stereo camera topics, **Then** learner sees pose estimates published at >30 Hz on GPU
2. **Given** comparison scenario, **When** running both cuVSLAM (GPU) and ORB-SLAM3 (CPU) on same data, **Then** learner measures latency difference (e.g., 10ms GPU vs 50ms CPU)
3. **Given** Isaac ROS depth estimation node, **When** processing RGB camera images, **Then** learner generates depth maps using AI model running on TensorRT
4. **Given** RViz2 with TF display, **When** Isaac ROS VSLAM running, **Then** learner visualizes robot's estimated trajectory overlaid on map

---

### Learning Journey 4: Autonomous Navigation with Nav2 (Priority: P2)

**Narrative**: Navigation 2 (Nav2) is ROS 2's navigation stack for mobile robots. Learners configure Nav2 for a bipedal humanoid (more complex than wheeled robots due to balance constraints). They create a 2D occupancy grid map of the environment (using SLAM or pre-made map), set navigation goals via RViz2, and observe Nav2 computing collision-free paths. They tune parameters (footprint, costmaps, planners) for humanoid-specific constraints (cannot turn in place, limited step height). Finally, they integrate Nav2 with Isaac ROS VSLAM for localization.

**Why this priority**: Navigation is a common robotics task, but it builds on VSLAM (LJ3) for localization. P2 because navigation is an application of perception, not a foundational perception concept itself.

**Independent Validation**: Learner can send a navigation goal to a humanoid in Isaac Sim via RViz2, watch Nav2 compute a path avoiding obstacles, and observe the robot autonomously navigate to the goal with collision avoidance in real-time.

**Learning Milestones**:
1. **Given** 2D map of environment, **When** launching Nav2 stack with map server, **Then** learner sees map displayed in RViz2 with robot localized
2. **Given** RViz2 "Nav2 Goal" tool, **When** clicking a target pose on map, **Then** Nav2 computes path (shown as green line) and robot begins navigating
3. **Given** obstacles appearing in path, **When** Nav2's dynamic costmap detects them via LiDAR, **Then** robot replans path to avoid obstacles
4. **Given** humanoid footprint (0.3m x 0.6m, non-circular), **When** tuning costmap parameters, **Then** robot navigates through narrow doorways without collisions

---

## Core Concepts & Dependencies

**Core Concepts** (Key terminology):
- **Isaac Sim**: NVIDIA's photorealistic robot simulator built on Omniverse, with ray-traced rendering, physics simulation, and ROS 2 integration
- **USD (Universal Scene Description)**: Open-source 3D scene description format (developed by Pixar) used by Isaac Sim for scene graphs, assets, and composition
- **Synthetic Data**: Artificially generated training data (images, labels) created in simulation, used to train AI models without manual annotation
- **Domain Randomization**: Technique where simulation parameters (lighting, textures, object poses) are randomized to create diverse training data, reducing sim-to-real gap
- **Isaac ROS**: Collection of GPU-accelerated ROS 2 packages for perception (VSLAM, depth estimation, object detection) leveraging CUDA and TensorRT
- **cuVSLAM (CUDA Visual SLAM)**: NVIDIA's GPU-accelerated Visual SLAM algorithm for real-time pose estimation from stereo or monocular cameras
- **Nav2 (Navigation 2)**: ROS 2's navigation framework for autonomous mobile robots, providing path planning, obstacle avoidance, and waypoint following
- **Costmap**: 2D/3D grid representing navigation costs (obstacles = high cost, free space = low cost), used by Nav2 planners to compute safe paths
- **VSLAM (Visual SLAM)**: Simultaneous Localization and Mapping using cameras (visual sensors) instead of LiDAR, estimating robot pose and building 3D map
- **TensorRT**: NVIDIA's library for optimizing and running deep learning models on GPUs with low latency (used by Isaac ROS for AI inference)

**Within-Module Dependencies**: Chapter 3.1 (Introduction, Isaac installation) is foundational → Chapter 3.2 (simulating humanoids) → Chapter 3.3 (ROS 2 integration) → Chapter 3.4 (synthetic data, independent) → Chapter 3.5 (Isaac ROS) requires 3.3 → Chapters 3.7-3.8 (Nav2) require 3.5 (VSLAM for localization) → Chapter 3.9 (mini-project integrates all).

**Cross-Module Dependencies**:
- **Requires from Module 1**: Chapter 1.2 (pub/sub for Isaac ROS topics), Chapter 1.4 (services, used by Nav2 action servers), Chapter 1.5-1.6 (URDF and RViz2 for visualization)
- **Requires from Module 2**: Understanding of simulation concepts (digital twins, sensor models), experience with sensor data (LiDAR, cameras, depth)—Isaac adds photorealism to same concepts
- **Provides for Module 4 (VLA)**: Perception pipelines (object detection, depth estimation) needed for voice-to-action tasks, navigation capabilities for humanoid movement, simulated testing environment for VLA experiments
- **Provides for Module 5 (Capstone)**: Complete perception and navigation stack, Isaac Sim as primary testing platform for autonomous humanoid

**External Dependencies**:
- **Software**: NVIDIA Omniverse (free, includes Isaac Sim), Isaac Sim 2023.1.0+, Isaac ROS (Docker recommended from NVIDIA NGC, or native via `sudo apt install ros-humble-isaac-ros-*`), Nav2 (`sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup`)
- **Hardware**: NVIDIA GPU (RTX 20-series or later, minimum RTX 2060 with 6GB VRAM, recommended RTX 3070+ with 8GB+ VRAM for complex scenes), 32GB+ RAM (Isaac Sim + large scenes are memory-intensive), 500GB+ SSD (Isaac Sim cache and USD assets require significant storage)
- **External Accounts**: NVIDIA Developer Account (free, required for Omniverse download), NGC Account (free, optional, for Isaac ROS Docker images)

## Out of Scope

- **Isaac Gym**: NVIDIA's RL training framework (reinforcement learning for robot control via GPU parallelization). Rationale: RL training is advanced AI topic beyond book scope; focus is on perception and navigation.
- **Custom Isaac ROS GEM Development**: Writing new GPU-accelerated perception nodes in C++/CUDA. Rationale: Requires CUDA programming and advanced CV knowledge; we use existing GEMs.
- **Omniverse Nucleus Collaboration**: Multi-user scene editing, version control for USD scenes. Rationale: Valuable for teams, but course is individual-focused; adds deployment complexity.
- **Advanced Nav2 Behaviors**: Behavior Trees for complex task planning (e.g., "search for object, pick up, deliver"). Rationale: Module 4 (VLA) covers task planning via LLMs; Nav2 Behavior Trees are alternative approach.
- **Multi-Robot SLAM and Coordination**: Fleet management, distributed SLAM. Rationale: Single-robot mastery is prerequisite; multi-robot is advanced topic.
- **3D Navigation (Aerial/Underwater)**: Nav2 focuses on 2D (ground robots); 3D navigation for drones/submarines is different domain. Rationale: Humanoids navigate on ground (2D sufficient); aerial robotics is separate specialization.
- **Sim-to-Real Transfer Techniques**: Fine-tuning models trained in simulation for real hardware (domain adaptation, system identification). Rationale: Requires real hardware for validation; book is simulation-focused.

---

## Planning Note

This is a concise specification (~195 lines) focused on learning outcomes, core concepts, and dependencies. For detailed chapter structure, code examples, and assessment designs, refer to:
- Detailed overlay: `.specify/templates/educational-content/modules/module-3-nvidia-isaac.md`
- Reference spec: `specs/001-module-1-ros2/spec.md`

Use this spec for `/sp.plan` to design implementation approach, then `/sp.tasks` to generate actionable task breakdown.
