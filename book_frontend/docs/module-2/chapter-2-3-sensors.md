---
id: chapter-2-3-sensors
title: "Chapter 2.3: Simulating Sensors"
sidebar_label: "2.3 Sensors"
sidebar_position: 3
---

# Chapter 2.3: Simulating Sensors

## Giving Your Robot Eyes and Ears

Real robots perceive the world through **sensors**: cameras see objects, LiDAR measures distances, IMUs detect orientation. In Gazebo, you can simulate these sensors with realistic noise, delays, and properties—enabling you to develop and test perception algorithms before deploying to hardware.

In this chapter, you'll add cameras, LiDAR, and IMUs to robots in Gazebo, visualize sensor data in RViz2, and process it in ROS 2 nodes.

---

## Learning Objectives

By the end of this chapter, you will:

- **Understand**: Explain how Gazebo simulates sensors and publishes data to ROS 2 topics
- **Apply**: Add camera, LiDAR, and IMU sensors to robot URDF/SDF models
- **Apply**: Configure sensor properties (update rate, resolution, FOV, noise)
- **Analyze**: Visualize sensor data in RViz2 (images, point clouds, laser scans)
- **Create**: ROS 2 node to subscribe to and process sensor data

**Estimated Time**: 2.5 hours

---

## Prerequisites

- **Chapter 2.2 complete** (Custom worlds, SDF basics)
- **Module 1 complete** (ROS 2 publishers/subscribers, URDF)
- **RViz2 and Gazebo installed**

---

## What You'll Build

By the end of this chapter, you'll have:

✅ **Robot with camera** streaming images to ROS 2
✅ **LiDAR sensor** publishing laser scans for obstacle detection
✅ **IMU sensor** reporting orientation and acceleration
✅ **ROS 2 node** processing sensor data in real-time
✅ **RViz2 visualization** of all sensor outputs

---

## Gazebo-ROS 2 Sensor Bridge

### How Sensors Work in Gazebo

**Workflow**:
```
Gazebo Sensor → Gazebo Plugin → ROS 2 Topic → Your Node
```

1. **Sensor** (in SDF/URDF): Defines type, properties, update rate
2. **Gazebo plugin**: Bridges sensor data to ROS 2
3. **ROS 2 topic**: Standard message type (`sensor_msgs/Image`, `sensor_msgs/LaserScan`)
4. **Your code**: Subscribes to topic, processes data

**Key insight**: Sensors in Gazebo publish to **the same ROS 2 topics** as real hardware—your code works with both!

---

## Camera Sensor

### Camera Basics

Cameras capture **RGB images** at a specified resolution and field of view.

**Use cases**:
- Object detection (find people, boxes, signs)
- Visual odometry (track movement)
- Line following
- QR code reading

### Adding Camera to Robot

Create a simple robot with camera:

**camera_bot.urdf**:

```xml
<?xml version="1.0"?>
<robot name="camera_bot">

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.3 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5"/>
      <inertia ixx="0.1" iyy="0.1" izz="0.1" ixy="0" ixz="0" iyz="0"/>
    </inertial>
  </link>

  <!-- Camera link -->
  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
      <material name="red">
        <color rgba="1 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.0001" iyy="0.0001" izz="0.0001" ixy="0" ixz="0" iyz="0"/>
    </inertial>
  </link>

  <!-- Joint connecting camera to base -->
  <joint name="camera_joint" type="fixed">
    <parent link="base_link"/>
    <child link="camera_link"/>
    <origin xyz="0.25 0 0.1" rpy="0 0 0"/>  <!-- Front of robot, looking forward -->
  </joint>

  <!-- Camera sensor -->
  <gazebo reference="camera_link">
    <sensor name="camera" type="camera">
      <update_rate>30</update_rate>  <!-- 30 FPS -->
      <visualize>true</visualize>
      <camera>
        <horizontal_fov>1.047</horizontal_fov>  <!-- 60 degrees -->
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>  <!-- Min distance -->
          <far>100</far>    <!-- Max distance -->
        </clip>
        <noise>
          <type>gaussian</type>
          <mean>0.0</mean>
          <stddev>0.007</stddev>  <!-- Realistic camera noise -->
        </noise>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <ros>
          <namespace>/camera_bot</namespace>
          <remapping>~/image_raw:=image_raw</remapping>
          <remapping>~/camera_info:=camera_info</remapping>
        </ros>
        <frame_name>camera_link</frame_name>
      </plugin>
    </sensor>
  </gazebo>

</robot>
```

**Key properties**:
- `<update_rate>`: Images per second (FPS)
- `<horizontal_fov>`: Field of view in radians (1.047 rad ≈ 60°)
- `<image>`: Resolution (640x480 = VGA)
- `<noise>`: Simulates real camera sensor noise
- `<plugin>`: Publishes to `/camera_bot/image_raw`

### Launch Camera Robot

**launch/camera_bot.launch.py**:

```python
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_robot_description')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'camera_bot.urdf')

    with open(urdf_file, 'r') as file:
        robot_description = file.read()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'camera_bot',
                '-topic', '/robot_description'
            ]
        )
    ])
```

**Start Gazebo and spawn robot**:

```bash
# Terminal 1: Start Gazebo
ign gazebo empty_world.sdf

# Terminal 2: Launch robot
ros2 launch my_robot_description camera_bot.launch.py
```

### View Camera Feed

**Check topics**:

```bash
ros2 topic list
# /camera_bot/image_raw
# /camera_bot/camera_info
```

**View in RViz2**:

```bash
rviz2
```

1. Set **Fixed Frame** to `base_link`
2. **Add** → **Image**
3. **Image Topic**: `/camera_bot/image_raw`
4. You should see live camera feed!

**View with command**:

```bash
ros2 run image_tools showimage --ros-args -r /image:=/camera_bot/image_raw
```

---

## LiDAR (Laser Scanner) Sensor

### LiDAR Basics

**LiDAR** (Light Detection and Ranging) shoots laser beams in a plane, measuring distance to obstacles.

**Output**: Array of distance measurements (laser scan)

**Use cases**:
- Obstacle avoidance
- SLAM (mapping)
- Navigation
- Perimeter detection

### Adding LiDAR to Robot

**lidar_bot.urdf**:

```xml
<?xml version="1.0"?>
<robot name="lidar_bot">

  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="0.2" length="0.15"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.2" length="0.15"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5"/>
      <inertia ixx="0.1" iyy="0.1" izz="0.1" ixy="0" ixz="0" iyz="0"/>
    </inertial>
  </link>

  <link name="lidar_link">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.07"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.07"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.0001" iyy="0.0001" izz="0.0001" ixy="0" ixz="0" iyz="0"/>
    </inertial>
  </link>

  <joint name="lidar_joint" type="fixed">
    <parent link="base_link"/>
    <child link="lidar_link"/>
    <origin xyz="0 0 0.15" rpy="0 0 0"/>  <!-- Top of robot -->
  </joint>

  <gazebo reference="lidar_link">
    <sensor name="lidar" type="gpu_lidar">
      <update_rate>10</update_rate>
      <visualize>true</visualize>
      <lidar>
        <scan>
          <horizontal>
            <samples>360</samples>  <!-- 360 laser beams -->
            <resolution>1</resolution>
            <min_angle>-3.14159</min_angle>  <!-- -π (180°) -->
            <max_angle>3.14159</max_angle>   <!-- +π (180°) -->
          </horizontal>
        </scan>
        <range>
          <min>0.12</min>  <!-- 12cm min distance -->
          <max>10.0</max>  <!-- 10m max distance -->
          <resolution>0.01</resolution>
        </range>
        <noise>
          <type>gaussian</type>
          <mean>0.0</mean>
          <stddev>0.01</stddev>
        </noise>
      </lidar>
      <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
        <ros>
          <namespace>/lidar_bot</namespace>
          <remapping>~/out:=scan</remapping>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
        <frame_name>lidar_link</frame_name>
      </plugin>
    </sensor>
  </gazebo>

</robot>
```

**Key properties**:
- `<samples>`: Number of laser beams (360 = 1 beam per degree)
- `<min_angle>` / `<max_angle>`: Scan arc (full circle = -π to +π)
- `<min>` / `<max>` range: Detection distance limits
- `<update_rate>`: Scans per second

### Visualize LiDAR in RViz2

1. Launch robot in Gazebo
2. Open RViz2
3. Set **Fixed Frame** to `base_link`
4. **Add** → **LaserScan**
5. **Topic**: `/lidar_bot/scan`
6. You'll see red dots representing laser hits!

**Echo scan data**:

```bash
ros2 topic echo /lidar_bot/scan
```

Output shows:
- `ranges[]`: Array of distances (in meters)
- `angle_min`, `angle_max`: Scan arc
- `angle_increment`: Angular resolution

---

## IMU (Inertial Measurement Unit) Sensor

### IMU Basics

**IMU** measures:
- **Linear acceleration** (m/s²) in X, Y, Z
- **Angular velocity** (rad/s) around X, Y, Z
- **Orientation** (quaternion or Euler angles)

**Use cases**:
- Balance control (humanoids, drones)
- Orientation tracking
- Dead reckoning navigation
- Vibration monitoring

### Adding IMU to Robot

Add to **lidar_bot.urdf** (inside `<robot>` tag):

```xml
<link name="imu_link">
  <visual>
    <geometry>
      <box size="0.03 0.03 0.01"/>
    </geometry>
    <material name="green">
      <color rgba="0 1 0 1"/>
    </material>
  </visual>
  <inertial>
    <mass value="0.01"/>
    <inertia ixx="0.00001" iyy="0.00001" izz="0.00001" ixy="0" ixz="0" iyz="0"/>
  </inertial>
</link>

<joint name="imu_joint" type="fixed">
  <parent link="base_link"/>
  <child link="imu_link"/>
  <origin xyz="0 0 0.05" rpy="0 0 0"/>  <!-- Center of robot -->
</joint>

<gazebo reference="imu_link">
  <sensor name="imu" type="imu">
    <update_rate>100</update_rate>  <!-- 100 Hz -->
    <imu>
      <angular_velocity>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.0002</stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.0002</stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.0002</stddev>
          </noise>
        </z>
      </angular_velocity>
      <linear_acceleration>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.017</stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.017</stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.017</stddev>
          </noise>
        </z>
      </linear_acceleration>
    </imu>
    <plugin name="imu_controller" filename="libgazebo_ros_imu_sensor.so">
      <ros>
        <namespace>/lidar_bot</namespace>
        <remapping>~/out:=imu</remapping>
      </ros>
      <frame_name>imu_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

### View IMU Data

```bash
ros2 topic echo /lidar_bot/imu
```

**Output** (`sensor_msgs/Imu`):
```yaml
orientation:
  x: 0.0
  y: 0.0
  z: 0.0
  w: 1.0  # Quaternion (no rotation)
angular_velocity:
  x: 0.0
  y: 0.0
  z: 0.0  # rad/s
linear_acceleration:
  x: 0.0
  y: 0.0
  z: 9.81  # Gravity (m/s²)
```

**In RViz2**:
1. **Add** → **Imu**
2. **Topic**: `/lidar_bot/imu`
3. Shows orientation box and acceleration arrow

---

## Depth Camera (RGB-D Sensor)

### Depth Camera Basics

**RGB-D cameras** (like Intel RealSense, Kinect) provide:
- RGB image (color)
- Depth image (distance to each pixel)
- Point cloud (3D coordinates)

**Use cases**:
- 3D object detection
- Obstacle avoidance
- Grasping (humanoid manipulation)
- SLAM with 3D mapping

### Adding Depth Camera

```xml
<gazebo reference="camera_link">
  <sensor name="depth_camera" type="depth">
    <update_rate>10</update_rate>
    <visualize>true</visualize>
    <camera>
      <horizontal_fov>1.047</horizontal_fov>
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>10.0</far>
      </clip>
    </camera>
    <plugin name="depth_camera_controller" filename="libgazebo_ros_camera.so">
      <ros>
        <namespace>/camera_bot</namespace>
      </ros>
      <camera_name>depth_camera</camera_name>
      <frame_name>camera_link</frame_name>
      <hack_baseline>0.07</hack_baseline>  <!-- Stereo baseline -->
      <min_depth>0.1</min_depth>
      <max_depth>10.0</max_depth>
    </plugin>
  </sensor>
</gazebo>
```

**Topics published**:
- `/camera_bot/depth_camera/image_raw` - RGB image
- `/camera_bot/depth_camera/depth/image_raw` - Depth image
- `/camera_bot/depth_camera/points` - Point cloud (`sensor_msgs/PointCloud2`)

**Visualize point cloud in RViz2**:
1. **Add** → **PointCloud2**
2. **Topic**: `/camera_bot/depth_camera/points`
3. **Fixed Frame**: `camera_link`
4. Shows 3D points colored by depth!

---

## Hands-On: Processing Sensor Data

Let's create a ROS 2 node that subscribes to sensor data.

### Example: Obstacle Detection with LiDAR

**obstacle_detector.py**:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class ObstacleDetector(Node):
    def __init__(self):
        super().__init__('obstacle_detector')

        self.subscription = self.create_subscription(
            LaserScan,
            '/lidar_bot/scan',
            self.scan_callback,
            10
        )

        self.get_logger().info('Obstacle detector started')

    def scan_callback(self, msg):
        # Get minimum distance from laser scan
        min_distance = min(msg.ranges)

        # Check if obstacle is too close
        if min_distance < 0.5:  # 50cm threshold
            self.get_logger().warn(f'Obstacle detected at {min_distance:.2f}m!')
        else:
            self.get_logger().info(f'Clear path (nearest: {min_distance:.2f}m)')

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run**:

```bash
python3 obstacle_detector.py
```

**Test**: Place obstacles near robot in Gazebo—node will log warnings!

---

## Sensor Configuration Best Practices

### 1. Match Real Hardware

If deploying to physical robot with RealSense D435:
- Resolution: 640x480
- FOV: 69° horizontal
- Update rate: 30 Hz

**Configure Gazebo sensor identically** for realistic testing.

### 2. Add Realistic Noise

Real sensors have noise. Add Gaussian noise:

```xml
<noise>
  <type>gaussian</type>
  <mean>0.0</mean>
  <stddev>0.01</stddev>  <!-- 1cm standard deviation for LiDAR -->
</noise>
```

### 3. Optimize Update Rates

**Don't overdo it**:
- Camera: 30 Hz (sufficient for most vision)
- LiDAR: 10 Hz (navigation, SLAM)
- IMU: 100 Hz (balance control needs high rate)

Higher rates = slower simulation.

### 4. Use GPU Sensors for Performance

```xml
<sensor name="lidar" type="gpu_lidar">  <!-- GPU-accelerated -->
```

GPU sensors offload computation to graphics card = faster.

---

## Common Sensor Message Types

| Sensor | ROS 2 Message Type | Key Fields |
|--------|-------------------|------------|
| Camera | `sensor_msgs/Image` | `height`, `width`, `data` |
| LiDAR | `sensor_msgs/LaserScan` | `ranges[]`, `angle_min`, `angle_max` |
| IMU | `sensor_msgs/Imu` | `orientation`, `angular_velocity`, `linear_acceleration` |
| Depth | `sensor_msgs/PointCloud2` | `data` (3D points) |
| GPS | `sensor_msgs/NavSatFix` | `latitude`, `longitude`, `altitude` |

---

## Multi-Sensor Robot

Combine sensors for robust perception:

**Warehouse robot**:
- **LiDAR** (front): Obstacle detection, navigation
- **Camera** (front): Barcode reading, object recognition
- **IMU**: Orientation tracking, tilt detection
- **Depth camera** (manipulator): 3D grasp planning

Each sensor publishes to separate topic—process independently or fuse data.

---

## Troubleshooting

### Issue: No sensor topics appearing

**Cause**: Gazebo plugin not loaded or robot not spawned.

**Fix**:
1. Check Gazebo console for plugin errors
2. Verify `libgazebo_ros_camera.so` exists: `ls /opt/ros/humble/lib/libgazebo_ros_*`
3. Ensure `ros_gz_sim` package installed: `sudo apt install ros-humble-ros-gz`

### Issue: Camera shows black image

**Cause**: Camera inside collision geometry or looking at void.

**Fix**:
- Position camera outside robot body
- Point camera at scene (check `<origin rpy>` in joint)

### Issue: LiDAR shows all inf (infinity) values

**Cause**: `<max>` range too low or LiDAR blocked.

**Fix**:
- Increase `<max>` range (e.g., 10m → 50m)
- Visualize LiDAR in Gazebo (green lines) to debug

### Issue: IMU orientation wrong

**Cause**: IMU link frame not aligned with robot.

**Fix**: Ensure IMU link `<origin rpy>` matches robot orientation (typically `0 0 0`).

---

## Key Takeaways

🎓 **Gazebo sensors** use plugins to bridge data to ROS 2 topics with standard message types.

🎓 **Camera sensor** publishes `sensor_msgs/Image` for vision tasks (640x480 @ 30 Hz typical).

🎓 **LiDAR sensor** publishes `sensor_msgs/LaserScan` with distance arrays (360 samples, 10 Hz typical).

🎓 **IMU sensor** publishes `sensor_msgs/Imu` with orientation, angular velocity, linear acceleration.

🎓 **Depth cameras** provide RGB + depth + point clouds for 3D perception.

🎓 **Add realistic noise** to simulate real hardware imperfections.

🎓 **Visualize in RViz2** to debug sensor placement, FOV, and data quality.

---

## What's Next?

You've equipped robots with sensors—now let's make them **move**!

In **Chapter 2.4: Robot Movement in Simulation**, you'll:

- Add wheels and motors to robots
- Implement differential drive controller
- Create velocity control nodes
- Use teleop for keyboard control
- Simulate realistic physics (friction, inertia)

**Continue to** → [Chapter 2.4: Robot Movement](./chapter-2-4-movement)

---

## Assessment: Multi-Sensor Robot

**Goal**: Create a robot with camera, LiDAR, and IMU, then visualize all sensors in RViz2.

**Requirements**:

1. **Robot URDF** with:
   - Camera sensor (640x480, 30 Hz)
   - LiDAR sensor (360 samples, 270° FOV)
   - IMU sensor (100 Hz)
   - All sensors with realistic noise

2. **Spawn in Gazebo** with obstacle course world

3. **RViz2 visualization** showing:
   - Camera image feed
   - LiDAR laser scan (red dots)
   - IMU orientation (box)
   - Robot model

4. **ROS 2 node** that:
   - Subscribes to LiDAR
   - Logs nearest obstacle distance every second

**Deliverables**:
- `multi_sensor_bot.urdf`
- Screenshot of RViz2 with all sensor displays
- Python node source code
- Video (10 seconds) showing sensors working in Gazebo

**Expected Pass Rate**: 70% of learners complete within 60 minutes.

**Bonus**: Add depth camera and visualize point cloud in RViz2.

---

## Additional Resources

📚 **Official Documentation**:
- [Gazebo Sensors](https://gazebosim.org/docs/latest/sensors/)
- [Gazebo-ROS 2 Plugins](https://github.com/ros-simulation/gazebo_ros_pkgs/wiki)
- [sensor_msgs Package](https://docs.ros2.org/latest/api/sensor_msgs/)

📺 **Video Tutorials**:
- The Construct - Simulating Sensors in Gazebo
- Articulated Robotics - Adding Cameras and LiDAR

🛠️ **Tools**:
- [image_view](http://wiki.ros.org/image_view) - View camera images
- [rqt_image_view](http://wiki.ros.org/rqt_image_view) - GUI image viewer
- [rviz_lidar_plugin](https://github.com/tier4/rviz_lidar_plugin) - Advanced LiDAR visualization

📦 **Example Robots**:
- [TurtleBot3 Sensors](https://github.com/ROBOTIS-GIT/turtlebot3_simulations) - LiDAR, camera, IMU
- [Clearpath Husky](https://github.com/husky/husky) - Multi-sensor mobile robot

---

**Chapter Status**: Complete ✅
**Next Chapter**: [2.4 Robot Movement](./chapter-2-4-movement)
