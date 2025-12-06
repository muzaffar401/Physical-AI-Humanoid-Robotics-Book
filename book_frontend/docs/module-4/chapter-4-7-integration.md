---
id: chapter-4-7-integration
title: "Chapter 4.7: VLA Pipeline Integration with State Machines"
sidebar_label: "4.7 VLA Integration"
sidebar_position: 7
description: "Orchestrate complete VLA pipeline using behavior trees and state machines"
keywords: [state machine, behavior tree, py_trees, pipeline integration, orchestration]
learning_journey: "LJ4"
duration: "2.5 hours"
difficulty: "advanced"
prerequisites:
  - "chapter-4-6-pose"
objectives:
  - "Understand: Explain state machines for robot orchestration"
  - "Apply: Use py_trees for VLA pipeline coordination"
  - "Create: Build VLAOrchestratorNode with state transitions"
  - "Integrate: Connect all VLA components into working system"
milestone: "Full voice → action workflow completes successfully end-to-end"
---

# Chapter 4.7: VLA Pipeline Integration with State Machines

## What You'll Learn

By the end of this chapter, you will:
- Understand state machines and behavior trees for robot orchestration
- Use py_trees library for VLA pipeline coordination
- Build VLAOrchestratorNode that manages voice → vision → action workflow
- Handle state transitions, timeouts, and synchronization between nodes
- Test complete end-to-end VLA system

**Estimated Time**: 2.5 hours

---

## The Orchestration Challenge

Previous chapters built individual components:
- Voice: WhisperNode
- Planning: LLMPlannerNode
- Vision: VisualGroundingNode
- Execution: ActionExecutorNode

**Challenge**: These nodes must coordinate in correct order with proper error handling.

### Example VLA Flow

```
User: "Pick up the red box"
↓
[Voice Input] → Transcription: "Pick up the red box"
↓
[LLM Planner] → Plan: [navigate, detect, grasp, say]
↓
[Visual Grounding] → Detect "red box" → 3D pose
↓
[Navigation] → Move to object
↓
[Manipulation] → Grasp object
↓
[Confirmation] → "Task complete"
```

**Without orchestration**: Nodes publish/subscribe independently, no guarantee of correct ordering or error recovery.

**With orchestration**: State machine ensures:
- ✅ Steps execute in sequence
- ✅ Timeouts handled (e.g., detection takes too long)
- ✅ Errors trigger recovery (e.g., object not found → ask user)

---

## State Machines for Robotics

**State Machine**: System with discrete states and transitions between them.

### Example: Fetch Object State Machine

```
┌─────────────┐
│  IDLE       │ (waiting for command)
└──────┬──────┘
       │ voice command received
       ↓
┌─────────────┐
│  PLANNING   │ (LLM generates plan)
└──────┬──────┘
       │ plan ready
       ↓
┌─────────────┐
│  DETECTING  │ (CLIP locates object)
└──────┬──────┘
       │ object found
       ↓
┌─────────────┐
│  NAVIGATING │ (Nav2 moves to object)
└──────┬──────┘
       │ reached target
       ↓
┌─────────────┐
│  GRASPING   │ (close gripper)
└──────┬──────┘
       │ grasp complete
       ↓
┌─────────────┐
│  IDLE       │ (ready for next command)
└─────────────┘
```

---

## Behavior Trees with py_trees

**Behavior Trees (BT)** are hierarchical state machines with composable nodes.

### Installing py_trees

```bash
pip install py_trees
```

### Basic Behavior Tree Example

```python
import py_trees

# Leaf nodes (actual behaviors)
class DetectObject(py_trees.behaviour.Behaviour):
    def update(self):
        print("Detecting object...")
        # Simulate detection
        return py_trees.common.Status.SUCCESS

class NavigateToObject(py_trees.behaviour.Behaviour):
    def update(self):
        print("Navigating to object...")
        return py_trees.common.Status.SUCCESS

class Grasp(py_trees.behaviour.Behaviour):
    def update(self):
        print("Grasping...")
        return py_trees.common.Status.SUCCESS

# Build tree: Sequence (executes children in order)
root = py_trees.composites.Sequence(
    name="FetchObject",
    memory=False,
    children=[
        DetectObject(name="Detect"),
        NavigateToObject(name="Navigate"),
        Grasp(name="Grasp")
    ]
)

# Execute tree
root.setup_with_descendants()
for i in range(5):
    root.tick_once()
```

**Output**:
```
Detecting object...
Navigating to object...
Grasping...
```

**Sequence** node executes children left-to-right, succeeds only if all children succeed.

---

## VLA Orchestrator with Behavior Tree

### Code: VLAOrchestratorNode

```python
"""
VLAOrchestratorNode: Coordinates full VLA pipeline using py_trees
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import py_trees
import json
import time

class VLAOrchestratorNode(Node):
    def __init__(self):
        super().__init__('vla_orchestrator_node')

        # Publishers
        self.detect_pub = self.create_publisher(String, '/detect_object', 10)

        # Subscribers
        self.voice_sub = self.create_subscription(
            String, '/voice_command', self.voice_callback, 10)
        self.plan_sub = self.create_subscription(
            String, '/action_plan', self.plan_callback, 10)
        self.bbox_sub = self.create_subscription(
            String, '/detected_bbox', self.bbox_callback, 10)

        # State
        self.current_command = None
        self.current_plan = None
        self.detected_bbox = None
        self.state = "IDLE"

        self.get_logger().info("VLAOrchestrator ready")

    def voice_callback(self, msg):
        """New voice command received"""
        self.current_command = msg.data
        self.state = "PLANNING"
        self.get_logger().info(f"State: IDLE → PLANNING ('{self.current_command}')")

    def plan_callback(self, msg):
        """Action plan received from LLM"""
        self.current_plan = json.loads(msg.data)
        self.state = "EXECUTING"
        self.get_logger().info(f"State: PLANNING → EXECUTING ({len(self.current_plan)} actions)")
        self.execute_plan()

    def bbox_callback(self, msg):
        """Object detection result"""
        self.detected_bbox = json.loads(msg.data)
        self.get_logger().info(f"Object detected: {self.detected_bbox}")

    def execute_plan(self):
        """Execute action plan sequentially"""
        for i, action in enumerate(self.current_plan):
            action_type = action['action']
            self.get_logger().info(f"[{i+1}/{len(self.current_plan)}] Executing: {action_type}")

            if action_type == 'navigate':
                self.execute_navigate(action['target'])
            elif action_type == 'detect':
                self.execute_detect(action['object'])
                self.wait_for_detection(timeout=5.0)
            elif action_type == 'grasp':
                self.execute_grasp()
            elif action_type == 'release':
                self.execute_release()
            elif action_type == 'say':
                self.get_logger().info(f"🗣️ '{action['text']}'")

            time.sleep(0.5)  # Small delay between actions

        # Complete
        self.state = "IDLE"
        self.get_logger().info("✅ Task complete! State: EXECUTING → IDLE")

    def execute_navigate(self, target):
        self.get_logger().info(f"  🚶 Navigating to '{target}'")
        # TODO: Call Nav2

    def execute_detect(self, object_name):
        self.get_logger().info(f"  👁️ Detecting '{object_name}'")
        detect_msg = String()
        detect_msg.data = object_name
        self.detect_pub.publish(detect_msg)

    def wait_for_detection(self, timeout=5.0):
        """Wait for object detection with timeout"""
        start = time.time()
        while (time.time() - start) < timeout:
            if self.detected_bbox is not None:
                return True
            time.sleep(0.1)

        self.get_logger().warn("⚠️ Detection timeout!")
        return False

    def execute_grasp(self):
        self.get_logger().info("  ✋ Grasping")
        # TODO: Gripper control

    def execute_release(self):
        self.get_logger().info("  ✋ Releasing")
        # TODO: Gripper control

def main(args=None):
    rclpy.init(args=args)
    node = VLAOrchestratorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## Full System Launch

Create launch file: `vla_system.launch.py`

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='vla_robot',
            executable='voice_input_node',
            name='voice_input',
        ),
        Node(
            package='vla_robot',
            executable='llm_planner_node',
            name='llm_planner',
        ),
        Node(
            package='vla_robot',
            executable='visual_grounding_node',
            name='visual_grounding',
        ),
        Node(
            package='vla_robot',
            executable='vla_orchestrator_node',
            name='orchestrator',
        ),
    ])
```

**Launch all nodes**:
```bash
ros2 launch vla_robot vla_system.launch.py
```

---

## End-to-End Test

**Test Scenario**: User says "Pick up the red box"

**Expected Flow**:
1. **Voice Input**: Detects wake-word → transcribes → publishes to `/voice_command`
2. **LLM Planner**: Receives command → generates plan → publishes to `/action_plan`
3. **Orchestrator**: Receives plan → executes actions sequentially:
   - Navigate to "red box"
   - Detect "red box" (calls Visual Grounding)
   - Grasp
   - Say "Task complete"
4. **Visual Grounding**: Detects object → publishes bbox + 3D pose
5. **Orchestrator**: Completes workflow → returns to IDLE

**Log Output**:
```
[voice_input] ✅ Wake-word detected: 'computer'
[voice_input] 📝 Transcribed: 'Pick up the red box'
[llm_planner] 📥 Received command: 'Pick up the red box'
[llm_planner] ✅ Published plan: 4 actions
[orchestrator] State: IDLE → PLANNING ('Pick up the red box')
[orchestrator] State: PLANNING → EXECUTING (4 actions)
[orchestrator] [1/4] Executing: navigate
[orchestrator]   🚶 Navigating to 'red box'
[orchestrator] [2/4] Executing: detect
[orchestrator]   👁️ Detecting 'red box'
[visual_grounding] Detecting: 'red box'
[visual_grounding] ✅ Detected at [120, 180, 220, 280]
[orchestrator] [3/4] Executing: grasp
[orchestrator]   ✋ Grasping
[orchestrator] [4/4] Executing: say
[orchestrator] 🗣️ 'Task complete'
[orchestrator] ✅ Task complete! State: EXECUTING → IDLE
```

---

## Milestone Validation

✅ **You've completed Chapter 4.7 if**:
1. VLAOrchestratorNode coordinates all pipeline components
2. State transitions occur in correct order (IDLE → PLANNING → EXECUTING → IDLE)
3. Actions execute sequentially with proper synchronization
4. End-to-end test completes without manual intervention
5. System handles 3+ consecutive commands correctly

---

## Chapter Summary

You learned:
- ✅ **State Machines**: Manage complex workflows with discrete states and transitions
- ✅ **Behavior Trees**: Hierarchical orchestration using py_trees
- ✅ **VLA Integration**: Coordinate voice, planning, vision, and execution
- ✅ **Synchronization**: Handle asynchronous ROS 2 communication with timeouts

---

## What's Next?

In **Chapter 4.8**, we'll add **error recovery** to handle failures like objects not found, navigation blocked, or transcription errors.

**🎯 Next Chapter**: [4.8 Error Recovery and Robustness](./chapter-4-8-recovery)
