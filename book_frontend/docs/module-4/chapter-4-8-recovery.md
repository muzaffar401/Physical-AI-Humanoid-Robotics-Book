---
id: chapter-4-8-recovery
title: "Chapter 4.8: Error Recovery and Robustness"
sidebar_label: "4.8 Error Recovery"
sidebar_position: 8
description: "Implement error detection and recovery strategies for robust VLA systems"
keywords: [error recovery, robustness, fault tolerance, retry logic, fallback strategies]
learning_journey: "LJ4"
duration: "2 hours"
difficulty: "advanced"
prerequisites:
  - "chapter-4-7-integration"
objectives:
  - "Understand: Identify common failure modes in VLA pipelines"
  - "Apply: Implement retry logic, timeouts, and fallback strategies"
  - "Create: Build error recovery behaviors for each VLA component"
  - "Evaluate: Test system robustness with intentional failures"
milestone: "VLA system recovers from 3+ failure types without human intervention"
---

# Chapter 4.8: Error Recovery and Robustness

## What You'll Learn

By the end of this chapter, you will:
- Identify common failure modes in VLA pipelines (detection, navigation, transcription errors)
- Implement retry logic and exponential backoff
- Design fallback strategies (e.g., ask user for help, try alternative objects)
- Build error recovery behaviors into orchestrator
- Test system robustness with intentional error injection

**Estimated Time**: 2 hours

---

## Common VLA Failure Modes

### 1. Transcription Errors
**Problem**: Whisper misinterprets speech
- User says: "Pick up the wrench"
- Whisper hears: "Pick up the ranch"

**Recovery Strategy**: Confidence scoring + confirmation
```python
if transcript_confidence < 0.8:
    say("Did you say 'pick up the ranch'? Please repeat.")
    retry_transcription()
```

### 2. Detection Failures
**Problem**: CLIP can't find object
- Object not in view
- Object occluded by other items
- Lighting conditions poor

**Recovery Strategy**: Search behavior
```python
if object_not_detected:
    rotate_360_degrees()  # Search for object
    if still_not_detected:
        say("I can't find the red box. Can you point to it?")
        wait_for_user_guidance()
```

### 3. Navigation Failures
**Problem**: Nav2 can't reach target
- Path blocked
- Target unreachable
- Localization lost

**Recovery Strategy**: Alternative paths + user query
```python
if navigation_failed:
    try_alternative_path()
    if still_failed:
        say("I can't reach the table. Can you move obstacles?")
        wait(10)  # Give user time
        retry_navigation()
```

### 4. LLM Hallucinations
**Problem**: LLM generates invalid actions
- Unknown action types ("fly", "teleport")
- Missing required parameters
- Unsafe commands

**Recovery Strategy**: Validation + clarification
```python
if invalid_action_detected:
    say("I don't understand that command. Can you rephrase?")
    request_new_voice_command()
```

### 5. Gripper Failures
**Problem**: Grasp unsuccessful
- Object slips
- Gripper misaligned
- Object too heavy

**Recovery Strategy**: Retry with adjusted approach
```python
if grasp_failed:
    adjust_gripper_angle()
    retry_grasp(max_attempts=3)
    if still_failed:
        say("I can't grasp this object. It may be too heavy.")
```

---

## Error Recovery Patterns

### Pattern 1: Retry with Exponential Backoff

```python
def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    """
    Retry function with exponential backoff

    Args:
        func: Function to retry
        max_retries: Maximum attempts
        base_delay: Initial delay in seconds

    Returns:
        Function result or None on failure
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                return None

            delay = base_delay * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed. Retrying in {delay}s...")
            time.sleep(delay)

# Usage
result = retry_with_backoff(lambda: detect_object("red box"))
```

### Pattern 2: Timeout with Fallback

```python
def with_timeout_fallback(func, timeout=5.0, fallback=None):
    """
    Execute function with timeout, return fallback on failure

    Args:
        func: Function to execute
        timeout: Timeout in seconds
        fallback: Value to return on timeout

    Returns:
        Function result or fallback
    """
    import threading

    result = [fallback]
    exception = [None]

    def worker():
        try:
            result[0] = func()
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print(f"Timeout after {timeout}s")
        return fallback

    if exception[0]:
        print(f"Error: {exception[0]}")
        return fallback

    return result[0]

# Usage
pose = with_timeout_fallback(
    lambda: get_object_pose("red box"),
    timeout=3.0,
    fallback=(0, 0, 0)  # Default position
)
```

### Pattern 3: State Recovery

```python
class RecoverableState:
    """State machine with recovery checkpoints"""

    def __init__(self):
        self.state = "IDLE"
        self.checkpoints = []

    def checkpoint(self):
        """Save current state"""
        self.checkpoints.append(self.state)

    def rollback(self):
        """Restore last checkpoint"""
        if self.checkpoints:
            self.state = self.checkpoints.pop()
            print(f"Rolled back to state: {self.state}")

    def transition(self, new_state):
        """Transition with checkpoint"""
        self.checkpoint()
        self.state = new_state

# Usage
state = RecoverableState()
state.transition("DETECTING")
# ... error occurs ...
state.rollback()  # Back to previous state
```

---

## Enhanced VLA Orchestrator with Error Recovery

```python
"""
VLAOrchestratorNode with error recovery
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import time

class RobustVLAOrchestrator(Node):
    def __init__(self):
        super().__init__('robust_vla_orchestrator')

        # ... (same initialization as Chapter 4.7) ...

        # Error recovery parameters
        self.declare_parameter('max_detection_retries', 3)
        self.declare_parameter('detection_timeout', 5.0)
        self.declare_parameter('enable_recovery', True)

    def execute_detect_with_recovery(self, object_name):
        """Detect object with retry and search behavior"""
        max_retries = self.get_parameter('max_detection_retries').value
        timeout = self.get_parameter('detection_timeout').value

        for attempt in range(max_retries):
            self.get_logger().info(f"Detection attempt {attempt + 1}/{max_retries}")

            # Request detection
            self.execute_detect(object_name)

            # Wait for result
            if self.wait_for_detection(timeout):
                self.get_logger().info("✅ Detection successful")
                return True

            # Recovery: Rotate and search
            if attempt < max_retries - 1:
                self.get_logger().warn(f"Detection failed. Searching...")
                self.execute_search_behavior()

        # All attempts failed
        self.get_logger().error(f"❌ Could not detect '{object_name}' after {max_retries} attempts")
        self.execute_ask_for_help(f"I can't find the {object_name}. Can you help?")
        return False

    def execute_search_behavior(self):
        """Rotate robot to search for object"""
        self.get_logger().info("🔍 Searching (rotating 90°)...")
        # TODO: Send rotation command to base
        time.sleep(2)  # Simulate rotation

    def execute_ask_for_help(self, message):
        """Ask user for help via speech"""
        self.get_logger().warn(f"🗣️ Asking for help: '{message}'")
        # TODO: Text-to-speech

    def execute_navigate_with_recovery(self, target):
        """Navigate with retry on failure"""
        max_retries = 2

        for attempt in range(max_retries):
            try:
                # Call Nav2 (placeholder)
                success = self.call_nav2(target)

                if success:
                    return True

                # Navigation failed
                self.get_logger().warn(f"Navigation attempt {attempt + 1} failed")

                if attempt < max_retries - 1:
                    # Try alternative path
                    self.get_logger().info("Trying alternative path...")
                    time.sleep(1)

            except Exception as e:
                self.get_logger().error(f"Navigation error: {e}")

        # Failed after retries
        self.execute_ask_for_help(f"I can't reach {target}. Please clear the path.")
        return False

    def call_nav2(self, target):
        """Placeholder for Nav2 call"""
        # TODO: Implement Nav2 action client
        return True  # Assume success for now

    def execute_grasp_with_recovery(self):
        """Grasp with force sensing and retry"""
        max_attempts = 3

        for attempt in range(max_attempts):
            self.get_logger().info(f"Grasp attempt {attempt + 1}/{max_attempts}")

            # Send grasp command
            self.execute_grasp()
            time.sleep(0.5)

            # Check if object secured (placeholder)
            object_secured = self.check_grasp_success()

            if object_secured:
                self.get_logger().info("✅ Grasp successful")
                return True

            # Adjust and retry
            if attempt < max_attempts - 1:
                self.get_logger().warn("Grasp failed, adjusting...")
                self.adjust_gripper_position()

        # Failed
        self.execute_ask_for_help("I can't grasp this object. Please help.")
        return False

    def check_grasp_success(self):
        """Check if object is grasped (force sensor, etc.)"""
        # TODO: Read force sensor
        return True  # Assume success for now

    def adjust_gripper_position(self):
        """Adjust gripper for better grasp"""
        self.get_logger().info("Adjusting gripper position...")
        time.sleep(0.5)

def main(args=None):
    rclpy.init(args=args)
    node = RobustVLAOrchestrator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## Testing Error Recovery

### Test 1: Object Not in View

**Setup**: Remove target object from camera view

**Expected Behavior**:
1. Detection attempt 1: Timeout (5s)
2. Search behavior: Rotate 90°
3. Detection attempt 2: Timeout
4. Search behavior: Rotate 90°
5. Detection attempt 3: Timeout
6. Ask for help: "I can't find the red box. Can you help?"

### Test 2: Navigation Blocked

**Setup**: Place obstacle in robot path

**Expected Behavior**:
1. Navigation attempt 1: Blocked
2. Try alternative path
3. If still blocked: "I can't reach the table. Please clear the path."

### Test 3: Transcription Garbled

**Setup**: Say unclear or nonsense phrase

**Expected Behavior**:
1. LLM planner: Invalid plan generated (validation fails)
2. System: "I don't understand that command. Can you rephrase?"

---

## Error Metrics Dashboard

Track error recovery effectiveness:

```python
class ErrorMetrics:
    def __init__(self):
        self.total_tasks = 0
        self.successful_tasks = 0
        self.failed_tasks = 0
        self.retries_by_type = {
            'detection': 0,
            'navigation': 0,
            'grasp': 0,
            'transcription': 0
        }

    def record_retry(self, error_type):
        if error_type in self.retries_by_type:
            self.retries_by_type[error_type] += 1

    def record_task_result(self, success):
        self.total_tasks += 1
        if success:
            self.successful_tasks += 1
        else:
            self.failed_tasks += 1

    def report(self):
        success_rate = (self.successful_tasks / self.total_tasks * 100
                        if self.total_tasks > 0 else 0)

        print("\n📊 Error Recovery Metrics")
        print(f"Tasks completed: {self.total_tasks}")
        print(f"Success rate: {success_rate:.1f}%")
        print(f"Failed tasks: {self.failed_tasks}")
        print(f"\nRetries by type:")
        for error_type, count in self.retries_by_type.items():
            print(f"  {error_type}: {count}")
```

---

## Milestone Validation

✅ **You've completed Chapter 4.8 if**:
1. System recovers from detection failures (retries + search)
2. System recovers from navigation failures (alternative paths)
3. System recovers from grasp failures (adjust + retry)
4. System asks user for help after exhausting retries
5. Success rate greater than 80% on 10 test scenarios with injected errors

---

## Chapter Summary

You learned:
- ✅ **Failure Modes**: Detection, navigation, grasp, transcription, LLM errors
- ✅ **Recovery Patterns**: Retry with backoff, timeout+fallback, state recovery
- ✅ **Robust Orchestration**: Error detection and recovery integrated into VLA pipeline
- ✅ **User Communication**: Ask for help when autonomous recovery fails

---

## What's Next?

In **Chapter 4.9**, you'll apply everything in a **Mini-Project**: Build a voice-controlled humanoid assistant that completes fetch-and-deliver tasks in a simulated home environment.

**🎯 Next Chapter**: [4.9 Mini-Project: Voice-Controlled Humanoid Assistant](./chapter-4-9-project)
