# Educational Content Specification Prompts

## Overview

This directory contains modular specification prompt templates for the **Physical AI &
Humanoid Robotics** course. The templates adapt Spec-Kit Plus's software-focused
spec template for educational content (books, courses, tutorials) using Spec-Driven
Development methodology.

**Key Innovation**: Modular system (base template + module overlays) that maps
educational concepts to software development primitives:

| Educational Concept | Software Equivalent |
|---------------------|---------------------|
| Learning Journeys | User Stories |
| Learning Objectives (Bloom's taxonomy) | Functional Requirements |
| Assessment Criteria | Success Criteria |
| Prerequisites | Dependencies |
| Core Concepts & Terminology | Key Entities |

---

## Directory Structure

```
.specify/templates/educational-content/
├── README.md                        # This file
├── base-module-prompt.md            # Shared template structure
└── modules/
    ├── module-1-ros2.md             # ROS 2 overlay with example chapters
    ├── module-2-gazebo-unity.md     # Gazebo/Unity simulation overlay
    ├── module-3-nvidia-isaac.md     # NVIDIA Isaac overlay
    ├── module-4-vla.md              # Vision-Language-Action overlay
    └── module-5-capstone.md         # Capstone project overlay
```

---

## How to Use

### Step 1: Choose Your Module

Select which module you want to create a specification for:

- **Module 1**: The Robotic Nervous System (ROS 2)
- **Module 2**: The Digital Twin (Gazebo & Unity)
- **Module 3**: The AI-Robot Brain (NVIDIA Isaac)
- **Module 4**: Vision-Language-Action (VLA)
- **Module 5**: Capstone Project - The Autonomous Humanoid

### Step 2: Combine Base + Module Overlay

#### Method A: Manual Combination (Recommended for understanding structure)

1. **Read** `base-module-prompt.md` to understand the template structure
2. **Read** the corresponding module file (e.g., `modules/module-1-ros2.md`)
3. **Merge mentally**: The module overlay pre-fills specific sections marked in the
   base template
4. **Fill remaining `[FILL]` placeholders** with content specific to your book/course

#### Method B: Copy-Paste Combination (Quick start)

1. **Copy** all content from `base-module-prompt.md`
2. **Replace template sections** with pre-filled content from module overlay where
   provided
3. **Fill `[FILL]` placeholders** that remain

**Note**: Module overlays PRE-FILL these sections:
- Module Information (metadata, description, learning goals)
- Learning Journeys (with examples and templates)
- Suggested chapter titles and outlines
- Core concepts & terminology (with examples)
- Cross-module dependencies
- Out of scope

You still need to FILL:
- Remaining chapter details (for chapters beyond examples)
- Additional learning objectives per chapter
- Complete code example specifications
- Complete diagram specifications
- Specific assessments

### Step 3: Run `/sp.specify`

Once you've combined and filled the template:

```bash
# Copy your completed prompt to clipboard, then run:
/sp.specify [paste your combined prompt here]
```

This generates `specs/[module-name]/spec.md` using the Spec-Kit Plus template.

### Step 4: Clarify (if needed)

```bash
/sp.clarify
```

This identifies underspecified sections and asks targeted questions.

### Step 5: Continue SDD Workflow

```bash
/sp.plan      # Generate implementation plan (chapter writing, code creation, diagrams)
/sp.tasks     # Break down into granular tasks
/sp.implement # Execute tasks (write chapters, create examples, generate diagrams)
```

---

## Example Workflow: Module 1 (ROS 2)

### 1. Read the Base Template

Open `base-module-prompt.md` and review sections:
- Module Information (template)
- Learning Journeys (template with Given/When/Then format)
- Chapter Breakdown (template for each chapter)
- Core Concepts & Terminology (template)
- Dependencies, Out of Scope, Quality Checklists

### 2. Read Module 1 Overlay

Open `modules/module-1-ros2.md` and note what's pre-filled:

✅ **Module Information** (all fields filled):
- Module 1: The Robotic Nervous System (ROS 2)
- 12 hours over 4 weeks
- Prerequisites: Basic Python, CLI familiarity
- Target audience: Developers new to ROS 2

✅ **Learning Journeys** (3 complete examples + templates):
- LJ1: ROS 2 Communication Fundamentals (P1) - COMPLETE
- LJ2: Robot Descriptions with URDF (P2) - COMPLETE
- LJ3: Services for Command-Response Patterns (P2) - COMPLETE

✅ **Chapter Breakdown**:
- Chapter 1.1: Introduction to ROS 2 and Physical AI - **COMPLETE EXAMPLE**
- Chapter 1.2: Your First ROS 2 Node - Publishers & Subscribers - **COMPLETE EXAMPLE**
- Chapters 1.3-1.7: Templates with suggested titles

✅ **Core Concepts**: 12 terms pre-filled (ROS 2 Node, Topic, Publisher, Subscriber,
etc.)

✅ **Dependencies**: Within-module and cross-module dependencies documented

✅ **Out of Scope**: Topics deferred (Actions, ROS 1, Hardware, C++)

### 3. Merge and Fill

**What you need to add**:

1. **Complete Chapters 1.3-1.7** using the provided titles and templates from Chapter
   1.1-1.2 as examples:
   - Learning Objectives (Bloom's taxonomy)
   - Content Outline (Introduction, Deep Dive, Hands-On, Summary)
   - Code Examples (with filenames, purpose, expected output, testing)
   - Diagrams (with filenames, alt text, size constraints)
   - Assessments (formative and summative)

2. **Expand Learning Journeys** (optional): Module 1 has 3, you could add 1-2 more if
   needed

3. **Add More Terminology** (optional): 12 terms provided, add more if critical concepts
   missing

### 4. Run Spec Generation

```bash
# Paste your completed prompt into /sp.specify
/sp.specify [your merged Module 1 content]
```

**Expected output**: `specs/module-1-ros2/spec.md` created with all sections filled.

### 5. Review and Clarify

```bash
/sp.clarify
```

If any sections are underspecified, this command asks questions like:
- "Chapter 1.3 learning objectives are missing. What should learners Remember,
  Understand, Apply, Analyze?"
- "Code example for custom messages lacks expected output. What should learners see?"

Answer questions, update spec.

### 6. Generate Plan and Tasks

```bash
/sp.plan   # Creates specs/module-1-ros2/plan.md
           # Includes: chapter writing approach, code example creation,
           # diagram generation, assessment design

/sp.tasks  # Creates specs/module-1-ros2/tasks.md
           # Example tasks:
           # T001: Write Chapter 1.3 content (Introduction, Deep Dive, Hands-On)
           # T002: Create custom message code example (IMU sensor)
           # T003: Design message flow diagram for Chapter 1.3
           # T004: Write formative assessments for Chapter 1.3
```

### 7. Implement

```bash
/sp.implement
```

Executes tasks, writing chapters to `book_frontend/docs/module-1/`, creating code
examples in `book_frontend/static/examples/module-1/`, etc.

---

## Quality Gates

Before running `/sp.specify`, verify:

### Completeness Checklist

- [ ] All `[FILL]` placeholders replaced with actual content
- [ ] Learning objectives use Bloom's taxonomy verbs (Remember, Understand, Apply,
      Analyze, Create)
- [ ] Code examples have:
  - [ ] Absolute file paths from repo root
  - [ ] Expected output specified
  - [ ] Testing instructions provided
- [ ] Diagrams have:
  - [ ] File paths specified
  - [ ] Descriptive alt text (WCAG 2.1 AA)
  - [ ] Size constraints (<200KB)
- [ ] Prerequisites clearly map to prior modules/chapters
- [ ] Constitution compliance checklists completed (Markdown, Accessibility, Code,
      Writing Style)

### After `/sp.specify` Generates Spec

- [ ] Review `specs/[module-name]/spec.md` for completeness
- [ ] Run `/sp.clarify` to identify gaps
- [ ] Verify all sections from template are present:
  - [ ] Module Information
  - [ ] Learning Journeys
  - [ ] Chapter Breakdown (all chapters)
  - [ ] Core Concepts & Terminology
  - [ ] Dependencies
  - [ ] Out of Scope
  - [ ] Quality Standards Checklists

---

## Module Overlay Details

### Module 1: ROS 2 (850 lines)

**Pre-filled**:
- Module metadata (12 hours, prerequisites, audience)
- 3 complete learning journeys with milestones
- **2 fully detailed example chapters** (1.1, 1.2) with code, diagrams, assessments
- 6 suggested chapter titles with outlines (1.3-1.7, mini-project)
- 12 core concepts with definitions and analogies
- Cross-module dependencies
- Out of scope (Actions, ROS 1, Hardware, C++, etc.)

**You add**: Complete details for Chapters 1.3-1.7

---

### Module 2: Gazebo & Unity (550 lines)

**Pre-filled**:
- Module metadata (12 hours, requires Module 1)
- 4 learning journeys (physics simulation, sensors, ros_gz_bridge, Unity optional)
- 8 suggested chapter titles with outlines
- Core concepts (Digital Twin, Gazebo, SDF, Plugins, LiDAR, IMU, etc.)
- Dependencies (requires Module 1 Ch 1.2, 1.5, 1.6)
- Out of scope (Advanced physics, multi-robot, custom plugins)

**You add**: Detailed chapter content, code examples, diagrams

---

### Module 3: NVIDIA Isaac (610 lines)

**Pre-filled**:
- Module metadata (14 hours, requires Modules 1-2, GPU recommended)
- 4 learning journeys (Isaac Sim, synthetic data, Isaac ROS, Nav2)
- 9 suggested chapter titles
- Core concepts (Isaac Sim, USD, Synthetic Data, cuVSLAM, Nav2, TensorRT, etc.)
- Dependencies (requires Module 1 basics, Module 2 simulation concepts)
- Out of scope (Isaac Gym RL, custom GEMs, multi-robot)

**You add**: Detailed chapter content, code examples, diagrams

---

### Module 4: VLA (580 lines)

**Pre-filled**:
- Module metadata (10 hours, requires Modules 1-3, API keys needed)
- 4 learning journeys (Whisper voice, LLM planning, visual grounding, end-to-end
  pipeline)
- 9 suggested chapter titles
- Core concepts (VLA, Whisper, LLM, Prompt Engineering, CLIP, Action Primitives, etc.)
- Dependencies (requires all prior modules)
- Out of scope (End-to-end neural VLA, multimodal LLMs, TTS, advanced manipulation)

**You add**: Detailed chapter content, code examples, diagrams

---

### Module 5: Capstone (580 lines)

**Pre-filled**:
- Module metadata (8-12 hours, requires ALL modules)
- 4 learning journeys (project scoping, incremental integration, error handling,
  documentation)
- 10 chapter structure (proposal, architecture, integration steps, testing,
  documentation, presentation)
- **5 predefined scenarios** (room cleanup, warehouse retrieval, search-rescue, tour
  guide, custom)
- **Assessment rubric** (100 points: proposal 10%, implementation 50%, error handling
  15%, documentation 15%, demo 10%)
- Core concepts (Capstone, Integration Testing, Graceful Degradation, etc.)
- Dependencies (synthesizes all modules)

**You add**: Less content needed—capstone is project-based, not lecture-based. May
add scenario-specific guidance.

---

## Constitution Compliance

All module overlays enforce the 40-rule constitution from
`.specify/memory/constitution.md`:

### Key Rules Embedded

- **Rule II**: Markdown quality (semantic headings, fenced code blocks, 100-char
  wrapping)
- **Rule V**: Accessibility (WCAG 2.1 AA, alt text for all images, 4.5:1 contrast)
- **Rule VI**: Code quality (all examples tested, no hardcoded secrets, meaningful
  names)
- **Rule IX**: Writing style (active voice, second person, acronyms defined)
- **Rule XXX**: Performance (<2s page load, <200KB images, Lighthouse >90)

Each chapter template includes accessibility checklists.

---

## Tips for Success

### 1. Start with Module 1

Module 1 has the most complete examples (Chapters 1.1 and 1.2 fully detailed). Use
these as templates for other chapters and modules.

### 2. Use Bloom's Taxonomy Verbs

**Remember**: define, list, identify, recall
**Understand**: explain, describe, compare, summarize
**Apply**: implement, use, execute, solve
**Analyze**: compare, contrast, debug, diagnose
**Create**: design, build, generate, compose

Each chapter should have 3-5 learning objectives spanning multiple taxonomy levels.

### 3. Fill Code Examples Completely

**Required fields**:
- Filename (absolute path from repo root)
- Language (python, bash, xml, etc.)
- Purpose (what it demonstrates)
- Prerequisites (ROS 2 version, dependencies)
- Expected output (console output, return values)
- Testing (how to verify it works)

**Optional but valuable**:
- Common issues (troubleshooting tips)
- Code snippet (inline, or note to create file)

### 4. Write Descriptive Alt Text

**Bad**: "Diagram of ROS 2"
**Good**: "Diagram showing ROS 2 graph with three nodes: camera_node publishing to
/image_raw topic, object_detector_node subscribing and publishing to /detections,
and robot_controller subscribing to detections. Arrows indicate message flow
direction."

### 5. Define Success Criteria

**For Learning Objectives**: Use Given/When/Then format
- **Given** ROS 2 installed, **When** running turtlesim demo, **Then** learner can
  list nodes with CLI

**For Assessments**: Specify pass rates
- Quiz: 80% pass rate (questions straightforward if chapter completed)
- Coding: 70% pass rate (requires applying multiple concepts)

---

## Troubleshooting

### Problem: `/sp.specify` fails with "Missing required section"

**Solution**: Ensure you've filled all `[FILL]` placeholders. The spec template
requires certain sections to be complete.

### Problem: Too much content, prompt is 2000+ lines

**Solution**: This is expected for Module 1 (combines base 400 lines + overlay 850
lines). Split into multiple `/sp.specify` runs:
1. First run: Module overview + Chapters 1.1-1.3
2. Second run: Chapters 1.4-1.7

### Problem: Don't know what to write for Chapter X

**Solution**: Use examples from Module 1 Chapters 1.1-1.2 as templates. Every chapter
should have:
- Learning Objectives (3-5 using Bloom's taxonomy)
- Content Outline (Intro, Deep Dive, Hands-On, Summary)
- Code Examples (at least 1-2)
- Diagrams (at least 1)
- Assessments (formative + summative)

### Problem: Cross-module dependencies unclear

**Solution**: Check the "Cross-Module Dependencies" section in each overlay:
- Within-module: Which chapters depend on others?
- Cross-module: What does this module require from prior modules?
- Example: Module 2 requires Module 1 Ch 1.2 (pub/sub) and 1.5 (URDF)

---

## Validation

After completing all 5 modules' specs, run cross-module validation:

### Dependency Chain Check

1. Module 1 → Module 2: Verify Module 2's prerequisites align with Module 1's
   outcomes (pub/sub, URDF, RViz2)
2. Module 2 → Module 3: Verify Module 3 builds on simulation concepts from Module 2
3. Module 3 → Module 4: Verify Module 4 uses perception/navigation from Module 3
4. Modules 1-4 → Module 5: Verify capstone scenarios are achievable with prior modules

### Terminology Consistency

Ensure terms introduced in Module 1 (ROS 2 Node, Topic, Publisher, etc.) are used
consistently in later modules (same definitions, no synonyms).

### Difficulty Progression

- Module 1: Foundational (ROS 2 basics)
- Module 2: Intermediate (simulation, building on Module 1)
- Module 3: Advanced (Isaac platform, GPU acceleration)
- Module 4: Advanced (AI integration, LLMs)
- Module 5: Synthesis (all prior knowledge)

---

## Support

For questions or issues:

1. **Review this README** and the plan file at the project root
2. **Check examples**: Module 1 Chapters 1.1-1.2 are complete references
3. **Use `/sp.clarify`**: Identifies missing content automatically
4. **Ask in course forums or project issues**

---

**Template Version**: 1.0
**Created**: 2025-11-30
**Compatible With**: Spec-Kit Plus, Docusaurus v3.x, Physical AI & Humanoid Robotics
course
