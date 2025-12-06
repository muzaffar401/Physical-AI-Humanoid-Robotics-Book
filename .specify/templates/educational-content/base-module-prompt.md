# Base Module Specification Prompt Template

**Instructions**: This is the shared template structure for all educational modules.
Combine this with a module-specific overlay from `modules/` directory before using
with `/sp.specify`.

**Usage**:
1. Copy this base template
2. Merge with module overlay (e.g., `modules/module-1-ros2.md`)
3. Fill any remaining `[FILL]` placeholders
4. Run `/sp.specify [paste combined content]`

---

## Module Information

- **Module Number**: [1-5]
- **Module Title**: [Full module title]
- **Estimated Duration**: [Total hours over number of weeks]
- **Prerequisites**:
  - [Prerequisite 1]
  - [Prerequisite 2]
  - [Add more as needed]
- **Target Audience**: [Description of intended learners: experience level, background]

## Module Description

[2-3 paragraphs describing:
- What this module teaches
- Why it matters in the Physical AI & Humanoid Robotics context
- What learners will be able to do by the end
- Key technologies/concepts covered]

**Key Focus**: [1-2 sentences highlighting the primary learning focus]

## Module Learning Goals

[3-5 high-level learning goals using Bloom's taxonomy action verbs]

1. **Understand**: [Conceptual knowledge goal]
2. **Apply**: [Practical skill goal]
3. **Analyze**: [Critical thinking/comparison goal]
4. **Create**: [Synthesis/design goal (if applicable)]
5. **[Additional goal]**: [Description]

---

## Learning Journeys

<!--
Learning Journeys replace "User Stories" for educational content.
Each journey narrates the learner's progression from novice to mastery in a
specific skill area.

Guidelines:
- Provide 3-5 learning journeys per module
- Priority P1 = foundational (must-know), P2 = intermediate, P3 = advanced
- Use Given/When/Then format for milestones (testable outcomes)
- Each journey should be independently validatable
-->

### Learning Journey [N]: [Journey Title] (Priority: P[1-3])

**Narrative**: [Describe the learner's progression from initial state to mastery.
What do they start with? What do they build? What do they master?]

**Why this priority**: [Explain the foundational importance or prerequisite
relationships. Why is this P1, P2, or P3?]

**Independent Validation**: [How can the learner verify mastery independently
without instructor assessment?]

**Example**: "Learner can [specific action] and observe [specific measurable
result]"

**Learning Milestones** (Given/When/Then format):

1. **Given** [initial state/context], **When** [learner performs action],
   **Then** [observable outcome]
2. **Given** [prerequisite knowledge], **When** [task/exercise], **Then**
   [measurable result]
3. **Given** [tools/resources], **When** [application scenario], **Then**
   [success criteria]
4. [Add 3-5 milestones showing clear progression]

---

### Learning Journey [N+1]: [Journey Title] (Priority: P[1-3])

[Repeat structure above for each learning journey]

**Guidance**: Include 3-5 learning journeys total, covering the major skill
areas in this module.

---

## Chapter Breakdown

<!--
Each chapter represents a focused learning session with clear objectives,
content outline, code examples, diagrams, and assessments.

Structure ensures:
- Bloom's taxonomy alignment
- Accessibility (WCAG 2.1 AA)
- Code quality (tested, runnable)
- Assessment validation
-->

### Chapter [N]: [Chapter Title]

**Duration**: [Hours, e.g., "2 hours"]
**Prerequisites**: [Prior chapters or external knowledge required]

#### Learning Objectives (Bloom's Taxonomy)

- **Remember**: [Factual knowledge - define, list, identify]
- **Understand**: [Conceptual understanding - explain, describe, compare]
- **Apply**: [Practical skill - implement, use, execute]
- **Analyze**: [Critical thinking - compare, contrast, debug]
- **Create**: [Synthesis/design - optional, for advanced chapters]

#### Content Outline

1. **Introduction** ([Duration, e.g., "30 min"])
   - [Topic 1: Hook/motivation]
   - [Topic 2: Real-world context]
   - [Topic 3: Learning objectives preview]

2. **Deep Dive** ([Duration, e.g., "45 min"])
   - [Concept 1: Core technical explanation]
   - [Concept 2: Architecture/components]
   - [Concept 3: How it works under the hood]
   - [Concept 4: Constraints and limitations]

3. **Hands-On Practice** ([Duration, e.g., "60 min"])
   - **Walkthrough**: [Step-by-step guided example]
   - **Exercise 1**: [Structured practice with scaffolding]
   - **Exercise 2**: [Open-ended challenge]
   - **Debugging Practice**: [Intentional error to fix - optional]

4. **Summary & Transition** ([Duration, e.g., "10 min"])
   - [Key takeaways (3-5 bullet points)]
   - [Connection to next chapter]
   - [Optional: Further reading/resources]

#### Code Examples

<!--
Per Constitution Rule VI: All code examples MUST be syntactically valid, tested,
and executable. Distinguish between:
- Complete examples (fully working, tested)
- Exercise templates (starter code with TODO markers)
-->

**Example [N]**: [Brief example description]

- **Filename**: [Absolute path from repo root, e.g.,
  `book_frontend/static/examples/module-1/example-name.py`]
- **Language**: [Python, C++, Bash, XML, etc.]
- **Type**: [Complete example | Exercise template]
- **Purpose**: [What this code demonstrates or teaches]
- **Prerequisites**: [Software, packages, or dependencies needed to run]
- **Expected Output**:
  ```
  [Show expected console output, return values, or results]
  ```
- **Testing**: [How to verify it works - command to run, expected behavior]
- **Common Issues**: [Optional: Known pitfalls or troubleshooting tips]

[Repeat for each code example in the chapter]

#### Diagrams & Media

<!--
Per Constitution Rule VII: Images must be optimized (<200KB), have descriptive
alt text (WCAG 2.1 AA), and use appropriate formats (SVG preferred for
diagrams, WebP/PNG for images).
-->

**Diagram/Image [N]**: [Brief description]

- **Filename**: [Path from repo root, e.g.,
  `static/img/module-1/chapter-name/diagram-name.svg`]
- **Type**: [SVG (preferred for diagrams) | PNG | JPEG | Mermaid (inline)]
- **Alt Text**: [Descriptive alt text for screen readers - be specific about
  what the diagram shows, not just "diagram of X"]
- **Purpose**: [What this visual illustrates or clarifies]
- **Size**: [Must be <200KB per Rule VII]
- **Source**: [Optional: Tool used to create (draw.io, Figma, etc.) and link to
  source file]

[Repeat for each diagram/image in the chapter]

#### Assessments

<!--
Per educational best practices:
- Formative assessments: During learning, low stakes, immediate feedback
- Summative assessments: End of chapter, higher stakes, measures mastery
-->

**Formative Assessments** (during chapter):

- **Self-Check Questions**:
  - [Question 1: Multiple choice or true/false with correct answer]
  - [Question 2: Concept check]
  - [Question 3: Application question]

- **Code Debugging Exercises**:
  - [Exercise 1: "What's wrong with this code?" - provide broken code snippet]
  - [Exercise 2: "Why does this fail?" - diagnostic question]

**Summative Assessments** (end of chapter):

- **Conceptual Quiz**:
  - [5-10 multiple choice questions covering key concepts]
  - **Topics Covered**: [List main topics tested]
  - **Expected Pass Rate**: [e.g., "80% - questions are straightforward if
    chapter was completed"]

- **Coding Challenge**:
  - [Description of coding task that integrates chapter concepts]
  - **Rubric**:
    - [Criterion 1: e.g., "Code runs without errors (40%)"]
    - [Criterion 2: e.g., "Correct output (30%)"]
    - [Criterion 3: e.g., "Code quality and style (20%)"]
    - [Criterion 4: e.g., "Comments and documentation (10%)"]
  - **Expected Pass Rate**: [e.g., "70% - requires applying multiple concepts"]

- **Optional: Project Component**:
  - [If chapter contributes to a larger project, describe the component]

#### Accessibility Checklist (WCAG 2.1 AA Compliance - Constitution Rule V)

Per the project constitution, all content MUST meet accessibility standards:

- [ ] All code blocks have language identifiers (e.g., \`\`\`python)
- [ ] All images and diagrams have descriptive alt text
- [ ] Semantic heading hierarchy maintained (no skipped levels: H1→H2→H3)
- [ ] Color is not the sole means of conveying information
- [ ] Sufficient color contrast (4.5:1 for normal text, 3:1 for large text)
- [ ] Interactive elements are keyboard-navigable
- [ ] No ASCII art in code examples (not screen-reader friendly)
- [ ] Video/audio content has text alternatives (transcripts/captions)

---

[Repeat the Chapter structure above for each chapter in the module]

**Suggested Chapter Count**: 5-7 chapters per module (allows 1.5-2.5 hours per
chapter for 12-hour module)

---

## Core Concepts & Terminology

<!--
Define key terms introduced in this module. This creates a shared vocabulary
for consistency across modules and supports learners with varying backgrounds.
-->

### Key Term Template

For each major concept introduced in this module:

- **Term**: [Concept name]
- **Definition**: [Clear, concise definition in plain language]
- **Analogy**: [Real-world comparison to aid understanding]
- **First Introduced**: [Chapter number where term is first used]
- **Related Terms**: [Connected concepts or prerequisite terms]
- **Code/Usage Example**: [Optional: Brief code snippet or usage context]

**Examples**:

- **Term**: [Fill with actual term from module]
- **Definition**: [Fill]
- **Analogy**: [Fill]
- **First Introduced**: Chapter [N]
- **Related Terms**: [Term 1, Term 2, Term 3]

[Provide 10-15 key terms per module]

---

## Dependencies & Knowledge Flow

<!--
Explicitly document prerequisite relationships to ensure proper learning
sequencing and identify cross-module dependencies.
-->

### Within-Module Dependencies

**Prerequisite Chains**:

- Chapter [N] is foundational; MUST precede [which chapters]
- Chapter [N] requires Chapter [M] because [reason]
- Chapter [N] integrates Chapters [X, Y, Z] concepts

**Example**:
- Chapter 1.1 is the module entry point; all other chapters depend on it
- Chapter 1.5 requires Chapter 1.2 for [specific concept]

### Cross-Module Dependencies

**What This Module Requires** (from prior modules):

- From **Module [N]**: [Specific concepts, chapters, or skills needed]
- Example: "Module 2 requires understanding of ROS 2 pub/sub (Module 1,
  Chapter 1.2) and URDF (Module 1, Chapter 1.5)"

**What This Module Provides** (for future modules):

- For **Module [N+1]**: [Concepts taught here that are prerequisites there]
- Example: "Module 1 provides ROS 2 fundamentals required for Module 2's
  Gazebo integration"

### External Dependencies

**Software Requirements**:

- [Software 1]: [Version, installation notes]
- [Software 2]: [Version, installation notes]
- Example: "ROS 2 Humble (Ubuntu 22.04 recommended, also supports RHEL, macOS,
  Windows via WSL2)"

**Hardware Requirements** (if applicable):

- [Hardware requirement: e.g., "GPU with CUDA support for simulation"]
- [Minimum specs: e.g., "16GB RAM recommended for Isaac Sim"]

**External Accounts** (if applicable):

- [Service/platform: e.g., "NVIDIA Omniverse account (free)"]

---

## Out of Scope

<!--
Explicitly state what is NOT covered to manage learner expectations and prevent
scope creep. Provide rationale for exclusions.
-->

### Explicitly NOT Covered in This Module

- **[Advanced Topic Deferred]**: "[Topic name] - covered in Module [N] because
  [reason]"
- **[Alternative Approach]**: "[Tool/Method] - out of scope because [reason,
  e.g., 'we focus on approach X for consistency']"
- **[Production Concern]**: "[Topic] - this is educational content; production
  topics like [X, Y] are excluded"
- **[Legacy Technology]**: "[Old version/tool] - we focus exclusively on
  [current version] as it's the industry standard"

**Rationale**: [Overall explanation for scope decisions - e.g., "Maintains
focused learning path; avoids overwhelming beginners; aligns with course
objectives"]

---

## Content Quality Requirements (Constitution Compliance)

<!--
All content MUST comply with the 40-rule constitution. Key rules embedded as
checklists for each chapter. Review constitution at
.specify/memory/constitution.md
-->

### Markdown Quality (Constitution Rule II)

- [ ] CommonMark-compliant syntax (no proprietary extensions)
- [ ] Semantic heading hierarchy (H1 for title, H2 for major sections, no
      skipped levels)
- [ ] 100-character line wrapping for readability (except URLs, tables, code)
- [ ] Fenced code blocks with language identifiers (\`\`\`python, \`\`\`bash,
      etc.)
- [ ] Reference-style links for repeated URLs ([label]: url)

### Accessibility Standards (Constitution Rule V - WCAG 2.1 AA)

- [ ] All images and diagrams have descriptive alt text (not just "image of X")
- [ ] Color contrast meets 4.5:1 ratio for normal text, 3:1 for large text
- [ ] Color is not the sole means of conveying information (use labels, icons,
      patterns)
- [ ] Semantic HTML used where markdown is insufficient
- [ ] Keyboard navigation support for all interactive elements
- [ ] Screen reader compatibility (no ASCII art, proper heading structure)
- [ ] Text alternatives for video/audio content

### Code Quality (Constitution Rule VI)

- [ ] All code examples are syntactically valid
- [ ] Code has been tested in the specified environment
- [ ] No hardcoded secrets, credentials, or sensitive data
- [ ] Meaningful variable names (not x, y, foo, bar in production examples)
- [ ] Comments explain WHY, not just WHAT (for complex logic)
- [ ] Exercise templates clearly marked with # TODO: or similar

### Writing Style (Constitution Rule IX)

- [ ] Active voice preferred over passive ("You create" not "A node is
      created")
- [ ] Second person ("you") for direct engagement
- [ ] Acronyms defined on first use (e.g., "ROS 2 (Robot Operating System 2)")
- [ ] Clear, concise, technical language (avoid jargon without explanation)
- [ ] Consistent terminology (use the same term throughout; avoid synonyms)

### Performance Budgets (Constitution Rule XXX)

- [ ] Page load time <2 seconds on 3G connection
- [ ] Images optimized and <200KB each (use WebP format when possible)
- [ ] Lighthouse score >90 for performance, accessibility, SEO
- [ ] Minimal JavaScript (Docusaurus handles this, but avoid custom scripts)

---

## Notes for Spec Authoring

<!--
Guidance for filling out this template via /sp.specify
-->

**When Combining with Module Overlay**:

1. Replace all `[FILL]` and `[N]` placeholders with actual content
2. Module overlays will pre-fill many sections; verify they align with current
   course outline
3. Ensure all learning journeys have Given/When/Then milestones
4. All code examples MUST have filenames, expected outputs, and testing
   instructions
5. All diagrams MUST have alt text and size estimates

**Quality Gates Before Running /sp.specify**:

- [ ] All `[FILL]` placeholders replaced with actual content
- [ ] Learning objectives use Bloom's taxonomy verbs (Remember, Understand,
      Apply, Analyze, Create)
- [ ] Code examples specify absolute file paths from repo root
- [ ] Diagrams specify alt text and size constraints (<200KB)
- [ ] Prerequisites clearly map to prior modules/chapters
- [ ] Constitution compliance checklists completed

**After /sp.specify Generates Spec**:

- Review `specs/[module-name]/spec.md` for completeness
- Run `/sp.clarify` if any sections need refinement
- Proceed to `/sp.plan` for implementation planning (chapter writing, code
  examples, diagram creation)
- Then `/sp.tasks` for granular task breakdown
- Finally `/sp.implement` to execute

---

**Template Version**: 1.0
**Created**: 2025-11-30
**Compatible With**: Spec-Kit Plus methodology, Docusaurus v3.x, Physical AI &
Humanoid Robotics course structure
