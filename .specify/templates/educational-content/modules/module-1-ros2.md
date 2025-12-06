# Module 1 Overlay: The Robotic Nervous System (ROS 2)

**Instructions**: Combine this with `base-module-prompt.md` to create the complete
Module 1 specification prompt. This overlay pre-fills module-specific details and
provides 2 complete example chapters.

---

## Module Information (PRE-FILLED)

- **Module Number**: 1
- **Module Title**: The Robotic Nervous System (ROS 2)
- **Estimated Duration**: 12 hours over 4 weeks (3 hours/week)
- **Prerequisites**:
  - Basic Python programming (functions, classes, imports)
  - Command-line interface familiarity (cd, ls, running scripts)
  - Ubuntu/Linux basics OR Windows WSL2
  - No prior robotics or ROS experience required
- **Target Audience**: Software developers, AI engineers, and robotics enthusiasts
  new to ROS 2 who want to build Physical AI applications with humanoid robots

## Module Description (PRE-FILLED)

ROS 2 (Robot Operating System 2) is the middleware that powers modern robotics,
from research humanoids to commercial autonomous systems. Unlike traditional
software where everything runs in one process, ROS 2 enables distributed
architectures where sensors, AI models, and actuators communicate as independent
nodes over a robust message-passing system.

This module introduces the ROS 2 graph model: nodes publish and subscribe to topics,
call services for request-response patterns, and describe robot morphology using
URDF (Unified Robot Description Format). You'll learn to build pub/sub systems for
real-time sensor streaming, create custom message types for structured data, and
visualize robot models in RViz2. By module's end, you'll have a working
understanding of how AI "brains" control physical "bodies" through ROS 2.

**Key Focus**: Communication patterns (publish-subscribe, services), robot modeling
(URDF), visualization (RViz2), and the foundation for all subsequent modules
(simulation, navigation, voice control).

## Module Learning Goals (PRE-FILLED)

1. **Understand**: ROS 2 graph architecture (nodes, topics, services, actions) and
   how DDS middleware enables real-time, distributed robotics systems
2. **Apply**: Publish-subscribe pattern to stream sensor data between nodes using
   standard and custom message types
3. **Analyze**: Message flow and system behavior using ros2 CLI tools (node list,
   topic echo, rqt_graph)
4. **Create**: URDF robot descriptions for humanoid robots and visualize them in
   RViz2 for simulation readiness

---

## Learning Journeys (PRE-FILLED)

### Learning Journey 1: ROS 2 Communication Fundamentals (Priority: P1)

**Narrative**: Learners begin by observing ROS 2 in action through the turtlesim
demo, where they identify nodes and topics using CLI tools. They progress to
modifying existing publisher code to change message content, then create their own
talker/listener node pairs from scratch. The journey culminates in designing custom
message types (.msg files) for specific sensor data like IMU (Inertial Measurement
Unit) or LiDAR scans, understanding how structured data flows through the graph.

**Why this priority**: This is the foundation of all ROS 2 development. Without
understanding publish-subscribe communication, learners cannot progress to services,
actions, robot control, or integration with AI models. Every subsequent module
assumes mastery of pub/sub.

**Independent Validation**: Learner can create a Python ROS 2 node that publishes
custom sensor data to a topic, subscribe to it in another terminal using
`ros2 topic echo`, and visualize the complete message flow graph using `rqt_graph`
showing publisher, topic, and subscriber relationships.

**Learning Milestones**:

1. **Given** ROS 2 Humble installed and sourced, **When** running
   `ros2 run turtlesim turtlesim_node` and using `ros2 node list`, **Then**
   learner can identify the `/turtlesim` node and list its topics with
   `ros2 topic list`

2. **Given** template talker.py code that publishes "Hello World", **When**
   modifying the string to "Custom Message: [timestamp]", **Then** learner can
   observe the updated messages with `ros2 topic echo /chatter`

3. **Given** understanding of std_msgs/String, **When** creating a custom .msg file
   with fields like `int32 sensor_id`, `float64 temperature`, **Then** learner can
   build the package, publish custom messages, and verify structure with
   `ros2 topic echo`

4. **Given** multiple nodes publishing and subscribing, **When** running
   `rqt_graph`, **Then** learner can identify all nodes, topics, message flow
   directions, and diagnose missing connections (e.g., topic name mismatches)

### Learning Journey 2: Robot Descriptions with URDF (Priority: P2)

**Narrative**: Learners start by examining existing URDF files for simple robots
(e.g., a two-wheeled rover), understanding the XML structure of links (physical
parts) and joints (connections). They modify link properties like size and color to
see visual changes in RViz2. Next, they create a simple articulated robot (arm with
2-3 joints) from scratch, defining coordinate frames and joint types (revolute,
prismatic). The journey culminates in adapting a template for a humanoid robot with
torso, arms, legs, and head, preparing for Module 2's simulation.

**Why this priority**: URDF is essential for simulation in Gazebo (Module 2) and
Isaac (Module 3). While not as foundational as pub/sub, it's required before any
simulated robot control. P2 priority allows learners to master communication first,
then tackle robot modeling.

**Independent Validation**: Learner can create a URDF file for a humanoid robot
with at least 10 links (torso, head, 2 arms, 2 legs, 4 wheels/feet) and
corresponding joints, load it in RViz2, and successfully visualize all links with
correct parent-child relationships and coordinate frames.

**Learning Milestones**:

1. **Given** an existing URDF file for a simple robot, **When** modifying a link's
   `<visual>` geometry from box to cylinder and changing color, **Then** learner
   can reload in RViz2 and observe the visual changes

2. **Given** understanding of `<link>` and `<joint>` tags, **When** creating a URDF
   for a 2-joint robotic arm (base + link1 + link2), **Then** learner can define
   revolute joints, set joint limits, and visualize rotation in RViz2

3. **Given** a humanoid template with torso defined, **When** adding `<link>` tags
   for left/right arms and legs with appropriate `<joint>` connections, **Then**
   learner can load the model and verify all links appear in RViz2's TF tree

4. **Given** a complete URDF, **When** publishing joint states via a node, **Then**
   learner can animate the robot in RViz2 (e.g., arm raising, leg moving)

### Learning Journey 3: Services for Command-Response Patterns (Priority: P2)

**Narrative**: After mastering pub/sub (continuous data streams), learners explore
services for one-time request-response interactions. They begin by calling existing
services like `/spawn` in turtlesim to add new turtles. Next, they create a simple
service server that performs a calculation (e.g., add two integers) and a client
that calls it. Finally, they design a robot control service (e.g., "move to
position" or "set motor speed") that returns success/failure, understanding when to
use services vs topics.

**Why this priority**: Services complement topics and are common in robot control
(e.g., Nav2's navigation services). However, they're less fundamental than pub/sub,
hence P2. Many simple robots can function with topics alone, but services enable
cleaner command patterns.

**Independent Validation**: Learner can create a service server node that accepts a
request (e.g., target position for a robot), performs validation (e.g., position in
bounds), and returns a response (success or error message). They can call this
service from a separate client node or CLI using `ros2 service call`.

**Learning Milestones**:

1. **Given** turtlesim running, **When** calling `ros2 service call /spawn
   turtlesim/srv/Spawn "{x: 5.0, y: 5.0, theta: 0.0}"`, **Then** learner observes a
   new turtle spawn at the specified coordinates

2. **Given** template service server code (AddTwoInts), **When** running the server
   and calling it with `ros2 service call /add_two_ints example_interfaces/srv/
   AddTwoInts "{a: 5, b: 3}"`, **Then** learner receives response with sum: 8

3. **Given** understanding of srv file structure, **When** creating a custom .srv
   file (e.g., `SetMotorSpeed.srv` with `int32 motor_id, float64 speed` →
   `bool success, string message`), **Then** learner can build, implement server,
   and call successfully

4. **Given** a scenario requiring both topics and services, **When** analyzing
   requirements (e.g., continuous sensor stream vs one-time configuration), **Then**
   learner can justify which pattern to use and explain trade-offs

---

## Chapter Breakdown

### Chapter 1.1: Introduction to ROS 2 and Physical AI (COMPLETE EXAMPLE)

**Duration**: 2 hours
**Prerequisites**: None (module entry point)

#### Learning Objectives (Bloom's Taxonomy)

- **Remember**: Define ROS 2, node, topic, message, Physical AI, and middleware
- **Understand**: Explain why Physical AI requires middleware like ROS 2 and how it
  differs from ROS 1 (real-time, security, multi-platform)
- **Apply**: Install ROS 2 Humble on Ubuntu 22.04 and run the turtlesim demo to
  observe nodes and topics

#### Content Outline

1. **Introduction** (30 min)
   - **What is Physical AI?**: AI systems that perceive and act in the physical
     world (contrast with digital AI like chatbots or recommender systems)
   - **Real-world Physical AI examples**:
     - Humanoid robots (Tesla Optimus, Figure 01, Boston Dynamics Atlas)
     - Autonomous vehicles (Waymo, Tesla FSD, robotaxis)
     - Warehouse automation (Amazon Proteus, Locus robots)
     - Surgical robots (da Vinci system)
   - **Why middleware matters**: Physical AI requires coordinating:
     - Sensors (cameras, LiDAR, IMU) producing continuous data streams
     - AI models (computer vision, planning, NLP) processing data
     - Actuators (motors, grippers) executing commands
     - All running as distributed processes, often on different computers
   - **Analogy**: ROS 2 is like a "nervous system" connecting brain (AI) to
     sensors (eyes, ears) and muscles (actuators)

2. **Deep Dive** (45 min)
   - **ROS 2 Architecture**:
     - **Nodes**: Independent processes (e.g., camera_driver, object_detector,
       motor_controller)
     - **Topics**: Named channels for asynchronous message passing (pub/sub
       pattern)
     - **DDS Middleware**: Data Distribution Service - enables real-time,
       peer-to-peer communication without central broker (unlike ROS 1's roscore)
   - **ROS 1 vs ROS 2 Comparison**:
     - ROS 1: Single master (roscore) - single point of failure, no real-time
       guarantees
     - ROS 2: Peer-to-peer via DDS - robust, real-time capable, supports security
       (encryption)
     - Use case: ROS 1 for research/prototypes, ROS 2 for production and humanoids
   - **The ROS 2 Graph Visualized**:
     - Example: Camera node publishes to `/image_raw` topic → Object detector node
       subscribes, processes, publishes to `/detections` topic → Robot controller
       subscribes and sends motor commands
     - Show graph diagram (see Diagrams section below)
   - **Why ROS 2 for Humanoids**:
     - Real-time control for balance and walking (strict timing requirements)
     - Security for human-robot interaction environments
     - Cross-platform (works on embedded systems, workstations, cloud)

3. **Hands-On Practice** (40 min)
   - **Walkthrough: Install ROS 2 Humble on Ubuntu 22.04**
     - Use provided installation script (see Code Examples)
     - Source setup.bash in .bashrc for auto-loading
   - **Exercise 1: Run turtlesim and explore with CLI tools**
     - Run: `ros2 run turtlesim turtlesim_node`
     - In another terminal: `ros2 node list` (identify /turtlesim node)
     - Run: `ros2 topic list` (see /turtle1/cmd_vel, /turtle1/pose, etc.)
     - Run: `ros2 topic echo /turtle1/pose` (observe real-time pose updates)
   - **Exercise 2: Control turtle with keyboard, observe message flow**
     - Run: `ros2 run turtlesim turtle_teleop_key`
     - Drive turtle with arrow keys
     - Run: `ros2 topic echo /turtle1/cmd_vel` to see velocity commands
     - **Reflection question**: What message type is /cmd_vel? Use
       `ros2 topic info /turtle1/cmd_vel` to find out

4. **Summary & Transition** (5 min)
   - **Key takeaways**:
     - Physical AI requires distributed systems; ROS 2 is the industry standard
       middleware
     - Nodes communicate via topics (pub/sub) and services (request/response)
     - DDS middleware makes ROS 2 real-time and robust (vs ROS 1)
     - CLI tools (node list, topic echo, topic info) are essential for debugging
   - **Next chapter**: Building your first publisher-subscriber node pair in Python

#### Code Examples

**Example 1: ROS 2 Humble Installation Script**

- **Filename**: `book_frontend/static/examples/module-1/install_ros2_humble.sh`
- **Language**: Bash
- **Type**: Complete example (tested on Ubuntu 22.04)
- **Purpose**: Automates ROS 2 Humble installation (locale setup, apt repos, package
  install)
- **Prerequisites**: Ubuntu 22.04 LTS, sudo access, internet connection
- **Expected Output**:
  ```bash
  locale: en_US.UTF-8
  Hit:1 http://packages.ros.org/ros2/ubuntu jammy InRelease
  Reading package lists... Done
  Building dependency tree... Done
  The following NEW packages will be installed:
    ros-humble-desktop python3-argcomplete
  ...
  ROS 2 Humble installation complete!
  Run: source /opt/ros/humble/setup.bash
  Verify: ros2 --version
  ```
- **Testing**: After running script, execute `ros2 --version` → should output
  `ros2 cli version: 0.25.x`
- **Common Issues**:
  - Locale errors: Script sets en_US.UTF-8; if different locale needed, modify
    locale-gen line
  - GPG key errors: Script adds ROS 2 apt key; if expired, check
    docs.ros.org/en/humble

**Example 2: Sourcing ROS 2 in .bashrc**

- **Filename**: `book_frontend/static/examples/module-1/bashrc_ros2_setup.sh`
- **Language**: Bash
- **Type**: Complete example (snippet to add to .bashrc)
- **Purpose**: Auto-sources ROS 2 environment in every new terminal
- **Prerequisites**: ROS 2 Humble installed at `/opt/ros/humble`
- **Expected Output**: After adding to .bashrc and opening new terminal,
  `echo $ROS_DISTRO` outputs `humble`
- **Testing**:
  ```bash
  cat >> ~/.bashrc << 'EOF'
  # ROS 2 Humble setup
  source /opt/ros/humble/setup.bash
  export ROS_DOMAIN_ID=0  # Change if multiple ROS 2 systems on network
  EOF
  source ~/.bashrc
  echo $ROS_DISTRO  # Should print: humble
  ```

#### Diagrams & Media

**Diagram 1: ROS 2 Graph Conceptual Model**

- **Filename**: `static/img/module-1/chapter-1-1/ros2-graph-concept.svg`
- **Type**: SVG (created in draw.io)
- **Alt Text**: "Diagram showing ROS 2 graph with three nodes: camera_node publishing
  to /image_raw topic (solid arrow), object_detector_node subscribing to image_raw
  and publishing to /detections topic (two arrows in/out), and robot_controller_node
  subscribing to detections and publishing to /cmd_vel topic. Topics shown as
  rounded rectangles, nodes as circles, arrows indicate message flow direction."
- **Purpose**: Visualizes pub/sub pattern conceptually before hands-on CLI
  exploration. Shows multi-hop message flow (sensor → AI → actuator).
- **Size**: ~30KB (simple 3-node graph)
- **Source**: `static/img/module-1/chapter-1-1/ros2-graph-concept.drawio` (editable)

**Diagram 2: ROS 1 vs ROS 2 Architecture Comparison**

- **Filename**: `static/img/module-1/chapter-1-1/ros1-vs-ros2-architecture.svg`
- **Type**: SVG
- **Alt Text**: "Side-by-side comparison diagram. Left side shows ROS 1 with central
  roscore node connected to three other nodes in star topology, labeled 'Single
  Point of Failure'. Right side shows ROS 2 with four nodes in mesh topology, all
  directly connected via DDS, labeled 'Peer-to-Peer, No Central Broker'. Arrows
  indicate communication paths."
- **Purpose**: Illustrates key architectural difference driving ROS 2's advantages
  (robustness, real-time capability)
- **Size**: ~40KB
- **Source**: `static/img/module-1/chapter-1-1/ros1-vs-ros2-architecture.drawio`

**Image 1: Turtlesim Demo Screenshot**

- **Filename**: `static/img/module-1/chapter-1-1/turtlesim-demo-screenshot.png`
- **Type**: PNG (screenshot, optimized)
- **Alt Text**: "Screenshot of turtlesim window showing a blue background with a
  turtle icon in the center. The turtle has drawn a colorful curved path as it moved
  across the screen."
- **Purpose**: Gives learners a visual preview of what to expect when running the
  demo
- **Size**: ~80KB (optimized PNG)

#### Assessments

**Formative Assessments** (during chapter):

**Self-Check Questions**:

1. **What is Physical AI?**
   - A) AI that only works on physical computers (not cloud)
   - B) AI systems that perceive and act in the physical world ✓
   - C) AI for physics simulations
   - D) AI running on robots without any software

2. **Why is DDS middleware important in ROS 2?**
   - A) It makes ROS 2 slower but more secure
   - B) It enables peer-to-peer communication without a central broker ✓
   - C) It requires more powerful computers
   - D) It only works on Linux

3. **True or False: In ROS 2, topics are used for request-response patterns.**
   - False (Topics are pub/sub; services are request-response) ✓

**Code Debugging Exercise**:

- **Scenario**: "You run `ros2 topic list` but see no topics even though turtlesim
  is running. What might be wrong?"
- **Answer**: ROS_DOMAIN_ID mismatch between terminals, or forgot to source
  setup.bash in the terminal running topic list

**Summative Assessments** (end of chapter):

**Conceptual Quiz** (5 multiple-choice questions):

1. What is the primary role of middleware in Physical AI systems?
2. Which of the following is NOT an advantage of ROS 2 over ROS 1?
3. What command shows all running nodes?
4. What does `ros2 topic echo /turtle1/pose` display?
5. In the pub/sub pattern, can multiple nodes subscribe to the same topic?

**Topics Covered**: Physical AI definition, ROS 2 vs ROS 1, DDS middleware, CLI
tools, pub/sub basics

**Expected Pass Rate**: 90% (straightforward if chapter completed; installation
section well-documented)

**Coding Challenge**:

**Task**: Install ROS 2 Humble, run turtlesim, and use CLI tools to identify:
- The node name running turtlesim
- The topic that turtle position is published to
- The message type of that topic

**Submission**: Screenshot of terminal showing:
1. `ros2 node list` output
2. `ros2 topic list` output
3. `ros2 topic info /turtle1/pose` output showing message type

**Rubric**:
- Installation successful (turtlesim runs): 30%
- Correct node identification: 20%
- Correct topic identification: 20%
- Correct message type: 20%
- Screenshot clarity and completeness: 10%

**Expected Pass Rate**: 85% (technical setup issues may affect some learners on
non-standard systems)

#### Accessibility Checklist (WCAG 2.1 AA Compliance)

- [x] All code blocks have language identifiers (`bash`, `python`)
- [x] All diagrams have descriptive alt text explaining content, not just "diagram
      of ROS 2"
- [x] Heading hierarchy: H4 for Learning Objectives, H4 for Content Outline sections
      (H1=Module, H2=Major sections, H3=Chapters, H4=Subsections)
- [x] Installation steps are keyboard-accessible (all terminal commands, no
      GUI-only instructions)
- [x] Diagrams use shapes and labels, not color alone, to convey information

---

### Chapter 1.2: Your First ROS 2 Node - Publishers & Subscribers (COMPLETE EXAMPLE)

**Duration**: 2.5 hours
**Prerequisites**: Chapter 1.1 (ROS 2 Humble installed and sourced)

#### Learning Objectives (Bloom's Taxonomy)

- **Remember**: Define publisher, subscriber, rclpy, and message type in ROS 2
  context
- **Understand**: Explain the publish-subscribe pattern and when it's preferable to
  direct function calls
- **Apply**: Create a Python ROS 2 node that publishes string messages to a topic
  and another node that subscribes to it
- **Analyze**: Use `rqt_graph` to visualize publisher-subscriber relationships and
  identify missing connections

#### Content Outline

1. **Introduction** (20 min)
   - **Why publish-subscribe?**: Decoupling producers and consumers
     - Example: Camera node publishes images; multiple nodes can subscribe (object
       detector, display, logger) without camera knowing about them
     - Contrast with direct function calls: tight coupling, hard to add new consumers
   - **Real-world analogy**: YouTube channels (publishers) and subscribers. Channel
     doesn't track who subscribes; subscribers get notified of new videos; many
     subscribers possible.
   - **ROS 2 pub/sub components**:
     - **Publisher**: Node that sends messages to a topic
     - **Subscriber**: Node that receives messages from a topic
     - **Topic**: Named channel (e.g., /sensor_data)
     - **Message Type**: Data structure (e.g., std_msgs/String)

2. **Deep Dive** (50 min)
   - **rclpy Library**: Python client library for ROS 2
     - `rclpy.init()` and `rclpy.spin()` for node lifecycle
     - `Node` class as base for all ROS 2 nodes
   - **Creating a Publisher**:
     - `self.create_publisher(msg_type, topic_name, queue_size)`
     - **Queue size**: Buffer for messages when subscriber lags (typically 10)
   - **Creating a Subscriber**:
     - `self.create_subscription(msg_type, topic_name, callback, queue_size)`
     - **Callback function**: Executed when message received
   - **Message Types**:
     - Standard messages: `std_msgs/String`, `std_msgs/Int32`, `geometry_msgs/Twist`
     - Importing: `from std_msgs.msg import String`
   - **Publishing Workflow**:
     1. Create publisher in node's `__init__`
     2. Create timer to trigger publishing at regular interval
     3. In timer callback, create message, populate data, call `publisher.publish(msg)`
   - **Subscribing Workflow**:
     1. Create subscription in node's `__init__`
     2. Define callback function to handle received messages
     3. Callback runs asynchronously when messages arrive

3. **Hands-On Practice** (70 min)
   - **Walkthrough: Create talker node (publisher)**
     - Create package: `ros2 pkg create --build-type ament_python py_pubsub`
     - Write `talker.py` (see Code Examples)
     - Build with `colcon build`, source `install/setup.bash`
     - Run: `ros2 run py_pubsub talker`
   - **Exercise 1: Create listener node (subscriber)**
     - Write `listener.py` that subscribes to /chatter topic (template provided)
     - Run in separate terminal, observe received messages
   - **Exercise 2: Visualize with rqt_graph**
     - Run `rqt_graph` while talker and listener running
     - Identify nodes, topic, message flow direction
     - **Challenge**: Change topic name in talker to /chatter2, observe listener no
       longer receives messages (topic name mismatch debugging)

4. **Summary & Transition** (10 min)
   - **Key takeaways**:
     - Pub/sub decouples nodes; publishers and subscribers don't need to know about
       each other
     - rclpy provides `create_publisher` and `create_subscription` methods
     - Topics are strongly typed (message type must match)
     - rqt_graph is essential for debugging communication issues
   - **Next chapter**: Creating custom message types for structured sensor data

#### Code Examples

**Example 1: Talker Node (Publisher)**

- **Filename**: `book_frontend/static/examples/module-1/chapter-1-2/talker.py`
- **Language**: Python
- **Type**: Complete example (tested with ROS 2 Humble)
- **Purpose**: Demonstrates publishing string messages to /chatter topic at 1 Hz
- **Prerequisites**: ROS 2 Humble, py_pubsub package created
- **Expected Output**:
  ```
  [INFO] [talker]: Publishing: "Hello World: 0"
  [INFO] [talker]: Publishing: "Hello World: 1"
  [INFO] [talker]: Publishing: "Hello World: 2"
  ...
  ```
- **Testing**: Run `ros2 topic echo /chatter` in another terminal → should see
  messages
- **Code**:
  ```python
  import rclpy
  from rclpy.node import Node
  from std_msgs.msg import String


  class MinimalPublisher(Node):
      def __init__(self):
          super().__init__('talker')
          self.publisher_ = self.create_publisher(String, 'chatter', 10)
          self.timer = self.create_timer(1.0, self.timer_callback)  # 1 Hz
          self.i = 0

      def timer_callback(self):
          msg = String()
          msg.data = f'Hello World: {self.i}'
          self.publisher_.publish(msg)
          self.get_logger().info(f'Publishing: "{msg.data}"')
          self.i += 1


  def main(args=None):
      rclpy.init(args=args)
      node = MinimalPublisher()
      rclpy.spin(node)
      node.destroy_node()
      rclpy.shutdown()


  if __name__ == '__main__':
      main()
  ```

**Example 2: Listener Node (Subscriber)**

- **Filename**: `book_frontend/static/examples/module-1/chapter-1-2/listener.py`
- **Language**: Python
- **Type**: Complete example
- **Purpose**: Subscribes to /chatter topic and logs received messages
- **Prerequisites**: Talker node running
- **Expected Output**:
  ```
  [INFO] [listener]: I heard: "Hello World: 0"
  [INFO] [listener]: I heard: "Hello World: 1"
  ...
  ```
- **Testing**: Run while talker is running → should see messages logged
- **Code**:
  ```python
  import rclpy
  from rclpy.node import Node
  from std_msgs.msg import String


  class MinimalSubscriber(Node):
      def __init__(self):
          super().__init__('listener')
          self.subscription = self.create_subscription(
              String, 'chatter', self.listener_callback, 10)

      def listener_callback(self, msg):
          self.get_logger().info(f'I heard: "{msg.data}"')


  def main(args=None):
      rclpy.init(args=args)
      node = MinimalSubscriber()
      rclpy.spin(node)
      node.destroy_node()
      rclpy.shutdown()


  if __name__ == '__main__':
      main()
  ```

**Example 3: Package setup.py Configuration**

- **Filename**: `book_frontend/static/examples/module-1/chapter-1-2/setup.py`
- **Language**: Python
- **Type**: Complete example (setup.py for ament_python package)
- **Purpose**: Configures entry points for talker and listener executables
- **Prerequisites**: None (used during package creation)
- **Expected Output**: After `colcon build`, can run `ros2 run py_pubsub talker`
- **Code** (key section):
  ```python
  entry_points={
      'console_scripts': [
          'talker = py_pubsub.talker:main',
          'listener = py_pubsub.listener:main',
      ],
  },
  ```

#### Diagrams & Media

**Diagram 1: Publish-Subscribe Pattern Flow**

- **Filename**: `static/img/module-1/chapter-1-2/pubsub-pattern-flow.svg`
- **Type**: SVG (Mermaid diagram)
- **Alt Text**: "Sequence diagram showing publisher node creating message, publishing
  to /chatter topic (represented as central queue), and subscriber node receiving
  message from topic. Arrows show message flow from publisher to topic to subscriber
  with timestamps."
- **Purpose**: Illustrates asynchronous nature of pub/sub (publisher doesn't wait
  for subscriber)
- **Size**: ~25KB

**Diagram 2: rqt_graph Output Example**

- **Filename**: `static/img/module-1/chapter-1-2/rqt-graph-talker-listener.png`
- **Type**: PNG (screenshot)
- **Alt Text**: "Screenshot of rqt_graph showing two oval nodes labeled /talker and
  /listener connected by an arrow flowing through a rectangular topic box labeled
  /chatter. Arrow points from talker to chatter to listener, indicating message
  flow direction."
- **Purpose**: Previews what learners will see in rqt_graph during exercise
- **Size**: ~120KB (optimized screenshot)

#### Assessments

**Formative Assessments**:

**Self-Check Questions**:

1. **What does `create_publisher(String, 'chatter', 10)` return?**
   - Answer: A publisher object that can send String messages to /chatter topic

2. **Why use a timer in the publisher node?**
   - Answer: To publish messages at regular intervals (e.g., 1 Hz) without blocking

3. **True or False: A subscriber callback blocks the main thread while processing.**
   - False (callbacks run asynchronously in rclpy.spin())

**Code Debugging Exercise**:

- **Broken Code**: Listener doesn't receive messages
  ```python
  self.subscription = self.create_subscription(
      String, 'chatter2', self.listener_callback, 10)  # Wrong topic name!
  ```
- **Question**: Why doesn't the listener receive any messages?
- **Answer**: Topic name mismatch ('chatter2' vs 'chatter')

**Summative Assessments**:

**Conceptual Quiz** (7 questions):

1. What is the purpose of the queue_size parameter in create_publisher?
2. In pub/sub, does the publisher need to know which nodes are subscribing?
3. What tool visualizes ROS 2 node and topic relationships?
4. What happens if a subscriber is slower than the publisher?
5. Can multiple nodes publish to the same topic? Can multiple subscribe?
6. What library provides Python bindings for ROS 2?
7. What method makes a node process callbacks?

**Expected Pass Rate**: 85%

**Coding Challenge**:

**Task**: Create a publisher node that publishes your name to topic /student_name at
2 Hz, and a subscriber node that receives and logs it.

**Requirements**:
1. Publisher logs what it's publishing
2. Subscriber logs what it receives
3. Both run simultaneously
4. Screenshot of both terminals + rqt_graph

**Rubric**:
- Publisher implementation (correct message type, topic, rate): 30%
- Subscriber implementation (correct callback): 25%
- Both nodes run without errors: 20%
- Correct rqt_graph visualization: 15%
- Clean code and logging: 10%

**Expected Pass Rate**: 75% (debugging package setup and topic names can be tricky
for beginners)

#### Accessibility Checklist

- [x] Code blocks have `python` and `bash` identifiers
- [x] Diagrams have detailed alt text explaining message flow
- [x] All commands are terminal-based (keyboard accessible)
- [x] Color-blind friendly: rqt_graph uses shapes (ovals, rectangles) + labels, not
      just color

---

### Remaining Chapters (TEMPLATE STRUCTURE with Suggested Titles)

**Chapter 1.3: Custom Messages and Data Structures** (2 hours)

- **Learning Objectives**: Create custom .msg files for structured sensor data
  (e.g., IMU with orientation, angular velocity, linear acceleration), build package
  with message definitions, publish and subscribe to custom messages
- **Key Concepts**: .msg file syntax, field types (int32, float64, string, arrays),
  colcon build for message generation
- **Code Example**: IMU message publisher, custom message subscriber
- **Assessment**: Create custom message for GPS data (latitude, longitude, altitude,
  timestamp)

**Chapter 1.4: Services and Request-Response Patterns** (2 hours)

- **Learning Objectives**: Understand when to use services vs topics, create service
  server and client, handle synchronous request-response
- **Key Concepts**: .srv files, service server (`create_service`), service client
  (`create_client`), blocking vs asynchronous calls
- **Code Example**: AddTwoInts service, motor speed control service
- **Assessment**: Implement a "robot reset" service that returns success/failure

**Chapter 1.5: Robot Descriptions with URDF** (2.5 hours)

- **Learning Objectives**: Understand URDF XML structure (links, joints), create
  simple robot model, load in RViz2
- **Key Concepts**: `<link>`, `<joint>`, coordinate frames (TF), visual vs collision
  geometry, joint types (revolute, prismatic, fixed)
- **Code Example**: Two-wheeled robot URDF, robotic arm URDF
- **Assessment**: Create URDF for a humanoid torso with head and two arms

**Chapter 1.6: Visualizing Robots in RViz2** (1.5 hours)

- **Learning Objectives**: Load URDF in RViz2, visualize TF tree, publish joint
  states to animate robots
- **Key Concepts**: RViz2 panels (Add display, TF, RobotModel), joint_state_publisher,
  coordinate frame visualization
- **Code Example**: Launch file for RViz2 with URDF, joint state publisher node
- **Assessment**: Visualize Chapter 1.5's humanoid model and animate one arm raising

**Chapter 1.7: Putting It All Together - Module 1 Mini-Project** (1.5 hours)

- **Project**: Build a simulated "sensor tower" that publishes temperature, humidity,
  and light level data to separate topics, and a "monitor" node that subscribes to
  all three and logs combined readings
- **Requirements**: Custom messages for each sensor type, use of rqt_graph to verify
  connections, visualization in RViz2 (tower model)
- **Assessment**: Working system with all nodes communicating, rqt_graph screenshot,
  brief written reflection on when to use topics vs services

---

## Core Concepts & Terminology (PRE-FILLED)

- **Term**: ROS 2 Node
- **Definition**: An independent executable process that performs computation and
  communicates with other nodes via topics, services, or actions
- **Analogy**: Like a microservice in a distributed system—each has a specific job
  (e.g., camera_driver reads sensor, object_detector runs AI model, motor_controller
  commands actuators)
- **First Introduced**: Chapter 1.1
- **Related Terms**: Topic, Publisher, Subscriber, rclpy, rclcpp
- **Code Example**: `class MinimalNode(Node):` in talker.py

---

- **Term**: Topic
- **Definition**: Named channel for asynchronous message passing between nodes using
  publish-subscribe pattern
- **Analogy**: Like a radio frequency—publishers broadcast, subscribers tune in;
  multiple subscribers can listen simultaneously, messages are one-way
- **First Introduced**: Chapter 1.1
- **Related Terms**: Publisher, Subscriber, Message Type, rqt_graph
- **Code Example**: `'/chatter'` in create_publisher call

---

- **Term**: Publisher
- **Definition**: A node component that sends messages to a topic at regular or
  event-driven intervals
- **Analogy**: Like a news agency publishing articles to a wire service
- **First Introduced**: Chapter 1.2
- **Related Terms**: Subscriber, Topic, Message Type, Queue Size
- **Code Example**: `self.publisher_ = self.create_publisher(String, 'chatter', 10)`

---

- **Term**: Subscriber
- **Definition**: A node component that receives messages from a topic via a callback
  function
- **Analogy**: Like a news app that displays articles from a wire service
- **First Introduced**: Chapter 1.2
- **Related Terms**: Publisher, Topic, Callback, Message Type
- **Code Example**: `self.create_subscription(String, 'chatter', callback, 10)`

---

- **Term**: Message Type
- **Definition**: Data structure definition for messages sent over topics (e.g.,
  String, Int32, Twist, custom types)
- **Analogy**: Like a contract specifying what fields a JSON object must have
- **First Introduced**: Chapter 1.2
- **Related Terms**: .msg file, std_msgs, geometry_msgs, sensor_msgs
- **Code Example**: `from std_msgs.msg import String`

---

- **Term**: rclpy
- **Definition**: Python client library for ROS 2, providing node lifecycle, pub/sub,
  services, timers
- **Analogy**: Like React for web development—abstracts low-level details, provides
  high-level API
- **First Introduced**: Chapter 1.2
- **Related Terms**: rclcpp (C++ equivalent), Node class, spin(), init()
- **Code Example**: `import rclpy`

---

- **Term**: Service
- **Definition**: Synchronous request-response communication pattern between nodes
  (one client requests, one server responds)
- **Analogy**: Like a REST API call—client sends request, waits for response
- **First Introduced**: Chapter 1.4
- **Related Terms**: .srv file, Service Server, Service Client, Topic (async
  alternative)
- **Code Example**: `self.create_service(AddTwoInts, 'add_two_ints', callback)`

---

- **Term**: URDF (Unified Robot Description Format)
- **Definition**: XML format for describing robot morphology: links (physical parts),
  joints (connections), visual/collision geometry
- **Analogy**: Like a blueprint for a robot—specifies parts and how they connect
- **First Introduced**: Chapter 1.5
- **Related Terms**: Link, Joint, RViz2, xacro, SDF (Gazebo format)
- **Code Example**: `<link name="base_link"> <visual> <geometry> <box size="0.6 0.3
  0.2"/> </geometry> </visual> </link>`

---

- **Term**: Link (URDF)
- **Definition**: A rigid body in a robot model (e.g., chassis, wheel, arm segment)
  with visual, collision, and inertial properties
- **Analogy**: Like a bone in a skeleton
- **First Introduced**: Chapter 1.5
- **Related Terms**: Joint, URDF, Visual Geometry, Collision Geometry
- **Code Example**: `<link name="left_wheel"> ... </link>`

---

- **Term**: Joint (URDF)
- **Definition**: Connection between two links defining their relative motion (types:
  fixed, revolute, prismatic, continuous)
- **Analogy**: Like a hinge or slider between two parts
- **First Introduced**: Chapter 1.5
- **Related Terms**: Link, URDF, Parent Link, Child Link, Joint Limits
- **Code Example**: `<joint name="left_wheel_joint" type="continuous"> <parent
  link="base_link"/> <child link="left_wheel"/> </joint>`

---

- **Term**: RViz2
- **Definition**: 3D visualization tool for ROS 2—displays robot models, sensor data
  (point clouds, images), coordinate frames (TF)
- **Analogy**: Like Unity or Unreal Engine's scene view, but for robot debugging
- **First Introduced**: Chapter 1.6
- **Related Terms**: URDF, TF (Transform), RobotModel Display, Marker
- **Code Example**: `ros2 run rviz2 rviz2` (launch command)

---

- **Term**: DDS (Data Distribution Service)
- **Definition**: OMG standard for real-time, peer-to-peer publish-subscribe
  middleware; ROS 2's communication layer
- **Analogy**: Like WebSockets for browsers, but industrial-strength for robotics
- **First Introduced**: Chapter 1.1
- **Related Terms**: Middleware, QoS (Quality of Service), RTPS, ROS 1 (used custom
  middleware)
- **Code Example**: (Under the hood; users rarely interact directly)

---

[Continue with 2-3 more key terms as needed: colcon, package.xml, QoS, etc.]

---

## Cross-Module Dependencies (PRE-FILLED)

### Within-Module

- **Chapter 1.1** is foundational; MUST precede all other chapters (installs ROS 2,
  introduces core concepts)
- **Chapter 1.2** (Pub/Sub) is prerequisite for:
  - Chapter 1.3 (Custom Messages—extends pub/sub with custom types)
  - Chapter 1.5 (URDF—joint state publishing uses pub/sub)
  - Chapter 1.6 (RViz2—subscribes to joint states and sensor topics)
- **Chapter 1.5** (URDF) is prerequisite for Chapter 1.6 (RViz2 visualizes URDF
  models)
- **Chapter 1.7** (Mini-Project) integrates Chapters 1.1-1.6

**Recommended Sequence**: 1.1 → 1.2 → 1.3 → 1.4 → 1.5 → 1.6 → 1.7 (linear
progression)

### Cross-Module

**What Module 1 Provides for Future Modules**:

- **For Module 2 (Gazebo & Unity - Digital Twin)**:
  - ROS 2 pub/sub for sensor data streaming (Chapter 1.2, 1.3)
  - URDF robot descriptions (Chapter 1.5) - Gazebo loads URDF models
  - Understanding of topics (Gazebo publishes sensor topics, subscribes to motor
    commands)

- **For Module 3 (NVIDIA Isaac - AI-Robot Brain)**:
  - ROS 2 fundamentals (Module 3 uses Isaac ROS, which is ROS 2-based)
  - Services for navigation commands (Chapter 1.4 - Nav2 uses action servers, which
    build on services)
  - URDF (Isaac Sim can import URDF/USD robot models)

- **For Module 4 (VLA - Vision-Language-Action)**:
  - Pub/sub for voice command publishing and robot action topics
  - Services for request-response with LLMs
  - Full ROS 2 graph understanding for integrating voice → LLM → ROS 2 → robot

- **For Module 5 (Capstone - Autonomous Humanoid)**:
  - All Module 1 concepts (complete ROS 2 foundation)

### External Dependencies

**Software**:
- **ROS 2 Humble Hawksbill** (LTS release, supported until 2027)
  - **OS**: Ubuntu 22.04 LTS (primary), also RHEL 9, macOS, Windows 10/11 (via WSL2)
  - **Installation**: Chapter 1.1 covers installation; official docs at
    docs.ros.org/en/humble
- **Python 3.10+** (included with Ubuntu 22.04)
- **colcon** (build tool, installed with ROS 2 Desktop)

**Hardware**:
- **Minimum**: 4GB RAM, 2-core CPU (sufficient for turtlesim and basic nodes)
- **Recommended**: 8GB+ RAM, 4-core CPU (smoother RViz2 performance)
- **GPU**: Not required for Module 1 (simulation in Module 2+ benefits from GPU)

**External Accounts**:
- None required for Module 1

---

## Out of Scope (PRE-FILLED)

### Explicitly NOT Covered in Module 1

- **ROS 2 Actions**: Deferred to Module 3 (Nav2 uses action servers for goal-based
  navigation; more complex than topics/services)
  - **Rationale**: Actions add complexity (preemption, feedback, goals); better
    taught in context of real use case (navigation)

- **ROS 1 and ROS 1 Bridge**: This book focuses exclusively on ROS 2; migration from
  ROS 1 is out of scope
  - **Rationale**: ROS 1 is legacy (end of support 2025 for Noetic); humanoid
    robotics requires ROS 2's real-time capabilities

- **Real Hardware Integration**: Module 1 is simulation and localhost-only; hardware
  interfacing (motor drivers, sensor firmware) covered in Module 4 (VLA) if at all
  - **Rationale**: Educational focus is on ROS 2 concepts; hardware brings
    variability and troubleshooting that distracts from learning

- **Multi-Robot Systems**: Coordinating multiple robots (fleet management,
  multi-robot SLAM) is an advanced topic beyond book scope
  - **Rationale**: Single-robot mastery is prerequisite; multi-robot adds
    distributed systems complexity

- **Security and Encryption**: ROS 2 supports DDS security, but configuration is
  deferred (briefly mentioned in Chapter 1.1 comparison to ROS 1)
  - **Rationale**: Security is production concern; educational environments run on
    isolated networks

- **QoS (Quality of Service) Tuning**: Default QoS profiles used throughout Module 1;
  custom QoS (reliability, history depth) is advanced
  - **Rationale**: Default QoS works for 90% of use cases; tuning is optimization,
    not foundational

- **C++ Development**: All examples use Python (rclpy); C++ (rclcpp) is mentioned but
  not taught
  - **Rationale**: Python is more accessible for AI/ML practitioners; C++ offers
    performance but steeper learning curve

**Overall Rationale**: Module 1 establishes ROS 2 fundamentals—pub/sub, services,
URDF—without overwhelming learners. Advanced topics (actions, security, C++) are
either deferred to later modules or excluded to maintain focus on Physical AI
applications with Python.

---

**Module 1 Overlay Complete**
**Lines**: ~850
**Status**: Ready to combine with base-module-prompt.md for `/sp.specify`
