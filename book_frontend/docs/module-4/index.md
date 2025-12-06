# Module 4: Vision-Language-Action (VLA)

## Overview

Welcome to Module 4, where you'll learn to build embodied AI systems that combine **speech recognition**, **language models**, and **computer vision** to enable robots to understand and execute natural language commands. This module represents the cutting edge of Physical AI—systems that can perceive, reason, and act in the physical world.

By the end of this module, you'll build a complete VLA (Vision-Language-Action) pipeline where a humanoid robot responds to voice commands like "Bring me the red mug from the kitchen" by:
1. **Transcribing speech** with OpenAI Whisper
2. **Planning actions** using GPT-4 or Claude
3. **Locating objects** with CLIP vision-language models
4. **Executing tasks** with ROS 2 navigation and manipulation

## What You'll Build

- **Voice-controlled robot interface** using Whisper for real-time speech-to-text
- **AI task planner** that converts natural language to robot action sequences
- **Visual grounding system** that identifies objects from text descriptions
- **Robust VLA pipeline** with error recovery and state machine orchestration
- **Humanoid assistant** that autonomously completes fetch-and-deliver tasks

## Prerequisites

Before starting this module, you should have:

- **Module 1 (ROS 2)**: Publisher/subscriber patterns, ROS 2 nodes, topics
- **Module 2 or 3 (Simulation)**: Gazebo or Isaac Sim experience, robot navigation
- **Python proficiency**: Object-oriented programming, async/await, API usage
- **Hardware**: Microphone (USB or laptop mic), 16GB+ RAM, GPU optional but recommended
- **API Access**: OpenAI API key (Whisper + GPT-4) OR Anthropic API key (Claude 3)

## Module Structure

This module is organized into **4 learning journeys**, each building a core VLA component:

### Learning Journey 1: Voice-to-Text with Whisper (Priority: P1) 🎯
**Chapters 4.1-4.3** | **Goal**: Real-time speech transcription to ROS 2

- Ch 4.1: Introduction to Vision-Language-Action
- Ch 4.2: Speech-to-Text with Whisper
- Ch 4.3: Wake-Word Detection and Audio Processing

**Milestone**: Voice commands published to `/voice_command` topic with under 2 seconds latency

### Learning Journey 2: LLM-Based Task Planning (Priority: P1) 🎯
**Chapter 4.4** | **Goal**: Natural language to structured action plans

- Ch 4.4: LLMs for Cognitive Planning
- Ch 4.4B: Handling Ambiguity and Errors

**Milestone**: LLM generates valid action plans for 90%+ of test commands

### Learning Journey 3: Visual Grounding (Priority: P2)
**Chapters 4.5-4.6** | **Goal**: Text-to-object localization with 3D poses

- Ch 4.5: Visual Grounding with CLIP
- Ch 4.6: 3D Pose Estimation and Action Primitives

**Milestone**: Robot navigates to visually detected objects

### Learning Journey 4: VLA Pipeline Integration (Priority: P2)
**Chapters 4.7-4.8** | **Goal**: End-to-end voice → vision → action with error recovery

- Ch 4.7: VLA Pipeline Integration with State Machines
- Ch 4.8: Error Recovery and Robustness

**Milestone**: Full VLA pipeline recovers from 3+ failure types

### Mini-Project: Voice-Controlled Humanoid Assistant
**Chapter 4.9** | **Capstone**: Fetch-and-deliver tasks in simulated home

**Success Criteria**: 80%+ success rate on 5 fetch tasks, recover from 2+ errors

## API Keys and Cost Transparency

⚠️ **IMPORTANT**: This module requires paid API access to AI services. You have two options:

### Option 1: OpenAI APIs (Recommended for beginners)
- **Whisper API**: ~$0.006/minute of audio (~$0.10-$0.50 for entire module)
- **GPT-4 Turbo**: ~$0.01-$0.10 per command (~$3-$5 for entire module)
- **Total estimated cost**: $5-$10 for all exercises and mini-project

### Option 2: Anthropic Claude + Local Whisper
- **Claude 3 Sonnet**: ~$0.015 per command (~$3-$5 for entire module)
- **Local Whisper**: Free but requires 16GB+ RAM and slower processing
- **Total estimated cost**: $3-$5 (no Whisper API fees)

### Free Alternatives (Lower Quality)
- **Local Whisper**: Works on CPU but 5-10x slower than API
- **Open-source LLMs**: Llama 3, Mistral (lower planning quality, requires GPU)

All code examples use `.env` files for API keys—**never hardcode secrets**. See [API Keys Setup](../partials/api-keys-setup.md) for configuration instructions.

## Learning Outcomes

By completing this module, you will be able to:

1. **Integrate speech recognition** into ROS 2 systems with Whisper API or local models
2. **Design LLM prompts** for robot task planning with GPT-4 or Claude
3. **Implement visual grounding** using CLIP to match text queries to image regions
4. **Build VLA pipelines** that orchestrate voice → vision → action workflows
5. **Handle failures gracefully** with retry logic, replanning, and error recovery
6. **Apply ethical AI principles** to embodied systems (safety, privacy, transparency)

## Ethical AI Guidelines

As you build VLA systems, remember:

- **Safety First**: Never execute commands that could harm people, property, or the robot
- **Privacy**: Audio data contains sensitive information—handle recordings securely
- **Transparency**: Users should know when they're interacting with an AI system
- **Cost Awareness**: API calls cost money—warn users about rate limits and expenses
- **Bias Awareness**: LLMs and CLIP models may exhibit biases—validate outputs critically

See [LLM Safety Guidelines](../partials/llm-safety-guidelines.md) for detailed best practices.

## Hardware Requirements

### Minimum (Works but slow)
- **Microphone**: Any USB microphone or laptop built-in mic
- **RAM**: 8GB (API-only approach, no local Whisper)
- **GPU**: None (CLIP runs on CPU at ~5-10 FPS)
- **Internet**: Stable connection for API calls

### Recommended (Smooth experience)
- **Microphone**: USB condenser mic for better accuracy
- **RAM**: 16GB+ (for local Whisper if desired)
- **GPU**: NVIDIA RTX 2060+ or equivalent (CLIP runs at 30+ FPS)
- **Internet**: Stable connection with low latency (&lt;100ms)

## Getting Help

- **Issues with API keys**: Check your `.env` file and ensure keys are properly configured (see Chapter 4.1)
- **Speech recognition problems**: Check microphone permissions and audio levels
- **LLM not generating valid plans**: Review prompt engineering in Chapter 4.4
- **CLIP detection failures**: Verify image quality and try different query phrasings
- **ROS 2 integration issues**: Review Module 1 fundamentals on publishers/subscribers

## Module Navigation

- **Next**: [Chapter 4.1: Introduction to Vision-Language-Action](./chapter-4-1-introduction)
- **Previous**: [Module 3: Simulation with Isaac Sim](../module-module-3/

---

**Estimated Time**: 12 hours over 4 weeks (3 hours/week)
**Difficulty**: Advanced
**Prerequisites**: Modules 1, 2 or 3
**API Costs**: $5-$10 for completion

Let's begin your journey into embodied AI! 🤖🎤🔍
