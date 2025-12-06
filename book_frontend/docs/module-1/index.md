---
id: module-1-overview
title: "Module 1: The Robotic Nervous System (ROS 2)"
sidebar_label: "Overview"
sidebar_position: 0
---

# Module 1: The Robotic Nervous System (ROS 2)

## Welcome to ROS 2!

ROS 2 (Robot Operating System 2) is the middleware that powers modern robotics - from warehouse robots to humanoid assistants. Think of it as the nervous system that connects sensors, actuators, and AI into a cohesive robotic intelligence.

**Duration**: 12 hours over 4 weeks (3 hours/week)

---

## What You'll Learn

### 🔗 **Communication Fundamentals**
- Nodes, topics, publishers, and subscribers
- Real-time message passing at 10-100 Hz
- Building sensor data pipelines

### 🤖 **Robot Modeling with URDF**
- Describing robot morphology (links and joints)
- Visualizing robots in RViz2
- Creating humanoid robot models

### ⚙️ **Services & Request-Response**
- Synchronous communication patterns
- When to use topics vs services
- Building control APIs

---

## Module Structure

This module has **7 chapters** organized into 3 learning journeys:

### Chapter 1.1: Introduction to ROS 2 and Physical AI
Get oriented with ROS 2, install Humble, and run your first robot simulation.

### Chapter 1.2: Your First ROS 2 Node - Publishers & Subscribers
Create Python nodes that send and receive messages using the publish-subscribe pattern.

### Chapter 1.3: Custom Messages and Data Structures
Design custom message types for sensor data and build packages with colcon.

### Chapter 1.4: Services and Request-Response Patterns
Implement synchronous communication for robot commands and configuration.

### Chapter 1.5: Robot Descriptions with URDF
Model robots using URDF (Unified Robot Description Format) with links and joints.

### Chapter 1.6: Visualizing Robots in RViz2
Load robot models, visualize TF trees, and animate with joint state publishers.

### Chapter 1.7: Module 1 Mini-Project
Build a sensor tower that publishes temperature, humidity, and light data with monitoring dashboard.

---

## Prerequisites

- **Python 3.10+**: Basic programming knowledge
- **Ubuntu 22.04** (or WSL2 on Windows): Linux command line familiarity
- **3GB free disk space**: For ROS 2 Humble installation
- **No prior robotics experience required!**

---

## Learning Outcomes

By the end of this module, you will:

✅ **Understand** the ROS 2 graph model (nodes, topics, services)
✅ **Create** Python nodes that publish and subscribe to topics
✅ **Design** custom message types for sensor data
✅ **Build** URDF robot descriptions for humanoids
✅ **Visualize** robots in RViz2 with TF trees
✅ **Debug** ROS 2 systems with CLI tools (ros2 topic, ros2 node, rqt_graph)

---

## Why ROS 2?

**ROS 2 powers the robotics industry:**
- 🏭 **Industrial**: Boston Dynamics Spot, ABB robots, warehouse automation
- 🚗 **Automotive**: Autonomous vehicles, ADAS testing
- 🏠 **Consumer**: Home robots, companion robots
- 🚀 **Research**: NASA Mars rovers, university robotics labs

**Key advantages over ROS 1:**
- Real-time capable (DDS middleware)
- Secure (encrypted communication)
- Cross-platform (Linux, Windows, macOS)
- Production-ready (used in commercial robots)

---

## Quick Start

**Ready to begin?** Start with [Chapter 1.1: Introduction to ROS 2](./chapter-1-1-introduction)

Or jump to a specific topic:
- [📡 Chapter 1.2: Publishers & Subscribers](./chapter-1-2-pubsub)
- [🤖 Chapter 1.5: URDF Robot Modeling](./chapter-1-5-urdf)
- [👁️ Chapter 1.6: RViz2 Visualization](./chapter-1-6-rviz)

---

**Estimated Time**: 12 hours total
**Difficulty**: Beginner (no robotics background needed)
**Next Module**: [Module 2: Gazebo Simulation](../module-2/)
