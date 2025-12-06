---
id: chapter-4-6-pose
title: "Chapter 4.6: 3D Pose Estimation and Action Primitives"
sidebar_label: "4.6 3D Pose Estimation"
sidebar_position: 6
description: "Convert 2D detections to 3D poses using depth cameras for robot manipulation"
keywords: [3d pose, depth camera, rgb-d, object localization, tf frames]
learning_journey: "LJ3"
duration: "2 hours"
difficulty: "advanced"
prerequisites:
  - "chapter-4-5-clip"
  - "module-2-ros2-fundamentals"
objectives:
  - "Understand: Explain 2D to 3D projection using depth data"
  - "Apply: Convert bounding boxes to 3D object poses"
  - "Create: Publish TF frames for detected objects"
  - "Integrate: Connect visual grounding to navigation system"
milestone: "Robot navigates to visually detected objects with 3D coordinates"
---

# Chapter 4.6: 3D Pose Estimation and Action Primitives

## What You'll Learn

By the end of this chapter, you will:
- Convert 2D bounding boxes to 3D world coordinates using depth cameras
- Publish TF frames for detected objects
- Implement ActionExecutorNode that interprets LLM action plans
- Connect vision, planning, and navigation into working VLA pipeline
- Handle coordinate frame transformations (camera → robot base → world)

**Estimated Time**: 2 hours

---

## From 2D Detection to 3D Position

Chapter 4.5 gave us 2D bounding boxes: `[x1, y1, x2, y2]` in pixel coordinates.

**Problem**: Robots need 3D positions `(x, y, z)` in meters to navigate.

### RGB-D Cameras

**RGB-D cameras** (e.g., Intel RealSense, Azure Kinect) provide:
- RGB image: Color data
- Depth image: Distance from camera for each pixel (in meters)

**Key Idea**: For bounding box center `(cx, cy)`, look up depth at that pixel → distance `d` → compute 3D point.

---

## Camera Intrinsics and Projection

### Pinhole Camera Model

```
3D World Point (X, Y, Z) → 2D Image Pixel (u, v)
```

**Projection Formula**:
```
u = (fx * X / Z) + cx
v = (fy * Y / Z) + cy
```

Where:
- `(fx, fy)`: Focal lengths (pixels)
- `(cx, cy)`: Principal point (image center)
- These are camera **intrinsic parameters**

### Inverse Projection (Depth → 3D)

Given pixel `(u, v)` and depth `d`:
```
X = (u - cx) * d / fx
Y = (v - cy) * d / fy
Z = d
```

---

## Code: 2D to 3D Conversion

```python
"""
Convert 2D bounding box + depth to 3D pose
"""

import numpy as np

def bbox_to_3d_pose(bbox, depth_image, camera_intrinsics):
    """
    Convert bounding box to 3D position

    Args:
        bbox: [x1, y1, x2, y2] in pixels
        depth_image: numpy array (height, width), depth in meters
        camera_intrinsics: dict with 'fx', 'fy', 'cx', 'cy'

    Returns:
        (x, y, z) in meters relative to camera frame
    """
    x1, y1, x2, y2 = bbox

    # Bounding box center
    cx_bbox = int((x1 + x2) / 2)
    cy_bbox = int((y1 + y2) / 2)

    # Get depth at center
    depth = depth_image[cy_bbox, cx_bbox]

    if depth == 0 or depth > 10.0:  # Invalid depth
        return None

    # Camera intrinsics
    fx = camera_intrinsics['fx']
    fy = camera_intrinsics['fy']
    cx = camera_intrinsics['cx']
    cy = camera_intrinsics['cy']

    # Convert to 3D
    X = (cx_bbox - cx) * depth / fx
    Y = (cy_bbox - cy) * depth / fy
    Z = depth

    return (X, Y, Z)

# Example
bbox = [100, 150, 200, 250]
depth_image = np.random.rand(480, 640) * 3.0  # Mock depth data

intrinsics = {
    'fx': 525.0,  # Intel RealSense typical values
    'fy': 525.0,
    'cx': 320.0,
    'cy': 240.0
}

pose_3d = bbox_to_3d_pose(bbox, depth_image, intrinsics)
print(f"3D Pose: {pose_3d}")  # Example: (0.45, -0.32, 1.85) meters
```

---

## TF Frames: Coordinate Systems

Robots work with multiple coordinate frames:
- **camera_frame**: Origin at camera, Z-axis forward
- **base_link**: Robot base, Z-axis up
- **map**: World frame (fixed)

**TF (Transform Frames)** in ROS 2 manages transformations between frames.

### Publishing Detected Object as TF Frame

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
import tf2_ros

class ObjectTFPublisher(Node):
    def __init__(self):
        super().__init__('object_tf_publisher')
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

    def publish_object_pose(self, object_pose, object_name="detected_object"):
        """
        Publish object as TF frame

        Args:
            object_pose: (x, y, z) in camera frame
            object_name: TF frame name
        """
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'camera_link'
        t.child_frame_id = object_name

        t.transform.translation.x = object_pose[0]
        t.transform.translation.y = object_pose[1]
        t.transform.translation.z = object_pose[2]

        # No rotation (assume object upright)
        t.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(t)
        self.get_logger().info(f"Published TF: {object_name} at {object_pose}")

# Usage
node = ObjectTFPublisher()
node.publish_object_pose((1.2, 0.5, 0.3), "red_box")
```

**Result**: Run `rviz2` and add TF display to visualize `red_box` frame in 3D!

---

## Action Executor Node

Now let's execute LLM action plans using our vision and navigation systems.

### Architecture

```
[/action_plan topic] → [ActionExecutorNode]
                             ↓
                ┌────────────┴────────────┐
                ↓                         ↓
         [Navigate Action]        [Detect Action]
         (calls Nav2)             (calls CLIP)
                ↓                         ↓
         [Grasp Action]           [Release Action]
         (gripper control)        (gripper control)
```

### Code: ActionExecutorNode

```python
"""
ActionExecutorNode: Executes action plans from LLM
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class ActionExecutorNode(Node):
    def __init__(self):
        super().__init__('action_executor_node')

        # Subscribe to action plans
        self.plan_sub = self.create_subscription(
            String,
            '/action_plan',
            self.execute_plan,
            10
        )

        # Publishers for sub-actions
        self.detect_pub = self.create_publisher(String, '/detect_object', 10)

        self.get_logger().info("ActionExecutorNode ready")

    def execute_plan(self, msg):
        """Execute action plan step by step"""
        plan = json.loads(msg.data)
        self.get_logger().info(f"📋 Executing plan with {len(plan)} actions")

        for i, action in enumerate(plan):
            self.get_logger().info(f"  Step {i+1}: {action['action']}")

            if action['action'] == 'navigate':
                self.execute_navigate(action['target'])

            elif action['action'] == 'detect':
                self.execute_detect(action['object'])

            elif action['action'] == 'grasp':
                self.execute_grasp(action.get('object'))

            elif action['action'] == 'release':
                self.execute_release()

            elif action['action'] == 'say':
                self.get_logger().info(f"🗣️ Robot says: '{action['text']}'")

            elif action['action'] == 'wait':
                import time
                time.sleep(action['duration'])

        self.get_logger().info("✅ Plan execution complete")

    def execute_navigate(self, target):
        """Navigate to target using Nav2"""
        # Simplified: In real implementation, call Nav2 action client
        self.get_logger().info(f"🚶 Navigating to {target}...")
        # TODO: Implement Nav2 action client call

    def execute_detect(self, object_name):
        """Detect object using visual grounding"""
        detect_msg = String()
        detect_msg.data = object_name
        self.detect_pub.publish(detect_msg)
        self.get_logger().info(f"👁️ Detecting {object_name}...")

    def execute_grasp(self, object_name=None):
        """Close gripper"""
        self.get_logger().info(f"✋ Grasping{' ' + object_name if object_name else ''}...")
        # TODO: Gripper control

    def execute_release(self):
        """Open gripper"""
        self.get_logger().info("✋ Releasing...")
        # TODO: Gripper control

def main(args=None):
    rclpy.init(args=args)
    node = ActionExecutorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## End-to-End Test

```bash
# Terminal 1: Visual grounding
ros2 run vla_robot visual_grounding_node

# Terminal 2: LLM planner
ros2 run vla_robot llm_planner_node

# Terminal 3: Action executor
ros2 run vla_robot action_executor_node

# Terminal 4: Send voice command
ros2 topic pub --once /voice_command std_msgs/msg/String "data: 'Pick up the red box'"
```

**Expected Flow**:
1. LLM Planner: Generates `[navigate, detect, grasp, say]` plan
2. Action Executor: Executes navigate → detect
3. Visual Grounding: Detects red box, publishes bbox + 3D pose
4. Action Executor: Completes grasp → say

---

## Milestone Validation

✅ **You've completed Chapter 4.6 if**:
1. 2D bounding boxes converted to 3D poses using depth data
2. Object TF frames published and visible in RViz2
3. ActionExecutorNode executes LLM plans end-to-end
4. Robot navigates to detected object locations
5. Complete voice → plan → vision → navigation pipeline works

---

## Chapter Summary

You learned:
- ✅ **3D Pose Estimation**: Convert 2D bbox + depth → 3D coordinates
- ✅ **TF Frames**: Publish detected objects as coordinate frames
- ✅ **Action Execution**: Interpret LLM plans and call robot systems
- ✅ **Integration**: Connect voice, planning, vision, and navigation

---

## What's Next?

In **Chapter 4.7**, we'll integrate all components using **state machines** for robust orchestration with error handling.

**🎯 Next Chapter**: [4.7 VLA Pipeline Integration](./chapter-4-7-integration)
