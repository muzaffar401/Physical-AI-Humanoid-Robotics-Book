---
id: chapter-2-2-worlds
title: "Chapter 2.2: Creating Custom Worlds"
sidebar_label: "2.2 Custom Worlds"
sidebar_position: 2
---

# Chapter 2.2: Creating Custom Worlds

## Building Your Robot's Virtual Environment

Testing a warehouse robot? You need aisles, shelves, and pallets. Developing a home assistant? You need rooms, furniture, and doorways. **Custom Gazebo worlds** let you create precisely the testing environment your robot needs.

In this chapter, you'll learn SDF (Simulation Description Format) to build worlds from scratch—adding terrain, obstacles, lighting, and realistic physics properties.

---

## Learning Objectives

By the end of this chapter, you will:

- **Understand**: Explain SDF structure for world files vs URDF for robot models
- **Apply**: Create custom Gazebo worlds with ground planes, obstacles, and models
- **Apply**: Configure world properties (gravity, lighting, physics parameters)
- **Create**: Design realistic testing environments (warehouse, indoor, outdoor)

**Estimated Time**: 2 hours

---

## Prerequisites

- **Chapter 2.1 complete** (Gazebo installation and basics)
- **Module 1 complete** (URDF understanding helps with SDF)

---

## What You'll Build

By the end of this chapter, you'll have:

✅ **Empty world** with custom gravity and physics
✅ **Obstacle course** with boxes, cylinders, ramps
✅ **Warehouse environment** with aisles and shelves
✅ **Understanding of SDF** vs URDF differences

---

## SDF vs URDF

### URDF (Unified Robot Description Format)

- **Purpose**: Describe **robots** (links, joints, sensors)
- **Scope**: Single robot, kinematic tree structure
- **Used by**: ROS 2, MoveIt, robot_state_publisher

### SDF (Simulation Description Format)

- **Purpose**: Describe **entire worlds** (ground, buildings, multiple robots, lighting, physics)
- **Scope**: Complete simulation environment
- **Used by**: Gazebo, Ignition, physics engines

**Key difference**: SDF can include **multiple robots** and **environmental elements**. URDF describes **one robot**.

### SDF File Structure

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="my_world">
    <!-- Physics settings -->
    <physics>...</physics>

    <!-- Lighting -->
    <light>...</light>

    <!-- Models (ground, obstacles, robots) -->
    <model>...</model>
    <model>...</model>

    <!-- Include external models -->
    <include>...</include>
  </world>
</sdf>
```

---

## Hands-On: Creating an Empty World

### Step 1: Create World File

Create `empty_world.sdf`:

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="empty_world">

    <!-- Physics: How simulation runs -->
    <physics name="1ms" type="ode">
      <max_step_size>0.001</max_step_size>  <!-- 1ms timestep -->
      <real_time_factor>1.0</real_time_factor>  <!-- Real-time speed -->
    </physics>

    <!-- Sun: Directional light from above -->
    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- Ground Plane -->
    <model name="ground_plane">
      <static>true</static>  <!-- Doesn't move -->
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>  <!-- Points up (Z-axis) -->
              <size>100 100</size>    <!-- 100m x 100m -->
            </plane>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>100</mu>     <!-- Friction coefficient -->
                <mu2>50</mu2>
              </ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>  <!-- Light gray -->
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

  </world>
</sdf>
```

### Step 2: Launch World

```bash
ign gazebo empty_world.sdf
```

**Expected**: Gray ground plane with sunlight casting shadows.

---

## Physics Configuration

### Physics Engines

Gazebo supports multiple physics engines:

**ODE (Open Dynamics Engine)** - Default
```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
</physics>
```

**Bullet** - Fast collision detection
```xml
<physics type="bullet">
  <max_step_size>0.001</max_step_size>
</physics>
```

**DART** - Advanced constraints
```xml
<physics type="dart">
  <max_step_size>0.001</max_step_size>
</physics>
```

### Key Physics Parameters

**`max_step_size`**: Simulation timestep (smaller = more accurate, slower)
- **0.001** (1ms): Default, good for most robots
- **0.0001** (0.1ms): High precision (humanoid balance)
- **0.01** (10ms): Fast, less accurate (simple wheeled robots)

**`real_time_factor`**: Simulation speed relative to real-time
- **1.0**: Real-time (1 sim second = 1 real second)
- **0.5**: Half speed (useful for debugging)
- **2.0**: 2x speed (fast-forward testing)

**Custom gravity** (default is Earth: -9.81 m/s²):
```xml
<physics>
  <gravity>0 0 -3.72</gravity>  <!-- Mars gravity -->
</physics>
```

---

## Adding Models to World

### Simple Box Obstacle

```xml
<model name="box_obstacle">
  <pose>2 0 0.5 0 0 0</pose>  <!-- 2m forward, 0.5m up -->
  <static>false</static>  <!-- Can move/fall -->

  <link name="link">
    <collision name="collision">
      <geometry>
        <box>
          <size>1 1 1</size>  <!-- 1m cube -->
        </box>
      </geometry>
    </collision>

    <visual name="visual">
      <geometry>
        <box>
          <size>1 1 1</size>
        </box>
      </geometry>
      <material>
        <ambient>1 0 0 1</ambient>  <!-- Red -->
        <diffuse>1 0 0 1</diffuse>
      </material>
    </visual>

    <inertial>
      <mass>10</mass>
      <inertia>
        <ixx>1.67</ixx>
        <iyy>1.67</iyy>
        <izz>1.67</izz>
      </inertia>
    </inertial>
  </link>
</model>
```

**Properties**:
- `<pose>`: Position (x, y, z) + orientation (roll, pitch, yaw)
- `<static>`: If true, object doesn't move (infinite mass)
- `<mass>`: Mass in kg
- `<inertia>`: Moment of inertia (affects rotation)

---

## Hands-On: Obstacle Course

Let's create a world with multiple obstacles for robot testing.

### Create obstacle_course.sdf

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="obstacle_course">

    <physics name="1ms" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- Ground -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>50 50</size>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>50 50</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.5 0.5 0.5 1</ambient>
            <diffuse>0.5 0.5 0.5 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Wall 1 -->
    <model name="wall_1">
      <static>true</static>
      <pose>5 0 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.2 4 1</size>  <!-- Thin wall, 4m wide, 1m tall -->
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.2 4 1</size>
            </box>
          </geometry>
          <material>
            <ambient>0.7 0.7 0.7 1</ambient>
            <diffuse>0.7 0.7 0.7 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Cylinder Obstacle -->
    <model name="cylinder_1">
      <static>false</static>
      <pose>3 -2 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <cylinder>
              <radius>0.3</radius>
              <length>1.0</length>
            </cylinder>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <cylinder>
              <radius>0.3</radius>
              <length>1.0</length>
            </cylinder>
          </geometry>
          <material>
            <ambient>0 0 1 1</ambient>  <!-- Blue -->
            <diffuse>0 0 1 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>5</mass>
          <inertia>
            <ixx>0.5</ixx>
            <iyy>0.5</iyy>
            <izz>0.2</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Ramp -->
    <model name="ramp">
      <static>true</static>
      <pose>8 0 0 0 0.3 0</pose>  <!-- Tilted 0.3 radians (17°) -->
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>3 2 0.1</size>  <!-- 3m long, 2m wide, thin -->
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>3 2 0.1</size>
            </box>
          </geometry>
          <material>
            <ambient>1 1 0 1</ambient>  <!-- Yellow -->
            <diffuse>1 1 0 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

  </world>
</sdf>
```

**Launch**:

```bash
ign gazebo obstacle_course.sdf
```

**You should see**:
- Gray ground plane
- Gray wall blocking path
- Blue cylinder (movable)
- Yellow ramp at 17° angle

---

## Lighting Types

### Directional Light (Sun)

```xml
<light type="directional" name="sun">
  <pose>0 0 10 0 0 0</pose>
  <diffuse>1 1 1 1</diffuse>  <!-- White light -->
  <specular>0.5 0.5 0.5 1</specular>
  <direction>-0.5 0.1 -0.9</direction>  <!-- Angle of rays -->
  <cast_shadows>true</cast_shadows>
</light>
```

**Use**: Outdoor environments (sunlight)

### Point Light (Bulb)

```xml
<light type="point" name="lamp">
  <pose>0 0 3 0 0 0</pose>  <!-- 3m above ground -->
  <diffuse>1 1 0.9 1</diffuse>  <!-- Warm white -->
  <specular>0.5 0.5 0.5 1</specular>
  <attenuation>
    <range>10</range>  <!-- Light reaches 10m -->
    <linear>0.1</linear>
    <quadratic>0.01</quadratic>
  </attenuation>
</light>
```

**Use**: Indoor environments (ceiling lights)

### Spot Light (Flashlight)

```xml
<light type="spot" name="spotlight">
  <pose>0 0 5 0 1.57 0</pose>  <!-- Pointing down -->
  <diffuse>1 1 1 1</diffuse>
  <spot>
    <inner_angle>0.6</inner_angle>
    <outer_angle>1.0</outer_angle>
    <falloff>1.0</falloff>
  </spot>
  <direction>0 0 -1</direction>
</light>
```

**Use**: Focused lighting (stage, inspection area)

---

## Including External Models

Gazebo has a library of pre-built models. Use `<include>` to add them:

### Include Gazebo Model

```xml
<include>
  <uri>model://construction_cone</uri>
  <pose>2 2 0 0 0 0</pose>
  <name>cone_1</name>
</include>
```

**Common models**:
- `construction_cone`
- `coke_can`
- `table`
- `bookshelf`
- `ambulance`

**Note**: Models download from Gazebo Fuel on first use.

---

## Hands-On: Warehouse Environment

Create a realistic warehouse with aisles and shelves.

### Create warehouse.sdf

```xml
<?xml version="1.0"?>
<sdf version="1.8">
  <world name="warehouse">

    <physics name="1ms" type="ode">
      <max_step_size>0.001</max_step_size>
    </physics>

    <!-- Warehouse lighting (dimmer, point lights) -->
    <light type="point" name="ceiling_light_1">
      <pose>5 5 4 0 0 0</pose>
      <diffuse>0.8 0.8 0.7 1</diffuse>
      <attenuation>
        <range>15</range>
      </attenuation>
    </light>

    <light type="point" name="ceiling_light_2">
      <pose>-5 5 4 0 0 0</pose>
      <diffuse>0.8 0.8 0.7 1</diffuse>
      <attenuation>
        <range>15</range>
      </attenuation>
    </light>

    <!-- Ground (concrete texture) -->
    <model name="ground">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>40 40</size>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>40 40</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.6 0.6 0.6 1</ambient>
            <diffuse>0.6 0.6 0.6 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Shelf Row 1 -->
    <model name="shelf_row_1">
      <static>true</static>
      <pose>5 0 1 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 8 2</size>  <!-- Thin, long shelf -->
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 8 2</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.6 0.4 1</ambient>  <!-- Wood color -->
            <diffuse>0.8 0.6 0.4 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Shelf Row 2 (parallel aisle) -->
    <model name="shelf_row_2">
      <static>true</static>
      <pose>8 0 1 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 8 2</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 8 2</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.6 0.4 1</ambient>
            <diffuse>0.8 0.6 0.4 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Walls (enclose warehouse) -->
    <model name="wall_north">
      <static>true</static>
      <pose>0 15 1.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>40 0.2 3</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>40 0.2 3</size>
            </box>
          </geometry>
          <material>
            <ambient>0.9 0.9 0.9 1</ambient>
            <diffuse>0.9 0.9 0.9 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Add more walls (south, east, west) similarly -->

  </world>
</sdf>
```

**Result**: Enclosed warehouse with parallel shelf rows and overhead lighting—perfect for testing navigation algorithms!

---

## Surface Properties

Configure how objects interact:

### Friction

```xml
<surface>
  <friction>
    <ode>
      <mu>0.8</mu>     <!-- Friction coefficient 1 -->
      <mu2>0.8</mu2>   <!-- Friction coefficient 2 -->
    </ode>
  </friction>
</surface>
```

**Values**:
- **0.0**: Ice (no friction, slides forever)
- **0.5**: Low friction (tile floor)
- **1.0**: Medium (concrete)
- **100**: High (rubber on asphalt, prevents sliding)

### Restitution (Bounciness)

```xml
<surface>
  <bounce>
    <restitution_coefficient>0.9</restitution_coefficient>  <!-- Very bouncy -->
  </bounce>
</surface>
```

**Values**:
- **0.0**: No bounce (ball stops dead)
- **0.5**: Medium bounce
- **1.0**: Perfect elastic collision (ball bounces back to same height)

---

## Best Practices

### 1. Use Static for Non-Moving Objects

```xml
<model name="wall">
  <static>true</static>  <!-- Doesn't consume physics resources -->
  ...
</model>
```

**Why**: Static objects don't need collision detection with each other = faster simulation.

### 2. Simplify Collision Geometry

```xml
<!-- Visual: Complex mesh -->
<visual>
  <geometry>
    <mesh><uri>detailed_shelf.dae</uri></mesh>
  </geometry>
</visual>

<!-- Collision: Simple box -->
<collision>
  <geometry>
    <box><size>1 1 2</size></box>
  </geometry>
</collision>
```

### 3. Organize with Includes

**Main world**:
```xml
<include>
  <uri>model://my_warehouse_section</uri>
  <pose>0 0 0 0 0 0</pose>
</include>
```

Reuse components across worlds.

### 4. Name Everything Clearly

❌ `model_1`, `box_3`
✅ `shelf_aisle_2`, `loading_dock_barrier`

---

## Troubleshooting

### Issue: Objects fall through ground

**Cause**: No collision geometry on ground plane.

**Fix**: Ensure `<collision>` tag exists with plane geometry.

### Issue: Simulation runs slowly

**Cause**: Too many complex collision geometries.

**Fix**:
- Use `<static>true</static>` for non-moving objects
- Simplify collision shapes (boxes instead of meshes)
- Increase `max_step_size` (less accurate but faster)

### Issue: Models not appearing

**Cause**: Incorrect model URI or model not installed.

**Fix**: Use Gazebo Fuel models or local file paths:
```xml
<uri>file:///home/user/models/my_model</uri>
```

---

## Key Takeaways

🎓 **SDF** (Simulation Description Format) describes entire worlds with multiple models, lighting, and physics.

🎓 **Physics configuration** (timestep, gravity, engine) affects simulation accuracy and speed.

🎓 **Static models** (`<static>true</static>`) don't move and are computationally cheaper.

🎓 **Lighting types**: directional (sun), point (bulb), spot (flashlight) for different environments.

🎓 **Surface properties** (friction, restitution) control how objects interact physically.

🎓 **Include external models** from Gazebo Fuel library for quick world building.

---

## What's Next?

You've built custom worlds with obstacles and environments. Now let's add **sensors** to your robots!

In **Chapter 2.3: Simulating Sensors**, you'll:

- Add cameras, LiDAR, and IMU sensors to robots
- Configure sensor properties (resolution, FOV, update rate)
- Visualize sensor data in RViz2
- Process sensor data in ROS 2 nodes

**Continue to** → [Chapter 2.3: Simulating Sensors](./chapter-2-3-sensors)

---

## Assessment: Build Your Test World

**Goal**: Create a custom world for testing your robot.

**Requirements**:

1. **Ground plane** with custom friction (mu=0.8)
2. **3+ obstacles** of different shapes (box, cylinder, ramp)
3. **2+ light sources** (one directional, one point)
4. **Custom gravity** (try Moon: -1.62 or Mars: -3.72)
5. **At least 1 dynamic object** (`<static>false</static>`)

**Deliverables**:
- `my_test_world.sdf` file
- Screenshot of world in Gazebo
- Written description of testing scenario

**Expected Pass Rate**: 80% of learners complete within 45 minutes.

**Bonus**: Include external model from Gazebo Fuel (construction cone, table, etc.)

---

## Additional Resources

📚 **Official Documentation**:
- [SDF Format Specification](http://sdformat.org/)
- [Gazebo World Files](https://gazebosim.org/docs/latest/sdf_worlds/)
- [Gazebo Fuel Models](https://app.gazebosim.org/fuel/models)

📺 **Video Tutorials**:
- The Construct - Creating Gazebo Worlds
- Articulated Robotics - SDF World Building

🛠️ **Tools**:
- [Gazebo Model Editor](https://classic.gazebosim.org/tutorials?tut=model_editor) - GUI for building models
- [Blender to SDF Exporter](https://github.com/andreasBihlmaier/gazebo_models_worlds_collection)

---

**Chapter Status**: Complete ✅
**Next Chapter**: [2.3 Simulating Sensors](./chapter-2-3-sensors)
