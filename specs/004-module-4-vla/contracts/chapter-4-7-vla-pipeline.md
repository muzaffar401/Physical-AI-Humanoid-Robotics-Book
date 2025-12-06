# Contract: Chapter 4.7 - VLA Pipeline Integration

**Chapter**: 4.7-4.8 - VLA Pipeline with State Machines & Error Recovery
**Component**: VLAOrchestratorNode (End-to-end VLA system)
**Purpose**: Orchestrates voice → LLM → vision → action workflow using state machine, handles error recovery

## Overview

VLAOrchestratorNode coordinates all VLA components (WhisperNode, LLMPlannerNode, VisualGroundingNode, ActionExecutor) using a state machine (py_trees behavior tree). It manages state transitions (IDLE → LISTENING → PLANNING → GROUNDING → EXECUTING → SUCCESS/ERROR) and implements error recovery strategies.

## Functional Requirements

### FR-1: State Machine Management
- **States**:
  - IDLE: Waiting for voice command
  - LISTENING: Voice input active (WhisperNode transcribing)
  - PLANNING: LLM generating action plan
  - GROUNDING: Visual grounding detecting objects
  - NAVIGATING: Robot moving to target
  - EXECUTING: Gripper/manipulation action
  - SUCCESS: Task completed
  - ERROR: Failure occurred, recovery triggered

- **Transitions**:
  - IDLE → LISTENING (on wake-word detected)
  - LISTENING → PLANNING (on transcription received)
  - PLANNING → GROUNDING (on action plan received)
  - GROUNDING → NAVIGATING (on object detected)
  - NAVIGATING → EXECUTING (on navigation complete)
  - EXECUTING → SUCCESS (on action complete)
  - Any state → ERROR (on failure)
  - ERROR → IDLE (after recovery attempt)

### FR-2: Component Integration
- **Subscribes to**:
  - `/voice_command` (from WhisperNode)
  - `/action_plan` (from LLMPlannerNode)
  - `/object_pose` (from VisualGroundingNode)
  - `/navigation_feedback` (from Nav2)

- **Publishes to**:
  - `/object_query` (to VisualGroundingNode)
  - `/nav_goal` (to Nav2)
  - `/gripper_command` (to gripper controller)
  - `/system_status` (current state for monitoring)

### FR-3: Error Recovery
- **Speech Misrecognition**:
  - Confirm transcription with user ("Did you say X?")
  - Retry if user rejects (re-run WhisperNode)

- **LLM Hallucination**:
  - Validate plan against environment state
  - Reject impossible actions, request replan

- **Perception Failure** (object not found):
  - Trigger search behavior (rotate, move to different viewpoint)
  - If still not found after 3 attempts, report to user

- **Navigation Failure** (path blocked):
  - Retry Nav2 with alternative path
  - If blocked after 2 retries, report to user

### FR-4: py_trees Integration
- **Behavior Tree Structure**:
  ```
  Root (Sequence)
    ├─ Listen (Wait for /voice_command)
    ├─ Plan (Call LLM)
    ├─ Ground (Call CLIP)
    ├─ Navigate (Send Nav2 goal)
    ├─ Execute (Gripper command)
    └─ Report Success
  ```

- **Fallback Nodes** (for error recovery):
  ```
  Fallback: Perception
    ├─ Primary: CLIP detection
    └─ Fallback: Search behavior (rotate + retry)
  ```

## API Specification

**Node Name**: `vla_orchestrator_node`

**Subscribers**:
- `/voice_command` (std_msgs/String)
- `/action_plan` (std_msgs/String)
- `/object_pose` (geometry_msgs/PoseStamped)

**Publishers**:
- `/object_query` (std_msgs/String)
- `/nav_goal` (geometry_msgs/PoseStamped)
- `/system_status` (std_msgs/String): Current state

**Parameters**:
- `enable_confirmation`: Bool (default: true, confirm transcriptions)
- `max_retry_attempts`: Int (default: 3, for error recovery)

## Example Usage (Simplified State Machine)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from enum import Enum

class VLAState(Enum):
    IDLE = 0
    LISTENING = 1
    PLANNING = 2
    GROUNDING = 3
    EXECUTING = 4
    SUCCESS = 5
    ERROR = 6

class VLAOrchestratorNode(Node):
    def __init__(self):
        super().__init__('vla_orchestrator')
        self.state = VLAState.IDLE

        self.create_subscription(String, '/voice_command', self.voice_callback, 10)
        self.create_subscription(String, '/action_plan', self.plan_callback, 10)
        # ... other subscriptions

        self.status_pub = self.create_publisher(String, '/system_status', 10)

    def voice_callback(self, msg):
        if self.state == VLAState.IDLE:
            self.voice_command = msg.data
            self.transition(VLAState.PLANNING)

    def plan_callback(self, msg):
        if self.state == VLAState.PLANNING:
            self.action_plan = json.loads(msg.data)
            self.transition(VLAState.GROUNDING)
            self.execute_plan()

    def execute_plan(self):
        # Execute actions sequentially
        for action in self.action_plan:
            if action['action'] == 'navigate':
                self.transition(VLAState.GROUNDING)
                # Query visual grounding for target
                # Then navigate
            elif action['action'] == 'grasp':
                self.transition(VLAState.EXECUTING)
                # Send gripper command

        self.transition(VLAState.SUCCESS)

    def transition(self, new_state):
        self.get_logger().info(f"State: {self.state.name} → {new_state.name}")
        self.state = new_state
        msg = String()
        msg.data = new_state.name
        self.status_pub.publish(msg)

def main():
    rclpy.init()
    node = VLAOrchestratorNode()
    rclpy.spin(node)
    rclpy.shutdown()
```

## Acceptance Criteria

1. ✅ Executes full VLA pipeline for simple commands (voice → autonomous action)
2. ✅ State machine transitions correctly (observable in logs)
3. ✅ Recovers from 3+ failure types (speech, planning, perception, navigation)
4. ✅ Completes 4/5 test scenarios in mini-project (80% success rate)
5. ✅ Runs continuously without memory leaks or crashes

---

**Status**: ✅ Contract complete
**Implementation Effort**: ~8-10 hours
