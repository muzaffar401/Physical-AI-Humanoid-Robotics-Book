# Module 2 Overlay: The Digital Twin (Gazebo & Unity)

**Instructions**: Combine this with `base-module-prompt.md` to create the complete
Module 2 specification prompt.

---

## Module Information (PRE-FILLED)

- **Module Number**: 2
- **Module Title**: The Digital Twin (Gazebo & Unity)
- **Estimated Duration**: 12 hours over 4 weeks
- **Prerequisites**:
  - **Module 1 complete** (ROS 2 fundamentals, pub/sub, URDF)
  - Specifically: Chapter 1.2 (topics), 1.5 (URDF), 1.6 (RViz2)
  - Python programming
  - Basic 3D geometry understanding (coordinates, rotations)
- **Target Audience**: Developers and roboticists who completed Module 1 and want
  to simulate robots in physics-accurate environments

## Module Description (PRE-FILLED)

Before deploying robots in the physical world, we test them in digital twins—
photorealistic simulations that mirror real-world physics. This module covers Gazebo
(industry-standard physics simulator) and Unity (high-fidelity rendering engine).
You'll learn to spawn robots in simulated worlds, add sensors (cameras, LiDAR, IMU),
apply forces and torques, and stream sensor data to ROS 2 nodes.

Gazebo excels at physics accuracy (gravity, collisions, friction, joint dynamics)
and is deeply integrated with ROS 2 via `ros_gz_bridge`. Unity complements Gazebo
with photorealistic graphics, human-robot interaction scenarios, and procedural
world generation. By module's end, you'll simulate a humanoid robot in a virtual
environment, reading sensor data and controlling actuators—all before touching
physical hardware.

**Key Focus**: Physics simulation (Gazebo), world building, sensor models (LiDAR,
depth cameras, IMU), ROS 2 integration (ros_gz_bridge), and high-fidelity rendering
(Unity).

## Module Learning Goals (PRE-FILLED)

1. **Understand**: How physics engines simulate gravity, collisions, friction, and
   joint dynamics, and why digital twins reduce hardware risk
2. **Apply**: Spawn URDF robots in Gazebo, add Gazebo plugins for sensors (camera,
   LiDAR, IMU), and bridge sensor data to ROS 2 topics
3. **Analyze**: Compare Gazebo (physics-first) vs Unity (graphics-first) for
   different robot development use cases (e.g., control testing vs human-robot
   interaction)
4. **Create**: Build custom Gazebo worlds with obstacles and terrain, and implement
   closed-loop control (read sensor → compute command → actuate motors) in simulation

---

## Learning Journeys (PRE-FILLED)

### Learning Journey 1: Physics Simulation with Gazebo (Priority: P1)

**Narrative**: Learners start by spawning a simple wheeled robot (from Module 1 URDF)
in an empty Gazebo world, applying forces to wheels via ROS 2 topics, and observing
motion. They progress to adding inertia and friction properties, seeing how physical
parameters affect behavior. Next, they create worlds with obstacles and slopes,
understanding collision detection and contact physics. Finally, they simulate a
humanoid robot with joint controllers, preparing for balance and walking algorithms
in Module 3.

**Why this priority**: Physics simulation is foundational for all robot testing. It's
cheaper and safer than hardware experiments, and enables rapid iteration on control
algorithms.

**Independent Validation**: Learner can spawn a URDF robot in Gazebo, apply motor
commands via ROS 2 topics (e.g., `/cmd_vel`), observe realistic motion with physics
(acceleration, friction), and use Gazebo's built-in tools to inspect contact forces
and joint states.

**Learning Milestones**:
1. **Given** Gazebo running with empty world, **When** spawning a wheeled robot URDF,
   **Then** learner sees the robot appear, subject to gravity, and can apply forces
   via `/cmd_vel` topic
2. **Given** robot with inertia properties defined, **When** applying identical force
   to robots with different masses, **Then** learner observes different accelerations
   (F=ma validation)
3. **Given** world with obstacles, **When** robot collides with wall, **Then** learner
   observes collision detection (robot stops, contact forces displayed in Gazebo GUI)
4. **Given** humanoid URDF with joint plugins, **When** publishing joint position
   commands, **Then** learner sees humanoid move limbs in physics-accurate motion

### Learning Journey 2: Sensor Simulation (LiDAR, Cameras, IMU) (Priority: P1)

**Narrative**: After establishing physics, learners add perception. They begin with
a 2D LiDAR sensor plugin in Gazebo, observing scan data in RViz2 as the robot
rotates. They progress to depth cameras (3D point clouds) and RGB cameras (image
topics), understanding sensor models (FOV, resolution, noise). Next, they add an IMU
to measure orientation and angular velocity, crucial for humanoid balance. Finally,
they implement a simple obstacle avoidance algorithm: read LiDAR → detect obstacle →
command robot to turn.

**Why this priority**: Sensors are the eyes and ears of robots. Simulated sensors
generate training data for AI models (Module 3-4) and enable testing perception
algorithms without hardware.

**Independent Validation**: Learner can attach a LiDAR plugin to a Gazebo robot,
visualize scan data in RViz2, subscribe to the scan topic in a ROS 2 node, and
implement basic obstacle detection logic (if obstacle within X meters, publish stop
command).

**Learning Milestones**:
1. **Given** robot with LiDAR plugin in Gazebo, **When** running RViz2 and adding
   LaserScan display, **Then** learner sees real-time scan rays showing obstacles
2. **Given** depth camera plugin, **When** subscribing to `/camera/depth/points`
   topic, **Then** learner visualizes 3D point cloud in RViz2
3. **Given** IMU plugin, **When** tilting robot in Gazebo (apply torque), **Then**
   learner observes orientation quaternion changes in `/imu/data` topic
4. **Given** LiDAR data in ROS 2 node, **When** detecting obstacle <1 meter ahead,
   **Then** learner publishes Twist message with zero linear velocity (stop command)

### Learning Journey 3: Gazebo-ROS 2 Integration with ros_gz_bridge (Priority: P2)

**Narrative**: Learners understand that Gazebo uses its own transport (Ignition
Transport) while ROS 2 uses DDS. The `ros_gz_bridge` translates between them. They
start by manually bridging topics (e.g., `/cmd_vel` from ROS 2 to Gazebo), then
automate bridging via launch files. They explore bidirectional bridges (ROS → Gazebo
for commands, Gazebo → ROS for sensor data) and learn to debug bridge misconfigurations
(topic name mismatches, message type incompatibilities).

**Why this priority**: Critical for practical Gazebo use with ROS 2, but builds on
LJ1-2 (physics and sensors must work first). P2 because it's integration-focused,
not a new fundamental concept.

**Independent Validation**: Learner can write a ros_gz_bridge configuration that
bridges a custom topic (e.g., `/robot/custom_sensor`) from Gazebo to ROS 2, verify
the bridge is running with `ros2 topic list`, and subscribe to the bridged topic in
a ROS 2 node.

**Learning Milestones**:
1. **Given** Gazebo publishing `/model/robot/cmd_vel`, **When** configuring
   ros_gz_bridge to bridge to `/cmd_vel`, **Then** learner can control robot from
   ROS 2 teleop node
2. **Given** mismatch between Gazebo topic `/lidar/scan` and ROS 2 node expecting
   `/scan`, **When** configuring bridge remapping, **Then** learner resolves topic
   name mismatch
3. **Given** launch file with ros_gz_bridge node, **When** launching with
   `ros2 launch`, **Then** all configured topics bridge automatically
4. **Given** sensor publishing in Gazebo, **When** bridge fails due to message type
   incompatibility, **Then** learner diagnoses with `ros2 topic info` and fixes
   bridge config

### Learning Journey 4: Unity for High-Fidelity Rendering (Optional/P3)

**Narrative**: For human-robot interaction scenarios (e.g., robot navigating a
hospital, interacting with people), Gazebo's graphics may not suffice. Unity provides
photorealistic rendering and VR support. Learners import a robot model into Unity,
set up ROS-TCP-Connector for ROS 2 communication, and create a simulated indoor
environment. They compare Unity (great graphics, weaker physics) vs Gazebo (accurate
physics, simpler graphics) and learn when to use each.

**Why this priority**: P3 because Unity is optional (Gazebo suffices for most
robotics). Valuable for HRI researchers and those needing photorealistic training
data, but not core to Physical AI fundamentals.

**Independent Validation**: Learner can set up Unity with ROS-TCP-Connector, publish
robot commands from ROS 2 to Unity, and receive sensor data (simulated camera images)
back in ROS 2.

**Learning Milestones**:
1. **Given** Unity project with ROS-TCP-Connector, **When** publishing `/cmd_vel`
   from ROS 2, **Then** robot moves in Unity scene
2. **Given** Unity camera, **When** configured to publish to ROS 2 topic, **Then**
   learner receives images in RViz2
3. **Given** comparison scenario (need physics-accurate joint control), **When**
   evaluating Gazebo vs Unity, **Then** learner chooses Gazebo and justifies why
4. **Given** HRI scenario (robot must navigate realistic home environment with
   furniture, people), **When** evaluating, **Then** learner chooses Unity and
   justifies

---

## Suggested Chapter Structure (TEMPLATES)

### Chapter 2.1: Introduction to Digital Twins and Physics Simulation
- **Learning Objectives**: Define digital twin, explain benefits (cost, safety,
  iteration speed), understand physics engine components (rigid body dynamics,
  collision detection, constraint solvers)
- **Content**: Why simulate before deploy? Real-world robot failures are expensive.
  Gazebo architecture overview. Physics engines (ODE, Bullet, Simbody).
- **Hands-On**: Install Gazebo (Fortress or later), launch empty world, spawn simple
  shapes (box, sphere), apply forces via GUI
- **Assessment**: Quiz on digital twin benefits, install Gazebo successfully

### Chapter 2.2: Spawning Robots in Gazebo - URDF to SDF
- **Learning Objectives**: Convert URDF (Module 1) to SDF (Gazebo format), spawn
  robot in Gazebo, understand model components (links, joints, plugins)
- **Content**: URDF vs SDF differences, `<gazebo>` tags in URDF for Gazebo-specific
  properties, inertia and collision properties
- **Hands-On**: Take Module 1's wheeled robot URDF, add `<gazebo>` tags for friction,
  spawn in Gazebo
- **Assessment**: Spawn custom robot, verify physics (drops due to gravity)

### Chapter 2.3: Gazebo Plugins - Sensors and Actuators
- **Learning Objectives**: Understand Gazebo plugin architecture, add LiDAR plugin,
  configure camera plugin, add differential drive plugin for wheeled robots
- **Content**: Plugin types (model, sensor, world, system), libgazebo_ros_diff_drive,
  libgazebo_ros_ray_sensor
- **Hands-On**: Add 2D LiDAR to robot, visualize in RViz2; add camera, view images
- **Assessment**: Add IMU plugin, subscribe to `/imu/data`, verify orientation changes
  when robot tilted in Gazebo

### Chapter 2.4: Building Gazebo Worlds - Environments and Obstacles
- **Learning Objectives**: Create SDF world files, add static models (buildings,
  obstacles), use model database, create terrain (slopes, stairs)
- **Content**: SDF world syntax, Gazebo model database (online models), heightmaps
  for terrain
- **Hands-On**: Build warehouse world with obstacles, spawn robot, test navigation
- **Assessment**: Create custom world for testing (e.g., maze for robot to navigate)

### Chapter 2.5: Gazebo-ROS 2 Integration with ros_gz_bridge
- **Learning Objectives**: Understand Ignition Transport vs ROS 2 DDS, configure
  ros_gz_bridge, write launch files for automated bridging
- **Content**: Why bridge needed (different transports), topic and message type
  mapping, bidirectional bridges
- **Hands-On**: Bridge `/cmd_vel` to Gazebo, bridge `/scan` from Gazebo, test with
  teleop and RViz2
- **Assessment**: Debug bridge misconfiguration (wrong topic name or message type)

### Chapter 2.6: Closed-Loop Control in Simulation
- **Learning Objectives**: Implement sense-plan-act loop (read sensor → compute
  command → actuate), test obstacle avoidance algorithm
- **Content**: ROS 2 control loop pattern, reactive vs deliberative control
- **Hands-On**: Write node that reads `/scan`, detects obstacles, publishes `/cmd_vel`
  to avoid collisions
- **Assessment**: Implement wall-following behavior (keep constant distance from wall
  using LiDAR)

### Chapter 2.7: Unity for High-Fidelity Rendering (Optional)
- **Learning Objectives**: Set up Unity with ROS-TCP-Connector, compare Gazebo vs
  Unity trade-offs
- **Content**: Unity basics, ROS-TCP-Connector installation, when to use Unity
  (graphics) vs Gazebo (physics)
- **Hands-On**: Import robot into Unity, publish commands from ROS 2, receive camera
  images
- **Assessment**: Written comparison of Gazebo vs Unity for specific use case

### Chapter 2.8: Module 2 Mini-Project - Autonomous Navigation in Simulated Warehouse
- **Project**: Simulate a wheeled robot in a warehouse world, implement basic
  navigation (follow waypoints, avoid obstacles using LiDAR)
- **Requirements**: Custom Gazebo world, LiDAR and camera sensors, ROS 2 control node,
  ros_gz_bridge setup
- **Assessment**: Robot navigates from point A to B without collisions, sensor data
  logged, rqt_graph screenshot

---

## Core Concepts & Terminology (PRE-FILLED)

- **Term**: Digital Twin
- **Definition**: Virtual replica of a physical system that mirrors its behavior,
  used for testing, training, and validation before real-world deployment
- **Analogy**: Like a flight simulator for pilots—practice without risk
- **First Introduced**: Chapter 2.1
- **Related Terms**: Gazebo, Simulation, Physics Engine

---

- **Term**: Gazebo (Ignition Gazebo / Gazebo Fortress+)
- **Definition**: Open-source physics simulator for robotics, supporting rigid body
  dynamics, sensors, and ROS 2 integration
- **Analogy**: Like Unity/Unreal for games, but optimized for robotics physics
- **First Introduced**: Chapter 2.1
- **Related Terms**: SDF, Physics Engine, ros_gz_bridge, Plugin

---

- **Term**: SDF (Simulation Description Format)
- **Definition**: XML format for describing robots and worlds in Gazebo, similar to
  URDF but with additional simulation-specific features
- **Analogy**: Like URDF's older sibling with more features
- **First Introduced**: Chapter 2.2
- **Related Terms**: URDF, Gazebo, Model, World

---

- **Term**: Gazebo Plugin
- **Definition**: Shared library that extends Gazebo functionality (add sensors,
  actuators, custom physics), loaded dynamically into simulation
- **Analogy**: Like browser extensions for Chrome—adds features without modifying
  core software
- **First Introduced**: Chapter 2.3
- **Related Terms**: libgazebo_ros, Sensor Plugin, Model Plugin

---

- **Term**: ros_gz_bridge
- **Definition**: ROS 2 package that translates messages between ROS 2 (DDS transport)
  and Gazebo (Ignition Transport)
- **Analogy**: Like a translator between two people speaking different languages
- **First Introduced**: Chapter 2.5
- **Related Terms**: Ignition Transport, ROS 2 DDS, Topic Bridging

---

- **Term**: LiDAR (Light Detection and Ranging)
- **Definition**: Sensor that uses laser pulses to measure distances, producing 2D
  scan rays or 3D point clouds
- **Analogy**: Like echolocation for bats, but using light instead of sound
- **First Introduced**: Chapter 2.3
- **Related Terms**: LaserScan, Point Cloud, Range Sensor, Ray Sensor Plugin

---

- **Term**: IMU (Inertial Measurement Unit)
- **Definition**: Sensor that measures orientation (roll, pitch, yaw), angular
  velocity, and linear acceleration using accelerometers and gyroscopes
- **Analogy**: Like the inner ear's vestibular system for humans—senses balance and
  motion
- **First Introduced**: Chapter 2.3
- **Related Terms**: Orientation, Quaternion, Angular Velocity, sensor_msgs/Imu

---

- **Term**: Depth Camera
- **Definition**: Camera that measures distance to each pixel, producing RGBD (RGB +
  Depth) images or 3D point clouds
- **Analogy**: Like how our two eyes create depth perception through stereopsis
- **First Introduced**: Chapter 2.3
- **Related Terms**: Point Cloud, RGBD, sensor_msgs/PointCloud2, Stereo Camera

---

- **Term**: Physics Engine
- **Definition**: Software that simulates physical interactions (gravity, collisions,
  friction, joint constraints) using numerical methods
- **Analogy**: Like a video game physics engine (Havok, PhysX) but tuned for realism
  over performance
- **First Introduced**: Chapter 2.1
- **Related Terms**: ODE, Bullet, Collision Detection, Rigid Body Dynamics

---

[Continue with 3-5 more terms: Inertia, Collision Geometry, World, Unity,
ROS-TCP-Connector]

---

## Cross-Module Dependencies (PRE-FILLED)

### Within-Module
- **Chapter 2.1** is foundational (Gazebo installation, digital twin concepts)
- **Chapter 2.2** (Spawning robots) requires Chapter 2.1
- **Chapter 2.3** (Sensors) requires Chapter 2.2 (need spawned robot to attach
  sensors)
- **Chapter 2.5** (ros_gz_bridge) requires Chapters 2.2-2.3 (need robot and sensors
  to bridge)
- **Chapter 2.6** (Closed-loop control) integrates Chapters 2.3 + 2.5 (read sensors
  via bridge, command via bridge)
- **Chapter 2.7** (Unity) is optional and independent
- **Chapter 2.8** (Mini-Project) integrates all prior chapters

### Cross-Module

**What Module 2 Requires from Module 1**:
- **Chapter 1.2**: Pub/sub fundamentals (Gazebo publishes sensor topics)
- **Chapter 1.5**: URDF robot descriptions (Gazebo spawns URDF models)
- **Chapter 1.6**: RViz2 visualization (used to display Gazebo sensor data)

**What Module 2 Provides for Module 3 (NVIDIA Isaac)**:
- Understanding of physics simulation and sensor models
- Experience with digital twins (Isaac Sim is also a simulator)
- ROS 2 sensor topic patterns (Isaac ROS follows same patterns)

**What Module 2 Provides for Module 4 (VLA)**:
- Simulated testing environment for voice-controlled robots
- Sensor data streams (cameras, LiDAR) for perception
- Gazebo as platform for running VLA experiments

**What Module 2 Provides for Module 5 (Capstone)**:
- Complete simulation environment for testing autonomous humanoid
- Digital twin for validating voice → action pipeline

### External Dependencies

**Software**:
- **Gazebo Fortress or later** (Ignition Gazebo, not legacy Gazebo Classic)
  - **OS**: Ubuntu 22.04 (primary), also binaries for Jammy
  - **Installation**: Chapter 2.1
- **ros_gz** packages (ros_gz_bridge, ros_gz_sim)
  - Install: `sudo apt install ros-humble-ros-gz`
- **RViz2** (from Module 1, for sensor visualization)
- **Unity 2021.3 LTS** (optional, for Chapter 2.7)
  - **Unity ROS-TCP-Connector** package

**Hardware**:
- **GPU recommended**: Gazebo rendering benefits from discrete GPU (Intel/AMD/NVIDIA)
- **16GB+ RAM**: Gazebo + RViz2 + ROS 2 nodes can be memory-intensive with complex
  worlds

**External Accounts**:
- **Unity Account** (free, if using Chapter 2.7)

---

## Out of Scope (PRE-FILLED)

### Explicitly NOT Covered in Module 2

- **Advanced Physics Tuning**: Custom friction models, soft-body physics, fluid
  dynamics—focus is on rigid body robots
  - **Rationale**: Humanoid robotics primarily uses rigid body dynamics; soft-body
    is niche (e.g., soft grippers)

- **Gazebo Classic (Gazebo 11 and earlier)**: This module covers Ignition Gazebo
  (Fortress+), the modern rewrite
  - **Rationale**: Gazebo Classic is legacy; ROS 2 ecosystem is moving to Ignition

- **Custom Gazebo Plugin Development in C++**: We use existing plugins
  (libgazebo_ros_diff_drive, etc.) but don't write new ones
  - **Rationale**: Plugin development requires C++ and Gazebo API knowledge—out of
    scope for Python-focused course

- **Multi-Robot Simulation**: Coordinating multiple robots in one Gazebo world
  (swarms, fleets)
  - **Rationale**: Single-robot mastery is prerequisite; multi-robot is advanced

- **Photorealistic Rendering in Gazebo**: Basic Gazebo graphics only; Unity covered
  separately for photorealism
  - **Rationale**: Gazebo's strength is physics, not graphics; Unity handles
    high-fidelity rendering

- **Hardware-in-the-Loop (HIL) Simulation**: Connecting real hardware to Gazebo
  (e.g., real motors in simulated robot)
  - **Rationale**: Complex setup, specialized use case; course is simulation-first

- **Procedural World Generation**: Randomly generating Gazebo worlds for training
  (e.g., reinforcement learning)
  - **Rationale**: Advanced topic for Module 3 (AI training); Module 2 focuses on
    manual world creation

**Overall Rationale**: Module 2 provides practical simulation skills for testing
robots before hardware deployment. Advanced topics (custom physics, multi-robot,
procedural generation) deferred or excluded to maintain educational focus.

---

**Module 2 Overlay Complete**
**Lines**: ~550
**Status**: Ready to combine with base-module-prompt.md for `/sp.specify`
