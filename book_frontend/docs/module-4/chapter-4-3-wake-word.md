---
id: chapter-4-3-wake-word
title: "Chapter 4.3: Wake-Word Detection and Audio Processing"
sidebar_label: "4.3 Wake-Word Detection"
sidebar_position: 3
description: "Learn wake-word detection and audio preprocessing for selective robot voice interfaces"
keywords: [wake-word, porcupine, picovoice, vad, audio preprocessing, keyword spotting]
learning_journey: "LJ1"
duration: "2 hours"
difficulty: "intermediate"
prerequisites:
  - "chapter-4-2-speech-to-text"
objectives:
  - "Understand: Explain how wake-word detection (keyword spotting) works"
  - "Apply: Integrate Picovoice Porcupine for 'Hey Robot' wake-word"
  - "Apply: Implement Voice Activity Detection (VAD) for noise reduction"
  - "Create: Build production-ready VoiceInputNode with wake-word + Whisper"
milestone: "Robot only transcribes speech after detecting 'Hey Robot' wake-word"
---

# Chapter 4.3: Wake-Word Detection and Audio Processing

## What You'll Learn

By the end of this chapter, you will:
- Understand wake-word detection (keyword spotting) and why it's essential for voice interfaces
- Implement wake-word detection using Picovoice Porcupine ("Hey Robot")
- Apply Voice Activity Detection (VAD) to filter out silence and background noise
- Build a production-ready VoiceInputNode that combines wake-word + VAD + Whisper
- Handle audio preprocessing (resampling, normalization, noise reduction)

**Estimated Time**: 2 hours

---

## The Problem: Always-On Listening

In Chapter 4.2, our WhisperNode transcribed **all audio** continuously. This creates three problems:

### Problem 1: Privacy Concerns
If the robot listens to everything, users might accidentally trigger commands during private conversations:

```
[User talking to friend]: "I need to pick up the red box from the garage"
[Robot hears]: "Pick up the red box" → Robot starts executing task!
```

### Problem 2: Wasted API Costs
Whisper API costs $0.006/minute. Continuous listening for 8 hours/day = $2.88/day = $86/month for a single robot.

### Problem 3: Background Noise
Random sounds (TV, music, conversations) get transcribed as nonsense commands, causing errors downstream.

---

## The Solution: Wake-Word Detection

**Wake-word detection** (also called **keyword spotting**) is a lightweight model that listens for a specific trigger phrase ("Hey Robot", "Alexa", "OK Google") and only activates speech recognition when detected.

### Wake-Word + ASR Pipeline

```
[Microphone] → [Wake-Word Detector] → [Trigger detected?]
                         ↓ No                    ↓ Yes
                   [Ignore audio]         [Whisper ASR] → [Transcript]
```

**Benefits**:
- ✅ Privacy: Only transcribes speech after user says wake-word
- ✅ Cost: Whisper only runs after trigger (reduces API usage by 95%+)
- ✅ Accuracy: Eliminates false positives from background noise

### How Wake-Word Detection Works

Wake-word detectors use small neural networks (1-10MB) that run on CPU in real-time:

1. **Audio Input**: Continuously buffer audio in small chunks (e.g., 512 samples = 32ms at 16kHz)
2. **Feature Extraction**: Convert audio to mel-frequency cepstral coefficients (MFCCs) - compact audio features
3. **Neural Network**: Tiny CNN/RNN predicts probability that wake-word is present
4. **Threshold**: If probability > 0.5, trigger detected

**Latency**: under 100ms (near-instant response)
**False Positive Rate**: under 1 per hour (very reliable)

---

## Approach 1: Picovoice Porcupine (Recommended)

**Picovoice Porcupine** is a cross-platform wake-word detection library with:
- Pre-trained models for common wake-words ("Hey Robot", "Computer", "Jarvis")
- Custom wake-word training (upload 3-5 voice samples, get trained model)
- Free tier: 3 wake-words, unlimited usage on single device
- Supports 30+ languages

### Installation

```bash
pip install pvporcupine
```

### API Key Setup

1. Sign up at https://console.picovoice.ai/
2. Create a new project → Get Access Key
3. Add to `.env` file:

```bash
# In .env file
PICOVOICE_API_KEY=your_access_key_here
```

### Code Example: Basic Wake-Word Detection

Create file: `docs/assets/module-4/code/chapter-4-3/porcupine_basic.py`

```python
"""
Basic wake-word detection with Picovoice Porcupine
Detects "Hey Robot" (or similar) and prints notification
"""

import pvporcupine
import sounddevice as sd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Porcupine with built-in keyword
porcupine = pvporcupine.create(
    access_key=os.getenv("PICOVOICE_API_KEY"),
    keywords=["computer"]  # Built-in wake-word (alternatives: "jarvis", "alexa", "hey google")
)

print(f"🎤 Listening for wake-word: '{porcupine.keywords[0]}'")
print(f"   Sample rate: {porcupine.sample_rate} Hz")
print(f"   Frame length: {porcupine.frame_length} samples")

# Audio callback function
def audio_callback(indata, frames, time, status):
    """Called for each audio buffer from microphone"""
    if status:
        print(f"⚠️ Audio status: {status}")

    # Convert float32 to int16 (Porcupine expects int16)
    audio = (indata[:, 0] * 32767).astype(np.int16)

    # Process audio frame
    keyword_index = porcupine.process(audio)

    if keyword_index >= 0:
        print(f"\n✅ Wake-word detected: '{porcupine.keywords[keyword_index]}'")
        print("   (Normally would activate Whisper here...)\n")

# Start audio stream
try:
    with sd.InputStream(
        channels=1,
        samplerate=porcupine.sample_rate,
        blocksize=porcupine.frame_length,
        callback=audio_callback
    ):
        print("Press Ctrl+C to stop")
        # Keep running
        sd.sleep(100000)  # Sleep for a long time

except KeyboardInterrupt:
    print("\n🛑 Stopped listening")
finally:
    porcupine.delete()
```

### Guided Walkthrough: Testing Wake-Word Detection

**Step 1**: Install dependencies

```bash
pip install pvporcupine sounddevice numpy python-dotenv
```

**Step 2**: Create Picovoice account and get API key
- Go to https://console.picovoice.ai/
- Sign up (free tier available)
- Create project → Copy "Access Key"
- Add to `.env` file:
  ```
  PICOVOICE_API_KEY=your_key_here
  ```

**Step 3**: Run example

```bash
python3 porcupine_basic.py
```

**Expected Output**:
```
🎤 Listening for wake-word: 'computer'
   Sample rate: 16000 Hz
   Frame length: 512 samples
Press Ctrl+C to stop
```

**Step 4**: Say the wake-word

Say: **"Computer"** (clearly, not too fast or slow)

**Expected Response**:
```
✅ Wake-word detected: 'computer'
   (Normally would activate Whisper here...)
```

**Tips for Accuracy**:
- Speak clearly and at normal volume
- Avoid background noise (TV, music)
- Try different pronunciations if not detecting
- Built-in keywords work best; custom keywords require training

---

## Custom Wake-Words: Training "Hey Robot"

Picovoice allows training custom wake-words by providing voice samples.

### Training Process

1. **Go to Picovoice Console**: https://console.picovoice.ai/
2. **Navigate to "Wake Word"** → "Train New Wake Word"
3. **Enter wake phrase**: "Hey Robot"
4. **Record samples**: Record yourself saying "Hey Robot" 3-5 times
   - Vary speed and intonation slightly
   - Use same microphone you'll use for deployment
5. **Train model**: Click "Train" (takes 2-5 minutes)
6. **Download**: Get `.ppn` model file
7. **Update code**: Use custom model instead of built-in keyword

### Using Custom Wake-Word

```python
# Instead of keywords=["computer"], use custom model file
porcupine = pvporcupine.create(
    access_key=os.getenv("PICOVOICE_API_KEY"),
    keyword_paths=["path/to/hey-robot_en_linux_v3_0_0.ppn"]
)
```

---

## Voice Activity Detection (VAD)

**Problem**: Even with wake-word detection, we might capture silence or background noise after the trigger.

**Example**:
```
User: "Hey Robot [2 second pause] pick up the box"
                  ↑ We don't want to transcribe this silence
```

**Voice Activity Detection (VAD)** distinguishes speech from silence/noise.

### Approach: WebRTC VAD

**WebRTC VAD** is Google's lightweight VAD library:
- Fast (CPU-only, real-time)
- Low false positives
- Configurable aggressiveness (0-3)

### Installation

```bash
pip install webrtcvad
```

### Code Example: VAD for Trimming Silence

Create file: `docs/assets/module-4/code/chapter-4-3/vad_example.py`

```python
"""
Voice Activity Detection (VAD) example
Demonstrates detecting speech vs silence in audio
"""

import webrtcvad
import sounddevice as sd
import numpy as np

# Initialize VAD
vad = webrtcvad.Vad(3)  # Aggressiveness: 0 (least) to 3 (most aggressive)
                         # 3 = Only flag clear speech as "voice"

# Audio parameters
SAMPLE_RATE = 16000  # VAD requires 16kHz
FRAME_DURATION = 30  # Frame duration in ms (10, 20, or 30)
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION / 1000)  # 480 samples for 30ms

def is_speech(audio_frame):
    """
    Check if audio frame contains speech

    Args:
        audio_frame: numpy array of int16 audio samples

    Returns:
        bool: True if speech detected, False if silence/noise
    """
    # VAD requires bytes (int16 PCM)
    audio_bytes = audio_frame.tobytes()

    # Check if speech
    return vad.is_speech(audio_bytes, SAMPLE_RATE)

# Test with recording
print("🎤 Recording 3 seconds... Speak or stay silent!")
audio = sd.rec(
    int(3 * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype='int16'
)
sd.wait()

# Analyze in 30ms frames
num_frames = len(audio) // FRAME_SIZE
speech_frames = 0

for i in range(num_frames):
    frame = audio[i * FRAME_SIZE:(i + 1) * FRAME_SIZE, 0]
    if is_speech(frame):
        speech_frames += 1

speech_ratio = speech_frames / num_frames

print(f"\n📊 Analysis:")
print(f"   Total frames: {num_frames}")
print(f"   Speech frames: {speech_frames}")
print(f"   Speech ratio: {speech_ratio:.1%}")

if speech_ratio > 0.5:
    print("   ✅ Audio contains speech (would transcribe)")
else:
    print("   ❌ Audio is mostly silence (would skip)")
```

### Guided Walkthrough: Testing VAD

**Step 1**: Install webrtcvad

```bash
pip install webrtcvad sounddevice
```

**Step 2**: Run example

```bash
python3 vad_example.py
```

**Test Case 1: Speaking**
- Speak continuously for 3 seconds
- Expected: "Speech ratio: 80-100%", "would transcribe"

**Test Case 2: Silence**
- Stay silent for 3 seconds
- Expected: "Speech ratio: 0-10%", "would skip"

**Test Case 3: Mixed**
- Speak for 1 second, silence for 2 seconds
- Expected: "Speech ratio: 30-40%", "would skip"

---

## Production-Ready VoiceInputNode

Now let's combine wake-word detection, VAD, and Whisper into a single ROS 2 node.

### Architecture

```
[Microphone] → [Wake-Word (Porcupine)] → [Trigger?]
                         ↓ Yes
                    [Buffer Audio]
                         ↓
                    [VAD Check] → [Enough speech?]
                         ↓ Yes
                    [Whisper ASR]
                         ↓
                [Publish /voice_command]
```

### Code: VoiceInputNode (Wake-Word + VAD + Whisper)

Create file: `docs/assets/module-4/code/chapter-4-3/voice_input_node.py`

```python
"""
VoiceInputNode: Production-ready voice input system
Combines wake-word detection, VAD, and Whisper ASR
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pvporcupine
import webrtcvad
import sounddevice as sd
import numpy as np
import openai
import soundfile as sf
import tempfile
import os
from dotenv import load_dotenv
from collections import deque

load_dotenv()

class VoiceInputNode(Node):
    def __init__(self):
        super().__init__('voice_input_node')

        # ROS 2 Publisher
        self.publisher = self.create_publisher(String, '/voice_command', 10)

        # Initialize Porcupine (wake-word)
        self.porcupine = pvporcupine.create(
            access_key=os.getenv("PICOVOICE_API_KEY"),
            keywords=["computer"]  # Change to your custom wake-word if available
        )

        # Initialize VAD
        self.vad = webrtcvad.Vad(3)  # Aggressiveness level 3

        # Initialize Whisper client
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Audio buffer for post-wake-word recording
        self.sample_rate = self.porcupine.sample_rate
        self.frame_length = self.porcupine.frame_length
        self.recording_buffer = deque(maxlen=int(self.sample_rate * 5))  # 5 seconds max

        # State machine
        self.listening_for_wake_word = True
        self.recording_command = False
        self.silence_frames = 0
        self.MAX_SILENCE_FRAMES = 15  # ~0.5 seconds of silence ends recording

        self.get_logger().info(f"🎤 VoiceInputNode ready. Say '{self.porcupine.keywords[0]}' to activate!")

        # Start audio stream
        self.stream = sd.InputStream(
            channels=1,
            samplerate=self.sample_rate,
            blocksize=self.frame_length,
            callback=self.audio_callback
        )
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        """Called for each audio buffer"""
        if status:
            self.get_logger().warning(f"Audio status: {status}")

        # Convert float32 to int16
        audio_int16 = (indata[:, 0] * 32767).astype(np.int16)

        if self.listening_for_wake_word:
            # Check for wake-word
            keyword_index = self.porcupine.process(audio_int16)
            if keyword_index >= 0:
                self.get_logger().info(f"✅ Wake-word detected: '{self.porcupine.keywords[keyword_index]}'")
                self.start_recording()

        elif self.recording_command:
            # Buffer audio after wake-word
            self.recording_buffer.extend(audio_int16)

            # Check if speech or silence
            try:
                is_speech = self.vad.is_speech(audio_int16.tobytes(), self.sample_rate)
            except:
                is_speech = False  # Malformed audio

            if is_speech:
                self.silence_frames = 0  # Reset silence counter
            else:
                self.silence_frames += 1

            # End recording after sustained silence
            if self.silence_frames >= self.MAX_SILENCE_FRAMES:
                self.stop_recording()

    def start_recording(self):
        """Start recording user command"""
        self.listening_for_wake_word = False
        self.recording_command = True
        self.recording_buffer.clear()
        self.silence_frames = 0
        self.get_logger().info("🎙️ Recording command... (speak now)")

    def stop_recording(self):
        """Stop recording and transcribe"""
        self.recording_command = False
        self.get_logger().info("🔄 Processing audio...")

        # Convert buffer to numpy array
        audio_array = np.array(list(self.recording_buffer), dtype=np.int16)

        # Check if enough speech content
        if not self.has_sufficient_speech(audio_array):
            self.get_logger().warn("⚠️ Not enough speech detected. Ignoring.")
            self.listening_for_wake_word = True
            return

        # Transcribe with Whisper
        try:
            transcript = self.transcribe_audio(audio_array)

            if transcript and len(transcript.strip()) > 3:
                # Publish to ROS 2
                msg = String()
                msg.data = transcript
                self.publisher.publish(msg)
                self.get_logger().info(f"📝 Transcribed: '{transcript}'")
            else:
                self.get_logger().warn("⚠️ Transcript too short, ignoring")

        except Exception as e:
            self.get_logger().error(f"Transcription error: {e}")

        # Reset to wake-word listening
        self.listening_for_wake_word = True
        self.get_logger().info(f"🎤 Ready for next wake-word")

    def has_sufficient_speech(self, audio_array):
        """Check if audio has enough speech content using VAD"""
        frame_size = int(self.sample_rate * 0.03)  # 30ms frames
        num_frames = len(audio_array) // frame_size
        speech_frames = 0

        for i in range(num_frames):
            frame = audio_array[i * frame_size:(i + 1) * frame_size]
            try:
                if self.vad.is_speech(frame.tobytes(), self.sample_rate):
                    speech_frames += 1
            except:
                pass

        speech_ratio = speech_frames / max(num_frames, 1)
        return speech_ratio > 0.3  # At least 30% speech

    def transcribe_audio(self, audio_array):
        """Transcribe audio with Whisper API"""
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            sf.write(temp_file.name, audio_array, self.sample_rate)
            temp_filename = temp_file.name

        try:
            # Call Whisper API
            with open(temp_filename, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            return transcript.text
        finally:
            os.remove(temp_filename)

    def destroy_node(self):
        """Cleanup"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
        if self.porcupine:
            self.porcupine.delete()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = VoiceInputNode()

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

### Guided Walkthrough: Running VoiceInputNode

**Step 1**: Ensure all dependencies installed

```bash
pip install pvporcupine webrtcvad openai sounddevice soundfile python-dotenv
```

**Step 2**: Configure `.env` file

```bash
# .env file
PICOVOICE_API_KEY=your_picovoice_key
OPENAI_API_KEY=sk-proj-your_openai_key
```

**Step 3**: Save code to ROS 2 package

```bash
# In your ROS 2 workspace
cd ~/ros2_ws/src/vla_robot
cp voice_input_node.py vla_robot/voice_input_node.py
```

**Step 4**: Update `setup.py`

```python
entry_points={
    'console_scripts': [
        'voice_input_node = vla_robot.voice_input_node:main',
    ],
},
```

**Step 5**: Build and run

```bash
cd ~/ros2_ws
colcon build --packages-select vla_robot
source install/setup.bash

# Terminal 1: Run node
ros2 run vla_robot voice_input_node

# Terminal 2: Monitor output
ros2 topic echo /voice_command
```

**Step 6**: Test end-to-end workflow

1. Say: **"Computer"** (wake-word)
   - Expected log: "✅ Wake-word detected: 'computer'"
   - Expected log: "🎙️ Recording command... (speak now)"

2. Immediately say: **"Pick up the red box"**
   - Node records audio while you speak
   - After 0.5s silence, stops recording
   - Expected log: "🔄 Processing audio..."

3. Wait for transcription
   - Expected log: "📝 Transcribed: 'Pick up the red box.'"
   - Expected in Terminal 2: `data: 'Pick up the red box.'`

4. Say: **"Computer"** again (next command)
   - Repeat workflow for multiple commands

---

## Milestone Validation

✅ **You've completed Chapter 4.3 if**:
1. Wake-word detector only activates on "Computer" (or custom phrase)
2. VAD filters out silence (doesn't transcribe empty audio)
3. VoiceInputNode publishes commands to `/voice_command` only after wake-word
4. False positive rate under 1 per 10 minutes of ambient noise
5. Latency from wake-word to transcript under 3 seconds

**Test Scenario**:
```bash
# Run VoiceInputNode
ros2 run vla_robot voice_input_node

# Expected behavior:
- Background conversation → No transcription
- Say "Computer" → Activates recording
- Say "Move forward 2 meters" → Transcribed and published
- Silence for 30 seconds → No activity (cost savings!)
```

---

## Chapter Summary

In this chapter, you learned:
- ✅ **Wake-Word Detection**: Trigger ASR only when user says specific phrase ("Computer")
- ✅ **Keyword Spotting**: Lightweight neural networks (under 10MB) run on CPU in real-time
- ✅ **Picovoice Porcupine**: Industry-standard wake-word library with free tier and custom training
- ✅ **Voice Activity Detection (VAD)**: Filter silence and background noise using WebRTC VAD
- ✅ **Production Pipeline**: Wake-word → VAD → Whisper → ROS 2 topic
- ✅ **Cost Optimization**: Reduced Whisper API usage by 95% (only transcribe after wake-word)

---

## What's Next?

Voice input is now production-ready with wake-word and VAD. In **Chapter 4.4**, we'll use **Large Language Models (LLMs)** to convert natural language commands into structured robot action plans.

You'll learn:
- How LLMs (GPT-4, Claude 3) decompose tasks into action sequences
- Prompt engineering for robot task planning
- Few-shot examples and system messages
- Input validation and safety checks

**Ready to give your robot a brain?** Let's continue! 🚀

---

## Additional Resources

- [Picovoice Porcupine Docs](https://picovoice.ai/docs/porcupine/) - Official documentation
- [Wake-Word Detection Paper](https://arxiv.org/abs/1711.07128) - Technical deep dive
- [WebRTC VAD](https://webrtc.org/) - Voice Activity Detection algorithm
- [Custom Wake-Word Training Tutorial](https://picovoice.ai/blog/custom-wake-word/) - Step-by-step guide

---

**⏱️ Estimated Chapter Time**: 2 hours (reading, coding, testing)
**🎯 Next Chapter**: [4.4 LLMs for Cognitive Planning](./chapter-4-4-llm-planning)
