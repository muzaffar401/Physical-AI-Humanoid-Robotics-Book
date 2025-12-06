# Feature Specification: Module 2 - The Digital Twin (Gazebo & Unity)

**Feature Branch**: `002-module-2-gazebo-unity`
**Created**: 2025-11-30
**Status**: Draft

## Module Information

- **Module Number**: 2
- **Module Title**: The Digital Twin (Gazebo & Unity)
- **Estimated Duration**: 12 hours over 4 weeks
- **Prerequisites**:
  - **Module 1 complete** (ROS 2 fundamentals, pub/sub, URDF)
  - Specifically: Chapter 1.2 (topics), 1.5 (URDF), 1.6 (RViz2)
  - Python programming
  - Basic 3D geometry understanding (coordinates, rotations)
- **Target Audience**: Developers and roboticists who completed Module 1 and want to simulate robots in physics-accurate environments

## Module Description

Before deploying robots in the physical world, we test them in digital twins—photorealistic simulations that mirror real-world physics. This module covers Gazebo (industry-standard physics simulator) and Unity (high-fidelity rendering engine). You'll learn to spawn robots in simulated worlds, add sensors (cameras, LiDAR, IMU), apply forces and torques, and stream sensor data to ROS 2 nodes.

Gazebo excels at physics accuracy (gravity, collisions, friction, joint dynamics) and is deeply integrated with ROS 2 via `ros_gz_bridge`. Unity complements Gazebo with photorealistic graphics, human-robot interaction scenarios, and procedural world generation. By module's end, you'll simulate a humanoid robot in a virtual environment, reading sensor data and controlling actuators—all before touching physical hardware.

**Key Focus**: Physics simulation (Gazebo), world building, sensor models (LiDAR, depth cameras, IMU), ROS 2 integration (ros_gz_bridge), and high-fidelity rendering (Unity).

**NEW FEATURE**: Each of the 8 chapters provides a dual-view interface with Content and Summary tabs, allowing learners to toggle between full chapter content and condensed 1-2 page summaries for quick review and prerequisite refresher.

## User Scenarios & Testing

### User Story 1 - Content/Summary Tab Navigation (Priority: P1)

Learners access each chapter and toggle between full content (default) and condensed summary views to support different learning modes: deep learning (Content tab) and quick review/reference (Summary tab).

**Why this priority**: Core feature enabler - without tab navigation, summary feature cannot function. This is the minimum viable interface that delivers value (quick review capability).

**Independent Test**: Open any chapter, verify Content tab shows by default, click Summary tab and see 300-600 word condensed version, return to Content tab. Verifies tab toggle works independently without requiring other features.

**Acceptance Scenarios**:

1. **Given** learner opens Chapter 2.1 for first time, **When** page loads, **Then** Content tab is active (default) and displays full chapter content with all sections
2. **Given** learner is viewing Content tab, **When** clicks Summary tab, **Then** Summary tab becomes active and displays condensed 300-600 word summary
3. **Given** learner is viewing Summary tab, **When** clicks Content tab, **Then** Content tab becomes active and displays full chapter content
4. **Given** learner selects Summary tab in Chapter 2.1, **When** navigates to Chapter 2.2, **Then** Chapter 2.2 opens with Summary tab active (tab selection persists via groupId)
5. **Given** learner is viewing Summary tab, **When** using keyboard Tab/Shift+Tab to navigate, **Then** can select between tabs and press Enter/Space to activate selected tab
6. **Given** learner uses screen reader, **When** encountering tab interface, **Then** screen reader announces tab labels ("Content" and "Summary") with appropriate ARIA roles

---

### User Story 2 - Summary Content for Quick Review (Priority: P1)

Learners use Summary tab to quickly review core concepts (300-600 words) before assessments or when refreshing prerequisites for next chapter, without re-reading full content.

**Why this priority**: Primary value proposition - summaries enable efficient learning review. Testable independently by verifying summary content quality and usefulness.

**Independent Test**: Read Summary tab for any chapter, verify it contains core concepts, essential commands (2-3 code examples), key diagrams, and prerequisites for next chapter in 300-600 words.

**Acceptance Scenarios**:

1. **Given** learner completed Chapter 2.2 week ago, **When** opens Summary tab before Chapter 2.3, **Then** sees 500-550 word summary with world building concepts, minimal SDF example (10 lines), essential Gazebo commands, and key commands
2. **Given** learner reviewing for Module 2 assessment, **When** opens Chapter 2.3 Summary tab, **Then** sees 550-600 word summary with sensor types (LiDAR, camera, IMU), minimal plugin code, and sensor data visualization
3. **Given** learner needs quick reference for Gazebo commands, **When** opens Chapter 2.1 Summary tab, **Then** sees essential commands (gz sim, gz model, gz topic) with brief descriptions
4. **Given** learner preparing for next chapter, **When** reads Summary tab "Prerequisites for Next Chapter" section, **Then** understands what concepts to remember and what tools to have set up

---

## Learning Journeys

### Learning Journey 1: Physics Simulation with Gazebo (Priority: P1)

**Narrative**: Learners start by spawning a simple wheeled robot (from Module 1 URDF) in an empty Gazebo world, applying forces to wheels via ROS 2 topics, and observing motion. They progress to adding inertia and friction properties, seeing how physical parameters affect behavior. Next, they create worlds with obstacles and slopes, understanding collision detection and contact physics. Finally, they simulate a humanoid robot with joint controllers, preparing for balance and walking algorithms in Module 3.

**Why this priority**: Physics simulation is foundational for all robot testing. It's cheaper and safer than hardware experiments, and enables rapid iteration on control algorithms.

**Independent Validation**: Learner can spawn a URDF robot in Gazebo, apply motor commands via ROS 2 topics (e.g., `/cmd_vel`), observe realistic motion with physics (acceleration, friction), and use Gazebo's built-in tools to inspect contact forces and joint states.

**Learning Milestones**:
1. **Given** Gazebo running with empty world, **When** spawning a wheeled robot URDF, **Then** learner sees the robot appear, subject to gravity, and can apply forces via `/cmd_vel` topic
2. **Given** robot with inertia properties defined, **When** applying identical force to robots with different masses, **Then** learner observes different accelerations (F=ma validation)
3. **Given** world with obstacles, **When** robot collides with wall, **Then** learner observes collision detection (robot stops, contact forces displayed in Gazebo GUI)
4. **Given** humanoid URDF with joint plugins, **When** publishing joint position commands, **Then** learner sees humanoid move limbs in physics-accurate motion

---

### Learning Journey 2: Sensor Simulation (LiDAR, Cameras, IMU) (Priority: P1)

**Narrative**: After establishing physics, learners add perception. They begin with a 2D LiDAR sensor plugin in Gazebo, observing scan data in RViz2 as the robot rotates. They progress to depth cameras (3D point clouds) and RGB cameras (image topics), understanding sensor models (FOV, resolution, noise). Next, they add an IMU to measure orientation and angular velocity, crucial for humanoid balance. Finally, they implement a simple obstacle avoidance algorithm: read LiDAR → detect obstacle → command robot to turn.

**Why this priority**: Sensors are the eyes and ears of robots. Simulated sensors generate training data for AI models (Module 3-4) and enable testing perception algorithms without hardware.

**Independent Validation**: Learner can attach a LiDAR plugin to a Gazebo robot, visualize scan data in RViz2, subscribe to the scan topic in a ROS 2 node, and implement basic obstacle detection logic (if obstacle within X meters, publish stop command).

**Learning Milestones**:
1. **Given** robot with LiDAR plugin in Gazebo, **When** running RViz2 and adding LaserScan display, **Then** learner sees real-time scan rays showing obstacles
2. **Given** depth camera plugin, **When** subscribing to `/camera/depth/points` topic, **Then** learner visualizes 3D point cloud in RViz2
3. **Given** IMU plugin, **When** tilting robot in Gazebo (apply torque), **Then** learner observes orientation quaternion changes in `/imu/data` topic
4. **Given** LiDAR data in ROS 2 node, **When** detecting obstacle <1 meter ahead, **Then** learner publishes Twist message with zero linear velocity (stop command)

---

### Learning Journey 3: Gazebo-ROS 2 Integration with ros_gz_bridge (Priority: P2)

**Narrative**: Learners understand that Gazebo uses its own transport (Ignition Transport) while ROS 2 uses DDS. The `ros_gz_bridge` translates between them. They start by manually bridging topics (e.g., `/cmd_vel` from ROS 2 to Gazebo), then automate bridging via launch files. They explore bidirectional bridges (ROS → Gazebo for commands, Gazebo → ROS for sensor data) and learn to debug bridge misconfigurations (topic name mismatches, message type incompatibilities).

**Why this priority**: Critical for practical Gazebo use with ROS 2, but builds on LJ1-2 (physics and sensors must work first). P2 because it's integration-focused, not a new fundamental concept.

**Independent Validation**: Learner can write a ros_gz_bridge configuration that bridges a custom topic (e.g., `/robot/custom_sensor`) from Gazebo to ROS 2, verify the bridge is running with `ros2 topic list`, and subscribe to the bridged topic in a ROS 2 node.

**Learning Milestones**:
1. **Given** Gazebo publishing `/model/robot/cmd_vel`, **When** configuring ros_gz_bridge to bridge to `/cmd_vel`, **Then** learner can control robot from ROS 2 teleop node
2. **Given** mismatch between Gazebo topic `/lidar/scan` and ROS 2 node expecting `/scan`, **When** configuring bridge remapping, **Then** learner resolves topic name mismatch
3. **Given** launch file with ros_gz_bridge node, **When** launching with `ros2 launch`, **Then** all configured topics bridge automatically
4. **Given** sensor publishing in Gazebo, **When** bridge fails due to message type incompatibility, **Then** learner diagnoses with `ros2 topic info` and fixes bridge config

---

## Core Concepts & Dependencies

**Core Concepts** (Key terminology):
- **Digital Twin**: Virtual replica of a physical system that mirrors its behavior, used for testing before real-world deployment
- **Gazebo**: Open-source physics simulator for robotics supporting rigid body dynamics, sensors, and ROS 2 integration
- **SDF (Simulation Description Format)**: XML format for describing robots and worlds in Gazebo, similar to URDF but with simulation-specific features
- **Gazebo Plugin**: Shared library that extends Gazebo functionality (sensors, actuators, custom physics), loaded dynamically into simulation
- **ros_gz_bridge**: ROS 2 package translating messages between ROS 2 (DDS) and Gazebo (Ignition Transport)
- **LiDAR**: Sensor using laser pulses to measure distances, producing 2D scan rays or 3D point clouds
- **IMU (Inertial Measurement Unit)**: Sensor measuring orientation, angular velocity, and linear acceleration using accelerometers and gyroscopes
- **Depth Camera**: Camera measuring distance to each pixel, producing RGBD images or 3D point clouds

**Within-Module Dependencies**: Chapter 2.1 (Gazebo installation, digital twin concepts) is foundational → Chapter 2.2 (spawning robots) → Chapter 2.3 (sensors) → Chapter 2.5 (ros_gz_bridge) → Chapter 2.6 (closed-loop control integrates sensors + bridge) → Chapter 2.7 (Unity, optional) → Chapter 2.8 (mini-project integrates all).

**Cross-Module Dependencies**:
- **Requires from Module 1**: Chapter 1.2 (pub/sub for Gazebo sensor topics), Chapter 1.5 (URDF for spawning robots), Chapter 1.6 (RViz2 for visualizing Gazebo data)
- **Provides for Module 3 (NVIDIA Isaac)**: Understanding of physics simulation and sensor models, experience with digital twins, ROS 2 sensor topic patterns
- **Provides for Module 4 (VLA)**: Simulated testing environment for voice-controlled robots, sensor data streams for perception, Gazebo as platform for VLA experiments
- **Provides for Module 5 (Capstone)**: Complete simulation environment for testing autonomous humanoid, digital twin for validating voice → action pipeline

**External Dependencies**:
- **Software**: Gazebo Fortress or later (Ignition Gazebo), ros_gz packages (`sudo apt install ros-humble-ros-gz`), RViz2, Unity 2021.3 LTS (optional for Chapter 2.7), Unity ROS-TCP-Connector package
- **Hardware**: GPU recommended for Gazebo rendering (Intel/AMD/NVIDIA), 16GB+ RAM (Gazebo + RViz2 + ROS 2 can be memory-intensive)
- **External Accounts**: Unity Account (free, if using Chapter 2.7)

## Out of Scope

- **Advanced Physics Tuning**: Custom friction models, soft-body physics, fluid dynamics—focus is on rigid body robots. Rationale: Humanoid robotics primarily uses rigid body dynamics; soft-body is niche.
- **Gazebo Classic (Gazebo 11 and earlier)**: This module covers Ignition Gazebo (Fortress+), the modern rewrite. Rationale: Gazebo Classic is legacy; ROS 2 ecosystem is moving to Ignition.
- **Custom Gazebo Plugin Development in C++**: We use existing plugins but don't write new ones. Rationale: Plugin development requires C++ and Gazebo API knowledge—out of scope for Python-focused course.
- **Multi-Robot Simulation**: Coordinating multiple robots in one Gazebo world (swarms, fleets). Rationale: Single-robot mastery is prerequisite; multi-robot is advanced.
- **Photorealistic Rendering in Gazebo**: Basic Gazebo graphics only; Unity covered separately for photorealism. Rationale: Gazebo's strength is physics, not graphics; Unity handles high-fidelity rendering.
- **Hardware-in-the-Loop (HIL) Simulation**: Connecting real hardware to Gazebo (e.g., real motors in simulated robot). Rationale: Complex setup, specialized use case; course is simulation-first.

---

## Planning Note

This is a concise specification (~175 lines) focused on learning outcomes, core concepts, and dependencies. For detailed chapter structure, code examples, and assessment designs, refer to:
- Detailed overlay: `.specify/templates/educational-content/modules/module-2-gazebo-unity.md`
- Reference spec: `specs/001-module-1-ros2/spec.md`

Use this spec for `/sp.plan` to design implementation approach, then `/sp.tasks` to generate actionable task breakdown.
