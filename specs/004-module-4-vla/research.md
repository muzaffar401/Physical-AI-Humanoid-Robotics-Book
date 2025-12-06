# Research: Module 4 - Vision-Language-Action (VLA)

**Feature**: Module 4 - VLA
**Date**: 2025-12-01
**Status**: Research Complete

## Purpose

This document captures technical research decisions for Module 4 (Vision-Language-Action), covering speech-to-text technologies, LLM selection, visual grounding approaches, wake-word detection libraries, and state machine frameworks.

## Research Questions & Decisions

### 1. Speech-to-Text: Whisper API vs Local Deployment

**Question**: Should learners use OpenAI's Whisper API or deploy Whisper models locally?

**Options Considered**:

1. **Whisper API (OpenAI Cloud)**
   - **Pros**: Zero setup, handles all model sizes, auto-updates, consistent performance, ~1-2s latency
   - **Cons**: Requires API key, costs ~$0.006/minute (~$0.36/hour), requires internet, data leaves device
   - **Use case**: Quick prototyping, production with budget for API costs

2. **Local Whisper (openai-whisper library)**
   - **Pros**: No API costs, works offline, data stays local, full control
   - **Cons**: Requires Python environment setup, GPU recommended (8GB+ VRAM for medium model), 16GB+ RAM, slower on CPU (~10-20s for 30s audio on CPU, ~2-3s on GPU)
   - **Use case**: Budget-conscious, privacy-sensitive, high-volume transcription

3. **faster-whisper (optimized local)**
   - **Pros**: 4x faster than openai-whisper, lower memory usage, CTranslate2-based
   - **Cons**: Additional dependency complexity
   - **Use case**: Production local deployment

**Decision**: **Support both API and local with API as primary**
- **Rationale**: Beginners benefit from API simplicity (no GPU setup, faster onboarding), advanced learners can switch to local for cost/privacy. Most VLA pipelines need <2s latency - API meets this, local Whisper on GPU does too.
- **Implementation**: Chapter 4.2 demonstrates API approach first, then shows local alternative with cost/latency comparison table
- **Recommendation**: API for Ch 4.2-4.3 (prototyping), local for Ch 4.7+ (production)

**Model Size Recommendations**:
- **tiny**: 39M params, ~1GB VRAM, lowest accuracy, fastest (use for testing only)
- **base**: 74M params, ~1GB VRAM, acceptable accuracy, fast (good for real-time)
- **small**: 244M params, ~2GB VRAM, good accuracy (recommended minimum)
- **medium**: 769M params, ~5GB VRAM, better accuracy (recommended for production)
- **large**: 1550M params, ~10GB VRAM, best accuracy, slowest (overkill for most robots)

---

### 2. LLM Selection: GPT-4 vs Claude vs Open-Source

**Question**: Which LLM(s) should the module teach for robot task planning?

**Options Considered**:

1. **GPT-4 (OpenAI)**
   - **Pros**: Excellent reasoning, widely adopted, strong structured output (JSON mode), good docs, ChatGPT API compatible
   - **Cons**: Costs ~$0.01-$0.03 per command (8k context), closed-source, requires OpenAI account
   - **API Models**: `gpt-4-turbo-preview`, `gpt-4-1106-preview` (128k context)

2. **Claude 3 (Anthropic)**
   - **Pros**: Comparable reasoning, strong safety guardrails (refuses dangerous commands better), 100k context, good structured output
   - **Cons**: Costs ~$0.015-$0.075 per command (similar to GPT-4), requires Anthropic account, less ecosystem tooling
   - **API Models**: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku` (fastest, cheapest)

3. **Open-Source LLMs (LLaMA 3, Mistral, Vicuna)**
   - **Pros**: Free to run, privacy (local deployment), no API rate limits
   - **Cons**: Requires GPU (24GB+ VRAM for 70B models, 8GB for 7B), inferior reasoning for complex planning, harder to set up (Ollama, vLLM)
   - **Use case**: Advanced learners, budget-constrained, research environments

**Decision**: **Support both GPT-4 and Claude with examples for both**
- **Rationale**: Different learners have different API preferences (some already have OpenAI keys for Whisper, others prefer Anthropic). Both are production-grade. Avoid open-source for main content (setup burden, quality inconsistency).
- **Implementation**:
  - Ch 4.4 shows GPT-4 example first (more common), then Claude alternative
  - Provide side-by-side comparison table (cost, context length, latency, safety)
  - Code examples support both via env var: `LLM_PROVIDER=openai` or `LLM_PROVIDER=anthropic`
- **Cost Estimate**: $0.01-$0.05 per command (GPT-4), $0.015-$0.075 per command (Claude) for typical robot tasks

**Prompt Engineering Strategy**:
- System message: Robot capabilities (navigate, grasp, place, search), environment description
- Few-shot examples: 3-5 example commands → action plans
- Output format: JSON schema with action array `[{action, params}]`
- Safety: Include "refuse unsafe commands" instruction in system message

---

### 3. Visual Grounding: CLIP vs OWL-ViT vs YOLO+NLP

**Question**: Which visual grounding approach should learners use to map language ("red box") to image regions?

**Options Considered**:

1. **CLIP (OpenAI)**
   - **Pros**: Simple API, zero-shot (no training), text-image similarity scores, lightweight (ViT-B/32 ~150MB), CPU-friendly (slower but works)
   - **Cons**: Not a detector (need sliding window or grid search), coarse localization, ~1-2 FPS on CPU, ~30 FPS on GPU
   - **Use case**: Quick prototyping, single-object scenes, educational

2. **OWL-ViT (Google)**
   - **Pros**: Open-vocabulary object detection (CLIP-like but with bounding boxes), better localization, zero-shot
   - **Cons**: Requires PyTorch + Hugging Face Transformers, heavier model (~600MB), GPU strongly recommended, more complex API
   - **Use case**: Production-grade visual grounding, cluttered scenes

3. **YOLO + NLP Post-filtering**
   - **Pros**: Fast detection (YOLOv8 ~100 FPS on GPU), accurate bounding boxes
   - **Cons**: Closed-vocabulary (only detects pre-trained classes like "cup", "bottle"), needs language matching layer, two-stage approach
   - **Use case**: Known object categories, real-time performance critical

**Decision**: **CLIP as primary, OWL-ViT as advanced option**
- **Rationale**: CLIP is simpler for learners (fewer dependencies, clear API), sufficient for educational VLA demos. OWL-ViT is better for production but adds complexity. YOLO requires closed vocabulary (defeats VLA's open-ended language advantage).
- **Implementation**:
  - Ch 4.5: CLIP basics (text-image similarity, sliding window object detection)
  - Ch 4.5 (advanced): OWL-ViT for learners with GPU (optional section)
  - Provide performance comparison: CLIP (1-2 FPS CPU, 30 FPS GPU), OWL-ViT (5-10 FPS GPU)
- **Localization Approach**: Sliding window (divide image into grid, run CLIP on patches, find highest similarity)

**3D Pose Estimation**:
- Input: Bounding box from CLIP + depth image (from RGB-D camera like Intel RealSense)
- Process: Extract depth at bbox center → project to 3D using camera intrinsics → publish to TF
- Library: `ros2-numpy`, `cv_bridge`, `tf2_ros`

---

### 4. Wake-Word Detection Libraries

**Question**: Which wake-word library should learners use to activate voice commands ("Hey Robot")?

**Options Considered**:

1. **Porcupine (Picovoice)**
   - **Pros**: Free tier (3 wake-words), high accuracy (~99%), low latency (<100ms), cross-platform (Linux, Windows, Mac), pre-trained models ("Hey Picovoice"), custom training available
   - **Cons**: Requires API key (free tier), closed-source, custom wake-words require paid plan ($0.50/model)
   - **Use case**: Production-ready, easy setup

2. **Snowboy (Kitt.ai, archived)**
   - **Pros**: Open-source, custom wake-word training (via web interface), free
   - **Cons**: Project archived (2020), no longer maintained, lower accuracy, harder to set up
   - **Use case**: Legacy projects only

3. **Pocketsphinx (CMU Sphinx)**
   - **Pros**: Open-source, free, no API keys, offline
   - **Cons**: Lower accuracy, complex setup (requires phoneme dictionary), CPU-heavy
   - **Use case**: Research, fully offline requirements

4. **Custom VAD (Voice Activity Detection)**
   - **Pros**: Simple (detect speech vs silence), no wake-word needed
   - **Cons**: No keyword filtering (triggers on all speech), high false positives
   - **Use case**: Controlled environments only

**Decision**: **Porcupine as primary, optional Pocketsphinx for offline**
- **Rationale**: Porcupine is easiest to set up, production-grade, free tier sufficient for learning. Snowboy is unmaintained. Pocketsphinx is backup for learners needing offline.
- **Implementation**:
  - Ch 4.3: Porcupine integration with "Hey Robot" wake-word (use built-in "Hey Picovoice" then rename in tutorial)
  - Ch 4.3 (advanced): Pocketsphinx alternative for fully offline setup
- **Audio Flow**: Microphone → Porcupine detection → Whisper transcription (only after wake-word)

---

### 5. State Machine Frameworks for VLA Orchestration

**Question**: Which framework should learners use to orchestrate VLA pipeline (Listening → Planning → Executing → Error)?

**Options Considered**:

1. **py_trees (Behavior Trees)**
   - **Pros**: Modular (composable behaviors), ROS 2 integration (`py_trees_ros`), visualization tool (py_trees_ros_viewer), well-documented, Pythonic
   - **Cons**: Steeper learning curve (behavior tree paradigm), overkill for simple state machines
   - **Use case**: Complex robot behaviors, reusable behavior libraries

2. **SMACH (ROS State Machine)**
   - **Pros**: Simple state machine API, ROS 1 heritage (widely used), introspection/visualization (`smach_viewer`), easy to understand
   - **Cons**: ROS 2 support is experimental (`smach2`), less active development, verbose code
   - **Use case**: Traditional state machines, ROS 1 migration

3. **Custom State Machine (enum + transitions)**
   - **Pros**: No dependencies, full control, lightweight, easy to debug
   - **Cons**: No visualization, no reusable behaviors, manual error handling
   - **Use case**: Simple pipelines, learning state machine concepts

**Decision**: **py_trees as primary, custom state machine for intro**
- **Rationale**: py_trees is modern, ROS 2-native, and teaches valuable behavior tree pattern (used in commercial robots). SMACH is legacy. Custom is good for teaching concepts.
- **Implementation**:
  - Ch 4.7: Custom state machine (manual transitions) to introduce concepts
  - Ch 4.7 (advanced): py_trees behavior tree refactor with visualization
  - Ch 4.8: py_trees fallback nodes for error recovery
- **State Machine Structure**:
  ```
  States: IDLE → LISTENING → PLANNING → GROUNDING → NAVIGATING → EXECUTING → SUCCESS / ERROR
  Transitions: On voice_command → Planning, On plan_ready → Grounding, On error → Recovery
  ```

---

## Implementation Dependencies

### Required Python Packages

```plaintext
# Speech (API-based)
openai>=1.0.0  # Whisper API + GPT-4 API

# Speech (local alternative)
openai-whisper  # Local Whisper
faster-whisper  # Optimized local Whisper

# LLM (API-based)
anthropic>=0.20.0  # Claude API
openai>=1.0.0  # GPT-4 API

# Visual Grounding
openai-clip  # CLIP
torch>=2.0.0  # PyTorch (for CLIP)
torchvision>=0.15.0
transformers>=4.30.0  # For OWL-ViT (optional)

# Wake-Word
pvporcupine>=3.0.0  # Porcupine
# pocketsphinx  # Alternative (offline)

# ROS 2 Integration
rclpy  # ROS 2 Python client
sensor_msgs  # Image messages
geometry_msgs  # Pose messages
tf2_ros  # TF transforms
cv_bridge  # ROS-OpenCV bridge

# State Machine
py_trees>=2.2.0
py_trees_ros>=2.1.0  # ROS 2 integration

# Utilities
numpy
opencv-python
python-dotenv  # .env file management
sounddevice  # Microphone access
```

### Hardware Requirements

- **Minimum**: 16GB RAM, 4-core CPU, USB microphone, internet (for APIs)
- **Recommended**: 16GB RAM, GPU (RTX 2060+, 8GB VRAM), USB microphone, internet
- **Optional**: RGB-D camera (Intel RealSense D435) for 3D pose estimation

### API Keys & Costs

| Service | Purpose | Cost (Estimate) | Free Tier |
|---------|---------|-----------------|-----------|
| OpenAI Whisper | Speech-to-text | $0.006/minute (~$0.36/hour) | No |
| OpenAI GPT-4 | Task planning | $0.01-$0.03/command | $5 credit (new accounts) |
| Anthropic Claude 3 | Task planning (alternative) | $0.015-$0.075/command | No |
| Picovoice Porcupine | Wake-word | Free (up to 3 wake-words) | Yes (3 keywords) |

**Total Cost for Module**: ~$5-10 per learner (completing all exercises)

---

## Security & Privacy Considerations

1. **API Key Management**: All examples use `.env` files (never hardcode keys)
2. **Voice Data Privacy**: Whisper API sends audio to OpenAI servers (mention in docs, offer local alternative)
3. **LLM Safety**: Include prompt instructions to refuse unsafe commands ("Don't execute 'attack' or 'harm'")
4. **Rate Limiting**: Implement basic rate limiting to prevent accidental high API costs
5. **Microphone Permissions**: Code examples check for mic access before recording

---

## Performance Targets

| Component | Latency Target | Throughput Target | Notes |
|-----------|----------------|-------------------|-------|
| Whisper (API) | <2s | N/A | Per 30s audio clip |
| Whisper (local, GPU) | <3s | N/A | Per 30s audio clip |
| LLM Planning | <3s | N/A | Per command |
| CLIP (CPU) | ~500ms | 1-2 FPS | Per frame |
| CLIP (GPU) | ~30ms | 30 FPS | Per frame |
| Wake-Word Detection | <100ms | N/A | Per detection |
| End-to-End VLA | <10s | N/A | Voice → action start |

---

## Alternative Approaches Considered & Rejected

1. **End-to-End Neural VLA (RT-1, RT-2)**: Too advanced, requires massive datasets, not accessible for learners
2. **Multimodal LLMs (GPT-4V)**: High cost, emergent capability, less control over vision pipeline
3. **On-Device LLMs (LLaMA 7B)**: Setup burden, inferior reasoning quality for task planning
4. **Closed-Vocabulary Detection (YOLO only)**: Defeats purpose of open-ended language understanding
5. **SMACH over py_trees**: Less active ROS 2 support, less modern

---

## References

- [OpenAI Whisper Paper (2022)](https://arxiv.org/abs/2212.04356)
- [CLIP Paper (2021)](https://arxiv.org/abs/2103.00020)
- [OWL-ViT Paper (2022)](https://arxiv.org/abs/2205.06230)
- [Behavior Trees in Robotics (py_trees)](https://py-trees.readthedocs.io/)
- [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774)
- [Claude 3 Model Card](https://www.anthropic.com/claude)
- [Picovoice Porcupine Docs](https://picovoice.ai/docs/porcupine/)

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-12-01 | Support both Whisper API and local | API for ease, local for cost/privacy |
| 2025-12-01 | Teach both GPT-4 and Claude | Learner flexibility, avoid vendor lock-in |
| 2025-12-01 | CLIP primary, OWL-ViT advanced | Simplicity for learning, power for production |
| 2025-12-01 | Porcupine for wake-word | Best free tier, production-ready |
| 2025-12-01 | py_trees for state machine | Modern, ROS 2-native, behavior tree pattern |

---

**Status**: ✅ Research complete - ready for Phase 1 (Design)
**Next**: Create data-model.md (chapter structure), contracts/ (code specifications), quickstart.md (setup guide)
