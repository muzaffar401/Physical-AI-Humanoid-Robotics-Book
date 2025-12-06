---
id: chapter-2-4-movement
title: "Chapter 2.4: Robot Movement in Simulation"
sidebar_label: "2.4 Movement"
sidebar_position: 4
---

# Chapter 2.4: Robot Movement in Simulation

## Making Your Robot Move

Sensors let robots perceive—but **actuators** let them act. In this chapter, you'll add wheels, motors, and controllers to robots in Gazebo, enabling them to navigate through simulated environments with realistic physics.

You'll implement differential drive (two-wheeled robots), add Gazebo control plugins, and control robots with keyboard teleop and programmatic velocity commands.

---

## Learning Objectives

By the end of this chapter, you will:

- **Understand**: Explain differential drive kinematics and how ROS 2 controls robot motion
- **Apply**: Add wheels, joints, and motors to robot URDF with Gazebo plugins
- **Apply**: Configure `diff_drive` controller for two-wheeled robots
- **Create**: Velocity control nodes publishing to `/cmd_vel` topic
- **Analyze**: Debug motion issues using joint state monitoring and physics parameters

**Estimated Time**: 2.5 hours

---

## Prerequisites

- **Chapter 2.3 complete** (Sensors, Gazebo plugins)
- **Module 1 complete** (URDF, joints, ROS 2 publishers)
- **Basic kinematics** (velocity, angular velocity concepts)

---

## What You'll Build

By the end of this chapter, you'll have:

✅ **Two-wheeled differential drive robot** moving in Gazebo
✅ **Keyboard teleop** for manual control
✅ **Velocity control node** for programmatic movement
✅ **Realistic physics** (friction, inertia, wheel slip)
✅ **Understanding of cmd_vel** topic and Twist messages

---

## Differential Drive Basics

### What is Differential Drive?

**Differential drive** uses two independently-controlled wheels (left and right) to achieve motion.

**Movement patterns**:
- **Forward**: Both wheels same speed, same direction
- **Backward**: Both wheels same speed, reverse
- **Turn left**: Right wheel faster than left
- **Turn right**: Left wheel faster than right
- **Rotate in place**: Wheels same speed, opposite directions

**Used by**: Roomba, TurtleBot3, warehouse robots, most mobile robots

### Kinematics

**Input**: Linear velocity (`v`) + Angular velocity (`ω`)
**Output**: Left wheel speed (`v_left`) + Right wheel speed (`v_right`)

**Equations**:
```
v_left = v - (ω * wheel_separation / 2)
v_right = v + (ω * wheel_separation / 2)
```

Where:
- `v`: Linear velocity (m/s) — how fast moving forward
- `ω` (omega): Angular velocity (rad/s) — how fast rotating
- `wheel_separation`: Distance between wheels (m)

**Example**: Move forward at 0.5 m/s, turn left at 0.2 rad/s:
```
v_left = 0.5 - (0.2 * 0.4 / 2) = 0.46 m/s
v_right = 0.5 + (0.2 * 0.4 / 2) = 0.54 m/s
```

**ROS 2 handles this automatically** with `diff_drive` controller!

---

## Building a Differential Drive Robot

### Step 1: Robot URDF with Wheels

Create **diff_bot.urdf**:

```xml
<?xml version="1.0"?>
<robot name="diff_bot">

  <!-- Base link (robot body) -->
  <link name="base_link">
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
      <inertia ixx="0.4" iyy="0.4" izz="0.4" ixy="0" ixz="0" iyz="0"/>
    </inertial>
  </link>

  <!-- Left wheel -->
  <link name="left_wheel">
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
      <inertia ixx="0.01" iyy="0.01" izz="0.01" ixy="0" ixz="0" iyz="0"/>
    </inertial>
  </link>

  <!-- Left wheel joint (continuous = can rotate forever) -->
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0 0.225 -0.05" rpy="-1.5707 0 0"/>  <!-- Side of robot, rpy rotates to horizontal -->
    <axis xyz="0 0 1"/>  <!-- Rotation axis (after rpy transform) -->
  </joint>

  <!-- Right wheel -->
  <link name="right_wheel">
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
      <inertia ixx="0.01" iyy="0.01" izz="0.01" ixy="0" ixz="0" iyz="0"/>
    </inertial>
  </link>

  <!-- Right wheel joint -->
  <joint name="right_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel"/>
    <origin xyz="0 -0.225 -0.05" rpy="-1.5707 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <!-- Caster wheel (front support, no motor) -->
  <link name="caster">
    <visual>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
      <surface>
        <friction>
          <ode>
            <mu>0.0</mu>  <!-- Frictionless for smooth rotation -->
            <mu2>0.0</mu2>
          </ode>
        </friction>
      </surface>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.001" iyy="0.001" izz="0.001" ixy="0" ixz="0" iyz="0"/>
    </inertial>
  </link>

  <!-- Caster joint (fixed, caster rolls passively) -->
  <joint name="caster_joint" type="fixed">
    <parent link="base_link"/>
    <child link="caster"/>
    <origin xyz="0.25 0 -0.15" rpy="0 0 0"/>  <!-- Front of robot -->
  </joint>

</robot>
```

**Key points**:
- **Continuous joints**: Allow infinite rotation (wheels)
- **Wheel placement**: Y-axis separation = 0.45m (0.225 + 0.225)
- **Caster wheel**: Passive support (no motor, low friction)
- **Inertia**: Affects acceleration (heavier = slower to speed up)

---

## Step 2: Add Differential Drive Plugin

Add Gazebo plugin for motor control:

```xml
<!-- Add this inside <robot> tag, after all links/joints -->

<gazebo>
  <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">

    <!-- Update rate (Hz) -->
    <update_rate>50</update_rate>

    <!-- Wheel joints -->
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>

    <!-- Robot dimensions -->
    <wheel_separation>0.45</wheel_separation>  <!-- Distance between wheels (m) -->
    <wheel_diameter>0.2</wheel_diameter>  <!-- Wheel diameter (m) -->

    <!-- Limits -->
    <max_wheel_torque>20</max_wheel_torque>  <!-- Nm -->
    <max_wheel_acceleration>1.0</max_wheel_acceleration>  <!-- rad/s² -->

    <!-- Topic names -->
    <command_topic>cmd_vel</command_topic>  <!-- Subscribe: velocity commands -->
    <odometry_topic>odom</odometry_topic>  <!-- Publish: position estimate -->

    <!-- Frames -->
    <odometry_frame>odom</odometry_frame>
    <robot_base_frame>base_link</robot_base_frame>

    <!-- Odometry source -->
    <odometry_source>world</odometry_source>  <!-- "world" = perfect odometry, "encoder" = realistic -->

    <!-- Publish transforms -->
    <publish_odom>true</publish_odom>
    <publish_odom_tf>true</publish_odom_tf>
    <publish_wheel_tf>false</publish_wheel_tf>

  </plugin>
</gazebo>
```

**Plugin parameters explained**:
- `<left_joint>` / `<right_joint>`: Which joints to control
- `<wheel_separation>`: Used in differential drive equations
- `<wheel_diameter>`: Converts angular velocity (rad/s) → linear velocity (m/s)
- `<command_topic>`: Subscribes to `/cmd_vel` (Twist messages)
- `<odometry_topic>`: Publishes `/odom` (robot position estimate)
- `<odometry_source>`:
  - `world`: Perfect position (cheating, for debugging)
  - `encoder`: Realistic wheel encoders (drift over time)

---

## Step 3: Add Wheel Friction

For realistic motion, configure wheel surface properties:

```xml
<!-- Add inside each wheel's <collision> tag -->

<gazebo reference="left_wheel">
  <mu1>1.0</mu1>  <!-- Friction coefficient 1 -->
  <mu2>1.0</mu2>  <!-- Friction coefficient 2 -->
  <kp>1000000.0</kp>  <!-- Contact stiffness -->
  <kd>100.0</kd>  <!-- Contact damping -->
  <minDepth>0.001</minDepth>  <!-- Min penetration for contact -->
  <material>Gazebo/Black</material>
</gazebo>

<gazebo reference="right_wheel">
  <mu1>1.0</mu1>
  <mu2>1.0</mu2>
  <kp>1000000.0</kp>
  <kd>100.0</kd>
  <minDepth>0.001</minDepth>
  <material>Gazebo/Black</material>
</gazebo>

<gazebo reference="caster">
  <mu1>0.0</mu1>  <!-- No friction (free rolling) -->
  <mu2>0.0</mu2>
  <kp>1000000.0</kp>
  <kd>100.0</kd>
  <material>Gazebo/Gray</material>
</gazebo>
```

**Why friction matters**:
- High friction (1.0): Wheels grip well, no sliding
- Low friction (0.1): Wheels slip (like driving on ice)
- Zero friction (caster): Free rolling support

---

## Step 4: Launch Robot in Gazebo

**launch/diff_bot.launch.py**:

```python
import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_robot_description')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'diff_bot.urdf')

    with open(urdf_file, 'r') as file:
        robot_description = file.read()

    return LaunchDescription([
        # Start Gazebo
        ExecuteProcess(
            cmd=['ign', 'gazebo', 'empty_world.sdf'],
            output='screen'
        ),

        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),

        # Spawn robot in Gazebo
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'diff_bot',
                '-topic', '/robot_description',
                '-x', '0',
                '-y', '0',
                '-z', '0.15'  # Spawn above ground (wheels touch)
            ]
        )
    ])
```

**Launch**:

```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_description
source install/setup.bash

ros2 launch my_robot_description diff_bot.launch.py
```

**Expected**: Robot appears in Gazebo, wheels on ground, caster at front.

---

## Controlling with Keyboard Teleop

### Install Teleop Twist Keyboard

```bash
sudo apt install ros-humble-teleop-twist-keyboard
```

### Run Teleop

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

**Controls**:
```
Reading from the keyboard and publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

i: forward
,: backward
j: turn left
l: turn right
k: stop

CTRL-C to quit
```

**What it does**: Publishes `geometry_msgs/Twist` messages to `/cmd_vel`.

**Try it**: Press `i` (forward), robot should move! Press `k` to stop.

---

## Understanding cmd_vel Topic

### Twist Message Structure

```yaml
geometry_msgs/Twist:
  linear:
    x: 0.5   # Forward velocity (m/s)
    y: 0.0   # Sideways (not used for diff drive)
    z: 0.0   # Up/down (not used)
  angular:
    x: 0.0   # Roll (not used)
    y: 0.0   # Pitch (not used)
    z: 0.2   # Yaw rotation (rad/s)
```

**For differential drive**:
- `linear.x`: Forward/backward speed (positive = forward)
- `angular.z`: Rotation speed (positive = counterclockwise)

### Echo cmd_vel

```bash
ros2 topic echo /cmd_vel
```

Press `i` in teleop, you'll see:
```yaml
linear:
  x: 0.5
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
```

---

## Programmatic Velocity Control

Let's create a node that moves the robot in a square pattern.

**square_mover.py**:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class SquareMover(Node):
    def __init__(self):
        super().__init__('square_mover')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Square mover started')

    def move_forward(self, duration):
        """Move forward for specified duration (seconds)"""
        msg = Twist()
        msg.linear.x = 0.3  # 0.3 m/s forward

        start_time = time.time()
        while time.time() - start_time < duration:
            self.publisher.publish(msg)
            time.sleep(0.1)

        self.stop()

    def turn_left(self, duration):
        """Turn left 90 degrees"""
        msg = Twist()
        msg.angular.z = 0.5  # 0.5 rad/s counterclockwise

        start_time = time.time()
        while time.time() - start_time < duration:
            self.publisher.publish(msg)
            time.sleep(0.1)

        self.stop()

    def stop(self):
        """Stop all motion"""
        msg = Twist()  # All zeros
        self.publisher.publish(msg)
        time.sleep(0.5)

    def drive_square(self):
        """Drive in square pattern"""
        self.get_logger().info('Driving square...')

        for i in range(4):
            self.get_logger().info(f'Side {i+1}')
            self.move_forward(3.0)  # 3 seconds forward
            self.turn_left(3.14)    # ~90° turn (π/2 rad at 0.5 rad/s ≈ 3.14s)

        self.get_logger().info('Square complete!')

def main(args=None):
    rclpy.init(args=args)
    node = SquareMover()

    try:
        node.drive_square()
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run**:

```bash
python3 square_mover.py
```

**Robot should**:
1. Move forward 3 seconds
2. Turn left ~90°
3. Repeat 4 times (square!)

**Note**: This is **open-loop** control (no feedback). Real robots use odometry for closed-loop control.

---

## Odometry Topic

The `diff_drive` plugin publishes **odometry** (position estimate) to `/odom`.

### View Odometry

```bash
ros2 topic echo /odom
```

**Output** (`nav_msgs/Odometry`):
```yaml
pose:
  pose:
    position:
      x: 1.23
      y: 0.45
      z: 0.0
    orientation:
      x: 0.0
      y: 0.0
      z: 0.707
      w: 0.707  # Quaternion (45° rotation)
twist:
  twist:
    linear:
      x: 0.3  # Current velocity
    angular:
      z: 0.0
```

**Fields**:
- `pose.position`: Robot position (x, y, z) in meters
- `pose.orientation`: Robot heading (quaternion)
- `twist.linear`: Current linear velocity
- `twist.angular`: Current angular velocity

**Use cases**:
- Navigation (know where you are)
- Dead reckoning
- Velocity feedback control

---

## Physics Tuning for Realistic Motion

### Issue: Robot moves too fast/slow

**Adjust max velocity** in teleop:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p speed:=0.3 -p turn:=0.5
```

**Or limit in plugin**:

```xml
<max_linear_velocity>1.0</max_linear_velocity>  <!-- m/s -->
<max_angular_velocity>2.0</max_angular_velocity>  <!-- rad/s -->
```

### Issue: Robot slides/drifts

**Increase wheel friction**:

```xml
<gazebo reference="left_wheel">
  <mu1>1.5</mu1>  <!-- Higher friction -->
  <mu2>1.5</mu2>
</gazebo>
```

### Issue: Robot tips over on turns

**Lower center of mass** or **increase base width**:

```xml
<link name="base_link">
  <inertial>
    <origin xyz="0 0 -0.05" rpy="0 0 0"/>  <!-- Lower CoM -->
    <mass value="15"/>  <!-- Heavier base -->
  </inertial>
</link>
```

### Issue: Wheels penetrate ground

**Increase contact stiffness**:

```xml
<kp>10000000.0</kp>  <!-- Very stiff contact -->
```

---

## Advanced: Ackermann Steering (Car-Like)

Differential drive isn't the only option. **Ackermann steering** (like a car) uses:
- **Front wheels**: Steer left/right (steering angle)
- **Rear wheels**: Drive forward/backward (throttle)

**Plugin**: `libgazebo_ros_ackermann_drive.so`

**Used by**: Autonomous cars, RC cars, F1TENTH racing

**For this course**: We focus on differential drive (more common in humanoids and mobile robots).

---

## Hands-On: Obstacle Avoider

Combine LiDAR (Chapter 2.3) + Motion (this chapter) for autonomous obstacle avoidance.

**obstacle_avoider.py**:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')

        self.scan_sub = self.create_subscription(
            LaserScan, '/lidar_bot/scan', self.scan_callback, 10
        )
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.get_logger().info('Obstacle avoider started')

    def scan_callback(self, msg):
        # Get distance in front (center of scan)
        front_distance = msg.ranges[len(msg.ranges) // 2]

        cmd = Twist()

        if front_distance < 0.5:  # Obstacle within 50cm
            self.get_logger().warn(f'Obstacle at {front_distance:.2f}m - Turning!')
            cmd.angular.z = 0.5  # Turn left
        else:
            self.get_logger().info(f'Clear ahead ({front_distance:.2f}m) - Moving forward')
            cmd.linear.x = 0.3  # Move forward

        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run**: Robot drives forward, turns when detecting obstacles!

---

## Debugging Motion Issues

### Check joint states

```bash
ros2 topic echo /joint_states
```

Verify `left_wheel_joint` and `right_wheel_joint` are moving (velocity ≠ 0).

### Visualize in RViz2

1. Launch RViz2
2. Set **Fixed Frame** to `odom`
3. **Add** → **RobotModel**
4. **Add** → **Odometry** (topic: `/odom`)
5. Watch robot move with odometry trail!

### Check cmd_vel is published

```bash
ros2 topic hz /cmd_vel
```

Should show publication rate (10-50 Hz typical).

### Gazebo GUI physics monitor

In Gazebo:
- **View** → **Transparent** (see collision boxes)
- **View** → **Contacts** (see wheel-ground contact)

---

## Key Takeaways

🎓 **Differential drive** uses two independently-controlled wheels for motion (forward, turn, rotate).

🎓 **`/cmd_vel` topic** receives `geometry_msgs/Twist` messages (linear.x + angular.z).

🎓 **Gazebo `diff_drive` plugin** handles wheel kinematics and publishes odometry.

🎓 **Teleop twist keyboard** provides manual control for testing.

🎓 **Odometry** (`/odom` topic) estimates robot position from wheel encoders.

🎓 **Friction, inertia, and physics tuning** affect motion realism.

🎓 **Combine sensors + motion** for autonomous behaviors (obstacle avoidance, wall following).

---

## What's Next?

You've mastered robot movement—now let's **map environments** and **navigate autonomously**!

In **Chapter 2.5: Simultaneous Localization and Mapping (SLAM)**, you'll:

- Understand SLAM algorithms (Cartographer, SLAM Toolbox)
- Build 2D maps using LiDAR data
- Localize robot in known maps
- Save and load maps for navigation

**Continue to** → [Chapter 2.5: SLAM Mapping](./chapter-2-5-slam)

---

## Assessment: Autonomous Navigator

**Goal**: Create a robot that navigates through an obstacle course autonomously.

**Requirements**:

1. **Robot with**:
   - Differential drive (2 wheels + caster)
   - LiDAR sensor (270° FOV)
   - Proper friction and inertia

2. **World**: Obstacle course from Chapter 2.2 (walls, cylinders, ramps)

3. **Navigation node** that:
   - Reads LiDAR data
   - Publishes to `/cmd_vel`
   - Avoids obstacles (maintain 0.5m clearance)
   - Explores environment for 60 seconds

4. **RViz2 visualization** showing:
   - Robot model
   - LaserScan
   - Odometry path trail

**Deliverables**:
- Robot URDF with diff_drive plugin
- Python navigation node source
- Video (30 seconds) of autonomous navigation
- Screenshot of odometry trail in RViz2

**Expected Pass Rate**: 65% of learners complete within 90 minutes.

**Bonus**: Implement wall-following behavior (stay 0.3m from nearest wall).

---

## Additional Resources

📚 **Official Documentation**:
- [Gazebo Differential Drive Plugin](https://github.com/ros-simulation/gazebo_ros_pkgs/wiki/ROS-2-Migration:-Diff-Drive)
- [geometry_msgs/Twist](https://docs.ros2.org/latest/api/geometry_msgs/msg/Twist.html)
- [nav_msgs/Odometry](https://docs.ros2.org/latest/api/nav_msgs/msg/Odometry.html)

📺 **Video Tutorials**:
- The Construct - Differential Drive Robot
- Articulated Robotics - Robot Kinematics Explained
- ROS 2 Basics - Teleop and Motion Control

🛠️ **Tools**:
- [teleop_twist_joy](https://github.com/ros2/teleop_twist_joy) - Joystick control
- [rqt_robot_steering](http://wiki.ros.org/rqt_robot_steering) - GUI velocity control
- [PlotJuggler](https://github.com/facontidavide/PlotJuggler) - Plot odometry over time

📦 **Example Robots**:
- [TurtleBot3 Burger](https://github.com/ROBOTIS-GIT/turtlebot3) - Classic diff drive
- [ROSbot 2.0](https://github.com/husarion/rosbot_description) - Four-wheel diff drive
- [Clearpath Jackal](https://github.com/jackal/jackal) - Outdoor mobile robot

---

**Chapter Status**: Complete ✅
**Next Chapter**: [2.5 SLAM Mapping](./chapter-2-5-slam)
