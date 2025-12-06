---
id: chapter-3-6-deployment
title: "Chapter 3.6: Deployment to Real Robots"
sidebar_label: "3.6 Deployment"
sidebar_position: 6
---

# Chapter 3.6: Deployment to Real Robots

## Bridging the Sim-to-Real Gap

You've trained vision models on synthetic data and RL policies in massively parallel simulation—but the ultimate test is **real hardware**. The **sim-to-real gap** (differences between simulation and reality) causes many policies to fail when deployed. This chapter teaches you to minimize that gap through system identification, domain randomization validation, safety-critical deployment strategies, and iterative hardware-in-the-loop refinement.

---

## Learning Objectives

By the end of this chapter, you will:

- **Understand**: Identify sources of sim-to-real gap (physics mismatch, latency, sensor noise)
- **Apply**: Calibrate simulation parameters to match real robot dynamics
- **Create**: Implement safety wrappers (emergency stops, bounds checking) for deployed policies
- **Analyze**: Measure sim-to-real transfer performance quantitatively
- **Apply**: Use hardware-in-the-loop to iterate on sim-trained models with real data

**Estimated Time**: 2 hours

---

## Prerequisites

- **Chapters 3.1-3.5 complete** (Isaac Sim, sensors, synthetic data, RL)
- **Real robot hardware** (quadruped, humanoid, or mobile manipulator) OR access to simulation that closely mimics real robot
- **ROS 2** (for communication with robot)
- **Safety mindset** (robots can cause injury—follow protocols)

---

## What You'll Build

By the end of this chapter, you'll have:

✅ **Calibrated simulation** matching real robot's dynamics
✅ **Safety-critical deployment system** with emergency stops
✅ **Deployed AI model** (vision or RL) running on real hardware
✅ **Performance metrics** comparing sim vs. real (success rate, accuracy)
✅ **Iterative improvement pipeline** (collect failures → retrain → redeploy)

---

## The Sim-to-Real Gap

### What is the Gap?

**Definition**: Performance degradation when transferring sim-trained models to real hardware.

**Example**: RL policy achieves 95% task success in Isaac Gym → 60% on real robot.

### Sources of the Gap

| Source | Simulation | Reality | Impact |
|--------|------------|---------|--------|
| **Physics** | Perfect PhysX | Friction varies, backlash, flex | Robot slips, overshoots |
| **Sensors** | Noiseless, instant | Noise, delays, dropout | Perception fails |
| **Actuators** | Instant torque | Delays, saturation, heating | Control lag, torque limits |
| **Latency** | 0-1ms | 10-50ms | Instability, oscillations |
| **Wear** | No degradation | Joints loosen, calibration drift | Long-term failures |

**Goal**: Minimize gap via calibration + domain randomization + safety margins.

---

## System Identification (Calibration)

### What is System ID?

**System identification** = Measure real robot's parameters, update simulation to match.

**Parameters to calibrate**:
- Link masses and inertias
- Joint friction and damping
- Motor torque constants
- Sensor noise characteristics
- Time delays

### Step-by-Step: Calibrating a Quadruped

#### 1. Mass and Inertia

**Real robot test**:
1. Weigh robot on scale → Total mass
2. Suspend robot from each leg → Measure swing period → Compute inertia

**Simulation update**:
```xml
<!-- URDF: Update measured masses -->
<link name="base">
  <inertial>
    <mass value="12.3"/>  <!-- Measured: 12.3 kg -->
    <inertia ixx="0.15" iyy="0.25" izz="0.20" .../>  <!-- Computed from swing test -->
  </inertial>
</link>
```

#### 2. Joint Friction

**Real robot test** (per joint):
1. Command constant velocity (e.g., 1 rad/s)
2. Measure steady-state torque required
3. Friction torque ≈ steady-state torque

**Simulation update**:
```python
# Isaac Gym
dof_props['friction'][joint_idx] = measured_friction  # e.g., 0.15 Nm
```

#### 3. Motor Dynamics

**Real robot test**:
1. Command step input (0 → max torque)
2. Measure time to reach 90% of commanded torque → Time constant τ
3. Model as first-order: `Torque(t) = Torque_cmd * (1 - exp(-t/τ))`

**Simulation update**:
```python
# Isaac Gym: Add actuator dynamics
actuator_model = gymapi.ActuatorProperties()
actuator_model.type = gymapi.ACTUATOR_FIRST_ORDER
actuator_model.time_constant = measured_tau  # e.g., 0.02 seconds
gym.set_actor_dof_actuator_properties(env, robot, actuator_model)
```

#### 4. Sensor Noise

**Real robot test**:
1. Place robot stationary
2. Record IMU data for 60 seconds
3. Compute standard deviation of readings → Noise level

**Simulation update**:
```python
# Add Gaussian noise to simulated IMU
imu_reading = true_value + np.random.normal(0, measured_stddev)
```

---

## Domain Randomization Validation

### Testing Robustness Before Deployment

Before deploying to hardware, **validate** domain randomization covers real-world variations.

**Method**:
1. Train policy with domain randomization in sim
2. Test policy in sim with **realistic parameter ranges** (based on system ID)
3. If policy succeeds → Likely works on real hardware

**Example**:
```python
# Randomization ranges (based on measurements)
mass_range = (real_mass * 0.9, real_mass * 1.1)  # ±10%
friction_range = (real_friction * 0.7, real_friction * 1.3)  # ±30%

# Test policy with these ranges
# If success rate > 90% → Deploy
```

**If fails**: Increase randomization range in training → Retrain.

---

## Safety-Critical Deployment

### Hardware Safety Protocols

**Before ANY real robot test**:

1. **Emergency stop button** accessible at all times
2. **Soft surfaces** (foam mats) under robot to prevent damage
3. **Tether/harness** for aerial or balancing robots
4. **Human spotter** ready to intervene
5. **Limited velocity/torque** initially (25% max until validated)

### Software Safety Wrappers

**Implement watchdogs and bounds checking**:

```python
class SafetyWrapper:
    def __init__(self, policy, robot):
        self.policy = policy
        self.robot = robot

        # Safety limits
        self.max_joint_vel = 5.0  # rad/s
        self.max_joint_torque = 20.0  # Nm
        self.max_base_tilt = 45.0  # degrees

    def get_action(self, obs):
        # Run policy
        action = self.policy(obs)

        # Clip to safe ranges
        action = np.clip(action, self.robot.action_space.low, self.robot.action_space.high)

        # Check safety violations
        if self.is_unsafe(obs):
            print("SAFETY VIOLATION - Emergency stop!")
            return self.emergency_stop_action()

        return action

    def is_unsafe(self, obs):
        # Check if robot is tipping over
        base_tilt = np.rad2deg(np.arcsin(obs[2]))  # Z-component of up vector
        if abs(base_tilt) > self.max_base_tilt:
            return True

        # Check joint velocities
        joint_vels = obs[10:22]
        if np.any(np.abs(joint_vels) > self.max_joint_vel):
            return True

        return False

    def emergency_stop_action(self):
        # Command zero velocity on all joints
        return np.zeros(self.robot.num_actions)
```

**Usage**:
```python
safe_policy = SafetyWrapper(trained_policy, robot)
action = safe_policy.get_action(observation)
```

---

## Hands-On: Deploying Vision Model

Let's deploy a YOLOv8 object detector (trained on synthetic data in Chapter 3.4) to a real robot camera.

### Step 1: Export Model for Edge Deployment

**Convert to TensorRT** (NVIDIA GPU acceleration):
```bash
# Requires NVIDIA Jetson or PC with TensorRT
yolo export model=best.pt format=engine device=0  # TensorRT engine
```

**Output**: `best.engine` (optimized for inference)

### Step 2: ROS 2 Detection Node

**File**: `object_detector_node.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose
from cv_bridge import CvBridge
import cv2
import tensorrt as trt
import numpy as np

class ObjectDetectorNode(Node):
    def __init__(self):
        super().__init__('object_detector')

        # Load TensorRT engine
        self.engine = self.load_engine('best.engine')
        self.context = self.engine.create_execution_context()

        # ROS 2 interfaces
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10
        )
        self.publisher = self.create_publisher(Detection2DArray, '/detections', 10)

        self.get_logger().info('Object detector node started')

    def load_engine(self, engine_path):
        """Load TensorRT engine"""
        with open(engine_path, 'rb') as f, trt.Runtime(trt.Logger(trt.Logger.WARNING)) as runtime:
            return runtime.deserialize_cuda_engine(f.read())

    def image_callback(self, msg):
        # Convert ROS Image to OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Preprocess
        input_tensor = self.preprocess(cv_image)

        # Run inference
        outputs = self.infer(input_tensor)

        # Post-process (NMS, decode boxes)
        detections = self.postprocess(outputs)

        # Publish detections
        det_msg = Detection2DArray()
        det_msg.header = msg.header
        for det in detections:
            d = Detection2D()
            d.bbox.center.x = det['x']
            d.bbox.center.y = det['y']
            d.bbox.size_x = det['w']
            d.bbox.size_y = det['h']

            hyp = ObjectHypothesisWithPose()
            hyp.id = str(det['class_id'])
            hyp.score = det['confidence']
            d.results.append(hyp)

            det_msg.detections.append(d)

        self.publisher.publish(det_msg)

    def preprocess(self, image):
        # Resize to 640x640, normalize
        img = cv2.resize(image, (640, 640))
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))  # HWC -> CHW
        return np.expand_dims(img, axis=0)  # Add batch dimension

    def infer(self, input_tensor):
        # Allocate GPU memory and run inference
        # (Simplified - full version uses CUDA streams)
        return self.context.execute_v2([input_tensor])

    def postprocess(self, outputs):
        # Decode YOLO outputs, apply NMS
        # (Implementation details omitted for brevity)
        return []  # List of {'x', 'y', 'w', 'h', 'class_id', 'confidence'}

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run on robot**:
```bash
ros2 run my_vision object_detector_node
```

**Verify**:
```bash
ros2 topic echo /detections
```

### Step 3: Measure Real-World Performance

**Collect ground-truth test set**:
1. Capture 100 real images from robot camera
2. Manually annotate bounding boxes (using LabelImg tool)

**Evaluate model**:
```python
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

# Load ground truth
coco_gt = COCO('real_annotations.json')

# Load predictions
coco_dt = coco_gt.loadRes('model_predictions.json')

# Evaluate
coco_eval = COCOeval(coco_gt, coco_dt, 'bbox')
coco_eval.evaluate()
coco_eval.accumulate()
coco_eval.summarize()

# Prints: mAP @ IoU=0.5:0.95, mAP @ IoU=0.5, etc.
```

**Expected**: mAP 70-90% if domain randomization was good. If less than 50%, need more randomization.

---

## Deploying RL Policies

### Step 1: Export Policy

**TorchScript** (portable PyTorch format):
```python
policy = torch.jit.load('trained_policy.pt')
policy.eval()

# Test on dummy input
obs = torch.randn(1, 34)  # Example observation
with torch.no_grad():
    action = policy(obs)
print(f"Action: {action}")
```

### Step 2: ROS 2 Control Node

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
import torch
import numpy as np

class RLControllerNode(Node):
    def __init__(self):
        super().__init__('rl_controller')

        # Load policy
        self.policy = torch.jit.load('trained_policy.pt')
        self.policy.eval()

        # ROS 2 interfaces
        self.joint_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_callback, 10
        )
        self.cmd_pub = self.create_publisher(
            Float64MultiArray, '/joint_position_commands', 10
        )

        # Safety wrapper
        self.max_joint_vel = 5.0  # rad/s

        self.get_logger().info('RL controller started')

    def joint_callback(self, msg):
        # Build observation vector
        obs = self.build_observation(msg)

        # Safety check
        if self.is_safe(obs):
            # Run policy
            with torch.no_grad():
                action = self.policy(torch.tensor(obs, dtype=torch.float32).unsqueeze(0))
            action = action.squeeze(0).numpy()

            # Publish commands
            cmd = Float64MultiArray()
            cmd.data = action.tolist()
            self.cmd_pub.publish(cmd)
        else:
            self.get_logger().warn('Unsafe state detected - stopping')
            self.publish_zero_command()

    def build_observation(self, joint_msg):
        # Extract joint positions and velocities
        # (Match observation structure used in training)
        return np.concatenate([joint_msg.position, joint_msg.velocity])

    def is_safe(self, obs):
        # Check velocity limits
        velocities = obs[12:24]  # Example indices
        return np.all(np.abs(velocities) < self.max_joint_vel)

    def publish_zero_command(self):
        cmd = Float64MultiArray()
        cmd.data = [0.0] * 12  # Zero velocity on all joints
        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = RLControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Step 3: Incremental Testing

**Safety-first rollout**:
1. **Day 1**: Test in simulation (Isaac Sim) with real robot URDF
2. **Day 2**: Test on real robot with **joints locked** (verify sensor readings)
3. **Day 3**: Test with **25% max torque** (slow, safe movements)
4. **Day 4**: Test with **50% max torque** (if stable)
5. **Day 5**: Test with **100% max torque** (full performance)

**At each stage**: Monitor for oscillations, instability, unexpected behavior.

---

## Measuring Sim-to-Real Transfer

### Quantitative Metrics

**For vision models**:
- **mAP (mean Average Precision)**: Compare sim validation mAP vs. real test mAP
- **False positive rate**: Detections on non-existent objects
- **Latency**: Inference time (ms per frame)

**For RL policies**:
- **Task success rate**: % of trials achieving goal (walk 10m, grasp object)
- **Episode length**: Steps before failure (longer = more stable)
- **Reward**: Compare cumulative reward (sim vs. real)

### Example: Quadruped Walking

**Simulation**: 95% success rate (walks 10m without falling)
**Real hardware**: 75% success rate

**Gap**: 20 percentage points

**Analysis**:
- Failures due to: Ground friction lower than expected (slipping on smooth lab floor)
- **Solution**: Add floor material to sim randomization range, retrain

---

## Hardware-in-the-Loop (HITL)

### Iterative Improvement Cycle

**Problem**: Initial deployment fails. How to improve?

**HITL workflow**:
1. **Deploy** policy to real robot
2. **Collect failure cases** (log state, action, outcome when robot falls)
3. **Add failures to sim** (recreate scenarios in Isaac Sim)
4. **Retrain** policy with augmented data
5. **Re-deploy** and repeat

**Example**:
- Robot fails when turning sharply (loses balance)
- In sim: Add sharp turn scenarios to training (randomize angular velocity commands)
- Retrain for 500 epochs
- Re-deploy → Sharp turn success rate improves 60% → 85%

### Fine-Tuning on Real Data

**Collect small real dataset** (10-100 examples):
- Record robot states and successful actions (when human manually controls)
- Fine-tune policy with supervised learning on this data
- Often closes remaining sim-to-real gap

**Imitation learning**:
```python
# Load sim-trained policy
policy = torch.load('sim_policy.pt')

# Load real demonstrations
real_states = np.load('real_demos_states.npy')
real_actions = np.load('real_demos_actions.npy')

# Fine-tune (supervised learning)
optimizer = torch.optim.Adam(policy.parameters(), lr=1e-4)
for epoch in range(100):
    pred_actions = policy(torch.tensor(real_states, dtype=torch.float32))
    loss = F.mse_loss(pred_actions, torch.tensor(real_actions, dtype=torch.float32))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Save fine-tuned policy
torch.save(policy, 'finetuned_policy.pt')
```

---

## Common Deployment Issues

### Issue: Policy oscillates/vibrates on real robot

**Cause**: Simulation timestep too large (e.g., 50 Hz) vs. real control loop (200 Hz).

**Fix**: Match simulation and real control frequencies.

### Issue: Robot falls immediately

**Cause**: Observation mismatch (sim uses perfect state, real uses noisy sensors).

**Fix**: Add sensor noise to sim observations during training.

### Issue: Actions too aggressive (robot jerks)

**Cause**: No action smoothing.

**Fix**: Low-pass filter actions:
```python
prev_action = 0
alpha = 0.8  # Smoothing factor

def smooth_action(action):
    global prev_action
    smoothed = alpha * action + (1 - alpha) * prev_action
    prev_action = smoothed
    return smoothed
```

---

## Key Takeaways

🎓 **Sim-to-real gap** arises from physics mismatches, sensor noise, latency, and actuator dynamics—minimize via calibration and domain randomization.

🎓 **System identification** measures real robot parameters (mass, friction, motor dynamics) to update simulation for accuracy.

🎓 **Safety wrappers** (bounds checking, emergency stops) are mandatory for real hardware deployment—protect robot and humans.

🎓 **Incremental testing** (25% → 50% → 100% torque) reduces risk of catastrophic failures during initial deployment.

🎓 **Hardware-in-the-loop** enables iterative improvement—collect failures, retrain in sim, redeploy.

🎓 **Fine-tuning on real data** (10-100 examples) often closes remaining performance gap without full retraining.

---

## Module 3 Complete!

**Congratulations!** You've mastered NVIDIA Isaac Sim for Physical AI development.

**Skills acquired**:
✅ Photorealistic environment creation with USD and PBR
✅ Advanced sensor simulation (RGB-D, LiDAR, segmentation)
✅ Synthetic data generation for computer vision AI
✅ Reinforcement learning with massively parallel simulation
✅ Sim-to-real deployment for real robot hardware

**Next**: Module 4 introduces **Vision-Language-Action (VLA) models**—the frontier of Physical AI, where robots understand natural language commands and execute complex tasks using foundation models!

---

## Assessment: End-to-End Deployment

**Goal**: Deploy a sim-trained model to real hardware (or high-fidelity sim) and evaluate performance.

**Requirements**:

1. **Model training** (choose one):
   - Object detection model (YOLOv8) on synthetic warehouse data
   - RL locomotion policy for quadruped/humanoid

2. **System calibration**:
   - Measure 3+ robot parameters (mass, friction, etc.)
   - Update simulation to match measurements
   - Re-validate model in calibrated sim

3. **Safety implementation**:
   - Implement SafetyWrapper class with bounds checking
   - Emergency stop mechanism (software or hardware button)
   - Velocity/torque limits (25% of max initially)

4. **Deployment**:
   - Deploy to real robot or high-fidelity sim
   - Run 20+ test trials
   - Record success rate, failure modes

5. **Performance analysis**:
   - Compare sim performance vs. real performance (quantitative metrics)
   - Identify failure modes (slipping, perception errors, etc.)
   - Propose improvements (more randomization, fine-tuning, etc.)

6. **Deliverables**:
   - Trained model weights
   - Calibration measurements and updated sim config
   - Safety wrapper code
   - Deployment ROS 2 node
   - Video (60 seconds) of real robot executing task
   - Report (500 words):
     - Sim vs. real performance metrics
     - Failure analysis
     - Lessons learned
     - Next steps for improvement

**Expected Pass Rate**: 50% of learners complete within 180 minutes (excluding training time).

**Bonus**: Implement HITL loop—collect 10 failure cases, retrain, measure improvement.

---

## Additional Resources

📚 **Official Documentation**:
- [Isaac Sim to Real Robot](https://docs.omniverse.nvidia.com/isaacsim/latest/advanced_tutorials/tutorial_advanced_domain_randomization.html)
- [System Identification for Robotics](http://www.roboticsproceedings.org/rss07/p03.pdf)

📺 **Video Tutorials**:
- NVIDIA Isaac - Sim-to-Real Transfer
- Deploying RL Policies to Hardware
- Hardware Safety Best Practices

🛠️ **Tools**:
- [TensorRT](https://developer.nvidia.com/tensorrt) - Model optimization for deployment
- [ONNX Runtime](https://onnxruntime.ai/) - Cross-platform inference
- [ROS 2 Control](https://control.ros.org/) - Real-time robot controllers

📖 **Papers**:
- "Closing the Sim-to-Real Loop" (Chebotar et al., 2019)
- "Sim-to-Real Transfer of Robotic Control" (Peng et al., 2018)
- "Learning to Walk in Minutes Using Massively Parallel Deep RL" (Rudin et al., 2022)

📦 **Robot Platforms**:
- [Unitree Go1](https://www.unitree.com/) - Affordable quadruped
- [NVIDIA Jetson](https://developer.nvidia.com/embedded/jetson-orin) - Edge AI compute
- [DynamixelSDK](https://github.com/ROBOTIS-GIT/DynamixelSDK) - Servo control library

---

**Chapter Status**: Complete ✅
**Module 3 Status**: Complete ✅ 🎉
**Next Module**: [Module 4: Vision-Language-Action Models](../module-module-4/
