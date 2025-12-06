# Contract: Chapter 4.2 - Whisper ROS 2 Node

**Chapter**: 4.2 - Speech-to-Text with Whisper
**Component**: WhisperNode (ROS 2 node for speech-to-text integration)
**Purpose**: Specification for WhisperNode that captures microphone audio, transcribes with Whisper (API or local), and publishes to `/voice_command` topic

## Overview

The WhisperNode is a ROS 2 node that provides speech-to-text functionality for the VLA pipeline. It continuously listens to microphone input, transcribes audio using OpenAI Whisper (API or local model), and publishes transcriptions to the `/voice_command` topic for downstream processing by LLM planning nodes.

## Functional Requirements

### FR-1: Audio Capture
- **Requirement**: Node MUST capture audio from system microphone at 16kHz sample rate (Whisper's expected input)
- **Input**: Microphone audio stream
- **Output**: Audio buffer (16kHz, mono, float32)
- **Constraints**:
  - Configurable device index (support multiple microphones)
  - Configurable chunk size (default: 30 seconds for API, 5 seconds for streaming)
- **Test**: Record 5-second audio, verify sample rate and format

### FR-2: Whisper API Integration
- **Requirement**: Node MUST support OpenAI Whisper API for transcription
- **Input**: Audio buffer (16kHz, mono)
- **Output**: Transcript text (string)
- **Constraints**:
  - API key loaded from environment variable `OPENAI_API_KEY`
  - Timeout: 10 seconds (fail gracefully on timeout)
  - Error handling: Log API errors, retry once on transient failures
- **Test**: Send sample audio to API, verify transcript accuracy
- **Performance**: <2 seconds latency for 30-second audio clip

### FR-3: Local Whisper Integration (Alternative)
- **Requirement**: Node MUST support local Whisper models as alternative to API
- **Input**: Audio buffer (16kHz, mono)
- **Output**: Transcript text (string)
- **Constraints**:
  - Model size configurable (tiny, base, small, medium, large)
  - Device configurable (CPU, CUDA)
  - Model loaded once at initialization (not per-transcription)
- **Test**: Send sample audio to local model, verify transcript accuracy
- **Performance**: <3 seconds latency on GPU (RTX 2060+), <20 seconds on CPU

### FR-4: ROS 2 Topic Publishing
- **Requirement**: Node MUST publish transcriptions to `/voice_command` topic
- **Input**: Transcript text (string)
- **Output**: `std_msgs/String` message on `/voice_command` topic
- **Constraints**:
  - Publish only on successful transcription (skip on errors)
  - Include timestamp in log (for debugging)
- **Test**: Subscribe to `/voice_command` with `ros2 topic echo`, verify messages received
- **Performance**: <10ms from transcription completion to publish

### FR-5: Mode Selection
- **Requirement**: Node MUST support runtime mode selection (API vs local)
- **Input**: Environment variable `WHISPER_MODE` (values: `api` or `local`)
- **Behavior**:
  - If `api`: Use OpenAI Whisper API
  - If `local`: Load local Whisper model
  - Default: `api` (easier for beginners)
- **Test**: Run node with `WHISPER_MODE=api`, then `WHISPER_MODE=local`, verify both work

### FR-6: Audio Preprocessing (Optional)
- **Requirement**: Node SHOULD support basic audio preprocessing (noise reduction, VAD)
- **Input**: Raw audio buffer
- **Output**: Preprocessed audio buffer
- **Constraints**:
  - Optional (disabled by default)
  - Enabled via parameter `enable_preprocessing=true`
- **Test**: Record audio with background noise, compare transcription with/without preprocessing

## Non-Functional Requirements

### NFR-1: Latency
- **Requirement**: End-to-end latency (audio capture → publish) MUST be <2 seconds for API, <3 seconds for local GPU
- **Test**: Measure time from audio start to topic publish with `ros2 topic hz`

### NFR-2: Robustness
- **Requirement**: Node MUST handle API failures gracefully (network errors, timeouts, rate limits)
- **Behavior**: Log error, skip transcription, continue listening (don't crash)
- **Test**: Disconnect network, verify node logs error and continues

### NFR-3: Resource Usage
- **Requirement**:
  - CPU usage <20% (when using API)
  - GPU VRAM <2GB (when using local Whisper base model)
  - RAM <1GB (excluding model weights)
- **Test**: Monitor with `htop`, `nvidia-smi`

### NFR-4: Configurability
- **Requirement**: Node MUST support configuration via environment variables:
  - `OPENAI_API_KEY`: API key (required for API mode)
  - `WHISPER_MODE`: `api` or `local` (default: `api`)
  - `WHISPER_MODEL`: Model size for local mode (default: `base`)
  - `AUDIO_DEVICE_INDEX`: Microphone device index (default: 0)
  - `AUDIO_CHUNK_DURATION`: Recording duration in seconds (default: 30)
- **Test**: Set env vars, verify node respects configuration

## API Specification

### ROS 2 Node

**Node Name**: `whisper_node`

**Publishers**:
- **Topic**: `/voice_command`
- **Type**: `std_msgs/String`
- **QoS**: `rclpy.qos.qos_profile_system_default`
- **Rate**: Variable (publishes on each transcription)

**Parameters**:
- `whisper_mode`: String (`api` or `local`, default: `api`)
- `whisper_model`: String (local model size: `tiny`, `base`, `small`, `medium`, `large`, default: `base`)
- `audio_device_index`: Int (microphone device index, default: 0)
- `audio_chunk_duration`: Float (recording duration in seconds, default: 30.0)
- `enable_preprocessing`: Bool (enable noise reduction, default: false)

**Lifecycle**:
1. Initialization: Load API key or local model, initialize audio device
2. Main Loop: Record audio → Transcribe → Publish → Repeat
3. Shutdown: Release audio device, cleanup resources

### Python Class Structure

```python
class WhisperNode(Node):
    def __init__(self):
        # Initialize ROS 2 node, load parameters, setup publisher
        # Load Whisper model (API client or local model)
        # Initialize audio device

    def record_audio(self, duration: float) -> np.ndarray:
        # Capture audio from microphone
        # Return: audio array (16kHz, mono, float32)

    def transcribe_api(self, audio: np.ndarray) -> str:
        # Send audio to Whisper API
        # Return: transcript text

    def transcribe_local(self, audio: np.ndarray) -> str:
        # Run local Whisper model on audio
        # Return: transcript text

    def publish_transcript(self, text: str):
        # Publish to /voice_command topic

    def run(self):
        # Main loop: record → transcribe → publish
```

## Data Flow

```
[Microphone]
    ↓ (16kHz audio)
[Audio Capture]
    ↓ (audio buffer)
[Preprocessing] (optional, noise reduction)
    ↓ (cleaned audio)
[Whisper Transcription] (API or local)
    ↓ (transcript text)
[ROS 2 Publisher]
    ↓ (std_msgs/String)
[/voice_command topic]
    ↓
[Downstream nodes] (LLM Planner, etc.)
```

## Error Handling

### Error Cases

1. **No microphone detected**
   - Behavior: Log error, exit with code 1
   - Message: "ERROR: No microphone found. Check `arecord -l` and set AUDIO_DEVICE_INDEX."

2. **API key missing (API mode)**
   - Behavior: Log error, exit with code 1
   - Message: "ERROR: OPENAI_API_KEY not set. Add to .env file."

3. **API timeout or network error**
   - Behavior: Log warning, skip transcription, continue listening
   - Message: "WARNING: Whisper API timeout. Retrying next audio chunk."

4. **API rate limit exceeded**
   - Behavior: Log warning, wait 60 seconds, retry
   - Message: "WARNING: API rate limit exceeded. Waiting 60s..."

5. **Local model loading failed**
   - Behavior: Log error, exit with code 1
   - Message: "ERROR: Failed to load Whisper model 'base'. Check PyTorch installation."

6. **Audio capture failed**
   - Behavior: Log error, retry 3 times, exit if all fail
   - Message: "ERROR: Audio capture failed. Retrying (attempt 2/3)..."

## Testing

### Unit Tests

1. **Test Audio Capture**: Mock microphone, verify 16kHz output
2. **Test API Transcription**: Mock Whisper API, verify JSON parsing
3. **Test Local Transcription**: Load Whisper base model, verify transcription
4. **Test ROS 2 Publishing**: Mock publisher, verify message format
5. **Test Error Handling**: Inject API errors, verify graceful fallback

### Integration Tests

1. **End-to-End Test (API mode)**:
   ```bash
   # Run node with API mode
   export WHISPER_MODE=api
   ros2 run vla_robot whisper_node

   # In another terminal, subscribe to topic
   ros2 topic echo /voice_command

   # Speak into microphone: "Hello robot"
   # Verify transcript appears in topic echo
   ```

2. **End-to-End Test (local mode)**:
   ```bash
   # Run node with local mode
   export WHISPER_MODE=local
   export WHISPER_MODEL=base
   ros2 run vla_robot whisper_node

   # Same verification as above
   ```

3. **Latency Test**:
   ```bash
   # Measure latency
   time ros2 topic echo /voice_command --once
   # Should complete within 2-3 seconds
   ```

## Dependencies

### Python Packages
- `rclpy` - ROS 2 Python client
- `std_msgs` - ROS 2 standard messages
- `openai>=1.0.0` - OpenAI API client (for API mode)
- `openai-whisper` - Local Whisper (for local mode)
- `sounddevice>=0.4.6` - Audio capture
- `soundfile>=0.12.1` - Audio file I/O
- `numpy>=1.24.0` - Array operations
- `python-dotenv>=1.0.0` - Environment variable loading
- `noisereduce>=3.0.0` - Audio preprocessing (optional)

### System Dependencies
- Microphone (USB or built-in)
- ALSA or PulseAudio (Linux audio system)
- CUDA 11.8+ (optional, for local GPU acceleration)

## Example Usage

### Minimal Example (API mode)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import openai
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

class WhisperNode(Node):
    def __init__(self):
        super().__init__('whisper_node')
        self.publisher = self.create_publisher(String, '/voice_command', 10)
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def record_audio(self, duration=5):
        fs = 16000
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()
        return audio.flatten()

    def transcribe(self, audio):
        # Save audio to temporary file (Whisper API requires file upload)
        import soundfile as sf
        sf.write("temp_audio.wav", audio, 16000)

        with open("temp_audio.wav", "rb") as f:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return transcript.text

    def run(self):
        while rclpy.ok():
            self.get_logger().info("Recording...")
            audio = self.record_audio(duration=5)

            self.get_logger().info("Transcribing...")
            text = self.transcribe(audio)

            msg = String()
            msg.data = text
            self.publisher.publish(msg)
            self.get_logger().info(f"Published: {text}")

def main():
    rclpy.init()
    node = WhisperNode()
    node.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Acceptance Criteria

1. ✅ Node starts without errors with valid API key or local model
2. ✅ Audio captured at 16kHz from microphone
3. ✅ Transcriptions published to `/voice_command` topic
4. ✅ Latency <2s (API) or <3s (local GPU) for 5-second audio
5. ✅ Node handles API errors gracefully (no crashes)
6. ✅ Both API and local modes work
7. ✅ Transcriptions are >80% accurate for clear speech
8. ✅ Node can run continuously for 30+ minutes without memory leaks

---

**Status**: ✅ Contract complete - ready for implementation in Chapter 4.2
**Implementation Effort**: ~4-6 hours (API mode: 2-3h, local mode: 1-2h, testing: 1h)
