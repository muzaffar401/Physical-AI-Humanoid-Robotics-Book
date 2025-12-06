# Contract: Summary Content

**Date**: 2025-12-02
**Feature**: Module 1 Content/Summary Tab Interface
**Phase**: Phase 1 - Design
**Contract Type**: Content Creation and Validation

## Purpose

Define the contract for creating chapter summary content that appears in the Summary tab of each Module 1 chapter.

## Input Specification

**Required Input**:
- Full chapter content (.md or .mdx file)
- "Key Takeaways" section from chapter (typically at end)
- Chapter learning objectives (from beginning of chapter)
- All code examples in chapter
- All diagrams/images in chapter

**Input Format**: Markdown with frontmatter
**Input Location**: `book_frontend/docs/module-1/chapter-{number}-{slug}.md`

## Output Specification

**Required Output**:
- Summary content (300-600 words)
- Markdown format with syntax-highlighted code blocks
- 6 required sections (see Structure below)
- 2-3 code examples maximum
- 1-2 diagrams

**Output Format**: Markdown (embedded in MDX TabItem)
**Output Location**: Same file as input, within `<TabItem value="summary">` component

## Structure Requirements

Summary MUST include exactly these 6 sections in order:

### 1. Learning Objectives Recap
- 3-4 bullet points
- Extract from chapter's "Learning Objectives" section
- Use concise phrasing (5-10 words per bullet)

**Example**:
```markdown
**Learning Objectives Recap**:
- Understand publish-subscribe pattern in ROS 2
- Create publisher and subscriber nodes with rclpy
- Debug with ros2 CLI and rqt_graph
```

### 2. Core Concepts
- 3-5 definition list items
- Extract from "Key Takeaways" section
- Each definition: 2-3 sentences explaining what/why/how
- Use bold for terms

**Example**:
```markdown
**Core Concepts**:
- **Publisher**: Node that sends messages to a topic (e.g., sensor data, commands). Multiple subscribers can listen to same topic for decoupled communication.
- **Subscriber**: Node that receives messages from a topic. Executes callback function when message arrives, enabling event-driven architecture.
- **Topic**: Named bus for messages. Topics are typed (e.g., std_msgs/String) and use publish-subscribe pattern for loose coupling between nodes.
```

### 3. Essential Commands/Code
- 2-3 code examples maximum
- Syntax-highlighted with language identifier (```python, ```bash, ```xml)
- Brief inline comments explaining purpose
- Simplify examples to <10 lines if possible

**Example**:
```markdown
**Essential Commands**:
```bash
# List all active topics
ros2 topic list

# Show messages published to /chatter topic
ros2 topic echo /chatter

# Visualize ROS 2 graph (nodes and topics)
rqt_graph
```
```

### 4. Key Diagram
- 1-2 diagrams from chapter (select most important)
- Descriptive alt text for accessibility
- Caption explaining diagram significance

**Example**:
```markdown
**Key Diagram**:
![ROS 2 publish-subscribe architecture showing talker node publishing to /chatter topic and listener node subscribing](../assets/module-1/pub-sub-diagram.png)
*Publisher and subscriber communicate through named topic without direct coupling*
```

### 5. Quick Check
- 3 self-assessment checklist items
- Phrased as questions starting with "Can you..."
- Focus on key skills from learning objectives

**Example**:
```markdown
**Quick Check**:
- [ ] Can you explain the difference between publisher and subscriber?
- [ ] Can you use ros2 topic echo to inspect messages?
- [ ] Can you visualize your system with rqt_graph?
```

### 6. Prerequisites for Next Chapter
- 2-3 bullet points
- Identify what learner must understand or have from this chapter
- Link concepts to next chapter's topic

**Example**:
```markdown
**Prerequisites for Next Chapter** (1.3: Custom Messages):
- Understand how topics and messages work from this chapter
- Have a working pub/sub node pair (talker/listener)
- Be comfortable with rclpy Node creation
```

## Content Guidelines

### Word Count
- **Minimum**: 300 words
- **Maximum**: 600 words
- **Validation**: Use word count tool (exclude code blocks from count)

### Bloom's Taxonomy Level
- Focus on **Remember** and **Understand** levels
- Avoid **Apply**, **Analyze**, **Create** depth (full Content covers these)
- Example Remember: "Define publisher" ✅
- Example Apply: "Implement publisher with error handling" ❌ (too deep for summary)

### Writing Style
- **Voice**: Active voice, second person ("you will", not "one should")
- **Tense**: Present tense for concepts, imperative for commands
- **Tone**: Clear, concise, educational
- **Formatting**: Bullet points, definition lists, headings

### Code Examples
- **Maximum**: 3 code blocks
- **Length**: <10 lines each (simplify if needed)
- **Language**: Python, bash, or XML (match chapter content)
- **Comments**: Inline comments explaining purpose

### Diagrams
- **Maximum**: 2 diagrams
- **Source**: Select from existing chapter diagrams
- **Alt Text**: Descriptive (not just filename)
- **Caption**: Explain significance in 1 sentence

## Validation Checklist

Before submitting summary content, verify:

**Structure**:
- [ ] Has all 6 required sections in order
- [ ] Learning Objectives Recap: 3-4 bullets
- [ ] Core Concepts: 3-5 definitions, 2-3 sentences each
- [ ] Essential Commands/Code: 2-3 examples max
- [ ] Key Diagram: 1-2 diagrams with alt text
- [ ] Quick Check: 3 questions
- [ ] Prerequisites for Next Chapter: 2-3 bullets

**Content Quality**:
- [ ] Word count: 300-600 words (exclude code blocks)
- [ ] Extracts from Key Takeaways section (not new content)
- [ ] Uses Remember/Understand Bloom's levels
- [ ] All code examples tested on ROS 2 Humble + Ubuntu 22.04
- [ ] Code blocks have language identifiers
- [ ] Images have descriptive alt text

**Writing Style**:
- [ ] Active voice, second person
- [ ] Present tense for concepts
- [ ] No jargon without definitions
- [ ] Consistent formatting (bullets, bold for terms)

**Technical Accuracy**:
- [ ] All concepts match full chapter content
- [ ] No contradictions with full Content tab
- [ ] Commands are correct and tested
- [ ] Prerequisites accurately reflect next chapter needs

## Error Handling

**If summary exceeds 600 words**:
1. Remove least essential concept from Core Concepts
2. Simplify definitions to 2 sentences (not 3)
3. Reduce code examples to 2 (not 3)

**If summary below 300 words**:
1. Expand Core Concepts definitions to 3 sentences
2. Add 4th learning objective if chapter has it
3. Add context to Prerequisites for Next Chapter

**If Key Takeaways section missing**:
1. Extract from chapter Introduction and conclusion sections
2. Identify 4-6 most important concepts
3. Expand to 2-3 sentences each

## Examples

### Good Summary (Chapter 1.2)

Word count: 525 words ✅
Sections: All 6 present ✅
Code examples: 2 (minimal talker.py + commands) ✅
Diagrams: 1 (pub/sub architecture) ✅
Bloom's level: Remember/Understand ✅

### Bad Summary (Hypothetical)

Word count: 750 words ❌ (exceeds 600)
Sections: Missing "Quick Check" ❌
Code examples: 5 (too many) ❌
Diagrams: None ❌
Bloom's level: Includes Apply/Analyze depth ❌ (too advanced for summary)

## Acceptance Criteria

Summary content is accepted when:
1. ✅ Passes all items in Validation Checklist
2. ✅ Word count verified with tool (300-600 words)
3. ✅ Code examples tested on ROS 2 Humble + Ubuntu 22.04
4. ✅ Peer review confirms clarity and accuracy
5. ✅ Renders correctly in Docusaurus (no broken images, correct syntax highlighting)

## Non-Acceptance Criteria

Summary content is rejected when:
1. ❌ Word count outside 300-600 range
2. ❌ Missing any of 6 required sections
3. ❌ More than 3 code examples
4. ❌ No diagrams included
5. ❌ Code examples untested or have errors
6. ❌ Images missing alt text
7. ❌ Content not extracted from Key Takeaways (new content added)
8. ❌ Uses Apply/Analyze Bloom's levels (too advanced)

## Versioning

- **Version**: 1.0
- **Created**: 2025-12-02
- **Last Updated**: 2025-12-02
- **Status**: Active

## References

- [Specification: Module 1 Content/Summary Tabs](../spec.md)
- [Data Model: Chapter Structure](../data-model.md)
- [Bloom's Taxonomy Reference](https://cft.vanderbilt.edu/guides-sub-pages/blooms-taxonomy/)
- [WCAG 2.1 AA - Images Alt Text](https://www.w3.org/WAI/tutorials/images/)

## Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-12-02 | 1.0 | Initial contract creation | AI Agent |
