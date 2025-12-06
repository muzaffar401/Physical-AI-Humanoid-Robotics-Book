---
id: chapter-2-6-nav2
title: "Chapter 2.6: Autonomous Navigation with Nav2"
sidebar_label: "2.6 Nav2"
sidebar_position: 6
---

# Chapter 2.6: Autonomous Navigation with Nav2

## From Teleoperation to Full Autonomy

You've built maps, localized your robot—now it's time for the **ultimate goal**: **autonomous navigation**. Point to a destination on the map, and your robot plans a path, avoids obstacles, and navigates there completely on its own.

**Nav2** (Navigation2) is ROS 2's navigation framework, providing path planning, obstacle avoidance, recovery behaviors, and a complete autonomous navigation pipeline.

In this chapter, you'll configure Nav2, send navigation goals, tune behavior parameters, and build a fully autonomous mobile robot.

---

## Learning Objectives

By the end of this chapter, you will:

- **Understand**: Explain Nav2 architecture (global planner, local planner, controller, behavior server)
- **Apply**: Configure Nav2 for differential drive robot with LiDAR
- **Apply**: Send navigation goals via RViz2 and programmatically (Action client)
- **Analyze**: Tune costmap parameters for obstacle inflation and safety margins
- **Create**: Fully autonomous delivery robot that navigates to multiple waypoints

**Estimated Time**: 3.5 hours

---

## Prerequisites

- **Chapter 2.5 complete** (SLAM, map creation)
- **Chapter 2.4 complete** (Differential drive robot)
- **Chapter 2.3 complete** (LiDAR sensor)
- **Saved map** from SLAM (`.pgm` + `.yaml`)

---

## What You'll Build

By the end of this chapter, you'll have:

✅ **Nav2 stack** configured and running
✅ **Autonomous navigation** to goal poses clicked in RViz2
✅ **Path planning** with obstacle avoidance
✅ **Recovery behaviors** (rotate, back up) when stuck
✅ **Multi-waypoint mission** executing autonomously

---

## Nav2 Architecture

### The Navigation Stack

**Nav2** consists of modular servers working together:

```
User/Application
      ↓
Navigation Action Server (BT Navigator)
      ↓
Behavior Tree (controls execution flow)
      ↓
+-----------------------+
| Global Planner        |  → Plans path from start to goal (A*, Dijkstra)
| Local Planner         |  → Follows global path, avoids obstacles (DWB)
| Controller Server     |  → Sends velocity commands to robot
| Recoveries Server     |  → Handles stuck situations (spin, backup)
+-----------------------+
      ↓
Costmaps (Global + Local)
      ↓
Map + Sensors (LiDAR, depth camera)
```

### Key Components

**1. Global Planner** (`NavFn`, `Smac Planner`)
- Plans **optimal path** from start to goal on static map
- Uses A* or Dijkstra search
- Output: Sequence of waypoints

**2. Local Planner / Controller** (`DWB`, `TEB`, `RPP`)
- Follows global path while **avoiding dynamic obstacles**
- Generates velocity commands (`/cmd_vel`)
- Looks ahead a few meters (local costmap)

**3. Costmaps** (Global + Local)
- **Global costmap**: Entire map, static obstacles
- **Local costmap**: Small area around robot, includes sensor data
- Inflates obstacles (safety buffer)

**4. Behavior Server** (`Spin`, `Backup`, `Wait`)
- **Recovery behaviors** when stuck
- Example: If path blocked → back up, rotate, retry

**5. BT Navigator** (Behavior Tree)
- Orchestrates navigation logic
- Example: Try navigate → if stuck → spin → retry → if fail → report error

---

## Installation

```bash
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
```

---

## Hands-On: Nav2 Basic Setup

### Step 1: Prepare Robot and Map

**Requirements**:
- Differential drive robot with LiDAR (from Chapter 2.4)
- Saved map files: `warehouse_map.pgm`, `warehouse_map.yaml`
- TF tree: `map → odom → base_link → lidar_link`

### Step 2: Create Nav2 Configuration

Nav2 uses **YAML config files** for all parameters. Start with a template.

**Create config/nav2_params.yaml**:

```yaml
bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: base_link
    odom_topic: /odom
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    plugin_lib_names:
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_compute_path_through_poses_action_bt_node
    - nav2_smooth_path_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_spin_action_bt_node
    - nav2_wait_action_bt_node
    - nav2_back_up_action_bt_node
    - nav2_drive_on_heading_bt_node
    - nav2_clear_costmap_service_bt_node
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
    - nav2_goal_updated_condition_bt_node
    - nav2_globally_updated_goal_condition_bt_node
    - nav2_is_path_valid_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_service_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node
    - nav2_truncate_path_local_action_bt_node
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_time_expired_condition_bt_node
    - nav2_path_expiring_timer_condition
    - nav2_distance_traveled_condition_bt_node
    - nav2_single_trigger_bt_node
    - nav2_goal_updated_controller_bt_node
    - nav2_is_battery_low_condition_bt_node
    - nav2_navigate_through_poses_action_bt_node
    - nav2_navigate_to_pose_action_bt_node
    - nav2_remove_passed_goals_action_bt_node
    - nav2_planner_selector_bt_node
    - nav2_controller_selector_bt_node
    - nav2_goal_checker_selector_bt_node
    - nav2_controller_cancel_bt_node
    - nav2_path_longer_on_approach_bt_node
    - nav2_wait_cancel_bt_node
    - nav2_spin_cancel_bt_node
    - nav2_back_up_cancel_bt_node
    - nav2_drive_on_heading_cancel_bt_node

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    failure_tolerance: 0.3
    progress_checker_plugin: "progress_checker"
    goal_checker_plugins: ["general_goal_checker"]
    controller_plugins: ["FollowPath"]

    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0

    general_goal_checker:
      stateful: True
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25

    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      debug_trajectory_details: True
      min_vel_x: 0.0
      min_vel_y: 0.0
      max_vel_x: 0.5
      max_vel_y: 0.0
      max_vel_theta: 1.0
      min_speed_xy: 0.0
      max_speed_xy: 0.5
      min_speed_theta: 0.0
      acc_lim_x: 2.5
      acc_lim_y: 0.0
      acc_lim_theta: 3.2
      decel_lim_x: -2.5
      decel_lim_y: 0.0
      decel_lim_theta: -3.2
      vx_samples: 20
      vy_samples: 5
      vth_samples: 20
      sim_time: 1.7
      linear_granularity: 0.05
      angular_granularity: 0.025
      transform_tolerance: 0.2
      xy_goal_tolerance: 0.25
      trans_stopped_velocity: 0.25
      short_circuit_trajectory_evaluation: True
      stateful: True
      critics: ["RotateToGoal", "Oscillation", "BaseObstacle", "GoalAlign", "PathAlign", "PathDist", "GoalDist"]
      BaseObstacle.scale: 0.02
      PathAlign.scale: 32.0
      PathAlign.forward_point_distance: 0.1
      GoalAlign.scale: 24.0
      GoalAlign.forward_point_distance: 0.1
      PathDist.scale: 32.0
      GoalDist.scale: 24.0
      RotateToGoal.scale: 32.0
      RotateToGoal.slowing_factor: 5.0
      RotateToGoal.lookahead_time: -1.0

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: odom
      robot_base_frame: base_link
      use_sim_time: True
      rolling_window: true
      width: 3
      height: 3
      resolution: 0.05
      robot_radius: 0.25
      plugins: ["voxel_layer", "inflation_layer"]
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        enabled: True
        publish_voxel_map: True
        origin_z: 0.0
        z_resolution: 0.05
        z_voxels: 16
        max_obstacle_height: 2.0
        mark_threshold: 0
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
      always_send_full_costmap: True

global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: map
      robot_base_frame: base_link
      use_sim_time: True
      robot_radius: 0.25
      resolution: 0.05
      track_unknown_space: true
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: True
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
      always_send_full_costmap: True

planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    use_sim_time: True
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true

smoother_server:
  ros__parameters:
    use_sim_time: True
    smoother_plugins: ["simple_smoother"]
    simple_smoother:
      plugin: "nav2_smoother::SimpleSmoother"
      tolerance: 1.0e-10
      max_its: 1000
      do_refinement: True

behavior_server:
  ros__parameters:
    costmap_topic: local_costmap/costmap_raw
    footprint_topic: local_costmap/published_footprint
    cycle_frequency: 10.0
    behavior_plugins: ["spin", "backup", "drive_on_heading", "wait"]
    spin:
      plugin: "nav2_behaviors::Spin"
    backup:
      plugin: "nav2_behaviors::BackUp"
    drive_on_heading:
      plugin: "nav2_behaviors::DriveOnHeading"
    wait:
      plugin: "nav2_behaviors::Wait"
    global_frame: odom
    robot_base_frame: base_link
    transform_tolerance: 0.1
    use_sim_time: true
    simulate_ahead_time: 2.0
    max_rotational_vel: 1.0
    min_rotational_vel: 0.4
    rotational_acc_lim: 3.2

robot_state_publisher:
  ros__parameters:
    use_sim_time: True

waypoint_follower:
  ros__parameters:
    use_sim_time: True
    loop_rate: 20
    stop_on_failure: false
    waypoint_task_executor_plugin: "wait_at_waypoint"
    wait_at_waypoint:
      plugin: "nav2_waypoint_follower::WaitAtWaypoint"
      enabled: True
      waypoint_pause_duration: 200

velocity_smoother:
  ros__parameters:
    use_sim_time: True
    smoothing_frequency: 20.0
    scale_velocities: False
    feedback: "OPEN_LOOP"
    max_velocity: [0.5, 0.0, 1.0]
    min_velocity: [-0.5, 0.0, -1.0]
    max_accel: [2.5, 0.0, 3.2]
    max_decel: [-2.5, 0.0, -3.2]
    odom_topic: "odom"
    odom_duration: 0.1
    deadband_velocity: [0.0, 0.0, 0.0]
    velocity_timeout: 1.0
```

**Key parameters to understand**:
- `robot_radius: 0.25` - Safety bubble around robot (meters)
- `max_vel_x: 0.5` - Max forward speed (m/s)
- `inflation_radius: 0.55` - How far to inflate obstacles (robot radius + clearance)
- `xy_goal_tolerance: 0.25` - How close to goal = "reached" (meters)
- `use_sim_time: True` - Use Gazebo clock (crucial for simulation!)

### Step 3: Create Nav2 Launch File

**Create launch/nav2.launch.py**:

```python
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_robot_description')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    map_file = os.path.join(pkg_dir, 'maps', 'warehouse_map.yaml')
    nav2_params_file = os.path.join(pkg_dir, 'config', 'nav2_params.yaml')

    return LaunchDescription([
        # Nav2 bringup (includes all Nav2 nodes)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
            ),
            launch_arguments={
                'map': map_file,
                'params_file': nav2_params_file,
                'use_sim_time': 'True'
            }.items()
        )
    ])
```

### Step 4: Launch Everything

**Terminal 1: Gazebo + Robot**

```bash
ros2 launch my_robot_description diff_bot.launch.py
```

**Terminal 2: Nav2 Stack**

```bash
ros2 launch my_robot_description nav2.launch.py
```

**Terminal 3: RViz2**

```bash
rviz2 -d /opt/ros/humble/share/nav2_bringup/rviz/nav2_default_view.rviz
```

**Expected**:
- Map loads (gray/white/black)
- Robot appears on map
- Green/red costmap overlays visible
- Nav2 nodes running: `ros2 node list`

---

## Sending Navigation Goals

### Method 1: RViz2 (Interactive)

In RViz2:

1. **Set Initial Pose**:
   - Click **2D Pose Estimate** button (top toolbar)
   - Click and drag on map where robot actually is
   - AMCL particles converge

2. **Send Goal**:
   - Click **Nav2 Goal** button (top toolbar)
   - Click on map where you want robot to go
   - Drag to set orientation
   - Release → Robot starts navigating!

**Watch**:
- **Global plan** (green line): Optimal path from A* planner
- **Local plan** (blue dots): Controller's trajectory
- **Costmaps**: Red = dangerous, yellow = inflated obstacles

### Method 2: Programmatic (Action Client)

**navigate_to_pose.py**:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped

class Navigator(Node):
    def __init__(self):
        super().__init__('navigator')
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.get_logger().info('Waiting for navigation action server...')
        self._action_client.wait_for_server()
        self.get_logger().info('Navigation action server available!')

    def send_goal(self, x, y, yaw):
        """Send navigation goal (x, y in meters, yaw in radians)"""
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()

        # Position
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = 0.0

        # Orientation (yaw → quaternion)
        import math
        goal_msg.pose.pose.orientation.z = math.sin(yaw / 2.0)
        goal_msg.pose.pose.orientation.w = math.cos(yaw / 2.0)

        self.get_logger().info(f'Sending goal: x={x}, y={y}, yaw={yaw}')

        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected!')
            return

        self.get_logger().info('Goal accepted, navigating...')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        # Log distance remaining, ETA, etc.
        self.get_logger().info(f'Distance remaining: {feedback.distance_remaining:.2f}m')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Navigation result: {result}')

def main(args=None):
    rclpy.init(args=args)
    navigator = Navigator()

    # Navigate to goal (5m forward, 2m left, facing 0°)
    navigator.send_goal(5.0, 2.0, 0.0)

    rclpy.spin(navigator)
    navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run**:

```bash
python3 navigate_to_pose.py
```

**Robot navigates to (5.0, 2.0) autonomously!**

---

## Understanding Costmaps

### What is a Costmap?

A **2D grid** where each cell has a **cost** (0-255):
- **0** (black): Free space
- **255** (red): Lethal obstacle (collision if robot enters)
- **1-254**: Inflated zones (closer to obstacle = higher cost)
- **Unknown**: Gray (not yet observed)

**Purpose**: Planner avoids high-cost cells, ensuring safety margin.

### Global Costmap

- **Size**: Entire map
- **Source**: Static map from SLAM
- **Update rate**: 1 Hz (slow, map doesn't change much)
- **Use**: Global planner (A* pathfinding)

### Local Costmap

- **Size**: Small area around robot (e.g., 3m × 3m)
- **Source**: Static map + real-time sensor data (LiDAR)
- **Rolling window**: Moves with robot
- **Update rate**: 5 Hz (fast, obstacles appear/disappear)
- **Use**: Local planner (obstacle avoidance)

**Visualize in RViz2**:
- **Add** → **Map** (topic: `/global_costmap/costmap`)
- **Add** → **Map** (topic: `/local_costmap/costmap`)

---

## Tuning Navigation Behavior

### Increase Speed

In `nav2_params.yaml`:

```yaml
FollowPath:
  max_vel_x: 1.0  # Increase from 0.5 to 1.0 m/s
  max_vel_theta: 2.0  # Increase rotation speed
```

**Caution**: Faster = less time to react to obstacles.

### Tighter Goal Tolerance

```yaml
general_goal_checker:
  xy_goal_tolerance: 0.1  # Get within 10cm (was 25cm)
  yaw_goal_tolerance: 0.1  # Face within 5.7° (was 14.3°)
```

**Use**: Precision tasks (docking, alignment).

### Larger Safety Margin

```yaml
robot_radius: 0.3  # Increase from 0.25m
inflation_radius: 0.7  # Stay farther from walls
```

**Trade-off**: Can't navigate narrow spaces.

### Aggressive Obstacle Avoidance

```yaml
FollowPath:
  critics: ["RotateToGoal", "Oscillation", "BaseObstacle", "GoalAlign", "PathAlign", "PathDist", "GoalDist"]
  BaseObstacle.scale: 0.05  # Increase penalty for getting near obstacles
```

---

## Recovery Behaviors

When robot gets stuck, Nav2 triggers **recovery behaviors**:

### 1. Spin Recovery

- **Trigger**: Path blocked, can't find alternative
- **Action**: Rotate 360° to clear costmap (maybe obstacle moved)
- **Config**:

```yaml
spin:
  plugin: "nav2_behaviors::Spin"
  simulate_ahead_time: 2.0
```

### 2. Backup Recovery

- **Trigger**: Stuck against obstacle
- **Action**: Drive backward 0.5m
- **Config**:

```yaml
backup:
  plugin: "nav2_behaviors::BackUp"
  backup_dist: 0.5  # meters
  backup_speed: 0.2  # m/s
```

### 3. Wait Recovery

- **Trigger**: Dynamic obstacle (person) blocking path
- **Action**: Wait for obstacle to move
- **Config**:

```yaml
wait:
  plugin: "nav2_behaviors::Wait"
  wait_duration: 5.0  # seconds
```

**Sequence** (Behavior Tree):
1. Try navigate
2. If stuck → Clear costmap
3. If still stuck → Spin
4. If still stuck → Backup
5. If still stuck → Report failure

---

## Multi-Waypoint Navigation

Navigate through **sequence of poses** (patrol, delivery route).

**waypoint_follower.py**:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateThroughPoses
from geometry_msgs.msg import PoseStamped
import math

class WaypointFollower(Node):
    def __init__(self):
        super().__init__('waypoint_follower')
        self._action_client = ActionClient(self, NavigateThroughPoses, 'navigate_through_poses')
        self._action_client.wait_for_server()

    def create_pose(self, x, y, yaw):
        """Helper to create PoseStamped"""
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.z = math.sin(yaw / 2.0)
        pose.pose.orientation.w = math.cos(yaw / 2.0)
        return pose

    def follow_waypoints(self, waypoints):
        """waypoints: list of (x, y, yaw) tuples"""
        goal_msg = NavigateThroughPoses.Goal()
        goal_msg.poses = [self.create_pose(x, y, yaw) for x, y, yaw in waypoints]

        self.get_logger().info(f'Following {len(waypoints)} waypoints...')
        send_goal_future = self._action_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if goal_handle.accepted:
            self.get_logger().info('Waypoint mission accepted')
            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(self.result_callback)
        else:
            self.get_logger().error('Waypoint mission rejected')

    def result_callback(self, future):
        self.get_logger().info('Waypoint mission complete!')

def main(args=None):
    rclpy.init(args=args)
    follower = WaypointFollower()

    # Define patrol route (rectangle)
    waypoints = [
        (5.0, 0.0, 0.0),    # Point 1
        (5.0, 5.0, 1.57),   # Point 2 (facing up)
        (0.0, 5.0, 3.14),   # Point 3 (facing left)
        (0.0, 0.0, -1.57),  # Point 4 (facing down)
    ]

    follower.follow_waypoints(waypoints)
    rclpy.spin(follower)
    follower.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run**: Robot autonomously patrols rectangle!

---

## Dynamic Obstacle Avoidance

Nav2's **local costmap** includes real-time sensor data, enabling dynamic obstacle avoidance.

**Test**:
1. Start navigation to distant goal
2. In Gazebo, insert obstacle in robot's path (box, cylinder)
3. Watch local costmap update (red obstacle appears)
4. Robot **replans** around obstacle automatically!

**Key parameter**:

```yaml
local_costmap:
  voxel_layer:
    observation_sources: scan
    scan:
      topic: /scan
      clearing: True  # Remove obstacles when no longer detected
      marking: True   # Add obstacles when detected
```

---

## Common Nav2 Issues

### Issue: Robot doesn't move

**Cause**: No initial pose set (AMCL not localized).

**Fix**: Click **2D Pose Estimate** in RViz2.

### Issue: "No path found"

**Cause**: Goal is inside obstacle or unreachable.

**Fix**:
- Choose goal in free space (white on map)
- Check `robot_radius` isn't too large (squeezing robot)

### Issue: Robot rotates in place, doesn't move forward

**Cause**: `RotateToGoal` critic too aggressive.

**Fix**:

```yaml
RotateToGoal.scale: 16.0  # Reduce from 32.0
```

### Issue: Robot bumps into obstacles

**Cause**: Insufficient inflation or sensor noise.

**Fix**:
- Increase `inflation_radius: 0.7`
- Check LiDAR is publishing (`ros2 topic hz /scan`)

### Issue: Global path goes through obstacles

**Cause**: Map outdated or tolerance too high.

**Fix**:
- Remap environment if changed
- Reduce `planner_plugins/GridBased/tolerance: 0.2`

---

## Advanced: Behavior Trees

Nav2 uses **Behavior Trees (BT)** to orchestrate navigation logic.

**Default BT** (`navigate_w_replanning_and_recovery.xml`):
```xml
<BehaviorTree>
  <PipelineSequence name="NavigateWithReplanning">
    <RateController hz="1.0">
      <ComputePathToPose goal="{goal}" path="{path}"/>
    </RateController>
    <RecoveryNode number_of_retries="6" name="FollowPath">
      <FollowPath path="{path}"/>
      <SequenceStar name="RecoveryActions">
        <ClearEntireCostmap/>
        <Spin/>
        <Wait wait_duration="5"/>
        <BackUp/>
      </SequenceStar>
    </RecoveryNode>
  </PipelineSequence>
</BehaviorTree>
```

**Custom BT**: Create your own logic (e.g., charge battery if low, take photo at waypoints).

---

## Hands-On: Delivery Robot Mission

**Challenge**: Robot delivers packages to 3 locations, returns to depot.

**waypoints**:
1. Depot (0, 0)
2. Location A (5, 3)
3. Location B (8, -2)
4. Location C (3, -5)
5. Return to depot

**Code**: Use `waypoint_follower.py` with these coordinates.

**Bonus**: Add "delivery action" at each waypoint (wait 5 seconds, play sound).

---

## Key Takeaways

🎓 **Nav2** is ROS 2's navigation stack—global planner, local controller, costmaps, recoveries.

🎓 **Global planner** (A*) finds optimal path on static map.

🎓 **Local controller** (DWB) follows path while avoiding dynamic obstacles.

🎓 **Costmaps** represent obstacles with inflated safety margins (robot radius + buffer).

🎓 **Recovery behaviors** (spin, backup, wait) handle stuck situations autonomously.

🎓 **Action clients** send navigation goals programmatically (`NavigateToPose`).

🎓 **Multi-waypoint navigation** enables patrol routes, deliveries, inspection tasks.

🎓 **Tuning** (speed, tolerance, inflation) balances safety, speed, and maneuverability.

---

## Module 2 Complete!

**Congratulations!** You've mastered simulation with Gazebo and autonomous navigation with Nav2.

**Skills acquired**:
✅ Gazebo world creation and physics tuning
✅ Sensor simulation (camera, LiDAR, IMU)
✅ Differential drive robot control
✅ SLAM mapping with SLAM Toolbox
✅ Autonomous navigation with Nav2

**Next**: Module 3 builds on this foundation with **advanced manipulation**, **motion planning**, and **MoveIt2** for humanoid arms!

---

## Assessment: Autonomous Warehouse Robot

**Goal**: Build a fully autonomous warehouse robot that navigates to delivery stations.

**Requirements**:

1. **Robot**:
   - Differential drive (2 wheels + caster)
   - LiDAR sensor (360°, 10m range)
   - Proper URDF with inertia, collision

2. **Environment**: Multi-room warehouse world with:
   - 4+ delivery stations (marked locations)
   - Obstacles (shelves, boxes)
   - Open navigation areas

3. **Mapping**: Use SLAM Toolbox to map warehouse, save map files

4. **Navigation**:
   - Configure Nav2 with custom parameters
   - Robot navigates to all 4 stations autonomously
   - Handles dynamic obstacles (insert box during navigation)
   - Returns to depot after deliveries

5. **Deliverables**:
   - Robot URDF
   - Warehouse world SDF
   - Saved map (`.pgm` + `.yaml`)
   - Nav2 config file (`nav2_params.yaml`)
   - Python mission script (waypoint follower)
   - Video (120 seconds) showing full delivery mission
   - Written report (300 words) on challenges and solutions

**Expected Pass Rate**: 55% of learners complete within 180 minutes.

**Bonus**: Implement obstacle prediction (stop before collision based on obstacle velocity).

---

## Additional Resources

📚 **Official Documentation**:
- [Nav2 Documentation](https://navigation.ros.org/)
- [Nav2 Tuning Guide](https://navigation.ros.org/tuning/index.html)
- [Nav2 Configuration Guide](https://navigation.ros.org/configuration/index.html)

📺 **Video Tutorials**:
- The Construct - Nav2 Complete Course
- Articulated Robotics - Nav2 Basics
- ROS 2 Navigation - Steve Macenski (maintainer)

🛠️ **Tools**:
- [Groot](https://github.com/BehaviorTree/Groot) - Behavior tree visualization
- [PlotJuggler](https://github.com/facontidavide/PlotJuggler) - Plot navigation metrics
- [Nav2 Web Visualizer](https://github.com/ros-visualization/rvizweb) - Web-based RViz

📦 **Example Configurations**:
- [TurtleBot3 Nav2](https://github.com/ROBOTIS-GIT/turtlebot3/tree/humble-devel/turtlebot3_navigation2)
- [Nav2 Simple Commander](https://github.com/ros-planning/navigation2/tree/main/nav2_simple_commander) - Python API

📖 **Papers** (optional):
- "The Dynamic Window Approach to Collision Avoidance" - Fox et al.
- "Behavior Trees in Robotics and AI" - Colledanchise & Ögren

---

**Chapter Status**: Complete ✅
**Module 2 Status**: Complete ✅ 🎉
**Next Module**: [Module 3: Advanced Manipulation & MoveIt2](../module-3/chapter-3-1-introduction)
