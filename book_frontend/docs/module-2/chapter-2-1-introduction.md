---
id: chapter-2-1-introduction
title: "Chapter 2.1: Introduction to Gazebo"
sidebar_label: "2.1 Introduction"
sidebar_position: 1
---

# Chapter 2.1: Introduction to Gazebo

## Simulate Before You Build

Imagine spending months building a humanoid robot, only to discover your navigation algorithm fails because you didn't account for momentum when turning. Or your gripper can't pick up objects because friction coefficients were wrong. **Gazebo** lets you catch these issues in simulation—before expensive hardware mistakes.

In this chapter, you'll discover what digital twins are, why physics-based simulation is critical for robotics development, and how to install and run Gazebo with ROS 2. By the end, you'll spawn your first robot in a virtual world and understand the power of testing in simulation.

---

## Learning Objectives

By the end of this chapter, you will:

- **Understand**: Define digital twin, physics simulation, and Gazebo's role in robotics development
- **Understand**: Explain advantages of simulation-first development (cost, safety, iteration speed)
- **Apply**: Install Gazebo Fortress (Ignition Gazebo) and integrate with ROS 2 Humble
- **Apply**: Launch Gazebo, explore the interface, and spawn a robot from a URDF file
- **Analyze**: Inspect physics properties (gravity, friction, inertia) and their effects on robot behavior

**Estimated Time**: 2 hours

---

## Prerequisites

- **Module 1 complete** (especially Chapter 1.2 pub/sub, Chapter 1.5 URDF, Chapter 1.6 RViz2)
- **ROS 2 Humble installed** (from Chapter 1.1)
- **Ubuntu 22.04** (recommended) or **WSL2**
- **Basic 3D geometry understanding** (coordinates, rotations)

---

## What You'll Build

By the end of this chapter, you'll have:

✅ Gazebo Fortress installed and integrated with ROS 2
✅ Understanding of digital twins and physics simulation
✅ Your first robot spawned in a Gazebo world
✅ Ability to inspect physics properties and modify simulations

---

## What is a Digital Twin?

A **digital twin** is a virtual replica of a physical system that mirrors its behavior in real-time. In robotics, digital twins let you:

- **Test algorithms safely**: No risk of hardware damage from buggy code
- **Iterate faster**: Modify code, rerun simulation in seconds (no hardware setup)
- **Generate training data**: Simulate thousands of scenarios for AI model training
- **Validate before deployment**: Catch edge cases that human testing might miss

### Real-World Examples

**🚗 Automotive**: Waymo simulates billions of miles of autonomous driving before road testing. They recreate real-world accidents in simulation to verify safety improvements.

**🏭 Manufacturing**: BMW uses digital twins to test factory layouts and robot workflows before installing physical equipment—saving millions in reconfiguration costs.

**🚀 Aerospace**: NASA tested Mars rover navigation algorithms in simulated Martian terrain, accounting for gravity, dust, and rock formations.

**🤖 Humanoids**: Boston Dynamics runs Atlas through thousands of simulated parkour scenarios, tuning balance controllers before attempting on real hardware.

### Simulation vs. Real-World Testing

| Aspect | Simulation | Real-World |
|--------|-----------|------------|
| **Cost** | Free after setup | Hardware wear, facility costs |
| **Safety** | Crashes don't damage anything | Risk of injury/damage |
| **Iteration Speed** | Seconds to restart | Minutes to reset hardware |
| **Data Collection** | Millions of samples easily | Time-consuming, labor-intensive |
| **Realism** | Limited by model accuracy | Perfect ground truth |
| **Edge Cases** | Easy to script rare events | Hard to reproduce |

**Key Insight**: The best approach is **simulation-first** (develop and debug in Gazebo) **then hardware validation** (test on real robot). Gazebo reduces 90% of development time.

---

## Why Gazebo for Robotics?

Gazebo (specifically **Ignition Gazebo**, also called Gazebo Fortress/Garden/Harmonic) is the industry-standard robot simulator for several reasons:

### 1. Physics Accuracy

Gazebo simulates real-world physics using proven engines:

- **ODE (Open Dynamics Engine)**: Default physics engine, good for general robotics
- **Bullet**: Fast collision detection, used in gaming and VR
- **DART**: Advanced constraint handling for complex mechanisms

**What gets simulated**:
- Gravity, friction (static and dynamic), restitution (bounciness)
- Joint limits, damping, spring forces
- Collision detection and contact forces
- Inertia and momentum

### 2. ROS 2 Native Integration

Gazebo communicates with ROS 2 via `ros_gz_bridge`, translating between:
- **Gazebo's Ignition Transport** (internal message passing)
- **ROS 2's DDS** (your ROS 2 nodes)

This means you can:
- Control simulated robots with ROS 2 topics (e.g., `/cmd_vel`)
- Read simulated sensor data (cameras, LiDAR, IMU) in ROS 2 nodes
- Visualize Gazebo sensor data in RViz2

### 3. Rich Sensor Models

Gazebo simulates realistic sensors with configurable noise:

- **Cameras**: RGB, depth, thermal imaging
- **LiDAR**: 2D laser scanners, 3D point clouds (Velodyne models)
- **IMU**: Accelerometers, gyroscopes with drift
- **GPS**: Latitude/longitude with accuracy settings
- **Force/Torque sensors**: Measure contact forces

### 4. Extensibility with Plugins

Gazebo uses **plugins** (shared libraries) to add custom functionality:
- **Model plugins**: Attach to robots (e.g., differential drive controller)
- **Sensor plugins**: Add sensors (cameras, LiDAR)
- **World plugins**: Global behaviors (wind, lighting changes)
- **System plugins**: Core Gazebo extensions

You can use existing plugins or write your own (C++, advanced).

### 5. Industry Adoption

**Who uses Gazebo**:
- **Amazon Robotics**: Warehouse automation (testing picking algorithms)
- **NASA**: Mars rover navigation and manipulation
- **Automotive**: ADAS (Advanced Driver Assistance Systems) validation
- **Research Labs**: Worldwide standard for academic robotics research

**Competition Support**: Used in DARPA Robotics Challenge, RoboCup, Virtual RobotX.

---

## Gazebo Architecture: How It Works

### Gazebo vs. ROS 2 Relationship

```
┌──────────────────────────────────────┐
│         Your ROS 2 Nodes             │
│   (Python/C++ code you write)        │
└────────────┬─────────────────────────┘
             │ ROS 2 Topics
             │ (DDS middleware)
             v
┌──────────────────────────────────────┐
│       ros_gz_bridge                  │
│  (Translates ROS 2 ↔ Gazebo)        │
└────────────┬─────────────────────────┘
             │ Ignition Transport
             v
┌──────────────────────────────────────┐
│         Gazebo Simulation            │
│  - Physics Engine (ODE/Bullet/DART)  │
│  - Rendering (OGRE graphics engine)  │
│  - Sensor Models (cameras, LiDAR)    │
│  - World/Robot Models (SDF files)    │
└──────────────────────────────────────┘
```

**Key Components**:

1. **Gazebo Server** (`ign gazebo -s`): Runs physics simulation headless (no GUI)
2. **Gazebo Client** (`ign gazebo`): GUI for visualization and interaction
3. **SDF Files**: XML format describing worlds and robots (similar to URDF but more powerful)
4. **Plugins**: Extend functionality (sensors, controllers, custom physics)

---

## Hands-On: Installing Gazebo Fortress

We'll install **Gazebo Fortress**, which is compatible with ROS 2 Humble and supported until 2026.

### Step 1: Add Gazebo APT Repository

```bash
# Install prerequisites
sudo apt update
sudo apt install -y wget lsb-release gnupg

# Add Gazebo repository
sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
```

### Step 2: Install Gazebo Fortress

```bash
sudo apt update
sudo apt install -y ignition-fortress
```

**What gets installed**:
- `ign-gazebo7`: Gazebo Fortress simulation engine (~1.5GB)
- `ign-tools2`: Command-line tools (`ign gazebo`, `ign topic`)
- Physics engines (ODE, Bullet, DART)
- OGRE rendering engine

**Installation time**: 5-10 minutes.

### Step 3: Install ROS 2 - Gazebo Integration

```bash
sudo apt install -y ros-humble-ros-ign-gazebo ros-humble-ros-ign-bridge
```

**What gets installed**:
- `ros_ign_gazebo`: Launch files for Gazebo + ROS 2
- `ros_ign_bridge`: Topic/service translation between ROS 2 and Gazebo

### Step 4: Verify Installation

```bash
ign gazebo --version
```

Expected output:
```
Ignition Gazebo, version 7.x.x
```

---

## Running Your First Gazebo Simulation

### Step 1: Launch Gazebo with Empty World

```bash
ign gazebo empty.sdf
```

You should see a black window with a grid (empty world):

**Interface Tour**:
- **Viewport** (center): 3D view of the world
- **Scene Tree** (left panel): List of entities (models, lights, sensors)
- **Component Inspector** (right panel): Properties of selected entities
- **Toolbar** (top): Play/pause simulation, reset, camera controls

**Camera Controls**:
- **Left-click + drag**: Rotate view
- **Middle-click + drag**: Pan view
- **Scroll wheel**: Zoom in/out
- **Shift + arrows**: Move camera

### Step 2: Add Models from Gazebo Library

Gazebo includes pre-built models. Let's add some:

1. Click the **cube icon** (top toolbar) to open model library
2. Search for "ground_plane" and click to insert
3. You should see a gray ground plane appear
4. Insert more models: "sun" (lighting), "table", "chair"

**Try this**: Click the **play button** ▶️ (top toolbar). Objects with physics enabled will fall due to gravity!

### Step 3: Inspect Physics Properties

1. Click on an object in the viewport
2. Check **Component Inspector** (right panel)
3. Expand sections:
   - **Pose**: Position (x, y, z) and orientation (roll, pitch, yaw)
   - **Physics**: Mass, inertia, friction, restitution
   - **Collision**: Shape for collision detection
   - **Visual**: Mesh for rendering

**Experiment**:
- Change mass of an object (e.g., table to 0.1 kg)
- Press ▶️ play
- Observe how lighter objects fall/bounce differently

### Step 4: Spawn a Robot from URDF

Let's spawn a simple robot using a URDF from Module 1.

**Create a simple robot URDF** (`simple_robot.urdf`):

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <link name="chassis">
    <visual>
      <geometry>
        <box size="0.6 0.4 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.6 0.4 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <link name="wheel_left">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <joint name="wheel_left_joint" type="continuous">
    <parent link="chassis"/>
    <child link="wheel_left"/>
    <origin xyz="0 0.25 0" rpy="-1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <link name="wheel_right">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <joint name="wheel_right_joint" type="continuous">
    <parent link="chassis"/>
    <child link="wheel_right"/>
    <origin xyz="0 -0.25 0" rpy="-1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>
</robot>
```

**Spawn robot in Gazebo**:

```bash
# In one terminal: Launch Gazebo
ign gazebo empty.sdf

# In another terminal: Spawn robot
ign service -s /world/empty/create \
  --reqtype ignition.msgs.EntityFactory \
  --reptype ignition.msgs.Boolean \
  --timeout 1000 \
  --req 'sdf_filename: "/path/to/simple_robot.urdf", name: "my_robot"'
```

*(Note: Replace `/path/to/simple_robot.urdf` with actual file path)*

You should see your blue robot with two wheels appear in Gazebo!

---

## Understanding Physics in Gazebo

### Gravity

By default, Gazebo applies Earth gravity: **-9.81 m/s²** in the Z-axis.

**Experiment**:
1. Spawn robot 2 meters above ground: `<pose>0 0 2 0 0 0</pose>` in SDF
2. Press ▶️ play
3. Observe robot falling and landing (elastic collision)

**Change gravity** (in world SDF):
```xml
<physics name="1ms" type="ode">
  <gravity>0 0 -3.72</gravity> <!-- Mars gravity -->
</physics>
```

### Friction

Friction prevents sliding. Two types:
- **Static friction** (`mu1`): Resistance to start moving
- **Dynamic friction** (`mu2`): Resistance while moving

**Example**: Low friction (icy floor):
```xml
<collision name="collision">
  <surface>
    <friction>
      <ode>
        <mu>0.1</mu>  <!-- Low friction -->
        <mu2>0.1</mu2>
      </ode>
    </friction>
  </surface>
  <geometry>
    <plane><normal>0 0 1</normal></plane>
  </geometry>
</collision>
```

### Inertia

Inertia determines how hard it is to rotate an object. Calculated from mass distribution.

**Rule of thumb**:
- Large `ixx`: Hard to rotate around X-axis
- Symmetric objects: `ixx ≈ iyy ≈ izz`

**Gazebo can auto-calculate** inertia if you specify mass and geometry.

---

## Gazebo CLI Tools

### Useful Commands

**List running worlds**:
```bash
ign gazebo --list
```

**Get topic list** (similar to `ros2 topic list`):
```bash
ign topic -l
```

**Echo topic data**:
```bash
ign topic -e -t /world/empty/stats
```

**Call services**:
```bash
ign service -l  # List services
ign service -s /world/empty/control --reqtype ignition.msgs.WorldControl --req 'pause: true'
```

---

## Troubleshooting Common Issues

### Issue: "ign: command not found"

**Cause**: Gazebo not installed or not in PATH.

**Fix**:
```bash
sudo apt install -y ignition-fortress
source ~/.bashrc
```

### Issue: Gazebo window is black/frozen

**Cause**: Graphics driver issue (common with Intel integrated GPUs).

**Fix**:
1. Update graphics drivers:
   ```bash
   sudo ubuntu-drivers autoinstall
   ```
2. Try software rendering:
   ```bash
   LIBGL_ALWAYS_SOFTWARE=1 ign gazebo
   ```

### Issue: Robot falls through ground plane

**Cause**: Missing collision geometry or physics properties.

**Fix**: Ensure `<collision>` tags are present and mass &gt; 0 in URDF.

---

## Key Takeaways

🎓 **Digital twins** are virtual replicas of physical systems, enabling safe, fast, cost-effective testing before hardware deployment.

🎓 **Gazebo** is the industry-standard physics-based robot simulator, used by Amazon, NASA, and autonomous vehicle companies.

🎓 **Physics simulation** includes gravity, friction, inertia, collisions—allowing realistic robot behavior testing.

🎓 **ros_gz_bridge** connects Gazebo to ROS 2, enabling control via ROS 2 topics and services.

🎓 **SDF files** (Simulation Description Format) describe Gazebo worlds and robots, extending URDF with simulation-specific features.

---

## What's Next?

Now that you have Gazebo running and understand physics simulation, you're ready to build custom worlds and add sensors!

In **Chapter 2.2: Creating Custom Worlds**, you'll:

- Design Gazebo worlds with obstacles, terrain, and buildings
- Write SDF files to define world properties
- Add lighting, textures, and environmental effects
- Create realistic testing environments for your robots

**Continue to** → [Chapter 2.2: Creating Custom Worlds](./chapter-2-2-worlds)

---

## Assessment: Gazebo Setup Challenge

**Goal**: Verify your Gazebo installation and understanding of physics simulation.

**Tasks**:
1. Install Gazebo Fortress and ROS 2 integration packages
2. Launch Gazebo with an empty world
3. Insert a ground plane, sun (lighting), and 3 objects from the model library
4. Modify one object's mass to make it very light (0.1 kg)
5. Press play and observe physics (objects fall, collide)
6. Take a screenshot showing:
   - Gazebo viewport with objects
   - Component Inspector showing modified mass property

**Expected Pass Rate**: 85% of learners complete within 30 minutes.

---

## Additional Resources

📚 **Official Documentation**:
- [Gazebo Documentation](https://gazebosim.org/docs)
- [ROS 2 + Gazebo Integration Guide](https://docs.ros.org/en/humble/Tutorials/Advanced/Simulators/Gazebo/Gazebo.html)
- [SDF Format Specification](http://sdformat.org/)

📺 **Video Tutorials**:
- The Construct - Gazebo for Robotics
- Articulated Robotics - ROS 2 Gazebo Tutorials

🛠️ **Community**:
- [Gazebo Answers](https://answers.gazebosim.org/) - Q&A forum
- [ROS Discourse - Simulation Category](https://discourse.ros.org/c/simulation/)

---

**Chapter Status**: Complete ✅
**Next Chapter**: [2.2 Creating Custom Worlds](./chapter-2-2-worlds)
