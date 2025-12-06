# Contract: Chapter 4.4 - LLM Task Planner

**Chapter**: 4.4 - LLMs for Cognitive Planning
**Component**: LLMPlannerNode (ROS 2 node for LLM-based task planning)
**Purpose**: Receives voice commands from `/voice_command`, sends to LLM (GPT-4 or Claude), returns structured action plans to `/action_plan`

## Overview

LLMPlannerNode subscribes to `/voice_command` topic, sends natural language commands to an LLM (GPT-4 or Claude 3), receives structured action plans (JSON format), validates plans, and publishes to `/action_plan` topic for execution by downstream nodes.

## Functional Requirements

### FR-1: Subscribe to Voice Commands
- **Input**: `std_msgs/String` messages from `/voice_command` topic
- **Output**: Trigger LLM planning pipeline
- **Constraints**: QoS profile matches WhisperNode publisher

### FR-2: LLM Integration (GPT-4 and Claude 3 support)
- **Input**: Natural language command (string)
- **Output**: Action plan (JSON array of actions)
- **Constraints**:
  - Support both OpenAI GPT-4 and Anthropic Claude 3
  - Provider selected via env var `LLM_PROVIDER` (values: `openai` or `anthropic`)
  - Model configurable via `LLM_MODEL` (default: `gpt-4-turbo-preview` or `claude-3-sonnet-20240229`)
  - System prompt includes robot capabilities (navigate, grasp, place, search, wait)
  - Few-shot examples provided (3-5 example command → plan pairs)
  - Output format: JSON schema `[{action: string, target: string, params: dict}]`
  - Timeout: 10 seconds
- **Test**: Send command "Pick up the red box", verify JSON plan received

### FR-3: Prompt Engineering
- **System Prompt Template**:
  ```
  You are a robot task planner. Your job is to decompose natural language commands into sequences of action primitives.

  Available actions:
  - navigate(target: string) - Move to location or object
  - grasp(object: string) - Pick up object
  - place(location: string) - Put down held object
  - search(object: string) - Look around for object
  - wait(duration: float) - Wait for duration seconds

  Output format: JSON array of actions.
  Example: [{"action": "navigate", "target": "red box"}, {"action": "grasp", "object": "red box"}]

  Rules:
  - Break complex tasks into simple steps
  - Navigate before grasping
  - Refuse unsafe commands (harm, attack, etc.)
  - Ask clarifying questions if command is ambiguous
  ```

- **Few-Shot Examples** (in `planning_examples.json`):
  ```json
  [
    {
      "command": "Pick up the blue cup",
      "plan": [
        {"action": "navigate", "target": "blue cup"},
        {"action": "grasp", "object": "blue cup"}
      ]
    },
    {
      "command": "Bring me the wrench from the table",
      "plan": [
        {"action": "navigate", "target": "table"},
        {"action": "search", "object": "wrench"},
        {"action": "grasp", "object": "wrench"},
        {"action": "navigate", "target": "user"},
        {"action": "place", "location": "hand"}
      ]
    }
  ]
  ```

### FR-4: Plan Validation
- **Input**: LLM response (JSON string)
- **Output**: Validated action plan or error
- **Validation Rules**:
  - All actions must be in allowed primitives list
  - Required fields present (`action`, `target`/`object`/`location`)
  - No contradictory actions (e.g., grasp before navigate)
  - Safety check: Reject commands containing keywords (harm, attack, destroy, break)
- **Test**: Send invalid plan (unknown action), verify rejection

### FR-5: Publish Action Plans
- **Input**: Validated action plan (list of dicts)
- **Output**: `std_msgs/String` (JSON) on `/action_plan` topic
- **Constraints**: Publish only valid plans, log errors for invalid plans

### FR-6: Handle Ambiguity and Clarifications
- **Behavior**: If LLM detects ambiguous command (e.g., "Bring me that"), LLM should ask clarifying question
- **Output**: Publish clarification request to `/clarification_needed` topic (for user feedback)
- **Test**: Send "Go there", verify clarification request published

## Non-Functional Requirements

### NFR-1: Latency
- **Requirement**: LLM response received within 3 seconds (p95)
- **Test**: Measure time from voice command to action plan publish

### NFR-2: Robustness
- **Requirement**: Handle LLM API failures gracefully (timeouts, rate limits, network errors)
- **Behavior**: Log error, retry once, skip command if retry fails

### NFR-3: Cost Management
- **Requirement**: Log API costs per command (estimate based on token usage)
- **Behavior**: Log warning if single command exceeds $0.10

## API Specification

**Node Name**: `llm_planner_node`

**Subscribers**:
- `/voice_command` (std_msgs/String): Voice commands from WhisperNode

**Publishers**:
- `/action_plan` (std_msgs/String): JSON action plans for execution
- `/clarification_needed` (std_msgs/String): Clarification requests for user

**Parameters**:
- `llm_provider`: String (`openai` or `anthropic`, default: `openai`)
- `llm_model`: String (model ID, default: `gpt-4-turbo-preview`)

## Example Usage

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

class LLMPlannerNode(Node):
    def __init__(self):
        super().__init__('llm_planner_node')
        self.subscription = self.create_subscription(String, '/voice_command', self.voice_callback, 10)
        self.publisher = self.create_publisher(String, '/action_plan', 10)
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def voice_callback(self, msg):
        command = msg.data
        self.get_logger().info(f"Received command: {command}")

        # Call LLM
        plan = self.get_plan(command)
        if plan:
            msg_out = String()
            msg_out.data = json.dumps(plan)
            self.publisher.publish(msg_out)
            self.get_logger().info(f"Published plan: {plan}")

    def get_plan(self, command):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": command}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    def get_system_prompt(self):
        return """You are a robot task planner. Decompose commands into action sequences.
        Actions: navigate, grasp, place, search, wait.
        Output JSON: [{"action": "...", "target": "..."}]"""

def main():
    rclpy.init()
    node = LLMPlannerNode()
    rclpy.spin(node)
    rclpy.shutdown()
```

## Acceptance Criteria

1. ✅ Subscribes to `/voice_command` and publishes to `/action_plan`
2. ✅ Supports both GPT-4 and Claude 3
3. ✅ Generates valid action plans for 90%+ of test commands
4. ✅ Validates plans (all actions in primitives, required fields present)
5. ✅ Handles ambiguous commands (publishes clarification requests)
6. ✅ Refuses unsafe commands (logs rejection, doesn't publish plan)
7. ✅ Handles API errors gracefully (no crashes)

---

**Status**: ✅ Contract complete
**Implementation Effort**: ~4-5 hours
