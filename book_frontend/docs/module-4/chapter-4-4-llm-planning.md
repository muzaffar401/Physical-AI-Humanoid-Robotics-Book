---
id: chapter-4-4-llm-planning
title: "Chapter 4.4: LLMs for Cognitive Planning"
sidebar_label: "4.4 LLM Task Planning"
sidebar_position: 4
description: "Learn to use GPT-4 and Claude for robot task planning with prompt engineering"
keywords: [llm, gpt4, claude, task planning, prompt engineering, few-shot learning]
learning_journey: "LJ2"
duration: "3 hours"
difficulty: "advanced"
prerequisites:
  - "chapter-4-1-introduction"
  - "chapter-4-2-speech-to-text"
objectives:
  - "Understand: Explain how LLMs enable flexible robot task planning"
  - "Apply: Design prompts with system messages and few-shot examples"
  - "Apply: Compare GPT-4 vs Claude 3 for task decomposition"
  - "Create: Build LLMPlannerNode that converts commands to action plans"
  - "Evaluate: Implement validation and safety checks for LLM outputs"
milestone: "LLM generates valid action plans for 90%+ of test commands"
---

# Chapter 4.4: LLMs for Cognitive Planning

## What You'll Learn

By the end of this chapter, you will:
- Understand how Large Language Models (LLMs) enable flexible robot task planning
- Design effective prompts using system messages, few-shot examples, and structured outputs
- Compare GPT-4 vs Claude 3 for robot task decomposition
- Build an LLMPlannerNode that converts natural language to structured action plans
- Implement validation, safety checks, and error handling for LLM outputs
- Handle ambiguous commands and edge cases

**Estimated Time**: 3 hours

---

## The Vision-Language-Action Challenge

In traditional robotics, every task requires explicit programming:

```python
# Traditional: Hardcoded for every object and location
if command == "bring me the red mug":
    navigate(x=3.2, y=1.5)  # Kitchen table coordinates
    detect_object("red mug")
    grasp()
    navigate(x=0.0, y=0.0)  # User location
    release()
```

**Problem**: Requires coding for every possible command, object, and location. Cannot handle variations like:
- "Get the red cup" (is "cup" the same as "mug"?)
- "Bring me something to drink from" (requires inference)
- "Fetch the mug, but if it's not there, bring the blue one" (conditional logic)

---

## LLMs as Cognitive Planners

**Large Language Models (LLMs)** like GPT-4 and Claude have been trained on massive text datasets and can:
- **Understand natural language** with common-sense reasoning
- **Decompose complex tasks** into step-by-step action sequences
- **Generalize to new scenarios** without retraining
- **Handle ambiguity** through contextual understanding

### How LLMs Work (Simplified)

1. **Training**: LLM learns patterns from billions of text examples (books, websites, code)
2. **Inference**: Given a prompt (text input), LLM predicts most likely next tokens (words)
3. **Structured Output**: With careful prompt design, LLM outputs valid JSON/YAML action plans

**Key Insight**: LLMs aren't "thinking" like humans, but statistical patterns learned from data enable surprisingly robust reasoning for robot tasks.

---

## LLM Selection: GPT-4 vs Claude 3

### GPT-4 (OpenAI)

**Model**: `gpt-4-turbo-2024-04-09` (latest as of 2024)

**Pros**:
- ✅ Strongest reasoning capabilities for complex multi-step tasks
- ✅ Excellent at following structured output formats (JSON)
- ✅ Large context window (128k tokens = ~300 pages)
- ✅ Multimodal (can process images + text, useful for visual grounding)

**Cons**:
- ❌ More expensive (~$0.01 per command)
- ❌ Slower (1-3 seconds latency)

**Pricing**:
- Input: $10 per 1M tokens (~$0.005 per command)
- Output: $30 per 1M tokens (~$0.005 per response)
- **Total per command**: ~$0.01

### Claude 3 Sonnet (Anthropic)

**Model**: `claude-3-sonnet-20240229`

**Pros**:
- ✅ Excellent instruction following (often more reliable than GPT-4)
- ✅ Lower cost (~$0.003 per command)
- ✅ Faster (0.5-2 seconds latency)
- ✅ Strong safety guardrails (refuses unsafe commands)

**Cons**:
- ❌ Slightly weaker reasoning for complex multi-step tasks
- ❌ No multimodal support in Sonnet tier (need Claude 3 Opus for vision)

**Pricing**:
- Input: $3 per 1M tokens (~$0.0015 per command)
- Output: $15 per 1M tokens (~$0.0015 per response)
- **Total per command**: ~$0.003

### Recommendation

- **For learning**: Claude 3 Sonnet (cheaper, faster, great for prototyping)
- **For production**: GPT-4 Turbo (best reasoning, multimodal support)

We'll implement both and let you choose via ROS 2 parameter.

---

## Prompt Engineering for Robot Task Planning

**Prompt engineering** is the art of designing text inputs that guide LLMs to produce desired outputs. For robot task planning, we need:

1. **System Message**: Defines LLM's role and output format
2. **Few-Shot Examples**: Show LLM correct input-output patterns
3. **User Command**: The natural language command to decompose
4. **Structured Output**: JSON/YAML action plan

### Anatomy of a Good Prompt

```
┌─────────────────────────────────────────────────────────┐
│               SYSTEM MESSAGE                            │
│  "You are a robot task planner. Convert commands to     │
│   JSON action sequences with navigate/grasp/place."     │
├─────────────────────────────────────────────────────────┤
│               FEW-SHOT EXAMPLES                         │
│  User: "Pick up the red box"                           │
│  Assistant: [{"action": "navigate", ...}]              │
│                                                          │
│  User: "Bring me the wrench"                           │
│  Assistant: [{"action": "navigate", ...}, ...]         │
├─────────────────────────────────────────────────────────┤
│               USER COMMAND                              │
│  User: "Get the blue cup from the kitchen table"       │
└─────────────────────────────────────────────────────────┘
                         ↓
                  LLM GENERATES
                         ↓
┌─────────────────────────────────────────────────────────┐
│               STRUCTURED OUTPUT                         │
│  [                                                      │
│    {"action": "navigate", "target": "kitchen table"},  │
│    {"action": "detect", "object": "blue cup"},         │
│    {"action": "grasp", "object": "blue cup"},          │
│    {"action": "navigate", "target": "user"},           │
│    {"action": "release"}                               │
│  ]                                                      │
└─────────────────────────────────────────────────────────┘
```

---

## Action Primitives: Defining Robot Capabilities

Before writing prompts, we need to define **action primitives** — atomic robot actions.

### Core Action Primitives

| Action | Parameters | Description | Example |
|--------|-----------|-------------|---------|
| **navigate** | `target` (string) | Move to location or object | `{"action": "navigate", "target": "kitchen"}` |
| **detect** | `object` (string) | Search for object with vision | `{"action": "detect", "object": "red box"}` |
| **grasp** | `object` (string, optional) | Close gripper around object | `{"action": "grasp", "object": "wrench"}` |
| **release** | — | Open gripper to drop object | `{"action": "release"}` |
| **wait** | `duration` (float, seconds) | Pause execution | `{"action": "wait", "duration": 2.0}` |
| **say** | `text` (string) | Speak text to user | `{"action": "say", "text": "Task complete"}` |

### Design Principles

1. **Atomic**: Each action is indivisible (no "pick_up" = navigate + grasp)
2. **Composable**: Complex tasks = sequence of primitives
3. **Validated**: LLM outputs must map to actual robot capabilities

---

## System Message Design

The **system message** is the single most important part of the prompt. It defines:
- LLM's role
- Output format (JSON structure)
- Available actions (primitives)
- Constraints and safety rules

### Example System Message (v1)

```python
SYSTEM_MESSAGE = """
You are a robot task planner for a mobile manipulator robot. Your job is to convert natural language commands into JSON action sequences.

Available actions:
- navigate: Move to a location or object (parameter: target)
- detect: Search for and locate an object (parameter: object)
- grasp: Close gripper around detected object (parameter: object)
- release: Open gripper to drop object
- wait: Pause for duration in seconds (parameter: duration)
- say: Speak text to user (parameter: text)

Output format: JSON array of action objects.

Example:
User: "Pick up the red box"
Assistant: [
  {"action": "navigate", "target": "red box"},
  {"action": "detect", "object": "red box"},
  {"action": "grasp", "object": "red box"}
]

Rules:
- Always detect before grasping
- Navigate to object location before detecting
- End with "say" action to confirm completion
- If command is ambiguous, ask for clarification with "say" action

Only output valid JSON. Do not include explanations.
"""
```

---

## Few-Shot Examples

**Few-shot learning** means providing 2-5 example input-output pairs to show the LLM the pattern.

### Example Few-Shot Demonstrations

```python
FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": "Pick up the wrench"
    },
    {
        "role": "assistant",
        "content": """[
  {"action": "navigate", "target": "wrench"},
  {"action": "detect", "object": "wrench"},
  {"action": "grasp", "object": "wrench"},
  {"action": "say", "text": "I have picked up the wrench"}
]"""
    },
    {
        "role": "user",
        "content": "Bring me the red mug from the kitchen table"
    },
    {
        "role": "assistant",
        "content": """[
  {"action": "navigate", "target": "kitchen table"},
  {"action": "detect", "object": "red mug"},
  {"action": "grasp", "object": "red mug"},
  {"action": "navigate", "target": "user"},
  {"action": "release"},
  {"action": "say", "text": "Here is the red mug"}
]"""
    },
    {
        "role": "user",
        "content": "Move to the kitchen"
    },
    {
        "role": "assistant",
        "content": """[
  {"action": "navigate", "target": "kitchen"},
  {"action": "say", "text": "I have arrived at the kitchen"}
]"""
    }
]
```

**Why Few-Shot Works**: LLMs learn patterns from examples. By showing 3 diverse examples (simple grasp, fetch-deliver, navigation-only), the LLM infers the general structure.

---

## Code Example: Basic LLM Task Planner

Create file: `docs/assets/module-4/code/chapter-4-4/llm_planner_basic.py`

```python
"""
Basic LLM Task Planner
Demonstrates GPT-4 and Claude 3 for robot task decomposition
"""

import openai
import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

# System message
SYSTEM_MESSAGE = """
You are a robot task planner for a mobile manipulator robot. Convert natural language commands into JSON action sequences.

Available actions:
- navigate: Move to location/object (param: target)
- detect: Search for object (param: object)
- grasp: Close gripper (param: object, optional)
- release: Open gripper
- wait: Pause execution (param: duration in seconds)
- say: Speak text (param: text)

Output format: JSON array of actions only, no explanations.

Example:
User: "Pick up the red box"
[
  {"action": "navigate", "target": "red box"},
  {"action": "detect", "object": "red box"},
  {"action": "grasp", "object": "red box"},
  {"action": "say", "text": "Task complete"}
]

Rules:
1. Always detect before grasping
2. Navigate before detecting
3. End with "say" action
4. Keep actions simple and atomic
"""

# Few-shot examples
FEW_SHOT_EXAMPLES = [
    {"role": "user", "content": "Pick up the wrench"},
    {"role": "assistant", "content": '[{"action": "navigate", "target": "wrench"}, {"action": "detect", "object": "wrench"}, {"action": "grasp", "object": "wrench"}, {"action": "say", "text": "I have the wrench"}]'},
    {"role": "user", "content": "Bring me the red mug from the table"},
    {"role": "assistant", "content": '[{"action": "navigate", "target": "table"}, {"action": "detect", "object": "red mug"}, {"action": "grasp", "object": "red mug"}, {"action": "navigate", "target": "user"}, {"action": "release"}, {"action": "say", "text": "Here is the red mug"}]'}
]

def plan_with_gpt4(command):
    """Generate plan using GPT-4"""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE}
    ] + FEW_SHOT_EXAMPLES + [
        {"role": "user", "content": command}
    ]

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.0,  # Deterministic output
        max_tokens=500
    )

    plan_text = response.choices[0].message.content
    return json.loads(plan_text)

def plan_with_claude(command):
    """Generate plan using Claude 3 Sonnet"""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Claude uses system parameter separately
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=500,
        temperature=0.0,
        system=SYSTEM_MESSAGE,
        messages=FEW_SHOT_EXAMPLES + [
            {"role": "user", "content": command}
        ]
    )

    plan_text = message.content[0].text
    return json.loads(plan_text)

def main():
    """Test LLM planners"""
    test_commands = [
        "Pick up the blue box",
        "Bring me the wrench from the toolbox",
        "Move to the kitchen and wait for 5 seconds",
        "Get the red mug, but if you can't find it, bring the blue one instead"
    ]

    print("=" * 70)
    print("LLM Task Planner Comparison")
    print("=" * 70)

    for i, command in enumerate(test_commands, 1):
        print(f"\n🎯 Test {i}: \"{command}\"")
        print("-" * 70)

        # GPT-4
        print("\n📘 GPT-4 Plan:")
        try:
            gpt4_plan = plan_with_gpt4(command)
            print(json.dumps(gpt4_plan, indent=2))
        except Exception as e:
            print(f"❌ Error: {e}")

        # Claude 3
        print("\n📗 Claude 3 Plan:")
        try:
            claude_plan = plan_with_claude(command)
            print(json.dumps(claude_plan, indent=2))
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n" + "=" * 70)
    print("Comparison complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
```

### Guided Walkthrough: Testing LLM Planners

**Step 1**: Install dependencies

```bash
pip install openai anthropic python-dotenv
```

**Step 2**: Configure API keys in `.env`

```bash
# .env file
OPENAI_API_KEY=sk-proj-your_key_here
ANTHROPIC_API_KEY=sk-ant-your_key_here
```

**Step 3**: Run comparison

```bash
python3 llm_planner_basic.py
```

**Expected Output**:

```
======================================================================
LLM Task Planner Comparison
======================================================================

🎯 Test 1: "Pick up the blue box"
----------------------------------------------------------------------

📘 GPT-4 Plan:
[
  {"action": "navigate", "target": "blue box"},
  {"action": "detect", "object": "blue box"},
  {"action": "grasp", "object": "blue box"},
  {"action": "say", "text": "Task complete"}
]

📗 Claude 3 Plan:
[
  {"action": "navigate", "target": "blue box"},
  {"action": "detect", "object": "blue box"},
  {"action": "grasp", "object": "blue box"},
  {"action": "say", "text": "I have picked up the blue box"}
]

🎯 Test 2: "Bring me the wrench from the toolbox"
----------------------------------------------------------------------

📘 GPT-4 Plan:
[
  {"action": "navigate", "target": "toolbox"},
  {"action": "detect", "object": "wrench"},
  {"action": "grasp", "object": "wrench"},
  {"action": "navigate", "target": "user"},
  {"action": "release"},
  {"action": "say", "text": "Here is the wrench"}
]

📗 Claude 3 Plan:
[
  {"action": "navigate", "target": "toolbox"},
  {"action": "detect", "object": "wrench"},
  {"action": "grasp", "object": "wrench"},
  {"action": "navigate", "target": "user"},
  {"action": "release"},
  {"action": "say", "text": "Here is the wrench from the toolbox"}
]
```

**Observations**:
- Both LLMs generate valid, similar action sequences
- GPT-4 tends to be more concise
- Claude tends to include more context in "say" actions
- Both follow the navigation → detection → manipulation pattern

---

## Validation and Safety

LLMs can hallucinate (generate invalid outputs) or produce unsafe plans. We need validation layers:

### 1. JSON Validation

```python
def validate_json(plan_text):
    """Check if output is valid JSON"""
    try:
        plan = json.loads(plan_text)
        if not isinstance(plan, list):
            raise ValueError("Plan must be a JSON array")
        return plan
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
```

### 2. Action Whitelisting

```python
ALLOWED_ACTIONS = {"navigate", "detect", "grasp", "release", "wait", "say"}

def validate_actions(plan):
    """Check if all actions are allowed"""
    for step in plan:
        action = step.get("action")
        if action not in ALLOWED_ACTIONS:
            raise ValueError(f"Invalid action: {action}")
```

### 3. Parameter Validation

```python
def validate_parameters(plan):
    """Check if action parameters are valid"""
    for step in plan:
        action = step["action"]

        if action == "navigate" and "target" not in step:
            raise ValueError("navigate requires 'target' parameter")

        if action == "detect" and "object" not in step:
            raise ValueError("detect requires 'object' parameter")

        if action == "wait" and "duration" not in step:
            raise ValueError("wait requires 'duration' parameter")

        if action == "say" and "text" not in step:
            raise ValueError("say requires 'text' parameter")
```

### 4. Safety Checks

```python
UNSAFE_TARGETS = ["user", "human", "person", "child"]
UNSAFE_ACTIONS = ["throw", "hit", "damage"]

def validate_safety(plan):
    """Check for unsafe commands"""
    for step in plan:
        # Check for unsafe targets
        if "target" in step and any(unsafe in step["target"].lower() for unsafe in UNSAFE_TARGETS):
            if step["action"] in ["grasp", "release"]:
                raise ValueError(f"Unsafe: Cannot {step['action']} near {step['target']}")

        # Check for unsafe actions
        if "object" in step and any(unsafe in step["object"].lower() for unsafe in UNSAFE_ACTIONS):
            raise ValueError(f"Unsafe object reference: {step['object']}")
```

---

## ROS 2 Integration: LLMPlannerNode

Now let's integrate LLM planning into ROS 2.

### Architecture

```
[/voice_command topic] → [LLMPlannerNode] → [/action_plan topic]
                              ↓
                    [GPT-4 or Claude 3]
                              ↓
                       [Validation]
                              ↓
                    [Publish JSON plan]
```

### Code: LLMPlannerNode

Create file: `docs/assets/module-4/code/chapter-4-4/llm_planner_node.py`

```python
"""
LLMPlannerNode: ROS 2 node for LLM-based task planning
Subscribes to /voice_command, publishes to /action_plan
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import openai
import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

# System message and few-shot examples (from basic example)
SYSTEM_MESSAGE = """... (same as before) ..."""
FEW_SHOT_EXAMPLES = [... (same as before) ...]

# Validation
ALLOWED_ACTIONS = {"navigate", "detect", "grasp", "release", "wait", "say"}

class LLMPlannerNode(Node):
    def __init__(self):
        super().__init__('llm_planner_node')

        # Parameters
        self.declare_parameter('llm_provider', 'claude')  # 'gpt4' or 'claude'

        provider = self.get_parameter('llm_provider').value

        # Initialize LLM client
        if provider == 'gpt4':
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.generate_plan = self.plan_with_gpt4
            self.get_logger().info("Using GPT-4 for planning")
        else:
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.generate_plan = self.plan_with_claude
            self.get_logger().info("Using Claude 3 for planning")

        # Subscriber: voice commands
        self.subscription = self.create_subscription(
            String,
            '/voice_command',
            self.command_callback,
            10
        )

        # Publisher: action plans
        self.publisher = self.create_publisher(String, '/action_plan', 10)

        self.get_logger().info("LLMPlannerNode ready")

    def command_callback(self, msg):
        """Receive voice command and generate plan"""
        command = msg.data
        self.get_logger().info(f"📥 Received command: '{command}'")

        try:
            # Generate plan with LLM
            plan = self.generate_plan(command)

            # Validate plan
            self.validate_plan(plan)

            # Publish plan
            plan_msg = String()
            plan_msg.data = json.dumps(plan)
            self.publisher.publish(plan_msg)

            self.get_logger().info(f"✅ Published plan: {len(plan)} actions")

        except Exception as e:
            self.get_logger().error(f"❌ Planning failed: {e}")

    def plan_with_gpt4(self, command):
        """Generate plan using GPT-4"""
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGE}
        ] + FEW_SHOT_EXAMPLES + [
            {"role": "user", "content": command}
        ]

        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0.0,
            max_tokens=500
        )

        plan_text = response.choices[0].message.content
        return json.loads(plan_text)

    def plan_with_claude(self, command):
        """Generate plan using Claude 3"""
        message = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            temperature=0.0,
            system=SYSTEM_MESSAGE,
            messages=FEW_SHOT_EXAMPLES + [
                {"role": "user", "content": command}
            ]
        )

        plan_text = message.content[0].text
        return json.loads(plan_text)

    def validate_plan(self, plan):
        """Validate plan structure and safety"""
        if not isinstance(plan, list):
            raise ValueError("Plan must be a list")

        for step in plan:
            # Check action is allowed
            action = step.get("action")
            if action not in ALLOWED_ACTIONS:
                raise ValueError(f"Invalid action: {action}")

            # Check required parameters
            if action == "navigate" and "target" not in step:
                raise ValueError("navigate requires 'target'")
            if action == "detect" and "object" not in step:
                raise ValueError("detect requires 'object'")
            if action == "wait" and "duration" not in step:
                raise ValueError("wait requires 'duration'")
            if action == "say" and "text" not in step:
                raise ValueError("say requires 'text'")

def main(args=None):
    rclpy.init(args=args)
    node = LLMPlannerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Running LLMPlannerNode

```bash
# Terminal 1: Run planner node with Claude (default)
ros2 run vla_robot llm_planner_node

# OR with GPT-4
ros2 run vla_robot llm_planner_node --ros-args -p llm_provider:=gpt4

# Terminal 2: Send test command
ros2 topic pub --once /voice_command std_msgs/msg/String "data: 'Pick up the red box'"

# Terminal 3: Monitor action plan
ros2 topic echo /action_plan
```

**Expected Output (Terminal 3)**:
```
data: '[{"action": "navigate", "target": "red box"}, {"action": "detect", "object": "red box"}, {"action": "grasp", "object": "red box"}, {"action": "say", "text": "Task complete"}]'
---
```

---

## Milestone Validation

✅ **You've completed Chapter 4.4 if**:
1. LLMPlannerNode generates valid JSON action plans for natural language commands
2. Plans include correct action primitives (navigate, detect, grasp, etc.)
3. Validation catches invalid actions and missing parameters
4. Works with both GPT-4 and Claude 3 (user-selectable)
5. Success rate greater than 90% on test commands (see test suite below)

### Test Suite

```bash
# Test commands (expected: valid plans)
✅ "Pick up the wrench"
✅ "Bring me the blue mug from the table"
✅ "Move to the kitchen"
✅ "Get the red box and place it on the shelf"

# Edge cases (expected: error handling)
❌ "Throw the box at the wall" (unsafe action)
❌ "Bring me the xylophone" (ambiguous/uncommon object, should ask for clarification)
```

---

## Chapter Summary

In this chapter, you learned:
- ✅ **LLM Task Planning**: GPT-4 and Claude 3 decompose natural language into robot action sequences
- ✅ **Prompt Engineering**: System messages + few-shot examples guide LLM outputs
- ✅ **Action Primitives**: Atomic robot actions (navigate, detect, grasp, release, wait, say)
- ✅ **Validation**: JSON, action whitelisting, parameter checks, safety filters
- ✅ **ROS 2 Integration**: LLMPlannerNode subscribes to /voice_command, publishes /action_plan
- ✅ **Model Comparison**: GPT-4 (best reasoning, $0.01/command) vs Claude 3 (faster, $0.003/command)

---

## What's Next?

Now your robot can convert voice commands into action plans. In **Chapter 4.5**, we'll implement **visual grounding with CLIP** so the robot can locate objects mentioned in commands ("red box", "wrench") in camera images.

You'll learn:
- How CLIP matches text to image regions (zero-shot object detection)
- Integrating CLIP with ROS 2 for real-time object localization
- Bounding box detection and 3D pose estimation
- Combining LLM plans with visual perception

**Ready to give your robot vision?** Let's continue! 🚀

---

## Additional Resources

- [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774) - Model architecture and capabilities
- [Claude 3 Model Card](https://www.anthropic.com/claude) - Safety and performance details
- [Prompt Engineering Guide](https://www.promptingguide.ai/) - Comprehensive prompt design patterns
- [LLM Safety for Robotics](https://arxiv.org/abs/2308.14074) - Academic survey on safe LLM integration

---

**⏱️ Estimated Chapter Time**: 3 hours (reading, coding, prompt tuning)
**🎯 Next Chapter**: [4.5 Visual Grounding with CLIP](./chapter-4-5-clip)
