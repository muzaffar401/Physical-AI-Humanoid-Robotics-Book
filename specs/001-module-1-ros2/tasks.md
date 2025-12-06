# Tasks: Module 1 Content/Summary Tab Interface

**Input**: Design documents from `/specs/001-module-1-ros2/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/summary-content-contract.md

**Tests**: No automated tests requested in specification. Manual testing includes functional, accessibility, and performance validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Docusaurus site**: `book_frontend/docs/module-1/` for chapter files
- **Specs**: `specs/001-module-1-ros2/` for documentation
- All chapter files in same directory, can be modified in parallel with [P] marker

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify development environment and review documentation

- [ ] T001 Verify Node.js 18+ and npm installed for Docusaurus development
- [ ] T002 Navigate to book_frontend/ and run npm install to verify dependencies
- [ ] T003 [P] Review summary content contract in specs/001-module-1-ros2/contracts/summary-content-contract.md
- [ ] T004 [P] Review data model and summary template in specs/001-module-1-ros2/data-model.md
- [ ] T005 [P] Review quickstart guide in specs/001-module-1-ros2/quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Validate existing chapter structure and start development server

**⚠️ CRITICAL**: Must verify chapter files exist and dev server runs before any modifications

- [ ] T006 Verify all 7 chapter files exist in book_frontend/docs/module-1/ (chapter-1-1-introduction.md through chapter-1-7-mini-project.md)
- [ ] T007 Start Docusaurus dev server with npm start in book_frontend/ directory
- [ ] T008 Verify http://localhost:3000 loads and navigate to Module 1 chapters
- [ ] T009 Verify each chapter has a "Key Takeaways" section (source for summary extraction)

**Checkpoint**: Development environment ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Content/Summary Tab Navigation (Priority: P1) 🎯 MVP

**Goal**: Implement tab interface allowing learners to toggle between Content and Summary views in all 7 chapters

**Independent Test**: Open any chapter, verify Content tab shows by default, click Summary tab to see placeholder summary, click Content tab to return. Verify tab selection persists when navigating to another chapter. Test keyboard navigation (Tab/Shift+Tab, Enter/Space).

### Prototype Implementation (Chapter 1.2)

- [ ] T010 [US1] Rename book_frontend/docs/module-1/chapter-1-2-pubsub.md to chapter-1-2-pubsub.mdx
- [ ] T011 [US1] Add tab imports to book_frontend/docs/module-1/chapter-1-2-pubsub.mdx after frontmatter
- [ ] T012 [US1] Wrap existing content in Content TabItem in book_frontend/docs/module-1/chapter-1-2-pubsub.mdx
- [ ] T013 [US1] Add empty Summary TabItem with placeholder text in book_frontend/docs/module-1/chapter-1-2-pubsub.mdx
- [ ] T014 [US1] Verify tabs render correctly at http://localhost:3000/module-1/chapter-1-2-pubsub
- [ ] T015 [US1] Test keyboard navigation (Tab/Shift+Tab, Enter/Space) on Chapter 1.2 tabs
- [ ] T016 [US1] Test groupId persistence by switching to Summary tab, then navigating to another chapter

### Rollout to Remaining Chapters

- [ ] T017 [P] [US1] Convert book_frontend/docs/module-1/chapter-1-1-introduction.md to .mdx and add tab structure
- [ ] T018 [P] [US1] Convert book_frontend/docs/module-1/chapter-1-3-custom-messages.md to .mdx and add tab structure
- [ ] T019 [P] [US1] Convert book_frontend/docs/module-1/chapter-1-4-services.md to .mdx and add tab structure
- [ ] T020 [P] [US1] Convert book_frontend/docs/module-1/chapter-1-5-urdf.md to .mdx and add tab structure
- [ ] T021 [P] [US1] Convert book_frontend/docs/module-1/chapter-1-6-rviz.md to .mdx and add tab structure
- [ ] T022 [P] [US1] Convert book_frontend/docs/module-1/chapter-1-7-mini-project.md to .mdx and add tab structure

### Functional Testing

- [ ] T023 [US1] Verify all 7 chapters render without errors (check browser console)
- [ ] T024 [US1] Verify Content tab is default for all chapters on first load
- [ ] T025 [US1] Verify tab switching works correctly for all chapters
- [ ] T026 [US1] Verify groupId persistence across all chapters
- [ ] T027 [US1] Verify images display in both tabs for all chapters
- [ ] T028 [US1] Verify code syntax highlighting works in both tabs

**Checkpoint**: Tab interface fully functional - learners can toggle between Content and Summary tabs in all 7 chapters

---

## Phase 4: User Story 2 - Summary Content for Quick Review (Priority: P1)

**Goal**: Create 300-600 word summaries for all 7 chapters extracting from Key Takeaways sections

**Independent Test**: Read Summary tab for any chapter, verify it contains core concepts, essential commands (2-3 code examples), key diagrams, and prerequisites for next chapter in 300-600 words.

### Summary Content Creation

- [ ] T029 [P] [US2] Write Chapter 1.1 summary (400-450 words) in book_frontend/docs/module-1/chapter-1-1-introduction.mdx Summary TabItem
- [ ] T030 [P] [US2] Write Chapter 1.2 summary (500-550 words) in book_frontend/docs/module-1/chapter-1-2-pubsub.mdx Summary TabItem
- [ ] T031 [P] [US2] Write Chapter 1.3 summary (450-500 words) in book_frontend/docs/module-1/chapter-1-3-custom-messages.mdx Summary TabItem
- [ ] T032 [P] [US2] Write Chapter 1.4 summary (450-500 words) in book_frontend/docs/module-1/chapter-1-4-services.mdx Summary TabItem
- [ ] T033 [P] [US2] Write Chapter 1.5 summary (550-600 words) in book_frontend/docs/module-1/chapter-1-5-urdf.mdx Summary TabItem
- [ ] T034 [P] [US2] Write Chapter 1.6 summary (400-450 words) in book_frontend/docs/module-1/chapter-1-6-rviz.mdx Summary TabItem
- [ ] T035 [P] [US2] Write Chapter 1.7 summary (300-400 words) in book_frontend/docs/module-1/chapter-1-7-mini-project.mdx Summary TabItem

### Content Quality Validation

- [ ] T036 [US2] Verify all summaries are 300-600 words using word count tool
- [ ] T037 [US2] Verify each summary includes all 6 required sections (Learning Objectives Recap, Core Concepts, Essential Commands/Code, Key Diagram, Quick Check, Prerequisites for Next Chapter)
- [ ] T038 [US2] Verify each summary includes 2-3 code examples maximum
- [ ] T039 [US2] Verify each summary includes 1-2 key diagrams with alt text
- [ ] T040 [US2] Verify summaries extract from existing Key Takeaways sections
- [ ] T041 [US2] Verify all code blocks have language identifiers for syntax highlighting

**Checkpoint**: All summaries complete and meet quality standards - learners can use Summary tabs for quick review

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Comprehensive testing, accessibility validation, performance optimization, and documentation

### Accessibility Testing

- [ ] T042 [P] Test keyboard navigation across all chapters (Tab/Shift+Tab, Enter/Space, arrow keys)
- [ ] T043 [P] Test screen reader compatibility (NVDA on Windows OR VoiceOver on macOS) - verify tab labels announced
- [ ] T044 [P] Verify focus indicator visible on active tab (3:1 contrast ratio)
- [ ] T045 [P] Inspect ARIA attributes in browser DevTools (role="tablist", aria-selected, aria-controls)

### Performance Testing

- [ ] T046 [P] Run Lighthouse audit on Chapter 1.1 (target: Performance >90, Accessibility 100, Best Practices >90, SEO >90)
- [ ] T047 [P] Run Lighthouse audit on Chapter 1.2
- [ ] T048 [P] Run Lighthouse audit on Chapter 1.5 (largest summary)
- [ ] T049 [P] Verify page load time <2 seconds on 10 Mbps connection
- [ ] T050 [P] Verify tab switching <1 second (no layout shift)

### Cross-Browser Testing

- [ ] T051 [P] Test on Chrome latest (tabs, keyboard, performance)
- [ ] T052 [P] Test on Firefox latest (tabs, keyboard, performance)
- [ ] T053 [P] Test on Safari latest (tabs, keyboard, performance)
- [ ] T054 [P] Test on Edge latest (tabs, keyboard, performance)

### Mobile Responsiveness

- [ ] T055 [P] Test on mobile viewport (tabs stack vertically, touch-friendly)
- [ ] T056 [P] Verify tab interface works on iOS Safari
- [ ] T057 [P] Verify tab interface works on Android Chrome

### Documentation

- [ ] T058 [P] Create tab pattern guide in docs/tab-pattern-guide.md documenting implementation approach
- [ ] T059 [P] Document summary writing guidelines for future modules
- [ ] T060 [P] Update project README with tab feature mention (if applicable)
- [ ] T061 [P] Add HTML comments in each chapter linking Summary to Key Takeaways source

### Final Validation

- [ ] T062 Run quickstart validation from specs/001-module-1-ros2/quickstart.md
- [ ] T063 Verify all acceptance scenarios from spec.md User Story 1 pass
- [ ] T064 Verify all acceptance scenarios from spec.md User Story 2 pass
- [ ] T065 Verify all success criteria from spec.md are met (SC-001 through SC-005 for tabs, SC-014 through SC-017 for content)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion (T001-T005) - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion (T006-T009) - No dependencies on US2
- **User Story 2 (Phase 4)**: Depends on US1 completion (T010-T028) - Needs tab structure in place
- **Polish (Phase 5)**: Depends on US1 and US2 completion (T010-T041)

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Implements tab interface
  - Prototype first (T010-T016) before rollout (T017-T022)
  - Rollout tasks (T017-T022) can run in parallel [P]
  - Functional testing (T023-T028) must wait for rollout completion
- **User Story 2 (P1)**: Must start after US1 completion - Needs tab structure to add summaries
  - All summary writing tasks (T029-T035) can run in parallel [P]
  - Content validation (T036-T041) must wait for all summaries complete

### Within Each User Story

**User Story 1 Flow**:
1. Prototype Chapter 1.2 (T010-T016) - sequential, validate approach
2. Rollout to 6 chapters (T017-T022) - parallel [P] after prototype validation
3. Functional testing (T023-T028) - sequential, after rollout complete

**User Story 2 Flow**:
1. Write all summaries (T029-T035) - parallel [P]
2. Validate content quality (T036-T041) - sequential, after all summaries written

### Parallel Opportunities

- **Setup Phase**: T003, T004, T005 can run in parallel (different files)
- **US1 Rollout**: T017-T022 can run in parallel (different chapter files)
- **US2 Summaries**: T029-T035 can run in parallel (different chapter files)
- **Polish Phase**: Most tasks marked [P] can run in parallel:
  - Accessibility tests (T042-T045)
  - Performance audits (T046-T050)
  - Cross-browser tests (T051-T054)
  - Mobile tests (T055-T057)
  - Documentation (T058-T061)

---

## Parallel Example: User Story 1 Rollout

```bash
# After prototype validation (T016), launch all chapter conversions together:
Task T017: "Convert chapter-1-1-introduction.md to .mdx and add tab structure"
Task T018: "Convert chapter-1-3-custom-messages.md to .mdx and add tab structure"
Task T019: "Convert chapter-1-4-services.md to .mdx and add tab structure"
Task T020: "Convert chapter-1-5-urdf.md to .mdx and add tab structure"
Task T021: "Convert chapter-1-6-rviz.md to .mdx and add tab structure"
Task T022: "Convert chapter-1-7-mini-project.md to .mdx and add tab structure"

# All 6 chapters can be converted simultaneously (different files)
```

## Parallel Example: User Story 2 Summaries

```bash
# After tab structure complete (T028), launch all summary writing together:
Task T029: "Write Chapter 1.1 summary (400-450 words)"
Task T030: "Write Chapter 1.2 summary (500-550 words)"
Task T031: "Write Chapter 1.3 summary (450-500 words)"
Task T032: "Write Chapter 1.4 summary (450-500 words)"
Task T033: "Write Chapter 1.5 summary (550-600 words)"
Task T034: "Write Chapter 1.6 summary (400-450 words)"
Task T035: "Write Chapter 1.7 summary (300-400 words)"

# All 7 summaries can be written simultaneously (different files)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005) - 30 minutes
2. Complete Phase 2: Foundational (T006-T009) - 30 minutes
3. Complete Phase 3: User Story 1 (T010-T028) - 8-10 hours
   - Prototype: 2-3 hours
   - Rollout: 4-5 hours (parallel execution: 1-2 hours)
   - Testing: 2 hours
4. **STOP and VALIDATE**: Test tab navigation independently
5. Demo/review if ready (functional tabs without summaries)

**MVP Delivery**: Working tab interface in all 7 chapters (placeholder summaries)

### Incremental Delivery

1. **Sprint 1** (Setup + US1): 10-12 hours
   - Complete Setup + Foundational → Environment ready
   - Complete User Story 1 → Tab interface functional
   - **Deliverable**: Learners can toggle tabs (placeholder summaries)

2. **Sprint 2** (US2): 12-16 hours
   - Complete User Story 2 → All summaries written
   - **Deliverable**: Complete Content/Summary feature ready for learners

3. **Sprint 3** (Polish): 6-8 hours
   - Complete Polish phase → Fully tested and documented
   - **Deliverable**: Production-ready with accessibility validation

**Total Estimated Time**: 28-40 hours (matches plan.md estimate)

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (1 hour)
2. **US1 Prototype** (Developer A): 2-3 hours
3. **After prototype validation, parallel work**:
   - Developer A: T017-T019 (Chapters 1.1, 1.3, 1.4)
   - Developer B: T020-T022 (Chapters 1.5, 1.6, 1.7)
   - **Time saved**: 4-5 hours reduced to 2-3 hours
4. **US1 Testing** (Developer A): 2 hours
5. **US2 Summaries - parallel split**:
   - Developer A: T029-T031 (Chapters 1.1, 1.2, 1.3)
   - Developer B: T032-T035 (Chapters 1.4, 1.5, 1.6, 1.7)
   - **Time saved**: 12-16 hours reduced to 6-8 hours
6. **US2 Validation** (Developer A): 2 hours
7. **Polish - parallel split**:
   - Developer A: Accessibility + Performance
   - Developer B: Cross-browser + Documentation
   - **Time saved**: 6-8 hours reduced to 3-4 hours

**Total with 2 developers**: ~15-20 hours (vs 28-40 hours solo)

---

## Notes

- **[P] tasks**: Different files, can run in parallel safely
- **[Story] label**: Maps task to specific user story for traceability
- **No automated tests**: Spec doesn't request them; manual testing covers functional, accessibility, performance
- **Prototype-first approach**: Validate Chapter 1.2 before rolling out to others (reduces risk)
- **Word count validation**: Use online tool (https://wordcounter.net/) to verify 300-600 words
- **Screen reader testing**: Use NVDA (Windows, free) or VoiceOver (macOS, built-in)
- **Lighthouse audits**: Run from Chrome DevTools → Lighthouse tab
- **Commit strategy**: Commit after each chapter conversion, after each summary written, after each testing phase
- **Checkpoint validation**: Stop at each checkpoint to verify user story works independently
- **Avoid**: Modifying same chapter file simultaneously, skipping prototype validation, exceeding word count limits

---

## Task Count Summary

- **Total Tasks**: 65 tasks
- **Setup Phase**: 5 tasks
- **Foundational Phase**: 4 tasks (BLOCKING)
- **User Story 1 (P1)**: 19 tasks (7 sequential + 6 parallel rollout + 6 testing)
- **User Story 2 (P1)**: 13 tasks (7 parallel summaries + 6 validation)
- **Polish Phase**: 24 tasks (most parallel)

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel (54% of total tasks)

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 = 28 tasks (43% of total) delivers functional tab interface

**Full Feature**: All 65 tasks = Complete Content/Summary tab feature with comprehensive testing and documentation
