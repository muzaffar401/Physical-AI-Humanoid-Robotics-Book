# Implementation Plan: Module 2 - The Digital Twin (Gazebo & Unity)

**Branch**: `002-module-2-gazebo-unity` | **Date**: 2025-11-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-module-2-gazebo-unity/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Module 2 teaches learners to simulate humanoid robots in digital twins using Gazebo (physics-focused) and Unity (graphics-focused). The module covers physics simulation fundamentals, sensor integration (LiDAR, cameras, IMU), ROS 2 integration via ros_gz_bridge, and high-fidelity rendering. Learners will spawn robots in virtual environments, add sensors, apply forces, stream sensor data to ROS 2, and implement closed-loop control—all before touching physical hardware.

**Technical Approach**: Markdown-based educational content for Docusaurus book, with tested Python ROS 2 code examples, SDF/URDF robot descriptions, and visual diagrams. Content follows concise specification with 3 learning journeys focused on physics simulation (P1), sensor simulation (P1), and ros_gz_bridge integration (P2).

## Technical Context

**Language/Version**: Markdown (CommonMark), Python 3.10+, ROS 2 Humble
**Primary Dependencies**: Docusaurus 3.x, Gazebo Fortress/Garden, ros_gz packages, RViz2, Unity 2021.3 LTS (optional)
**Storage**: Git repository (markdown files, code examples, images), learner workspace for Gazebo simulations
**Testing**: Vale (grammar/style), markdown-link-check, code example validation (syntax + execution), Docusaurus build
**Target Platform**: Web (Docusaurus static site), learner platform: Ubuntu 22.04 (primary) or Windows WSL2
**Project Type**: Educational content (book chapter/module)
**Performance Goals**: <3s page load time, <200KB per image, 60 FPS in Gazebo simulations for learners
**Constraints**: WCAG 2.1 AA compliance, <500 lines per markdown file, all code examples must run successfully
**Scale/Scope**: 7-8 chapters, ~12 hours of learning content, 15-20 code examples, 10-15 diagrams, 2 assessments per chapter

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**✓ Documentation-First Development** (Rule I):
- Specification created (spec.md, 119 lines) with learning journeys, core concepts, dependencies
- Implementation plan follows spec → plan → tasks → implement workflow
- PHR will be created post-planning for traceability

**✓ Markdown Quality Standards** (Rule II):
- MUST use CommonMark-compliant syntax for all chapter files
- MUST maintain semantic heading hierarchy (H1 title, H2 chapters, H3 sections)
- MUST use fenced code blocks with language identifiers (```python, ```xml, ```bash)
- MUST wrap lines at 100 characters (except code blocks, URLs)

**✓ Content Organization & Modularity** (Rule III):
- Structure: `book_frontend/docs/module-2/` with chapters as separate files
- Naming: kebab-case (e.g., `chapter-2-1-introduction.md`, `chapter-2-3-gazebo-plugins.md`)
- Index: `book_frontend/docs/module-2/index.md` as module entry point
- Reusable content: `book_frontend/docs/_partials/ros2-setup.md`, `book_frontend/docs/_partials/gazebo-install.md`
- File size: Each chapter <500 lines (split if needed)

**✓ Accessibility (WCAG 2.1 AA)** (Rule V):
- All images MUST have descriptive alt text (e.g., "Gazebo UI showing wheeled robot with LiDAR scan rays displayed in RViz2")
- Code examples MUST be keyboard-navigable and screen-reader friendly
- Color contrast: 4.5:1 for text, diagrams use accessible color palettes

**✓ Code Examples: Tested & Runnable** (Rule VI):
- All Python/bash code MUST be syntactically valid (checked via linter)
- Examples MUST include expected output and testing instructions
- MUST use realistic names (not `foo`, `bar`)
- MUST include inline comments for ROS 2 concepts
- NO insecure patterns (hardcoded credentials, deprecated APIs)

**✓ Media Guidelines** (Rule VII):
- Images: SVG for diagrams (Gazebo architecture, ros_gz_bridge flow), WebP/PNG for screenshots
- File size: <200KB per image (compress with tools)
- Naming: descriptive (e.g., `gazebo-lidar-rviz2-visualization.svg`)
- Storage: `static/img/module-2/`
- Videos: Link to external hosting (YouTube) for Gazebo demos, DO NOT embed large files

**No violations**: All requirements align with constitution. No complexity exceptions needed.

## Project Structure

### Documentation (this feature)

```text
specs/002-module-2-gazebo-unity/
├── spec.md              # Feature specification (119 lines, completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output: ROS 2/Gazebo best practices, pedagogy research
├── data-model.md        # Phase 1 output: Chapter structure, learning objective taxonomy
├── quickstart.md        # Phase 1 output: Module prerequisites, installation guide
├── contracts/           # Phase 1 output: Code example contracts (inputs, outputs, testing)
│   ├── chapter-2-2-publisher-example.md
│   ├── chapter-2-3-lidar-plugin-example.md
│   └── chapter-2-5-ros-gz-bridge-config.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Educational Content (repository root)

```text
docs/
├── modules/
│   └── module-2/                           # Module 2 content
│       ├── index.md                        # Module overview, prerequisites, learning goals
│       ├── chapter-2-1-introduction.md     # Chapter 2.1: Intro to Digital Twins
│       ├── chapter-2-2-spawning-robots.md  # Chapter 2.2: URDF to Gazebo
│       ├── chapter-2-3-gazebo-plugins.md   # Chapter 2.3: Sensors and Actuators
│       ├── chapter-2-4-building-worlds.md  # Chapter 2.4: Environments and Obstacles
│       ├── chapter-2-5-ros-gz-bridge.md    # Chapter 2.5: ROS 2 Integration
│       ├── chapter-2-6-closed-loop.md      # Chapter 2.6: Sense-Plan-Act
│       ├── chapter-2-7-unity-optional.md   # Chapter 2.7: Unity (optional)
│       ├── chapter-2-8-mini-project.md     # Chapter 2.8: Autonomous Navigation Project
│       └── _category_.json                 # Docusaurus sidebar config
├── _partials/                              # Reusable content
│   ├── ros2-setup.md                       # ROS 2 installation (reused from Module 1)
│   ├── gazebo-install.md                   # Gazebo Fortress installation
│   └── troubleshooting-common-errors.md    # Common Gazebo/ros_gz_bridge errors
└── assets/
    └── module-2/                           # Module-specific assets
        ├── diagrams/                       # SVG diagrams
        │   ├── gazebo-architecture.svg
        │   ├── ros-gz-bridge-flow.svg
        │   └── sensor-plugin-lifecycle.svg
        ├── code/                           # Code examples
        │   ├── chapter-2-2/                # Chapter 2.2 code
        │   │   ├── simple_robot.urdf
        │   │   └── spawn_robot.launch.py
        │   ├── chapter-2-3/                # Chapter 2.3 code
        │   │   ├── robot_with_lidar.urdf
        │   │   └── lidar_subscriber.py
        │   └── chapter-2-6/                # Chapter 2.6 code
        │       └── obstacle_avoidance.py
        └── images/                         # Screenshots (WebP/PNG)
            ├── gazebo-empty-world.webp
            ├── rviz2-lidar-scan.webp
            └── unity-hri-scene.webp

tests/
├── content/                                # Content validation
│   ├── test_markdown_lint.py               # Vale, markdown linting
│   ├── test_links.py                       # Link checker
│   └── test_accessibility.py               # WCAG 2.1 AA checks
└── code_examples/                          # Code example tests
    ├── test_chapter_2_2_urdf.py            # Validate URDF syntax
    ├── test_chapter_2_3_lidar.py           # Test LiDAR plugin code
    └── test_chapter_2_6_obstacle.py        # Test obstacle avoidance logic
```

**Structure Decision**: Educational content (book module) with markdown chapters, reusable partials, and tested code examples. Structure follows Docusaurus conventions with `book_frontend/docs/module-2/` for learner-facing content and `specs/002-module-2-gazebo-unity/` for meta-documentation (spec, plan, tasks). All code examples stored in `book_frontend/docs/assets/module-2/code/` with corresponding test files to ensure runnability.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected. All requirements align with constitution standards for educational content.*

## Phase 0: Research & Best Practices

**Research Topics**:
1. **Gazebo Fortress vs. Garden**: Which version to recommend for ROS 2 Humble learners?
2. **ros_gz_bridge configuration patterns**: Best practices for bidirectional topic bridging
3. **Pedagogy**: Effective sequencing for teaching physics simulation (empty world → forces → collisions)
4. **Unity + ROS integration**: ROS-TCP-Connector setup, when to use Unity vs. Gazebo
5. **Code example testing**: How to validate Gazebo launch files and URDF models in CI
6. **Common learner errors**: Gazebo/ROS 2 integration pitfalls to address proactively

**Deliverable**: `research.md` with:
- Decision: Gazebo Fortress (LTS, stable with ROS 2 Humble)
- Rationale: Garden has newer features but Fortress has better documentation/community support
- Alternatives: Gazebo Classic (rejected: legacy, not ROS 2 native), Isaac Sim (Module 3)
- ros_gz_bridge patterns: Launch file examples, topic remapping strategies
- Pedagogical sequence: Empty world → apply forces → add sensors → bridge topics → closed-loop
- Unity decision: Optional Chapter 2.7 for HRI scenarios, not core requirement
- Testing approach: `gz sim` headless mode for CI, URDF validation with `check_urdf`

## Phase 1: Design & Content Structure

**Prerequisites:** `research.md` complete

### 1. Data Model (Chapter Structure)

**Deliverable**: `data-model.md` with:

**Learning Objective Taxonomy** (Bloom's):
- Chapter 2.1: Remember (define digital twin), Understand (explain benefits)
- Chapter 2.2: Apply (spawn URDF in Gazebo), Analyze (compare URDF vs. SDF)
- Chapter 2.3: Apply (attach LiDAR plugin), Create (custom sensor configuration)
- Chapter 2.4: Create (build warehouse world with obstacles)
- Chapter 2.5: Analyze (debug bridge misconfigurations), Apply (configure bridge)
- Chapter 2.6: Create (obstacle avoidance algorithm), Evaluate (test control loop)
- Chapter 2.7: Evaluate (compare Gazebo vs. Unity trade-offs)
- Chapter 2.8: Create (autonomous navigation mini-project)

**Chapter Dependencies**:
- 2.1 (foundational) → 2.2 (spawning) → 2.3 (sensors) → 2.5 (bridge) → 2.6 (control)
- 2.4 (worlds) independent, can follow 2.2
- 2.7 (Unity) independent, optional
- 2.8 (project) integrates all

**Content Outline per Chapter** (from spec overlay):
- Introduction (10-15%): Real-world motivation, learning objectives preview
- Deep Dive (30-40%): Core concepts, architecture, constraints
- Hands-On Practice (40-50%): Guided walkthrough + 2-3 exercises (guided → open-ended)
- Summary & Transition (5-10%): Key takeaways, connection to next chapter

### 2. API Contracts (Code Examples)

**Deliverable**: `contracts/` directory with example specifications

**Example**: `contracts/chapter-2-3-lidar-plugin-example.md`
```markdown
# Code Example: LiDAR Plugin in Gazebo

**File**: `book_frontend/docs/assets/module-2/code/chapter-2-3/robot_with_lidar.urdf`
**Type**: Complete URDF with Gazebo plugin tags
**Purpose**: Demonstrate attaching 2D LiDAR sensor to wheeled robot for obstacle detection
**Prerequisites**: Chapter 2.2 (spawning robots), ROS 2 Humble, Gazebo Fortress

## Input
- Robot URDF from Chapter 2.2 (simple wheeled robot)
- Gazebo plugin: `libgazebo_ros_ray_sensor.so`

## Expected Output
- Gazebo launches with robot + LiDAR
- `/scan` topic publishes `sensor_msgs/LaserScan` at 10 Hz
- RViz2 displays scan rays in real-time

## Testing Instructions
```bash
# Launch Gazebo with robot
gz sim robot_with_lidar.urdf

# In separate terminal, verify topic
ros2 topic echo /scan

# Visualize in RViz2
ros2 run rviz2 rviz2
# Add LaserScan display, set topic to /scan
```

## Common Issues
- Plugin not found: Ensure `ros-humble-ros-gz` installed
- No `/scan` topic: Check `<plugin>` tag has correct `topicName` parameter
- Scan data all zeros: Robot may be in empty world, add obstacles
```

**Other Contracts**:
- `chapter-2-2-spawn-robot.md`: Spawning URDF in Gazebo
- `chapter-2-5-ros-gz-bridge-config.md`: Bridging `/cmd_vel` from ROS 2 to Gazebo
- `chapter-2-6-obstacle-avoidance.md`: Reading `/scan`, publishing `/cmd_vel`

### 3. Quickstart Guide

**Deliverable**: `quickstart.md` with module prerequisites and setup

**Contents**:
- **Prerequisites**: Module 1 complete (Chapters 1.2, 1.5, 1.6), Python 3.10+, Ubuntu 22.04/WSL2
- **Installation**:
  - Gazebo Fortress: `sudo apt install gz-fortress`
  - ros_gz packages: `sudo apt install ros-humble-ros-gz`
  - Unity (optional): Download from Unity Hub, install ROS-TCP-Connector package
- **Verification**:
  - `gz sim --version` (should show Fortress 7.x)
  - `ros2 pkg list | grep ros_gz` (should list ros_gz_bridge, ros_gz_sim, etc.)
- **Workspace setup**:
  - Create `~/gazebo_ws/src` directory
  - Clone example repository with URDF files
- **Common setup issues**: GPU drivers, Gazebo black screen, ROS 2 sourcing

### 4. Agent Context Update

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude`

**Updates**:
- Add to `CLAUDE.md` or agent-specific file:
  - Module 2 technologies: Gazebo Fortress, ros_gz_bridge, SDF, URDF
  - Educational content patterns: learning journeys, Bloom's taxonomy, hands-on exercises
  - Testing: Vale linting, code example validation, Docusaurus build checks

**Outcome**: `.claude/context.md` updated with Module 2 technologies, preserving existing Module 1 context.

## Phase 1 Outputs Summary

**Files Created**:
1. `research.md` - Gazebo version decision, ros_gz_bridge patterns, pedagogy research
2. `data-model.md` - Chapter structure with Bloom's taxonomy objectives, dependencies
3. `contracts/chapter-2-*.md` - Code example specifications (3-5 examples)
4. `quickstart.md` - Prerequisites, installation, workspace setup
5. Agent context updated with Module 2 technologies

**Phase 1 Complete**: Ready for `/sp.tasks` to generate granular implementation tasks (write Chapter 2.1, create LiDAR example, design assessment quiz, etc.).

## Constitution Re-Check (Post-Design)

**✓ All gates pass**:
- Markdown structure defined (modular chapters, <500 lines each)
- Accessibility ensured (alt text in contracts, WCAG checks in test plan)
- Code examples have clear contracts with testing instructions
- Media guidelines followed (SVG for diagrams, <200KB images)
- No new complexity violations introduced

**Ready for Phase 2 (/sp.tasks)**: Plan approved, proceed to task breakdown.

---

**Next Steps**:
1. Review this plan for completeness
2. Run `/sp.tasks` to generate actionable task list from this plan
3. Implement tasks following red-green-refactor where applicable (write chapter → review → refine)
4. Create PHR for this planning session

**Estimated Effort**:
- Phase 0 (Research): 2-3 hours
- Phase 1 (Design): 3-4 hours
- Phase 2 (Tasks generation): 1 hour
- Implementation (per chapter): 4-6 hours × 8 chapters = 32-48 hours total
