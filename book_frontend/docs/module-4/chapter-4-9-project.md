---
id: chapter-4-9-project
title: "Chapter 4.9: Mini-Project - Voice-Controlled Humanoid Assistant"
sidebar_label: "4.9 Mini-Project"
sidebar_position: 9
description: "Build a complete voice-controlled humanoid assistant for fetch-and-deliver tasks"
keywords: [mini-project, capstone, voice control, humanoid robot, vla system]
learning_journey: "Project"
duration: "4 hours"
difficulty: "advanced"
prerequisites:
  - "chapter-4-8-recovery"
objectives:
  - "Apply: Integrate all VLA components into working system"
  - "Create: Complete humanoid assistant with voice control"
  - "Evaluate: Test on 5 fetch-and-deliver scenarios"
  - "Analyze: Measure success rate and identify failure patterns"
milestone: "80%+ success rate on 5 fetch tasks with error recovery"
---

# Chapter 4.9: Mini-Project - Voice-Controlled Humanoid Assistant

## Project Overview

**Goal**: Build a complete voice-controlled humanoid assistant that can:
- Listen for wake-word ("Hey Robot")
- Transcribe voice commands with Whisper
- Plan tasks using LLM (GPT-4 or Claude)
- Locate objects with CLIP visual grounding
- Navigate to objects using Nav2
- Grasp and deliver objects
- Recover from errors (object not found, navigation blocked, etc.)

**Success Criteria**: Complete 4 out of 5 fetch-and-deliver tasks successfully (80% success rate) with autonomous error recovery.

**Estimated Time**: 4 hours

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   VOICE-CONTROLLED ASSISTANT                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Microphone] → [Wake-Word (Porcupine)]                   │
│                         ↓                                   │
│                  [Whisper ASR]                             │
│                         ↓                                   │
│                  [/voice_command]                          │
│                         ↓                                   │
│              [LLM Planner (GPT-4/Claude)]                  │
│                         ↓                                   │
│                  [/action_plan]                            │
│                         ↓                                   │
│              [VLA Orchestrator]                            │
│         ┌───────┴────────┬────────┐                       │
│         ↓                ↓        ↓                        │
│  [Visual Grounding]  [Nav2]  [Gripper]                    │
│      (CLIP)                                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 1: Environment Setup (30 minutes)

### 1.1 Simulation Environment

Use Gazebo or Isaac Sim with a home environment:
- Kitchen with table
- Living room
- 5-10 household objects (mugs, boxes, tools, etc.)
- Humanoid or mobile manipulator robot

**Gazebo Setup**:
```bash
# Launch home world
ros2 launch your_package home_world.launch.py

# Launch robot
ros2 launch your_package spawn_robot.launch.py
```

### 1.2 Test Objects

Ensure environment contains:
1. **Red box** (on kitchen table)
2. **Blue mug** (on counter)
3. **Wrench** (on toolbox)
4. **Green bottle** (on shelf)
5. **Yellow book** (on desk)

### 1.3 API Keys

Verify `.env` file:
```bash
PICOVOICE_API_KEY=your_key
OPENAI_API_KEY=sk-proj-your_key
# OR
ANTHROPIC_API_KEY=sk-ant-your_key
```

---

## Part 2: System Integration (1 hour)

### 2.1 Launch All VLA Components

Create master launch file: `vla_full_system.launch.py`

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Voice input
        Node(
            package='vla_robot',
            executable='voice_input_node',
            name='voice_input',
            parameters=[{'whisper_mode': 'api'}]
        ),

        # LLM planner
        Node(
            package='vla_robot',
            executable='llm_planner_node',
            name='llm_planner',
            parameters=[{'llm_provider': 'claude'}]  # or 'gpt4'
        ),

        # Visual grounding
        Node(
            package='vla_robot',
            executable='visual_grounding_node',
            name='visual_grounding'
        ),

        # VLA orchestrator with error recovery
        Node(
            package='vla_robot',
            executable='robust_vla_orchestrator',
            name='orchestrator',
            parameters=[
                {'max_detection_retries': 3},
                {'detection_timeout': 5.0},
                {'enable_recovery': True}
            ]
        ),

        # Camera (if not already launched by simulation)
        Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            name='camera',
            parameters=[{
                'video_device': '/dev/video0',
                'image_width': 640,
                'image_height': 480,
                'framerate': 30.0
            }],
            remappings=[
                ('image_raw', '/camera/image_raw')
            ]
        ),
    ])
```

**Launch System**:
```bash
cd ~/ros2_ws
colcon build --packages-select vla_robot
source install/setup.bash
ros2 launch vla_robot vla_full_system.launch.py
```

### 2.2 Verify Connectivity

In separate terminals, check topics:
```bash
# Check voice commands
ros2 topic echo /voice_command

# Check action plans
ros2 topic echo /action_plan

# Check detections
ros2 topic echo /detected_bbox

# Check TF frames
ros2 run tf2_tools view_frames
```

---

## Part 3: Test Scenarios (1.5 hours)

Run each test scenario and record results.

### Scenario 1: Simple Fetch
**Command**: "Hey Robot, pick up the red box"

**Expected Flow**:
1. Wake-word detected
2. Transcription: "Pick up the red box"
3. LLM plan: `[navigate, detect, grasp, say]`
4. Navigate to "red box"
5. Detect with CLIP → bbox + 3D pose
6. Grasp object
7. Say "Task complete"

**Success Criteria**:
- ✅ Object detected (bbox published)
- ✅ Robot navigates to object
- ✅ Grasp executed
- ✅ No manual intervention

### Scenario 2: Fetch and Deliver
**Command**: "Bring me the blue mug from the counter"

**Expected Flow**:
1. Plan: `[navigate(counter), detect(blue mug), grasp, navigate(user), release, say]`
2. Navigate to counter
3. Detect blue mug
4. Grasp mug
5. Navigate back to user
6. Release mug
7. Confirm: "Here is the blue mug"

**Success Criteria**:
- ✅ Multi-step plan executed correctly
- ✅ Object delivered to user location
- ✅ Confirmation message spoken

### Scenario 3: Object Not Found (Error Recovery)
**Command**: "Get the purple hat"

**Setup**: No purple hat in environment

**Expected Behavior**:
1. Navigate + detect attempts
2. Detection fails after 3 retries
3. Search behavior (rotate 360°)
4. Still not found
5. Ask for help: "I can't find the purple hat. Can you help?"

**Success Criteria**:
- ✅ System doesn't crash
- ✅ Retry logic executed (3 attempts)
- ✅ Search behavior triggered
- ✅ User notification after exhausting retries

### Scenario 4: Navigation Blocked (Error Recovery)
**Command**: "Fetch the wrench from the toolbox"

**Setup**: Place obstacle in robot's path

**Expected Behavior**:
1. LLM plan generated correctly
2. Navigation starts
3. Nav2 reports path blocked
4. Alternative path attempted
5. If still blocked: "I can't reach the toolbox. Please clear the path."

**Success Criteria**:
- ✅ Navigation failure detected
- ✅ Alternative path attempted
- ✅ User notified if recovery fails

### Scenario 5: Ambiguous Command (Clarification)
**Command**: "Bring me something to drink"

**Expected Behavior**:
1. LLM interprets as generic query
2. Generates clarification: "say('What would you like? I see a blue mug and a green bottle.')"
3. Wait for user response
4. Execute refined command

**Success Criteria**:
- ✅ Clarification request sent
- ✅ LLM adapts to user feedback

---

## Part 4: Performance Analysis (1 hour)

### 4.1 Success Rate Calculation

Track results:

| Scenario | Success | Notes |
|----------|---------|-------|
| 1. Simple Fetch | ✅ | Completed in 15s |
| 2. Fetch & Deliver | ✅ | Completed in 28s |
| 3. Object Not Found | ✅ | Error recovery successful |
| 4. Navigation Blocked | ❌ | Got stuck, didn't ask for help |
| 5. Ambiguous Command | ✅ | Clarification worked |

**Success Rate**: 4/5 = **80%** ✅ (meets milestone!)

### 4.2 Failure Analysis

For failed scenarios, identify root causes:

**Scenario 4 Failure**:
- **Root Cause**: Nav2 recovery behavior got stuck in local minimum
- **Fix**: Increase recovery behavior timeout, add "give up" threshold
- **Code Change**: Update orchestrator with stricter navigation timeout

### 4.3 Performance Metrics

Measure key metrics:

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Success rate | 80% | greater than 80% | ✅ |
| Avg. completion time | 22s | under 60s | ✅ |
| Detection accuracy | 90% | greater than 80% | ✅ |
| False wake-word rate | 0.5/hr | under 1/hr | ✅ |
| API cost per task | $0.018 | under $0.05 | ✅ |

---

## Part 5: System Improvements (Optional, 30 minutes)

### 5.1 Add Voice Feedback

Integrate text-to-speech for better UX:
```python
import pyttsx3

def speak(text):
    """Text-to-speech output"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# In orchestrator
speak("Task complete")
```

### 5.2 Add Multi-Object Detection

Handle commands like "Pick up all the red objects":
```python
# In VisualGroundingNode
def detect_all_objects(self, query):
    """Return all matches, not just best one"""
    detections = []
    for bbox in all_candidate_bboxes:
        if similarity(bbox, query) > threshold:
            detections.append(bbox)
    return detections
```

### 5.3 Add Persistent Memory

Remember user preferences:
```python
# Store user preferences
preferences = {
    'favorite_mug': 'blue mug',
    'preferred_table': 'kitchen table'
}

# Use in LLM prompts
system_message += f"\nUser prefers: {preferences}"
```

---

## Milestone Validation

✅ **You've completed the Mini-Project if**:
1. Full VLA system runs without crashes (30+ minutes uptime)
2. Success rate greater than or equal to 80% (4/5 tasks)
3. Error recovery works for at least 2 failure types
4. System handles wake-word, transcription, planning, vision, navigation
5. Documented failure analysis and improvements

---

## Project Deliverables

Submit the following:

### 1. Demo Video (2-3 minutes)
- Show wake-word activation
- Complete fetch-and-deliver task
- Demonstrate error recovery

### 2. Performance Report
- Success rate table
- Completion time metrics
- Failure analysis

### 3. Code Repository
- All ROS 2 nodes
- Launch files
- Configuration files

### 4. Documentation
- System architecture diagram
- Setup instructions
- Lessons learned

---

## Chapter Summary

In this mini-project, you:
- ✅ **Integrated all VLA components** into working system
- ✅ **Tested 5 scenarios** including error cases
- ✅ **Measured performance** with quantitative metrics
- ✅ **Identified improvements** through failure analysis
- ✅ **Built production-ready** voice-controlled robot assistant

---

## What's Next?

**Congratulations!** You've completed Module 4: Vision-Language-Action. You now have a fully functional VLA system capable of:
- Understanding natural language commands
- Planning multi-step tasks
- Perceiving objects visually
- Executing manipulation and navigation
- Recovering from errors autonomously

### Next Steps

- **Deploy to real hardware** (if available)
- **Extend to more complex tasks** (multi-room navigation, object sorting)
- **Add multimodal perception** (audio localization, tactile sensing)
- **Explore advanced VLA models** (RT-2, PaLM-E, Embodied GPT)

---

## Additional Resources

- [VLA Research Papers](https://arxiv.org/list/cs.RO/recent) - Latest in vision-language-action
- [OK-Robot Project](https://ok-robot.github.io/) - Open-source VLA system
- [Physical AI Blog](https://www.anthropic.com/physical-ai) - Industry perspectives
- [RoboCasa](https://robocasa.ai/) - Simulation environments for home robots

---

**⏱️ Estimated Project Time**: 4 hours (setup, integration, testing, analysis)
**🎯 Module Complete**: Module 4 finished! 🎉
**📚 Course Complete**: You've mastered Physical AI and Humanoid Robotics!
