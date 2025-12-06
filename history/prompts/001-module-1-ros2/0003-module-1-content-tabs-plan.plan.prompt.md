---
id: 0003
title: Module 1 Content Tabs Plan
stage: plan
date: 2025-12-02
surface: agent
model: claude-sonnet-4-5
feature: 001-module-1-ros2
branch: 005-module-1-content-tabs
user: user
command: /sp.plan
labels: ["ros2", "docusaurus", "tabs", "planning", "module-1", "accessibility", "mdx"]
links:
  spec: specs/001-module-1-ros2/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-module-1-ros2/plan.md
  - specs/001-module-1-ros2/research.md
  - specs/001-module-1-ros2/data-model.md
  - specs/001-module-1-ros2/quickstart.md
  - specs/001-module-1-ros2/contracts/summary-content-contract.md
tests:
  - Constitution check validation (all principles satisfied ✅)
  - Technical context completeness (all fields specified)
  - Phase 0 research completion (Docusaurus tabs API documented)
  - Phase 1 design completion (data model, contracts, quickstart created)
---

## Prompt

alright now proceed with sp.plan

## Response snapshot

Created comprehensive implementation plan for Module 1 Content/Summary tab interface feature.

**Branch**: `005-module-1-content-tabs`
**Plan File**: `specs/005-module-1-content-tabs/plan.md`

**Planning Highlights**:

1. **Technical Context Defined**:
   - Language: JavaScript (Node.js 18+), MDX (Docusaurus 3.9.2)
   - Dependencies: @docusaurus/preset-classic (includes @theme/Tabs, @theme/TabItem)
   - Testing: Manual functional + accessibility (NVDA/VoiceOver) + Lighthouse audit
   - Performance: <2s page load, <1s tab switching, Lighthouse >90
   - Scope: 7 chapters in Module 1, ~3500 words of summary content

2. **Constitution Check**: ✅ All principles satisfied
   - Simplicity First: Uses built-in Docusaurus components
   - Testable Requirements: Clear acceptance criteria, measurable word counts
   - Accessibility by Design: WCAG 2.1 AA compliance
   - No Premature Optimization: Leverages existing infrastructure
   - Single Source of Truth: Content and Summary in same .mdx file

3. **Phase 0 - Research** (research.md):
   - Docusaurus 3.9.2 has fully-featured tab support built-in
   - @theme/Tabs and @theme/TabItem components from preset-classic
   - ARIA roles and keyboard navigation automatic
   - groupId persistence via localStorage
   - <100ms rendering overhead, no performance impact

4. **Phase 1 - Design**:
   - **Data Model** (data-model.md): Chapter structure with Content/Summary tabs, 6-section summary template, word count targets per chapter (300-600 words)
   - **Contracts** (contracts/summary-content-contract.md): Summary content creation rules, validation checklist, acceptance/rejection criteria
   - **Quickstart** (quickstart.md): Step-by-step guide for first tab implementation with Chapter 1.2 prototype

5. **Phase 2 - Implementation Plan**:
   - Phase 2.1: Prototype Chapter 1.2 (4-6 hours) - validate approach
   - Phase 2.2: Core Chapters 1.1, 1.3, 1.4, 1.5 (12-16 hours)
   - Phase 2.3: Final Chapters 1.6, 1.7 + regression testing (6-8 hours)
   - Phase 2.4: Documentation for future modules (2-4 hours)
   - **Total**: 28-40 hours

6. **Phase 3 - Testing and Validation**:
   - Functional: Tab rendering, switching, persistence, cross-chapter sync
   - Accessibility: Keyboard navigation, screen reader (NVDA/VoiceOver), focus indicator
   - Content Quality: Word counts (300-600), extraction from Key Takeaways, 2-3 code examples max
   - Performance: Lighthouse audit (>90 score), <2s page load, <1s tab switching

7. **Risks and Mitigations**:
   - Breaking existing chapters → Start with prototype, test thoroughly
   - Summary word count miss → Use word count tool, peer review
   - Accessibility issues → Built-in ARIA support, test with screen reader
   - Content sync → Single .mdx file, HTML comments linking sections

8. **Success Criteria**:
   - All 7 chapters converted to .mdx with working tabs
   - All summaries 300-600 words
   - Keyboard-accessible + screen-reader compatible
   - Lighthouse score >90
   - groupId persistence works across chapters

## Outcome

- ✅ Impact: Comprehensive 425-line implementation plan created for Module 1 tab feature, with phased rollout strategy (prototype → core → final → documentation), detailed testing checklists, and risk mitigations
- 🧪 Tests: Constitution check passed (all principles satisfied), technical context complete (no "NEEDS CLARIFICATION" markers), all Phase 0 and Phase 1 deliverables created
- 📁 Files: Created plan.md (425 lines), research.md (Docusaurus tabs research), data-model.md (chapter/summary structures), quickstart.md (first implementation guide), contracts/summary-content-contract.md (validation rules)
- 🔁 Next prompts: `/sp.tasks` to generate granular task breakdown (T001: Convert Ch 1.2, T002: Write Ch 1.2 summary, T003: Test Ch 1.2, etc.), then `/sp.implement` to execute tasks
- 🧠 Reflection: Plan provides clear implementation path with prototype-first approach to validate before full rollout. Strong emphasis on accessibility testing (keyboard + screen reader) and content quality validation (word counts, extraction from Key Takeaways). Phased strategy reduces risk of breaking existing chapters. Constitution check confirms no complexity violations - feature uses built-in Docusaurus capabilities without custom development. Research phase identified zero blockers - all required functionality exists in current installation.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan creation succeeded with all required artifacts
- Graders run and results (PASS/FAIL): Constitution check - PASS (all 6 principles satisfied), Technical context completeness - PASS (all fields specified), Phase 0 research - PASS (comprehensive findings), Phase 1 design - PASS (data model, contracts, quickstart complete)
- Prompt variant (if applicable): N/A (first iteration)
- Next experiment (smallest change to try): Proceed to `/sp.tasks` phase to generate granular task breakdown, then implement prototype with Chapter 1.2 to validate approach before full rollout
