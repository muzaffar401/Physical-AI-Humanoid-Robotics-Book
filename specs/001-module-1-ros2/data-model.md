# Data Model: Chapter Structure with Content/Summary Tabs

**Date**: 2025-12-02
**Feature**: Module 1 Content/Summary Tab Interface
**Phase**: Phase 1 - Design

## Overview

This document defines the data structures for Module 1 chapters with dual-view Content/Summary tab interface.

## Chapter Entity

**Entity Name**: Chapter

**Purpose**: Educational content unit covering specific ROS 2 topic, with full content and condensed summary views

**Attributes**:
- `id`: Unique identifier (e.g., "chapter-1-2-pubsub")
- `title`: Full chapter title (e.g., "Chapter 1.2: Publishers & Subscribers")
- `sidebar_position`: Order in sidebar navigation (1-7)
- `duration`: Estimated completion time in hours (e.g., 2.5)
- `prerequisites`: Array of prerequisite chapter IDs
- `learning_objectives`: Array of learning objectives (Bloom's Taxonomy)
- `content`: Full chapter content (all sections, examples, assessments)
- `summary`: Condensed 300-600 word version
- `key_takeaways`: Array of core concepts for summary extraction

**File Format**: MDX (Markdown with JSX support)

**Storage**: `book_frontend/docs/module-1/chapter-{number}-{slug}.mdx`

## Chapter File Structure

```mdx
---
# Frontmatter (YAML)
id: chapter-1-2-pubsub
title: "Chapter 1.2: Publishers & Subscribers"
sidebar_position: 2
---

# JSX Imports
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Tab Component
<Tabs defaultValue="content" groupId="chapter-view">

  <TabItem value="content" label="Content" default>

    # [Full Chapter Content]

    ## Learning Objectives (duration, prerequisites)
    ## Prerequisites
    ## What You'll Build
    ## Introduction
    ## Section 1
    ## Section 2
    ## Hands-On Activity
    ## Code Examples
    ## Diagrams
    ## Assessment
    ## Key Takeaways
    ## What's Next

  </TabItem>

  <TabItem value="summary" label="Summary">

    # [Condensed Summary Content]

    ## Quick Summary
    ### Learning Objectives Recap
    ### Core Concepts
    ### Essential Commands/Code
    ### Key Diagram
    ### Quick Check
    ### Prerequisites for Next Chapter

  </TabItem>

</Tabs>
```

## Summary Content Structure

**Entity Name**: Summary

**Purpose**: Condensed 300-600 word chapter version for quick review

**Template Structure**:

```markdown
## Quick Summary

**Learning Objectives Recap**:
- [Objective 1: action verb + outcome]
- [Objective 2: action verb + outcome]
- [Objective 3: action verb + outcome]
- [Objective 4: action verb + outcome] (optional)

**Core Concepts**:
- **[Term 1]**: [Definition in 2-3 sentences explaining what it is, why it matters, how it works]
- **[Term 2]**: [Definition in 2-3 sentences]
- **[Term 3]**: [Definition in 2-3 sentences]
- **[Term 4]**: [Definition in 2-3 sentences] (optional)
- **[Term 5]**: [Definition in 2-3 sentences] (optional)

**Essential Commands/Code**:
```[language]
# [Command 1 with brief description]
[command or code snippet]

# [Command 2 with brief description]
[command or code snippet]

# [Command 3 with brief description] (optional)
[command or code snippet]
```

**Key Diagram**:
![Diagram description for accessibility](../path/to/diagram.png)
*Caption explaining what diagram shows and why it matters*

**Quick Check**:
- [ ] [Can you perform task 1 or explain concept 1?]
- [ ] [Can you perform task 2 or explain concept 2?]
- [ ] [Can you perform task 3 or explain concept 3?]

**Prerequisites for Next Chapter**:
- [Prerequisite 1: concept or skill from this chapter]
- [Prerequisite 2: tool or environment setup]
- [Prerequisite 3: understanding or capability] (optional)
```

## Word Count Targets by Chapter

| Chapter | Topic | Target Words | Rationale |
|---------|-------|--------------|-----------|
| 1.1 | Introduction to ROS 2 | 400-450 | Conceptual overview, fewer code examples |
| 1.2 | Publishers & Subscribers | 500-550 | Core pattern, needs code examples |
| 1.3 | Custom Messages | 450-500 | Technical topic, .msg syntax |
| 1.4 | Services | 450-500 | Alternative pattern, comparison needed |
| 1.5 | URDF | 550-600 | Complex topic, URDF syntax examples |
| 1.6 | RViz2 | 400-450 | Visualization tool, GUI-focused |
| 1.7 | Mini-Project | 300-400 | Requirements checklist, less explanation |

**Total**: ~3200-3450 words of summary content across all 7 chapters

## Summary Content Guidelines

**Content Extraction Rules**:
1. Read "Key Takeaways" section at end of chapter
2. Expand each Key Takeaway bullet to 2-3 sentences with definition
3. Select 2-3 most critical code examples from chapter (simplify if >10 lines)
4. Include 1-2 key diagrams already present in chapter
5. Create "Quick Check" self-assessment items from learning objectives
6. Identify prerequisites for next chapter from current learning objectives

**Bloom's Taxonomy Constraint**:
- Summary focuses on **Remember** and **Understand** levels
- Avoid **Apply**, **Analyze**, **Create** depth (those belong in full Content)
- Example: "Define publisher and subscriber" (Remember) not "Implement pub/sub system" (Apply)

**Writing Style**:
- Active voice, second person ("you will", not "one should")
- Present tense for concepts ("ROS 2 uses pub/sub")
- Imperative for commands ("Run ros2 topic list")
- Bullet points for lists, definition lists for concepts
- Code blocks with language identifiers for syntax highlighting

## Tab Interface Component

**Component**: Docusaurus `<Tabs>` + `<TabItem>`

**Props Configuration**:
```jsx
<Tabs
  defaultValue="content"           // Content tab active by default
  groupId="chapter-view"           // Syncs selection across chapters
>
  <TabItem
    value="content"
    label="Content"
    default                         // Explicit default marker
  >
    [Full chapter content]
  </TabItem>

  <TabItem
    value="summary"
    label="Summary"
  >
    [300-600 word summary]
  </TabItem>
</Tabs>
```

**Accessibility Attributes** (auto-generated by Docusaurus):
- Container: `role="tablist"`, `aria-orientation="horizontal"`
- Tab buttons: `role="tab"`, `aria-selected="true|false"`, `aria-controls="[panel-id]"`
- Tab panels: `role="tabpanel"`, `aria-labelledby="[tab-id]"`

**CSS Classes** (for custom styling if needed):
- `.tabs-container`: Outer wrapper
- `.tabs__item`: Individual tab button
- `.tabs__item--active`: Active tab
- `.tabItem_node_modules-...`: Tab panel content

## Relationships

**Chapter ↔ Summary**: One-to-one composition
- Summary is part of chapter, not separate entity
- Both stored in same .mdx file
- Summary extracts from chapter's Key Takeaways section

**Chapter ↔ Learning Objectives**: One-to-many
- Each chapter has 3-6 learning objectives
- Objectives inform summary "Learning Objectives Recap"

**Chapter ↔ Key Takeaways**: One-to-many
- Each chapter has 4-8 key takeaways
- Key Takeaways are source for summary Core Concepts

**Chapter ↔ Code Examples**: One-to-many
- Full Content has 5-15 code examples
- Summary includes 2-3 most essential examples (simplified)

## Validation Rules

**Chapter File**:
- ✅ Must have .mdx extension (not .md)
- ✅ Must include tab imports after frontmatter
- ✅ Must wrap content in `<Tabs>` component
- ✅ Must have exactly 2 `<TabItem>` components (Content and Summary)
- ✅ Content tab must have `defaultValue="content"` and `default` prop
- ✅ Must use `groupId="chapter-view"` for persistence

**Summary Content**:
- ✅ Must be 300-600 words (verified with word count tool)
- ✅ Must include all 6 sections: Learning Objectives Recap, Core Concepts, Essential Commands/Code, Key Diagram, Quick Check, Prerequisites for Next Chapter
- ✅ Must extract Core Concepts from Key Takeaways section (consistency)
- ✅ Must include 2-3 code examples maximum (not full listings)
- ✅ Must use Remember/Understand Bloom's levels (not Apply/Analyze)

**Accessibility**:
- ✅ Tab labels must be text ("Content" and "Summary"), not icons only
- ✅ Images must have descriptive alt text
- ✅ Code blocks must have language identifiers for syntax highlighting
- ✅ Focus indicator must be visible (3:1 contrast ratio)

## Example Data Instances

### Chapter 1.2 - Full Data Model

```yaml
id: chapter-1-2-pubsub
title: "Chapter 1.2: Publishers & Subscribers"
sidebar_position: 2
duration: 2.5 hours
prerequisites:
  - chapter-1-1-introduction
learning_objectives:
  - "Define publisher, subscriber, topic, and message in ROS 2 context"
  - "Explain publish-subscribe pattern and its benefits for robotics"
  - "Create Python ROS 2 nodes using rclpy library"
  - "Visualize ROS 2 graph with rqt_graph"
key_takeaways:
  - "ROS 2 uses publish-subscribe pattern for asynchronous communication"
  - "Publishers send messages to topics, subscribers receive from topics"
  - "rclpy is the Python client library for ROS 2"
  - "Topics are typed and use DDS middleware for transport"
  - "rqt_graph visualizes nodes and topics for debugging"
content_sections:
  - "Learning Objectives"
  - "Prerequisites"
  - "What You'll Build"
  - "Introduction to Publish-Subscribe"
  - "Creating Your First Publisher"
  - "Creating Your First Subscriber"
  - "Testing Communication"
  - "Debugging with CLI Tools"
  - "Hands-On Activity"
  - "Assessment"
  - "Key Takeaways"
  - "What's Next"
summary_word_count: 525  # Target: 500-550
code_examples_full: 12
code_examples_summary: 3
diagrams_full: 4
diagrams_summary: 1
```

### Chapter 1.5 - Full Data Model

```yaml
id: chapter-1-5-urdf
title: "Chapter 1.5: Robot Descriptions with URDF"
sidebar_position: 5
duration: 2.5 hours
prerequisites:
  - chapter-1-1-introduction
learning_objectives:
  - "Understand URDF structure and purpose in ROS 2"
  - "Define links and joints in robot models"
  - "Create URDF files for simple robots"
  - "Load URDF in RViz2 for visualization"
key_takeaways:
  - "URDF (Unified Robot Description Format) describes robot morphology"
  - "Links represent rigid bodies, joints represent connections"
  - "Joint types: fixed, revolute, prismatic, continuous"
  - "URDF uses kinematic trees with parent-child relationships"
  - "robot_state_publisher broadcasts TF tree from URDF"
content_sections:
  - "Learning Objectives"
  - "Prerequisites"
  - "What You'll Build"
  - "Introduction to URDF"
  - "URDF Structure and XML Tags"
  - "Links and Visual/Collision Properties"
  - "Joints and Joint Types"
  - "Creating a Simple Robot"
  - "Creating a Robotic Arm"
  - "Hands-On Activity"
  - "Assessment"
  - "Key Takeaways"
  - "What's Next"
summary_word_count: 575  # Target: 550-600
code_examples_full: 8
code_examples_summary: 2
diagrams_full: 5
diagrams_summary: 2
```

## Next Steps

1. ✅ Data model defined
2. Proceed to contracts: Define summary content contract
3. Create quickstart guide for first implementation
4. Validate data model with Chapter 1.2 prototype
