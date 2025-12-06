---
id: chapter-2-5-slam
title: "Chapter 2.5: Simultaneous Localization and Mapping (SLAM)"
sidebar_label: "2.5 SLAM"
sidebar_position: 5
---

# Chapter 2.5: Simultaneous Localization and Mapping (SLAM)

## Teaching Your Robot to Map Unknown Worlds

Imagine deploying a robot in an unfamiliar warehouse. It needs to **build a map** while simultaneously **tracking its position** within that map. This chicken-and-egg problem is solved by **SLAM** (Simultaneous Localization and Mapping)—one of robotics' fundamental capabilities.

In this chapter, you'll use ROS 2 SLAM packages to build 2D maps from LiDAR data, save maps for future use, and localize robots in known environments.

---

## Learning Objectives

By the end of this chapter, you will:

- **Understand**: Explain the SLAM problem and how laser-based SLAM algorithms work
- **Apply**: Configure and run SLAM Toolbox for 2D mapping
- **Apply**: Drive robot to build complete environment maps
- **Analyze**: Evaluate map quality and identify common SLAM issues
- **Create**: Save maps and use them for localization (AMCL)

**Estimated Time**: 3 hours

---

## Prerequisites

- **Chapter 2.4 complete** (Robot movement, odometry)
- **Chapter 2.3 complete** (LiDAR sensor)
- **Module 1 complete** (ROS 2 topics, launch files)

---

## What You'll Build

By the end of this chapter, you'll have:

✅ **2D occupancy grid map** of simulated warehouse
✅ **Real-time SLAM** running with SLAM Toolbox
✅ **Saved map files** (`.pgm` image + `.yaml` metadata)
✅ **Localization system** (AMCL) to track robot in known map
✅ **Understanding of loop closure** and map optimization

---

## What is SLAM?

### The SLAM Problem

**Given**:
- Stream of sensor data (LiDAR scans)
- Control inputs (wheel velocities, odometry)

**Find**:
- **Map** of the environment (walls, obstacles)
- **Trajectory** of the robot (where it's been)

**Challenge**: Both are unknown! You need the map to localize, but need to localize to build the map.

### SLAM Solutions

**Laser SLAM** (2D):
- Input: LiDAR scans (ranges to obstacles)
- Output: 2D occupancy grid (black = obstacle, white = free, gray = unknown)
- Used by: Warehouse robots, vacuums, indoor navigation

**Visual SLAM** (3D):
- Input: Camera images or RGB-D
- Output: 3D point cloud or mesh
- Used by: Drones, AR/VR, outdoor robots

**For this chapter**: 2D laser SLAM with SLAM Toolbox.

---

## SLAM Toolbox Overview

**SLAM Toolbox** is a ROS 2 SLAM implementation featuring:
- **2D laser-based mapping** from LiDAR
- **Graph-based optimization** (pose graph)
- **Loop closure detection** (recognize revisited areas)
- **Map serialization** (save/load maps)
- **Localization mode** (track position in known map)

**Alternative**: Google Cartographer (more complex, better for large environments)

### Installation

```bash
sudo apt install ros-humble-slam-toolbox
```

---

## Occupancy Grid Maps

### What is an Occupancy Grid?

A **2D grid** where each cell represents a small area (e.g., 5cm × 5cm).

**Cell values**:
- **0**: Free space (white in visualization)
- **100**: Occupied (obstacle, black)
- **-1**: Unknown (gray, not yet scanned)

**Probabilistic**: SLAM updates cell probabilities as robot observes them.

### Map Representation

**PGM file** (Portable Gray Map):
- Image file (grayscale)
- Black pixels = obstacles
- White pixels = free space
- Gray pixels = unknown

**YAML metadata**:
```yaml
image: warehouse_map.pgm
resolution: 0.05  # meters per pixel (5cm)
origin: [-10.0, -10.0, 0.0]  # (x, y, yaw) of bottom-left pixel
occupied_thresh: 0.65  # Probability threshold for "occupied"
free_thresh: 0.25  # Probability threshold for "free"
negate: 0
```

---

## Hands-On: Building Your First Map

### Step 1: Setup Robot with LiDAR

Use `diff_bot` from Chapter 2.4 with LiDAR added (see Chapter 2.3).

**Ensure**:
- LiDAR topic: `/scan` (or remap in SLAM config)
- Odometry topic: `/odom`
- TF tree: `odom → base_link → lidar_link`

### Step 2: Launch Robot in World

Create a world with distinguishable features (walls, corners):

```bash
ros2 launch my_robot_description diff_bot.launch.py
```

**Alternative**: Use `warehouse.sdf` from Chapter 2.2.

### Step 3: Configure SLAM Toolbox

Create **config/mapper_params_online_async.yaml**:

```yaml
slam_toolbox:
  ros__parameters:
    # Plugin parameters
    solver_plugin: solver_plugins::CeresSolver
    ceres_linear_solver: SPARSE_NORMAL_CHOLESKY
    ceres_preconditioner: SCHUR_JACOBI
    ceres_trust_strategy: LEVENBERG_MARQUARDT
    ceres_dogleg_type: TRADITIONAL_DOGLEG
    ceres_loss_function: None

    # ROS Parameters
    odom_frame: odom
    map_frame: map
    base_frame: base_link
    scan_topic: /scan
    mode: mapping  # "mapping" or "localization"

    # Map settings
    map_update_interval: 1.0  # seconds
    resolution: 0.05  # meters per pixel (5cm)

    # Scan matching
    use_scan_matching: true
    use_scan_barycenter: true
    minimum_travel_distance: 0.2  # meters before adding new scan
    minimum_travel_heading: 0.2  # radians
    scan_buffer_size: 30
    scan_buffer_maximum_scan_distance: 20.0  # meters
    link_match_minimum_response_fine: 0.1
    link_scan_maximum_distance: 1.5

    # Loop closure
    loop_search_maximum_distance: 3.0  # meters
    do_loop_closing: true
    loop_match_minimum_chain_size: 10
    loop_match_maximum_variance_coarse: 3.0
    loop_match_minimum_response_coarse: 0.35
    loop_match_minimum_response_fine: 0.45

    # Correlation parameters
    correlation_search_space_dimension: 0.5
    correlation_search_space_resolution: 0.01
    correlation_search_space_smear_deviation: 0.1

    # Loop closure parameters
    loop_search_space_dimension: 8.0
    loop_search_space_resolution: 0.05
    loop_search_space_smear_deviation: 0.03

    # Scan matcher
    distance_variance_penalty: 0.5
    angle_variance_penalty: 1.0

    # Odometry
    fine_search_angle_offset: 0.00349
    coarse_search_angle_offset: 0.349
    coarse_angle_resolution: 0.0349
    minimum_angle_penalty: 0.9
    minimum_distance_penalty: 0.5
    use_response_expansion: true
```

**Key parameters**:
- `scan_topic`: Your LiDAR topic (default `/scan`)
- `resolution`: Map pixel size (0.05 = 5cm, balance detail vs size)
- `minimum_travel_distance`: How far robot moves before adding scan (prevents duplicate scans)
- `do_loop_closing`: Enable loop closure (correct drift when revisiting areas)

### Step 4: Launch SLAM Toolbox

**Create launch/slam.launch.py**:

```python
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_robot_description')
    config_file = os.path.join(pkg_dir, 'config', 'mapper_params_online_async.yaml')

    return LaunchDescription([
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[config_file]
        )
    ])
```

**Launch**:

```bash
ros2 launch my_robot_description slam.launch.py
```

**Check topics**:

```bash
ros2 topic list
# Should see:
# /map (nav_msgs/OccupancyGrid)
# /map_metadata
# /slam_toolbox/graph_visualization
```

### Step 5: Visualize in RViz2

```bash
rviz2
```

**Configure**:
1. **Fixed Frame**: `map`
2. **Add** → **Map** (topic: `/map`)
3. **Add** → **RobotModel**
4. **Add** → **LaserScan** (topic: `/scan`)
5. **Add** → **TF** (see frame relationships)

**You should see**:
- Gray background (unknown)
- Robot in center
- LiDAR scan (red dots)
- Map building as robot moves!

### Step 6: Drive and Build Map

**Option 1: Teleop**

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Drive robot around entire environment:
- Cover all rooms/areas
- Get close to walls (better scans)
- Revisit starting area (triggers loop closure)

**Option 2: Autonomous Exploration** (later with Nav2)

### Step 7: Monitor Map Quality

**Good signs**:
- Walls are straight, continuous lines
- Corners are sharp (90°)
- No "ghost" obstacles (false positives)

**Bad signs**:
- Walls drifting/curved (odometry error)
- Duplicate walls (poor scan matching)
- Holes in walls (missed scans)

**Fix**: Drive slower, improve odometry (better wheel encoders), tune SLAM parameters.

---

## Loop Closure

### What is Loop Closure?

When robot **revisits** a previously mapped area, SLAM recognizes it and **corrects accumulated drift**.

**Example**:
1. Robot drives in circle
2. Odometry drifts → map shows curved walls
3. Robot returns to start
4. SLAM matches current scan to start scan
5. **Loop closure**: Adjusts entire trajectory, straightens walls!

### Detecting Loop Closure

**In RViz2**:
- Watch `/slam_toolbox/graph_visualization` (PoseGraph markers)
- Loop closure = graph edges connecting distant poses

**In terminal**:

```bash
ros2 topic echo /slam_toolbox/feedback
```

Look for:
```
Loop closure detected!
```

**Best practice**: Always drive robot back to starting point before saving map.

---

## Saving Maps

### Save Map to Files

```bash
ros2 run nav2_map_server map_saver_cli -f ~/maps/warehouse_map
```

**Creates two files**:
- `warehouse_map.pgm` - Image (occupancy grid)
- `warehouse_map.yaml` - Metadata (resolution, origin)

**View map**:

```bash
eog ~/maps/warehouse_map.pgm  # Eye of GNOME image viewer
```

Or any image viewer—it's a standard image file!

---

## Localization in Known Map (AMCL)

Once you have a map, use **AMCL** (Adaptive Monte Carlo Localization) to track robot position.

### What is AMCL?

**AMCL** (Particle Filter Localization):
- **Input**: Map + LiDAR scans + odometry
- **Output**: Robot pose estimate (x, y, θ)
- **Method**: Maintains cloud of "particles" (pose hypotheses), converges to true pose

### Install AMCL

```bash
sudo apt install ros-humble-nav2-amcl
```

### Launch Map Server + AMCL

**Create launch/localization.launch.py**:

```python
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_robot_description')
    map_file = os.path.join(pkg_dir, 'maps', 'warehouse_map.yaml')

    return LaunchDescription([
        # Map server (loads and serves map)
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            parameters=[{'yaml_filename': map_file}]
        ),

        # Lifecycle manager (activates map_server)
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_localization',
            output='screen',
            parameters=[{
                'autostart': True,
                'node_names': ['map_server', 'amcl']
            }]
        ),

        # AMCL localization
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'alpha1': 0.2,
                'alpha2': 0.2,
                'alpha3': 0.2,
                'alpha4': 0.2,
                'alpha5': 0.2,
                'base_frame_id': 'base_link',
                'beam_skip_distance': 0.5,
                'beam_skip_error_threshold': 0.9,
                'beam_skip_threshold': 0.3,
                'do_beamskip': False,
                'global_frame_id': 'map',
                'lambda_short': 0.1,
                'laser_likelihood_max_dist': 2.0,
                'laser_max_range': 100.0,
                'laser_min_range': -1.0,
                'laser_model_type': 'likelihood_field',
                'max_beams': 60,
                'max_particles': 2000,
                'min_particles': 500,
                'odom_frame_id': 'odom',
                'pf_err': 0.05,
                'pf_z': 0.99,
                'recovery_alpha_fast': 0.0,
                'recovery_alpha_slow': 0.0,
                'resample_interval': 1,
                'robot_model_type': 'differential',
                'save_pose_rate': 0.5,
                'sigma_hit': 0.2,
                'tf_broadcast': True,
                'transform_tolerance': 1.0,
                'update_min_a': 0.2,
                'update_min_d': 0.25,
                'z_hit': 0.5,
                'z_max': 0.05,
                'z_rand': 0.5,
                'z_short': 0.05,
                'scan_topic': 'scan'
            }]
        )
    ])
```

**Launch**:

```bash
# Terminal 1: Robot in Gazebo
ros2 launch my_robot_description diff_bot.launch.py

# Terminal 2: Localization
ros2 launch my_robot_description localization.launch.py
```

### Set Initial Pose in RViz2

1. Open RViz2
2. Set **Fixed Frame** to `map`
3. **Add** → **Map** (topic: `/map`)
4. **Add** → **PoseArray** (topic: `/particlecloud`)
5. Click **2D Pose Estimate** button (top toolbar)
6. Click and drag on map where robot actually is

**Particles converge**: As robot moves, particles (green arrows) converge to true pose!

---

## SLAM Algorithms Comparison

| Algorithm | Pros | Cons | Use Case |
|-----------|------|------|----------|
| **SLAM Toolbox** | Fast, loop closure, ROS 2 native | 2D only | Indoor robots, warehouses |
| **Cartographer** | Very accurate, 3D, large maps | Complex config, slower | Autonomous cars, large areas |
| **Hector SLAM** | No odometry needed | Drifts without loop closure | Rescue robots, rough terrain |
| **GMapping** | Simple, fast | ROS 1 only, no loop closure | Legacy systems |

**Recommendation**: SLAM Toolbox for most ROS 2 projects.

---

## Common SLAM Issues

### Issue: Map drifts (curved walls)

**Cause**: Poor odometry accuracy.

**Fix**:
- Calibrate wheel diameter and separation
- Use better odometry source (wheel encoders, IMU fusion)
- Tune SLAM `distance_variance_penalty`

### Issue: Loop closure not detected

**Cause**: `loop_search_maximum_distance` too small.

**Fix**: Increase in config:

```yaml
loop_search_maximum_distance: 5.0  # meters
```

### Issue: Map has "ghost" walls

**Cause**: LiDAR noise or moving objects (people, boxes).

**Fix**:
- Drive slower (more scans per area)
- Increase `minimum_travel_distance` (fewer redundant scans)
- Add obstacles as "dynamic" (advanced, not in static maps)

### Issue: Robot "lost" in AMCL (particles scattered)

**Cause**: Initial pose wrong or sensor mismatch.

**Fix**:
- Set accurate **2D Pose Estimate** in RViz2
- Drive robot to unique feature (corner, doorway) to help localization
- Check LiDAR data matches map (frame IDs, topic names)

---

## Best Practices for Mapping

### 1. Drive Slowly and Smoothly

**Why**: Fast motion = motion blur in scans + poor scan matching.

**Tip**: Max 0.2 m/s during mapping.

### 2. Close the Loop

Always return to starting point before saving—triggers loop closure.

### 3. Maximize Feature Diversity

**Good**: Corners, doorways, furniture (unique features)
**Bad**: Long empty corridors (all scans look similar)

### 4. Avoid Dynamic Obstacles

Remove people, moving boxes during mapping—they create "ghost" obstacles.

### 5. Check TF Tree

```bash
ros2 run tf2_tools view_frames
```

Verify: `map → odom → base_link → lidar_link`

---

## Advanced: Pose Graph Optimization

SLAM Toolbox builds a **pose graph**:
- **Nodes**: Robot poses (x, y, θ) at scan times
- **Edges**: Constraints from odometry and scan matching

**Optimization**: Minimizes error across all edges (graph SLAM).

**Visualize**:

```bash
ros2 topic echo /slam_toolbox/graph_visualization
```

Shows graph as markers in RViz2 (`visualization_msgs/MarkerArray`).

---

## Hands-On: Multi-Room Mapping

**Challenge**: Map a multi-room environment (e.g., house with kitchen, bedroom, bathroom).

**Steps**:
1. Create world with 3+ rooms connected by doorways
2. Launch robot + SLAM Toolbox
3. Systematically explore each room (wall-follow pattern)
4. Return to start (loop closure)
5. Save map
6. Launch localization, set initial pose, drive around to verify

**Expected**: Complete map with all rooms, straight walls, sharp corners.

---

## Key Takeaways

🎓 **SLAM** solves simultaneous localization and mapping—builds map while tracking position.

🎓 **SLAM Toolbox** is ROS 2's primary 2D laser SLAM solution with loop closure.

🎓 **Occupancy grid maps** represent environment as 2D grid (free, occupied, unknown).

🎓 **Loop closure** corrects drift by recognizing revisited areas—always close the loop!

🎓 **Save maps** with `map_saver_cli` as `.pgm` image + `.yaml` metadata.

🎓 **AMCL** localizes robot in known map using particle filter (no mapping, just tracking).

🎓 **Good mapping**: Slow driving, feature-rich environment, loop closure, smooth odometry.

---

## What's Next?

You've mapped environments—now let's use those maps for **autonomous navigation**!

In **Chapter 2.6: Autonomous Navigation with Nav2**, you'll:

- Configure Nav2 navigation stack
- Set navigation goals programmatically
- Implement path planning (global and local)
- Add obstacle avoidance and recovery behaviors
- Build fully autonomous mobile robot

**Continue to** → [Chapter 2.6: Nav2 Navigation](./chapter-2-6-nav2)

---

## Assessment: Complete Mapping Pipeline

**Goal**: Map a complex environment, save it, and localize within it.

**Requirements**:

1. **Environment**: Multi-room world (3+ rooms, doorways, obstacles)

2. **Mapping phase**:
   - Robot with diff drive + LiDAR
   - SLAM Toolbox running
   - Drive through all areas
   - Return to start (loop closure)
   - Save map files

3. **Localization phase**:
   - Launch map server + AMCL
   - Set initial pose in RViz2
   - Drive around, verify localization accuracy

4. **Documentation**:
   - Map image (`.pgm` file)
   - RViz2 screenshot with particle cloud converged
   - Brief report (200 words) on challenges faced

**Deliverables**:
- Saved map files (`.pgm` + `.yaml`)
- SLAM config file (`mapper_params_online_async.yaml`)
- Localization launch file
- Video (60 seconds) showing mapping + localization
- Written report

**Expected Pass Rate**: 60% of learners complete within 120 minutes.

**Bonus**: Implement automatic exploration (robot explores autonomously without teleop).

---

## Additional Resources

📚 **Official Documentation**:
- [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox)
- [Nav2 SLAM](https://navigation.ros.org/tutorials/docs/navigation2_with_slam.html)
- [AMCL Documentation](https://navigation.ros.org/configuration/packages/configuring-amcl.html)

📺 **Video Tutorials**:
- The Construct - SLAM with ROS 2
- Articulated Robotics - Mapping Your World
- ROS 2 Navigation - SLAM and Localization

🛠️ **Tools**:
- [slam_toolbox RViz plugin](https://github.com/SteveMacenski/slam_toolbox#rviz-plugin) - Interactive SLAM control
- [map_server](https://github.com/ros-planning/navigation2/tree/main/nav2_map_server) - Map loading/saving
- [evo](https://github.com/MichaelGrupp/evo) - Trajectory evaluation (compare SLAM output)

📦 **Example Configurations**:
- [TurtleBot3 SLAM](https://github.com/ROBOTIS-GIT/turtlebot3/tree/humble-devel/turtlebot3_slam)
- [Nav2 SLAM Example](https://github.com/ros-planning/navigation2/tree/main/nav2_bringup/launch)

📖 **Papers** (optional deep dive):
- "A Tutorial on Graph-Based SLAM" - Grisetti et al.
- "Karto SLAM" - SRI International (basis for SLAM Toolbox)

---

**Chapter Status**: Complete ✅
**Next Chapter**: [2.6 Nav2 Navigation](./chapter-2-6-nav2)
