# Quickstart: First Tab Implementation

**Date**: 2025-12-02
**Feature**: Module 1 Content/Summary Tab Interface
**Phase**: Phase 1 - Design
**Audience**: Developers implementing the tab feature

## Overview

This guide walks you through implementing the Content/Summary tab interface for the first time, using Chapter 1.2 as a prototype. Follow these steps to convert a chapter from `.md` to `.mdx` and add the tab structure.

## Prerequisites

Before starting, ensure you have:
- ✅ Node.js 18+ installed (`node --version`)
- ✅ npm or yarn installed (`npm --version`)
- ✅ Git for version control
- ✅ Text editor (VS Code, Sublime, etc.)
- ✅ Docusaurus 3.9.2 already installed in `book_frontend/`
- ✅ Familiarity with Markdown and basic JSX syntax

## Quick Setup (5 minutes)

### Step 1: Navigate to Project
```bash
cd book_frontend/
```

### Step 2: Install Dependencies (if not done)
```bash
npm install
```

### Step 3: Start Development Server
```bash
npm start
```

This will:
- Build the Docusaurus site
- Launch local dev server
- Open browser to `http://localhost:3000`
- Enable hot reload (auto-refresh on file changes)

**Expected Output**:
```
[INFO] Starting the development server...
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

### Step 4: Verify Current State
Navigate to: `http://localhost:3000/module-1/chapter-1-2-pubsub`

You should see the full chapter content without tabs (current .md format).

## First Tab Implementation (30 minutes)

We'll convert Chapter 1.2 (Publishers & Subscribers) as a prototype to validate the approach.

### Step 1: Rename File (1 minute)

In `book_frontend/docs/module-1/`:
```bash
# Rename chapter-1-2-pubsub.md to chapter-1-2-pubsub.mdx
mv chapter-1-2-pubsub.md chapter-1-2-pubsub.mdx
```

**Why MDX?**: JSX components (like tabs) require `.mdx` format. Markdown features still work.

### Step 2: Add Tab Imports (1 minute)

Open `chapter-1-2-pubsub.mdx` and add these imports **after the frontmatter**, **before the content**:

```mdx
---
id: chapter-1-2-pubsub
title: "Chapter 1.2: Publishers & Subscribers"
sidebar_position: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Chapter 1.2: Your First ROS 2 Node - Publishers & Subscribers
[... rest of content ...]
```

**Important**: Imports must come **after** the `---` frontmatter closing and **before** any Markdown content.

### Step 3: Wrap Content in Tabs (5 minutes)

Wrap the **entire chapter content** in tab components:

```mdx
---
id: chapter-1-2-pubsub
title: "Chapter 1.2: Publishers & Subscribers"
sidebar_position: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs defaultValue="content" groupId="chapter-view">
  <TabItem value="content" label="Content" default>

# Chapter 1.2: Your First ROS 2 Node - Publishers & Subscribers

**Duration**: 2.5 hours | **Prerequisites**: Chapter 1.1

## Learning Objectives

[... ALL existing chapter content goes here ...]

## Key Takeaways

- ROS 2 uses publish-subscribe pattern for asynchronous communication
- Publishers send messages to topics, subscribers receive from topics
- rclpy is the Python client library for ROS 2
- rqt_graph visualizes nodes and topics for debugging

  </TabItem>
  <TabItem value="summary" label="Summary">

    {/* Summary content will go here in next step */}

  </TabItem>
</Tabs>
```

**Key Points**:
- `defaultValue="content"`: Content tab active by default
- `groupId="chapter-view"`: Syncs tab selection across chapters
- `default` attribute on Content TabItem: Explicit default marker
- Indentation: Doesn't matter for functionality, but helps readability

### Step 4: Write Summary Content (20 minutes)

Create the summary content extracting from the chapter's "Key Takeaways" section. Target: **500-550 words**.

```mdx
  <TabItem value="summary" label="Summary">

## Quick Summary

**Learning Objectives Recap**:
- Understand publish-subscribe pattern in ROS 2
- Create publisher and subscriber nodes with rclpy
- Debug with ros2 CLI and rqt_graph
- Visualize node communication with rqt_graph

**Core Concepts**:
- **Publisher**: Node that sends messages to a topic (e.g., sensor data, commands). Multiple subscribers can listen to same topic for decoupled, scalable communication.
- **Subscriber**: Node that receives messages from a topic. Executes callback function when message arrives, enabling event-driven, asynchronous architecture.
- **Topic**: Named bus for typed messages (e.g., std_msgs/String, sensor_msgs/Image). Topics use publish-subscribe pattern for loose coupling between nodes.
- **rclpy**: Python client library for ROS 2. Provides Node class, publisher/subscriber APIs, and utilities for building ROS 2 applications.

**Essential Commands**:
```bash
# List all active topics in the system
ros2 topic list

# Show messages being published to /chatter topic
ros2 topic echo /chatter

# Visualize ROS 2 graph with nodes and topics
rqt_graph
```

**Minimal Code Example** (talker.py):
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        msg = String()
        msg.data = 'Hello ROS 2!'
        self.publisher.publish(msg)

rclpy.init()
node = Talker()
rclpy.spin(node)
```

**Key Diagram**:
![ROS 2 publish-subscribe architecture showing talker publishing to topic and listener subscribing](../assets/module-1/pub-sub-diagram.png)
*Publisher and subscriber communicate through named topic without direct connection, enabling modular, decoupled systems*

**Quick Check**:
- [ ] Can you explain the difference between a publisher and subscriber?
- [ ] Can you use ros2 topic echo to inspect messages on a topic?
- [ ] Can you visualize your ROS 2 system with rqt_graph?

**Prerequisites for Next Chapter** (1.3: Custom Messages):
- Understand how topics and messages work from this chapter
- Have a working publisher/subscriber node pair (talker/listener)
- Be comfortable with rclpy Node class and basic APIs

  </TabItem>
</Tabs>
```

**Word Count Verification**:
- Copy summary content (exclude code blocks and headings)
- Paste into word count tool: https://wordcounter.net/
- Verify: 500-550 words ✅

### Step 5: Test Locally (3 minutes)

Save the file and check your browser (should auto-reload).

**Verify**:
- ✅ Page renders without errors
- ✅ Two tabs visible: "Content" and "Summary"
- ✅ Content tab is active by default (first load)
- ✅ Can click "Summary" tab to see summary
- ✅ Can click "Content" tab to return to full content
- ✅ Images display in both tabs
- ✅ Code syntax highlighting works in both tabs

**If you see errors**:
- Check imports are after frontmatter
- Check `<Tabs>` opening and `</Tabs>` closing tags match
- Check `<TabItem>` tags are properly closed
- Check no extra `#` headings outside TabItem (headings must be inside TabItem)

## Testing Checklist (5 minutes)

After implementing, run through this checklist:

### Functional Tests
- [ ] Both tabs render without errors
- [ ] Content tab is default (active on first load)
- [ ] Can switch between tabs with mouse clicks
- [ ] Tab switching is instant (<1s)
- [ ] Images display in both tabs
- [ ] Code blocks have syntax highlighting
- [ ] No broken links

### Keyboard Accessibility Tests
- [ ] Press Tab key: focus moves to tab list
- [ ] Press Arrow keys: navigate between tabs
- [ ] Press Enter or Space: activates selected tab
- [ ] Focus indicator visible (blue outline)

### Content Quality
- [ ] Summary is 500-550 words (use word count tool)
- [ ] Summary has all 6 required sections
- [ ] Core concepts extracted from Key Takeaways section
- [ ] 2-3 code examples maximum
- [ ] 1-2 diagrams included

## Troubleshooting

### Problem: Page shows blank or error

**Cause**: Syntax error in MDX (unclosed tags, mismatched imports)

**Solution**:
1. Check browser console for errors (F12)
2. Verify imports are correct
3. Ensure all `<Tabs>` and `<TabItem>` tags are closed
4. Check no Markdown headings (`#`) before first `<Tabs>` tag

### Problem: Tabs don't switch

**Cause**: Missing `value` prop or incorrect `defaultValue`

**Solution**:
```jsx
<Tabs defaultValue="content" groupId="chapter-view">
  <TabItem value="content" label="Content" default>
    [content]
  </TabItem>
  <TabItem value="summary" label="Summary">
    [summary]
  </TabItem>
</Tabs>
```

Ensure:
- `defaultValue="content"` matches first TabItem's `value="content"`
- Each TabItem has unique `value` prop

### Problem: Images don't display

**Cause**: Image path incorrect after MDX conversion

**Solution**:
- Verify image path relative to .mdx file location
- Example: `../assets/module-1/diagram.png` (two levels up, then into assets)
- Check image file exists at path

### Problem: Code syntax highlighting missing

**Cause**: Missing language identifier

**Solution**:
```markdown
```python  ← Add language identifier
import rclpy
```
```

Supported identifiers: `python`, `bash`, `xml`, `javascript`, `jsx`, `yaml`

## Next Steps

After successfully implementing Chapter 1.2:

1. **Get Approval**: Show user the working prototype, get feedback
2. **Measure Performance**: Run Lighthouse audit (target: >90 score)
3. **Test Accessibility**: Use NVDA or VoiceOver screen reader
4. **Roll Out**: Convert remaining 6 chapters (1.1, 1.3-1.7) using same process
5. **Document**: Add inline HTML comments linking Summary to Key Takeaways source

## Performance Validation

Run Lighthouse audit to ensure no performance degradation:

1. Open DevTools (F12)
2. Go to "Lighthouse" tab
3. Select "Desktop" mode
4. Click "Generate report"

**Expected Scores**:
- Performance: >90 ✅
- Accessibility: 100 ✅
- Best Practices: >90 ✅
- SEO: >90 ✅

If Performance <90:
- Check image sizes (<200KB each)
- Check no large code blocks (keep summaries concise)
- Verify no infinite loops in code examples

## Helpful Commands

```bash
# Start dev server
npm start

# Build for production
npm run build

# Serve production build locally
npm run serve

# Check for broken links (if installed)
npm run check:links

# Word count (on macOS/Linux)
wc -w chapter-1-2-pubsub.mdx

# Word count (on Windows)
(Get-Content chapter-1-2-pubsub.mdx | Measure-Object -Word).Words
```

## Resources

- [Docusaurus Tabs Documentation](https://docusaurus.io/docs/markdown-features/tabs)
- [MDX Format Guide](https://mdxjs.com/)
- [WCAG 2.1 AA Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Summary Content Contract](./contracts/summary-content-contract.md)
- [Data Model](./data-model.md)

## Questions?

If you encounter issues not covered here:
1. Check browser console for errors (F12)
2. Verify file paths and syntax
3. Review [research.md](./research.md) for Docusaurus tab API details
4. Consult [data-model.md](./data-model.md) for summary structure

---

**Quickstart Status**: ✅ Ready for prototype implementation with Chapter 1.2
**Estimated Time**: 30 minutes for first implementation, 15 minutes for subsequent chapters
