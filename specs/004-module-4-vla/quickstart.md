# Quickstart: Module 4 - Vision-Language-Action (VLA)

**Module**: 4 - Vision-Language-Action
**Date**: 2025-12-01
**Purpose**: Setup guide for learners to prepare development environment, API keys, hardware, and dependencies before starting Module 4

## Prerequisites

Before starting Module 4, you must complete:

✅ **Module 1**: ROS 2 fundamentals (nodes, topics, pub/sub, RViz2)
✅ **Module 2 OR Module 3**: Simulation environment (Gazebo OR Isaac Sim) with camera sensors
✅ **Python 3.10+**: Installed and working (`python3 --version`)
✅ **ROS 2 Humble**: Installed and sourced (`ros2 --version`)
✅ **Ubuntu 22.04 or WSL2**: Linux environment (Windows native not supported for ROS 2)

---

## Hardware Requirements

### Minimum Requirements
- **CPU**: 4 cores (Intel i5/AMD Ryzen 5 or better)
- **RAM**: 16GB (8GB for OS, 4GB for ROS 2, 4GB for APIs/buffers)
- **Storage**: 10GB free (for Whisper models if using local, code examples, simulation assets)
- **Microphone**: Any USB microphone or laptop built-in mic
- **Internet**: Required for API calls (Whisper, GPT-4, Claude)

### Recommended for Best Experience
- **CPU**: 8 cores (Intel i7/AMD Ryzen 7 or better)
- **RAM**: 32GB (supports local Whisper models + CLIP on GPU + simulation)
- **GPU**: NVIDIA RTX 2060 or better (8GB+ VRAM for CLIP, local Whisper, simulation)
- **Storage**: 20GB free (local Whisper models are 1-3GB each)
- **Microphone**: USB microphone with noise cancellation (Logitech, Blue Yeti, etc.)
- **Camera**: RGB-D camera like Intel RealSense D435 (optional, for real robot testing)

### GPU Acceleration (Optional but Recommended)

If you have an NVIDIA GPU:

```bash
# Check if CUDA is installed
nvcc --version  # Should show CUDA 11.8 or 12.x

# Check if PyTorch detects GPU
python3 -c "import torch; print(torch.cuda.is_available())"  # Should print True

# If False, install CUDA-enabled PyTorch:
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**With GPU**: CLIP runs at 30 FPS, local Whisper transcribes in 2-3s per 30s audio
**Without GPU (CPU only)**: CLIP runs at 1-2 FPS, local Whisper transcribes in 10-20s per 30s audio (still usable, just slower)

---

## API Keys Setup (Choose ONE LLM Provider)

Module 4 requires API keys for speech-to-text (Whisper) and LLM-based planning (GPT-4 OR Claude). You have two options:

### Option 1: OpenAI (Whisper + GPT-4)

**What you get**: OpenAI Whisper API for speech-to-text, GPT-4 for task planning
**Cost**: ~$5-10 to complete module (~$0.006/min for Whisper, ~$0.01-$0.03 per LLM command)
**Free Tier**: $5 credit for new accounts (usually enough for module completion)

**Steps**:
1. Create account at https://platform.openai.com/signup
2. Add payment method (Settings → Billing)
3. Create API key (API Keys → Create new secret key)
4. Copy key (starts with `sk-...`)

### Option 2: Anthropic (Claude 3) + OpenAI (Whisper only)

**What you get**: Claude 3 for task planning (alternative to GPT-4), OpenAI Whisper for speech-to-text
**Cost**: ~$5-10 to complete module (~$0.006/min for Whisper, ~$0.015-$0.075 per Claude command)
**Free Tier**: No free tier, but Claude often has better safety guardrails

**Steps**:
1. Create Anthropic account at https://console.anthropic.com/
2. Add payment method, create API key (starts with `sk-ant-...`)
3. Also create OpenAI account (for Whisper API, see Option 1)

### Wake-Word API Key (Optional, Free Tier Available)

**Picovoice Porcupine** for wake-word detection ("Hey Robot"):
1. Create account at https://console.picovoice.ai/signup
2. Free tier includes 3 custom wake-words (sufficient for module)
3. Get access key (Settings → Access Keys)

---

## Environment Configuration

Create a `.env` file in your workspace root (NEVER commit this file to Git):

```bash
# Navigate to your workspace (e.g., ~/ros2_ws/src/vla_project/)
cd ~/ros2_ws/src/vla_project

# Create .env file
nano .env
```

**If using OpenAI (Whisper + GPT-4)**:

```bash
# .env file contents
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview  # Or gpt-4-1106-preview
WHISPER_MODE=api  # Or 'local' for local Whisper

# Optional: Porcupine wake-word (free tier)
PORCUPINE_ACCESS_KEY=your_porcupine_key_here
```

**If using Anthropic (Claude 3) + OpenAI (Whisper)**:

```bash
# .env file contents
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # For Whisper only
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-sonnet-20240229  # Or claude-3-opus-20240229 (more expensive, better quality)
WHISPER_MODE=api  # Or 'local' for local Whisper

# Optional: Porcupine wake-word (free tier)
PORCUPINE_ACCESS_KEY=your_porcupine_key_here
```

**For local Whisper (no API costs for speech-to-text)**:

Change `WHISPER_MODE=local` and set model size:

```bash
WHISPER_MODE=local
WHISPER_MODEL=base  # Options: tiny, base, small, medium, large (larger = more accurate but slower)
```

**Security Warning**: NEVER commit `.env` to Git. Verify `.env` is in your `.gitignore`:

```bash
# Check if .env is ignored
echo ".env" >> .gitignore
git status  # .env should NOT appear in untracked files
```

---

## Python Dependencies Installation

### Step 1: Create Virtual Environment (Recommended)

```bash
# Navigate to your workspace
cd ~/ros2_ws/src/vla_project

# Create virtual environment
python3 -m venv venv

# Activate (do this EVERY time you start a new terminal)
source venv/bin/activate

# Your prompt should now show (venv)
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install core dependencies
pip install -r requirements.txt
```

**Create `requirements.txt`** (or download from course materials):

```text
# Speech (API-based, required)
openai>=1.0.0

# LLM (choose one or both)
anthropic>=0.20.0  # For Claude
# openai already installed above for GPT-4

# Visual Grounding (required)
torch>=2.0.0
torchvision>=0.15.0
openai-clip>=1.0.1

# Wake-Word Detection (optional)
pvporcupine>=3.0.0

# ROS 2 Integration (required)
# Note: rclpy is installed with ROS 2, but install Python packages:
opencv-python>=4.8.0
numpy>=1.24.0
python-dotenv>=1.0.0

# Audio Processing (required)
sounddevice>=0.4.6
soundfile>=0.12.1
noisereduce>=3.0.0  # For audio preprocessing

# Utilities
scipy>=1.11.0
```

**Optional - For local Whisper (skip if using API only)**:

```bash
# Install openai-whisper (for local deployment)
pip install openai-whisper

# Or faster-whisper (optimized, 4x faster)
pip install faster-whisper
```

### Step 3: Verify Installation

```bash
# Test OpenAI API (if using Whisper or GPT-4)
python3 << EOF
import openai
import os
from dotenv import load_dotenv
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("✅ OpenAI API key works!")
EOF

# Test Anthropic API (if using Claude)
python3 << EOF
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
print("✅ Anthropic API key works!")
EOF

# Test CLIP (visual grounding)
python3 << EOF
import torch
import clip
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
print(f"✅ CLIP works! Using device: {device}")
EOF

# Test microphone access
python3 << EOF
import sounddevice as sd
devices = sd.query_devices()
print("✅ Microphone detected!")
print(devices)
EOF
```

If all tests pass, you're ready to start Module 4!

---

## ROS 2 Workspace Setup

### Create Package for VLA Project

```bash
# Navigate to ROS 2 workspace
cd ~/ros2_ws/src

# Create package
ros2 pkg create vla_robot \
  --build-type ament_python \
  --dependencies rclpy std_msgs sensor_msgs geometry_msgs

# Navigate to package
cd vla_robot
```

### Add Code Examples from Module 4

As you progress through chapters, you'll add Python nodes:
- `vla_robot/whisper_node.py` (Chapter 4.2)
- `vla_robot/llm_planner_node.py` (Chapter 4.4)
- `vla_robot/visual_grounding_node.py` (Chapter 4.5-4.6)
- `vla_robot/vla_orchestrator.py` (Chapter 4.7)

### Build and Source

```bash
# Build workspace
cd ~/ros2_ws
colcon build --packages-select vla_robot

# Source (add to ~/.bashrc to auto-source)
source ~/ros2_ws/install/setup.bash

# Verify package is found
ros2 pkg list | grep vla_robot
```

---

## Microphone Setup & Testing

### Check Available Microphones

```bash
# List audio devices
python3 << EOF
import sounddevice as sd
print(sd.query_devices())
EOF
```

Example output:
```
> 0 USB Microphone, ALSA (2 in, 0 out)
  1 Built-in Audio, ALSA (2 in, 2 out)
```

### Set Default Microphone (if multiple devices)

```bash
# Add to .env file:
echo "AUDIO_DEVICE_INDEX=0" >> .env  # Use index from query_devices() output
```

### Test Recording

```bash
# Record 5-second audio clip
python3 << EOF
import sounddevice as sd
import soundfile as sf
import numpy as np

fs = 16000  # Whisper expects 16kHz
duration = 5
print("Recording... speak now!")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
sd.wait()
sf.write('test_recording.wav', audio, fs)
print("✅ Saved to test_recording.wav")
EOF

# Play back recording (optional)
aplay test_recording.wav  # Linux
# Or open in audio player
```

---

## Simulation Environment Check

Module 4 requires a simulation environment from Module 2 (Gazebo) OR Module 3 (Isaac Sim).

### Option 1: Gazebo (from Module 2)

```bash
# Verify Gazebo is installed
gazebo --version  # Should show Gazebo 11.x

# Launch test world
gazebo worlds/empty.world
```

### Option 2: Isaac Sim (from Module 3)

```bash
# Verify Isaac Sim is installed
# Launch Isaac Sim and check it opens without errors
```

### Check Camera Sensors

Your simulation should have:
- **RGB Camera**: For CLIP visual grounding
- **Depth Camera** (optional but recommended): For 3D pose estimation

Verify in RViz2:

```bash
# Launch your robot simulation (from Module 2/3)
# Then check camera topics:
ros2 topic list | grep camera

# Should see:
# /camera/image_raw (RGB)
# /camera/depth/image_raw (Depth, optional)
```

---

## Estimated Costs for Module 4

### API Costs (if using cloud APIs)

| Service | Usage | Cost Estimate |
|---------|-------|---------------|
| Whisper API | ~2 hours of audio total | ~$0.72 ($0.006/min × 120 min) |
| GPT-4 API | ~100 commands | ~$2-3 ($0.02-$0.03 per command) |
| Claude API | ~100 commands | ~$2-7 ($0.02-$0.07 per command) |
| Porcupine wake-word | Free tier | $0 (up to 3 wake-words) |

**Total**: ~$5-10 to complete entire Module 4 (all exercises + mini-project)

### How to Minimize Costs

1. **Use local Whisper**: Saves ~$0.72 (but requires GPU for good performance)
2. **Use smaller LLM models**: `gpt-3.5-turbo` (~$0.002 per command) instead of GPT-4 (less accurate planning but cheaper)
3. **Test with mocked APIs**: Module code examples include mocked API responses for testing without API calls
4. **Reuse test data**: Record audio once, reuse for multiple exercises

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'openai'"

**Solution**: Activate virtual environment and reinstall dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "openai.AuthenticationError: Invalid API key"

**Solution**: Check `.env` file has correct API key (no spaces, no quotes around key):
```bash
cat .env | grep OPENAI_API_KEY
# Should show: OPENAI_API_KEY=sk-proj-xxxx...
```

### Issue: CLIP fails with "CUDA out of memory"

**Solution**: Use CPU instead (slower but works):
```python
device = "cpu"  # Change from "cuda" to "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
```

### Issue: Microphone not detected

**Solution**: Check permissions and drivers:
```bash
# Linux: Check ALSA devices
arecord -l

# If no devices, install drivers:
sudo apt update && sudo apt install alsa-utils pulseaudio
```

### Issue: "Rate limit exceeded" from OpenAI API

**Solution**: You've hit API rate limits. Wait 60 seconds or upgrade to paid tier (higher limits):
- Free tier: 3 requests/min
- Paid tier: 200 requests/min

---

## Next Steps

Once setup is complete:

1. ✅ Verify all tests pass (API keys, CLIP, microphone)
2. ✅ Complete `requirements.txt` installation
3. ✅ Create `.env` file with API keys
4. ✅ Test simulation environment (Gazebo or Isaac Sim)
5. 🚀 **Start Chapter 4.1**: Introduction to Vision-Language-Action

---

## Support Resources

- **OpenAI API Docs**: https://platform.openai.com/docs
- **Anthropic Claude Docs**: https://docs.anthropic.com/
- **CLIP GitHub**: https://github.com/openai/CLIP
- **Porcupine Docs**: https://picovoice.ai/docs/porcupine/
- **ROS 2 Humble Docs**: https://docs.ros.org/en/humble/

---

**Status**: ✅ Quickstart guide complete - learners can now set up environment for Module 4
**Estimated Setup Time**: 30-60 minutes (depending on network speed for downloads)
