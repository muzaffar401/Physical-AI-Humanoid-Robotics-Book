---
id: chapter-3-5-reinforcement-learning
title: "Chapter 3.5: Reinforcement Learning with Isaac Gym"
sidebar_label: "3.5 Reinforcement Learning"
sidebar_position: 5
---

# Chapter 3.5: Reinforcement Learning with Isaac Gym

## Training Robot Controllers 100x Faster with Parallel Simulation

Training a humanoid to walk in traditional simulators takes **weeks** due to single-robot constraints. **Isaac Gym** changes the game: simulate **1,000+ robots in parallel on a single GPU**, learning 100x faster by experiencing thousands of environments simultaneously. This chapter teaches you to train robust RL policies for locomotion, manipulation, and navigation using state-of-the-art algorithms like PPO and SAC.

---

## Learning Objectives

By the end of this chapter, you will:

- **Understand**: Explain reinforcement learning fundamentals (MDP, rewards, policy gradients)
- **Understand**: Describe how Isaac Gym achieves massive parallelization with GPU physics
- **Apply**: Configure Isaac Gym environments for custom robot tasks
- **Create**: Train a quadruped robot to walk using PPO (Proximal Policy Optimization)
- **Analyze**: Implement domain randomization for sim-to-real transfer
- **Apply**: Deploy trained RL policies to simulated and real robots

**Estimated Time**: 3 hours

---

## Prerequisites

- **Chapter 3.1-3.4 complete** (Isaac Sim fundamentals)
- **Python** (NumPy, PyTorch basics)
- **Basic RL knowledge** helpful (Q-learning, policy gradients) but not required
- **NVIDIA GPU** (RTX 3080+ recommended for large parallel envs)

---

## What You'll Build

By the end of this chapter, you'll have:

✅ **Isaac Gym environment** with 512 parallel humanoid/quadruped robots
✅ **Trained locomotion policy** (walk forward, turn, balance)
✅ **Domain randomized training** for robust real-world deployment
✅ **Deployment pipeline** from RL policy → ROS 2 controller
✅ **Visualization tools** for policy debugging (reward curves, action histograms)

---

## Reinforcement Learning Crash Course

### What is RL?

**Reinforcement Learning** = Agent learns by trial and error, maximizing cumulative reward.

**Components**:
- **Agent**: The robot/controller (policy network)
- **Environment**: Simulation (physics, sensors)
- **State** (s): Observations (joint angles, velocities, sensor data)
- **Action** (a): Motor commands (joint torques, velocities)
- **Reward** (r): Scalar feedback (+1 for forward progress, -1 for falling)
- **Policy** (π): Neural network mapping state → action

**Goal**: Find policy π* that maximizes expected cumulative reward.

### Markov Decision Process (MDP)

**Formalization**:
- At timestep t, agent in state `s_t`
- Takes action `a_t ~ π(s_t)`
- Environment transitions to `s_{t+1}` with probability `P(s_{t+1} | s_t, a_t)`
- Receives reward `r_t = R(s_t, a_t)`

**Objective**: Maximize return (discounted sum of rewards):
```
G_t = r_t + γ r_{t+1} + γ² r_{t+2} + ...
```
Where `γ ∈ [0, 1]` is discount factor (0.99 typical).

### Policy Gradient Methods

**Direct approach**: Parameterize policy as neural network π_θ(a | s), optimize θ to maximize expected return.

**Popular algorithms**:
1. **PPO (Proximal Policy Optimization)**: Most widely used, stable, sample-efficient
2. **SAC (Soft Actor-Critic)**: Off-policy, continuous control, very stable
3. **TD3 (Twin Delayed DDPG)**: Similar to SAC, good for manipulation

**This chapter**: Focus on PPO (Isaac Gym's default).

---

## Isaac Gym Architecture

### Why Isaac Gym is Fast

**Traditional RL simulation**:
- 1 environment per CPU core
- Transfer states GPU ← CPU → GPU for NN inference
- **Speed**: 1,000 steps/sec (single env)

**Isaac Gym**:
- **1,000+ envs on single GPU** (PhysX parallel physics)
- All data stays on GPU (zero CPU-GPU transfer)
- **Speed**: 100,000+ steps/sec (1,000 envs) → **100x faster**

**Architecture**:
```
GPU:
  PhysX (1000 parallel robots) → Observations → Policy NN → Actions → PhysX
```

All operations CUDA-accelerated, no CPU bottleneck.

### Installation

Isaac Gym is integrated into Isaac Sim 2023.1+.

**Install additional RL libraries**:
```bash
pip install rl-games tensorboard matplotlib
```

---

## Hands-On: Training a Quadruped to Walk

We'll train ANYmal (quadruped robot) to walk forward using PPO.

### Step 1: Understanding the Task

**Goal**: Robot walks forward at 1 m/s, maintains upright orientation.

**State** (observations):
- Base orientation (quaternion, 4 values)
- Base linear velocity (3 values)
- Base angular velocity (3 values)
- Joint positions (12 values, 3 per leg)
- Joint velocities (12 values)
- **Total**: 34 observations

**Action**:
- Target joint positions for 12 joints (position control)
- **Total**: 12 actions (continuous, range -1 to 1, scaled to joint limits)

**Reward**:
- +1 for forward velocity close to target (1 m/s)
- -0.5 for angular velocity (penalize spinning)
- -0.2 for torques (energy efficiency)
- -10 if fallen (base height < 0.3m) → Episode ends

### Step 2: Define Environment

**File**: `anymal_env.py`

```python
import torch
from isaacgym import gymapi, gymtorch
from isaacgym.torch_utils import *
import numpy as np

class AnymalEnv:
    def __init__(self, num_envs=512, device='cuda'):
        self.num_envs = num_envs
        self.device = device
        self.max_episode_length = 1000  # 1000 timesteps per episode

        # Create Isaac Gym
        self.gym = gymapi.acquire_gym()
        self.sim_params = gymapi.SimParams()
        self.sim_params.dt = 0.02  # 50 Hz simulation
        self.sim_params.substeps = 2
        self.sim_params.up_axis = gymapi.UP_AXIS_Z
        self.sim_params.gravity = gymapi.Vec3(0, 0, -9.81)

        # PhysX GPU settings
        self.sim_params.physx.use_gpu = True
        self.sim_params.physx.solver_type = 1
        self.sim_params.physx.num_position_iterations = 4
        self.sim_params.physx.num_velocity_iterations = 1

        self.sim = self.gym.create_sim(0, 0, gymapi.SIM_PHYSX, self.sim_params)

        # Load robot URDF/USD
        asset_root = "~/isaac_assets/"
        asset_file = "anymal_c/urdf/anymal_c.urdf"
        asset_options = gymapi.AssetOptions()
        asset_options.default_dof_drive_mode = gymapi.DOF_MODE_POS
        self.robot_asset = self.gym.load_asset(self.sim, asset_root, asset_file, asset_options)

        # Create environments
        self.envs = []
        self.robot_handles = []
        spacing = 2.0
        lower = gymapi.Vec3(-spacing, -spacing, 0.0)
        upper = gymapi.Vec3(spacing, spacing, spacing)

        for i in range(num_envs):
            env = self.gym.create_env(self.sim, lower, upper, int(np.sqrt(num_envs)))
            self.envs.append(env)

            # Spawn robot
            pose = gymapi.Transform()
            pose.p = gymapi.Vec3(0, 0, 0.6)  # Start 0.6m above ground
            robot_handle = self.gym.create_actor(env, self.robot_asset, pose, f"robot_{i}", i, 1)
            self.robot_handles.append(robot_handle)

        # Observation and action spaces
        self.num_obs = 34
        self.num_actions = 12

        # State buffers (all on GPU)
        self.obs_buf = torch.zeros((num_envs, self.num_obs), device=device, dtype=torch.float)
        self.rew_buf = torch.zeros(num_envs, device=device, dtype=torch.float)
        self.reset_buf = torch.ones(num_envs, device=device, dtype=torch.long)  # Reset all initially
        self.progress_buf = torch.zeros(num_envs, device=device, dtype=torch.long)

    def reset(self, env_ids):
        """Reset specified environments"""
        # Reset robot to initial state
        # (Simplified - full version sets joint positions, velocities)
        self.progress_buf[env_ids] = 0

    def step(self, actions):
        """Apply actions, step simulation, compute rewards"""
        # Apply actions as joint position targets
        # (Simplified - full version uses gym.set_dof_position_target_tensor)

        # Step physics
        self.gym.simulate(self.sim)
        self.gym.fetch_results(self.sim, True)

        # Get observations
        # (Simplified - full version reads joint states, base pose from tensors)

        # Compute rewards
        self.compute_rewards()

        # Check for resets (fallen robots)
        self.reset_buf = torch.where(
            self.progress_buf >= self.max_episode_length,
            torch.ones_like(self.reset_buf),
            self.reset_buf
        )

        # Reset fallen envs
        reset_env_ids = self.reset_buf.nonzero(as_tuple=False).squeeze(-1)
        if len(reset_env_ids) > 0:
            self.reset(reset_env_ids)

        self.progress_buf += 1

        return self.obs_buf, self.rew_buf, self.reset_buf, {}

    def compute_rewards(self):
        """Reward function for walking forward"""
        # Get base linear velocity
        base_lin_vel = self.obs_buf[:, 7:10]  # Example indices

        # Reward forward velocity (X-axis)
        target_vel = 1.0
        vel_reward = -torch.abs(base_lin_vel[:, 0] - target_vel)

        # Penalize angular velocity (spinning)
        ang_vel = self.obs_buf[:, 10:13]
        ang_vel_penalty = -0.5 * torch.sum(torch.square(ang_vel), dim=1)

        # Total reward
        self.rew_buf[:] = vel_reward + ang_vel_penalty
```

**Note**: This is simplified. Full implementation uses `gymtorch` API for tensor-based state access.

### Step 3: Train with PPO

**File**: `train_ppo.py`

```python
import torch
from rl_games.algos_torch import torch_ext
from rl_games.algos_torch.a2c_continuous import A2CAgent
from rl_games.common import env_configurations, experiment, vecenv

from anymal_env import AnymalEnv

# RL-Games configuration
config = {
    'params': {
        'seed': 42,
        'algo': {
            'name': 'a2c_continuous'  # RL-Games calls PPO "a2c_continuous"
        },
        'model': {
            'name': 'continuous_a2c_logstd'
        },
        'network': {
            'name': 'actor_critic',
            'separate': False,
            'space': {
                'continuous': {
                    'mu_activation': 'None',
                    'sigma_activation': 'None',
                    'mu_init': {'name': 'default'},
                    'sigma_init': {'name': 'const_initializer', 'val': 0},
                    'fixed_sigma': True
                }
            },
            'mlp': {
                'units': [256, 128, 64],  # Hidden layer sizes
                'activation': 'elu',
                'd2rl': False
            }
        },
        'config': {
            'name': 'Anymal',
            'env_name': 'anymal',
            'multi_gpu': False,
            'ppo': True,
            'mixed_precision': False,
            'normalize_input': True,
            'normalize_value': True,
            'num_actors': 512,  # Number of parallel environments
            'reward_shaper': {},
            'normalize_advantage': True,
            'gamma': 0.99,
            'tau': 0.95,
            'learning_rate': 3e-4,
            'lr_schedule': 'adaptive',
            'kl_threshold': 0.008,
            'score_to_win': 20000,
            'max_epochs': 10000,
            'save_best_after': 100,
            'save_frequency': 500,
            'grad_norm': 1.0,
            'entropy_coef': 0.0,
            'truncate_grads': True,
            'e_clip': 0.2,
            'horizon_length': 32,
            'minibatch_size': 32768,
            'mini_epochs': 5,
            'critic_coef': 2,
            'clip_value': True,
            'seq_len': 4,
            'bounds_loss_coef': 0.0001
        }
    }
}

# Create environment
env = AnymalEnv(num_envs=512)

# Train
agent = A2CAgent('anymal', config['params'])
runner = experiment.Runner()
runner.run(config)
```

**Run**:
```bash
python train_ppo.py
```

**Expected**:
- Training starts, logs reward per episode
- TensorBoard logs saved to `runs/`
- Checkpoints saved every 500 epochs to `nn/`

**Monitor**:
```bash
tensorboard --logdir=runs/
```

**Training time**: ~2-4 hours on RTX 3080 for decent walking policy.

---

## Designing Reward Functions

### Reward Engineering is Critical

**Good reward** = Agent learns desired behavior quickly.
**Bad reward** = Agent exploits loopholes, never learns task.

### Example: Humanoid Walking

**Goal**: Walk forward at 1 m/s, stay upright.

**Reward components**:

```python
def compute_rewards(self):
    # 1. Forward velocity reward
    vel_reward = -torch.abs(self.base_lin_vel[:, 0] - 1.0)  # Target 1 m/s

    # 2. Upright orientation reward
    up_vec = quat_rotate(self.base_quat, to_torch([0, 0, 1], device=self.device))
    up_reward = torch.sum(up_vec * to_torch([0, 0, 1], device=self.device), dim=-1)

    # 3. Energy penalty (minimize torques)
    energy_penalty = -0.01 * torch.sum(torch.square(self.torques), dim=-1)

    # 4. Alive bonus (encourage not falling)
    alive_reward = 1.0

    # 5. Termination penalty
    fallen = self.base_pos[:, 2] < 0.3  # Base height < 30cm
    fallen_penalty = -10.0 * fallen.float()

    # Combine
    total_reward = vel_reward + 0.5 * up_reward + energy_penalty + alive_reward + fallen_penalty
    return total_reward
```

**Key principles**:
- **Dense rewards**: Reward every timestep (not just goal achievement)
- **Shaping**: Guide agent toward goal (e.g., reward approaching target velocity)
- **Penalties**: Discourage bad behavior (high energy, falling)
- **Scaling**: Balance components (vel_reward in [-1, 0], up_reward in [0, 1])

---

## Domain Randomization for RL

**Problem**: Policy trained in perfect sim → Fails on real robot (friction mismatch, sensor noise, delays).

**Solution**: Randomize physics during training → Policy robust to variations.

### Randomize Physics Parameters

```python
def randomize_physics(self):
    """Randomize dynamics every episode reset"""
    for env_id in reset_env_ids:
        # Randomize mass
        base_mass = np.random.uniform(10, 15)  # Robot weighs 10-15 kg
        self.gym.set_actor_rigid_body_masses(self.envs[env_id], self.robot_handles[env_id], [base_mass, ...])

        # Randomize friction
        friction = np.random.uniform(0.5, 1.5)
        for shape in self.gym.get_actor_rigid_shape_properties(self.envs[env_id], self.robot_handles[env_id]):
            shape.friction = friction
            self.gym.set_actor_rigid_shape_properties(self.envs[env_id], self.robot_handles[env_id], [shape])

        # Randomize joint damping
        damping = np.random.uniform(0.1, 0.5)
        dof_props = self.gym.get_actor_dof_properties(self.envs[env_id], self.robot_handles[env_id])
        dof_props['damping'] = damping
        self.gym.set_actor_dof_properties(self.envs[env_id], self.robot_handles[env_id], dof_props)
```

**Randomize every**: Mass, friction, damping, motor strength, time delays, sensor noise.

**Result**: Policy learns to walk despite uncertainty → Transfers to real hardware.

---

## Visualization and Debugging

### Rendering During Training

Isaac Gym can render one environment while training (others run headless for speed).

```python
# Enable viewer
viewer = self.gym.create_viewer(self.sim, gymapi.CameraProperties())
self.gym.viewer_camera_look_at(viewer, None, gymapi.Vec3(5, 5, 2), gymapi.Vec3(0, 0, 0))

# Training loop
for epoch in range(max_epochs):
    # ... training code ...

    # Render every 10 steps
    if epoch % 10 == 0:
        self.gym.draw_viewer(viewer, self.sim, True)
        self.gym.sync_frame_time(self.sim)
```

**Effect**: Watch robot learn in real-time (first env only, others invisible for speed).

### TensorBoard Logging

Log key metrics for analysis:

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/anymal')

# Log rewards
mean_reward = torch.mean(rew_buf).item()
writer.add_scalar('Reward/mean', mean_reward, epoch)

# Log episode length
mean_length = torch.mean(progress_buf.float()).item()
writer.add_scalar('Episode/length', mean_length, epoch)

# Log policy loss (from PPO algorithm)
writer.add_scalar('Loss/policy', policy_loss, epoch)
```

**View**:
```bash
tensorboard --logdir=runs/anymal
```

---

## Deploying Trained Policies

### Export Policy to ONNX

For deployment, export trained PyTorch policy to ONNX (cross-platform inference).

```python
import torch

# Load trained model
policy = torch.load('nn/anymal_best.pth')

# Dummy input (observation)
dummy_obs = torch.randn(1, 34)  # Batch size 1, 34 observations

# Export to ONNX
torch.onnx.export(
    policy,
    dummy_obs,
    'anymal_policy.onnx',
    input_names=['observations'],
    output_names=['actions'],
    dynamic_axes={'observations': {0: 'batch_size'}, 'actions': {0: 'batch_size'}}
)
```

### ROS 2 Policy Node

**File**: `policy_node.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
import torch

class PolicyNode(Node):
    def __init__(self):
        super().__init__('policy_node')
        self.policy = torch.jit.load('anymal_policy.pth')  # TorchScript model
        self.policy.eval()

        # Subscribe to joint states (observations)
        self.subscription = self.create_subscription(
            JointState, '/joint_states', self.joint_callback, 10
        )

        # Publish joint commands (actions)
        self.publisher = self.create_publisher(Float64MultiArray, '/joint_commands', 10)

    def joint_callback(self, msg):
        # Extract observations from joint states
        obs = torch.tensor(msg.position + msg.velocity, dtype=torch.float32).unsqueeze(0)

        # Run policy
        with torch.no_grad():
            actions = self.policy(obs)

        # Publish actions
        cmd = Float64MultiArray()
        cmd.data = actions.squeeze(0).tolist()
        self.publisher.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = PolicyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run on robot** (simulation or real hardware):
```bash
ros2 run my_robot_control policy_node
```

---

## Advanced: Curriculum Learning

**Problem**: Some tasks are too hard to learn from scratch (e.g., backflip).

**Solution**: Start easy, gradually increase difficulty.

### Example: Humanoid Standup → Walk → Run

```python
class HumanoidCurriculum:
    def __init__(self):
        self.stage = 0  # Start with stage 0

    def get_target_velocity(self):
        if self.stage == 0:
            return 0.0  # Stage 0: Just stand upright
        elif self.stage == 1:
            return 0.5  # Stage 1: Walk slowly (0.5 m/s)
        elif self.stage == 2:
            return 1.0  # Stage 2: Walk normal (1.0 m/s)
        else:
            return 2.0  # Stage 3: Run (2.0 m/s)

    def update_stage(self, mean_reward):
        # Advance to next stage if performance threshold met
        if self.stage == 0 and mean_reward > 10:
            self.stage = 1
        elif self.stage == 1 and mean_reward > 20:
            self.stage = 2
        elif self.stage == 2 and mean_reward > 30:
            self.stage = 3
```

**Integration**: Update target velocity in reward function based on curriculum stage.

---

## Key Takeaways

🎓 **Isaac Gym** enables 1,000+ parallel environments on single GPU → **100x faster RL training** than CPU-based sims.

🎓 **PPO (Proximal Policy Optimization)** is the go-to algorithm for continuous control (locomotion, manipulation).

🎓 **Reward engineering** is critical—dense, shaped rewards guide learning; sparse rewards slow convergence.

🎓 **Domain randomization** (mass, friction, delays) creates robust policies that transfer to real hardware.

🎓 **TensorBoard logging** tracks training progress—essential for debugging reward functions and hyperparameters.

🎓 **Deployment**: Export to ONNX or TorchScript → ROS 2 node → Real robot or sim.

---

## What's Next?

You've trained RL policies in simulation—now let's deploy them to real hardware!

In **Chapter 3.6: Deployment to Real Robots**, you'll:

- Bridge the sim-to-real gap with calibration and fine-tuning
- Deploy Isaac Sim-trained models to physical humanoids/quadrupeds
- Implement safety wrappers and failure recovery
- Measure real-world performance vs. simulation
- Iterate on design with hardware-in-the-loop testing

**Continue to** → [Chapter 3.6: Deployment to Real Robots](./chapter-3-6-deployment)

---

## Assessment: Train a Locomotion Policy

**Goal**: Train a quadruped or humanoid to walk forward using RL.

**Requirements**:

1. **Environment setup**:
   - 256+ parallel environments
   - Robot: ANYmal quadruped or humanoid (provide URDF)
   - Task: Walk forward at 0.5-1.0 m/s

2. **Reward function**:
   - Forward velocity reward
   - Upright orientation reward
   - Energy penalty
   - Termination penalty for falling

3. **Training**:
   - Train with PPO for 2,000+ epochs
   - Mean reward > 20 (or task-specific threshold)
   - Save checkpoints every 500 epochs

4. **Domain randomization**:
   - Randomize mass (±20%)
   - Randomize friction (0.5-1.5)
   - Randomize motor strength (±10%)

5. **Deliverables**:
   - Environment code (`robot_env.py`)
   - Training script (`train_ppo.py`)
   - Trained policy weights (`.pth`)
   - TensorBoard reward curve screenshot
   - Video (30 seconds) of trained policy executing
   - Report (400 words):
     - Reward function design choices
     - Training hyperparameters
     - Final performance metrics
     - Observations on learning behavior

**Expected Pass Rate**: 55% of learners complete within 240 minutes (including training time).

**Bonus**: Deploy policy to simulated robot in Isaac Sim, demonstrate navigation over uneven terrain.

---

## Additional Resources

📚 **Official Documentation**:
- [Isaac Gym Documentation](https://developer.nvidia.com/isaac-gym)
- [RL-Games Library](https://github.com/Denys88/rl_games)
- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/) - Alternative RL library

📺 **Video Tutorials**:
- NVIDIA Isaac Gym - Getting Started
- RL for Robotics - Fundamentals
- Training Humanoid Locomotion Policies

🛠️ **RL Frameworks**:
- [RL-Games](https://github.com/Denys88/rl_games) - High-performance PPO/SAC
- [Stable-Baselines3](https://github.com/DLR-RM/stable-baselines3) - Easy-to-use RL algorithms
- [RLlib](https://docs.ray.io/en/latest/rllib/index.html) - Scalable RL (Ray framework)

📖 **Papers**:
- "Proximal Policy Optimization Algorithms" (Schulman et al., 2017)
- "Learning Dexterous In-Hand Manipulation" (OpenAI, 2019) - Used Isaac Gym predecessor
- "Sim-to-Real Transfer for Biped Locomotion" (Peng et al., 2020)

📦 **Example Environments**:
- [Isaac Gym Benchmark Environments](https://github.com/NVIDIA-Omniverse/IsaacGymEnvs)
- [Legged Gym](https://github.com/leggedrobotics/legged_gym) - ANYmal, Unitree Go1 training

---

**Chapter Status**: Complete ✅
**Next Chapter**: [3.6 Deployment to Real Robots](./chapter-3-6-deployment)
