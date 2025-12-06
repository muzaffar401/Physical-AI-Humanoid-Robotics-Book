# Implementation Plan: Module 4 - Vision-Language-Action (VLA)

**Branch**: `004-module-4-vla` | **Date**: 2025-11-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-module-4-vla/spec.md`

**Note**: This template is filled in by the `/sp.plan` command.

## Summary

Module 4 teaches Vision-Language-Action (VLA) integration for Physical AI, enabling robots to understand voice commands, see their environment, reason about tasks via LLMs, and execute actions. Learners will integrate OpenAI Whisper for speech-to-text, GPT-4/Claude for task planning, CLIP for visual grounding, and implement end-to-end voice-controlled robot pipelines with error recovery—orchestrating voice → language → vision → action workflows.

**Technical Approach**: Markdown-based educational content for Docusaurus with tested Python ROS 2 examples, Whisper integration, LLM API calls, CLIP-based visual grounding, and state machine orchestration. Content follows concise specification with 4 learning journeys covering voice-to-text (P1), LLM task planning (P1), visual grounding (P2), and end-to-end VLA pipeline (P2).

## Technical Context

**Language/Version**: Markdown (CommonMark), Python 3.10+, ROS 2 Humble
**Primary Dependencies**: Docusaurus 3.x, OpenAI API (Whisper, GPT-4) OR Anthropic API (Claude 3), CLIP, Porcupine (wake-word), PyTorch
**Storage**: Git repository, learner workspace for VLA projects, API key management (.env files)
**Testing**: Vale, markdown-link-check, code validation, API mock testing, state machine validation
**Target Platform**: Web (Docusaurus), Ubuntu 22.04 (or WSL2), requires microphone, GPU recommended for CLIP
**Project Type**: Educational content (book module)
**Performance Goals**: <3s page load, <200KB images, <2s speech transcription latency, >30 Hz perception
**Constraints**: WCAG 2.1 AA, <500 lines per file, API keys required (paid), all examples work with API mocks
**Scale/Scope**: 9 chapters, ~10 hours content, 18-22 code examples, 10-14 diagrams

## Constitution Check

**✓ All gates pass** - Documentation-first, Markdown quality, Content modularity, Accessibility, Code examples tested (with API mocks), Media guidelines followed, NO hardcoded API keys

## Project Structure

**Documentation**: specs/004-module-4-vla/ (spec, plan, research, data-model, contracts, tasks)
**Content**: book_frontend/docs/module-4/ (9 chapter files, index, _category_.json)
**Assets**: book_frontend/docs/assets/module-4/ (diagrams, Whisper integration code, LLM prompt templates, CLIP examples, state machines, images)
**Tests**: tests/content/ (lint, links, accessibility), tests/code_examples/ (Whisper, LLM mock, CLIP, state machine validation)

## Phase 0: Research

**Topics**: Whisper API vs. local deployment, GPT-4 vs. Claude for robot planning, CLIP vs. OWL-ViT for visual grounding, wake-word libraries, state machine frameworks (SMACH vs. py_trees), API cost management

**Deliverable**: research.md with decisions on Whisper (API for simplicity, local optional), GPT-4/Claude (both supported, user choice), CLIP (simpler than OWL-ViT), Porcupine wake-word, py_trees for state machines

## Phase 1: Design

**Data Model**: Chapter structure with Bloom's taxonomy, dependencies (4.1→4.2-4.3, 4.4, 4.5 requires 4.4, 4.7 requires 4.2+4.4+4.5+4.6)

**Contracts**: Code example specs for Whisper ROS node, LLM task planner, CLIP visual grounding, end-to-end VLA pipeline

**Quickstart**: Prerequisites (Module 1 + Module 2 OR 3), API keys setup (.env), microphone setup, GPU optional

**Agent Context**: Update with VLA technologies (Whisper, GPT-4, Claude, CLIP, prompt engineering, state machines)

## Next Steps

Run `/sp.tasks` for task breakdown, implement chapters, create PHR

**Effort**: Research 2-3h, Design 3-4h, Implementation 36-54h (9 chapters × 4-6h)
