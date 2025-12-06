# Implementation Tasks: RAG Chatbot

**Feature**: Integrated RAG Chatbot for Physical AI Book
**Branch**: `005-rag-chatbot`
**Generated**: 2025-12-03
**Total Tasks**: 87 (Updated 2025-12-04: Added visual affordance for selection mode)

## Overview

This document breaks down the RAG chatbot implementation into atomic, executable tasks organized by user story. Each user story phase is independently testable and delivers incremental value.

**Technology Stack**:
- **Embeddings**: Hugging Face sentence-transformers (BAAI/bge-base-en-v1.5, 768 dimensions)
- **LLM/Agents**: OpenAI Agents Python SDK with gpt-4o-mini
- **Vector DB**: Qdrant Cloud (768-dim vectors, cosine similarity)
- **Database**: Neon Serverless Postgres (with automatic connection pooling)
- **Backend**: FastAPI with async/await
- **Frontend**: Docusaurus plugin with React components

**Implementation Strategy**: MVP-first (User Story 1 only), then incremental delivery of remaining stories.

---

## Task Summary

| Phase | User Story | Task Count | Status |
|-------|-----------|------------|--------|
| Phase 1 | Setup | 12 | Not Started |
| Phase 2 | Foundational | 8 | Not Started |
| Phase 3 | US1: Quick Content Search (P1) | 18 | Not Started |
| Phase 4 | US2: Selection Mode (P2) | 19 | Not Started |
| Phase 5 | US3: Suggested Questions (P3) | 8 | Not Started |
| Phase 6 | US4: Conversation History (P3) | 10 | Not Started |
| Phase 7 | US5: Response Feedback (P3) | 6 | Not Started |
| Phase 8 | Polish & Cross-Cutting | 6 | Not Started |

**Total**: 87 tasks (9 new tasks added for selection mode visual affordance)

---

## Dependencies & Execution Order

```
Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1 - MVP)
                                         ↓
                    Phase 4 (US2) ← Phase 3 complete
                    Phase 5 (US3) ← Phase 3 complete (independent of US2)
                    Phase 6 (US4) ← Phase 3 complete (independent of US2/US3)
                    Phase 7 (US5) ← Phase 3 complete (independent of US2/US3/US4)
                                         ↓
                    Phase 8 (Polish) ← All user stories complete
```

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1) = 38 tasks = Core chatbot functionality

---

## Phase 1: Setup & Infrastructure

**Goal**: Initialize project structure, dependencies, and development environment.

**Duration Estimate**: 1-2 days

### Tasks

- [ ] T001 Create backend project structure per plan.md (backend/, routers/, services/, models/, scripts/, tests/)
- [ ] T002 Create frontend plugin structure (book_frontend/src/plugins/rag-chatbot/)
- [ ] T003 [P] Create backend/requirements.txt with dependencies (FastAPI, OpenAI Agents Python SDK, sentence-transformers, Qdrant, SQLAlchemy, slowapi)
- [ ] T004 [P] Create backend/.env.template with all required environment variables
- [ ] T005 [P] Create backend/config.py for environment variable management using pydantic-settings
- [ ] T006 [P] Create backend/main.py FastAPI app entry point with CORS middleware
- [ ] T007 [P] Set up Qdrant Cloud account and create `book_content` collection (768 dims for BAAI/bge-base-en-v1.5, cosine)
- [ ] T008 [P] Set up Neon Serverless Postgres database and copy pooled connection string (-pooler suffix)
- [ ] T009 [P] Create backend/models/database.py with SQLAlchemy Base and engine setup
- [ ] T010 [P] Create Alembic configuration in backend/ for database migrations
- [ ] T011 [P] Create initial Alembic migration with chat_sessions, user_queries, chat_responses, user_feedback tables
- [ ] T012 [P] Create backend/.gitignore (venv/, .env, __pycache__, .pytest_cache/)

**Validation**:
- Backend structure matches plan.md
- `pip install -r requirements.txt` succeeds (includes sentence-transformers, OpenAI Agents Python SDK)
- Qdrant collection accessible via Python client with 768-dim vectors
- Neon Serverless Postgres pooled connection succeeds (connection string with -pooler suffix)
- Alembic migration runs successfully

---

## Phase 2: Foundational Components

**Goal**: Build shared infrastructure required by all user stories (database models, core services, API scaffolding).

**Duration Estimate**: 2-3 days

**Blocking**: Must complete before any user story implementation.

### Tasks

- [ ] T013 Implement ChatSession model in backend/models/database.py (SQLAlchemy ORM)
- [ ] T014 Implement UserQuery model in backend/models/database.py with mode validation
- [ ] T015 Implement ChatResponse model in backend/models/database.py with JSONB source_chunks
- [ ] T016 Implement UserFeedback model in backend/models/database.py with unique constraint
- [ ] T017 Create Pydantic schemas in backend/models/schemas.py (ChatQueryRequest, ChatResponse, FeedbackRequest)
- [ ] T018 Implement QdrantService in backend/services/qdrant_service.py (search, upsert, create_indices)
- [ ] T019 Implement embedding service in backend/services/embedding_service.py using sentence-transformers (BAAI/bge-base-en-v1.5 model)
- [ ] T019b Implement OpenAI Agents service in backend/services/agent_service.py using OpenAI Agents Python SDK (Agent and Runner classes)
- [ ] T020 Implement rate limiting middleware in backend/middleware/rate_limiter.py using slowapi (10 req/min)

**Validation**:
- All models have correct relationships and constraints
- Pydantic schemas validate selection mode correctly (selected_text required if mode='selection')
- QdrantService can connect to cloud instance
- EmbeddingService can generate 768-dim vectors using sentence-transformers
- AgentService can generate responses using OpenAI Agents SDK
- Rate limiter returns 429 after 10 requests

---

## Phase 3: User Story 1 - Quick Content Search and Answers (P1)

**Goal**: Implement core RAG chatbot functionality - users can ask questions and receive answers with citations.

**Why P1**: This is the MVP - the core value proposition of the chatbot. All other features depend on this working.

**Independent Test**: Open chatbot with Ctrl+K, ask "What is URDF?", verify response includes answer + citations to Module 1, Chapter 1.5.

**Duration Estimate**: 1 week

### Tasks

#### Backend - Content Ingestion
- [ ] T021 [US1] Create markdown parser in backend/scripts/ingest_content.py using markdown-it-py
- [ ] T022 [US1] Implement text chunking logic in ingest_content.py using LangChain RecursiveCharacterTextSplitter (500-1000 tokens, 100 overlap)
- [ ] T023 [US1] Implement metadata extraction from frontmatter (module_number, chapter_number, section_title)
- [ ] T024 [US1] Implement batch embedding generation for chunks using EmbeddingService (sentence-transformers model.encode())
- [ ] T025 [US1] Implement Qdrant batch upsert with payload (chunk_id, content_text, metadata, last_updated)
- [ ] T026 [US1] Add progress logging and error handling to ingestion script
- [ ] T027 [US1] Create verification script backend/scripts/verify_chunks.py (check chunk count, sample queries)
- [ ] T027b [FR-006] Implement incremental re-ingestion in ingest_content.py (detect changed files by comparing file modification timestamps or content hashes, re-embed only changed content, delete stale chunks)

#### Backend - RAG Service
- [ ] T028 [US1] Create RAGService in backend/services/rag_service.py with embed_query method (uses EmbeddingService)
- [ ] T029 [US1] Implement semantic_search method in RAGService (calls QdrantService, returns top 10 chunks)
- [ ] T030 [US1] Implement construct_prompt method in RAGService (system + context + query for OpenAI Agents)
- [ ] T031 [US1] Implement generate_answer method in RAGService (calls AgentService with OpenAI Agents SDK, returns response + source_chunks)
- [ ] T032 [US1] Implement DatabaseService in backend/services/database_service.py (CRUD for sessions, queries, responses)

#### Backend - API Endpoints
- [ ] T033 [US1] Implement POST /api/session endpoint in backend/routers/session.py (create new session)
- [ ] T034 [US1] Implement GET /api/health endpoint in backend/routers/health.py (status, version, timestamp)
- [ ] T035 [US1] Implement POST /api/chat endpoint in backend/routers/chat.py for full_book mode (validate, call RAGService, save to DB, return response)
- [ ] T036 [US1] Add error handling and validation to /api/chat (400 for validation errors, 500 for server errors)

#### Frontend - Chat Widget UI
- [ ] T037 [P] [US1] Create ChatWidget component in book_frontend/src/plugins/rag-chatbot/components/ChatWidget.tsx (collapsible, portal-rendered)
- [ ] T038 [P] [US1] Create ChatMessage component for rendering user/bot messages with markdown support (react-markdown)
- [ ] T039 [P] [US1] Create ChatInput component with text input and submit button
- [ ] T040 [P] [US1] Create CitationLink component for clickable citations (navigates to chapter URL)
- [ ] T041 [P] [US1] Implement useChat hook in hooks/useChat.ts (manages chat state, messages array, loading state)
- [ ] T042 [P] [US1] Implement useKeyboard hook in hooks/useKeyboard.ts (detects Ctrl+K/Cmd+K to open chat)
- [ ] T043 [P] [US1] Create chatClient.ts in api/ (fetch wrapper for POST /api/chat, POST /api/session)
- [ ] T044 [P] [US1] Create chat.module.css with responsive styles (desktop, tablet, mobile)
- [ ] T045 [US1] Register plugin in book_frontend/src/plugins/rag-chatbot/index.tsx (Docusaurus plugin API)
- [ ] T046 [US1] Update docusaurus.config.ts to load rag-chatbot plugin

#### Integration & Testing
- [ ] T047 [US1] Run content ingestion script on book_frontend/docs/ using sentence-transformers (verify ~500+ chunks with 768-dim embeddings ingested)
- [ ] T048 [US1] Manual test: Open chat with Ctrl+K, ask "What is ROS 2?", verify response and citations

**Acceptance Criteria**:
- ✅ User can press Ctrl+K to open chat widget
- ✅ User can type question and submit
- ✅ Chatbot responds within 3 seconds with answer
- ✅ Response includes clickable citations to relevant chapters
- ✅ Citations navigate to correct book pages
- ✅ Out-of-scope questions receive polite "not covered" response

---

## Phase 4: User Story 2 - Context-Specific Help (Selection Mode) (P2)

**Goal**: Enable users to select text on page and ask questions about the selection (no vector search, direct LLM query). Includes visual affordance (floating "Ask AI" button) for better discoverability.

**Why P2**: Enhances UX by providing context-specific help. Depends on US1 (core chat working).

**Independent Test**: Select code example on page, click floating "Ask AI" button, verify chat opens in selection mode and response only references selected text.

**Duration Estimate**: 4-5 days (includes visual affordance for better UX)

### Tasks

#### Backend - Selection Mode Support
- [ ] T049 [US2] Update POST /api/chat endpoint to handle mode='selection' (skip vector search, use selected_text as context)
- [ ] T050 [US2] Update RAGService.generate_answer to support selection mode (different prompt construction)
- [ ] T051 [US2] Add validation in Pydantic schema: selected_text required if mode='selection', null if mode='full_book'
- [ ] T052 [US2] Create POST /api/chat/selection convenience endpoint in backend/routers/chat.py

#### Frontend - Selection Detection
- [ ] T053 [P] [US2] Create SelectionDetector component in components/SelectionDetector.tsx (listens to window.getSelection())
- [ ] T054 [P] [US2] Implement useSelection hook in hooks/useSelection.ts (tracks selected text, clears on blur)
- [ ] T055 [US2] Update ChatWidget to show "Ask about your selection" mode indicator when text selected
- [ ] T056 [US2] Update chatClient.ts to send mode='selection' and selected_text when selection active
- [ ] T057 [US2] Update ChatInput placeholder text based on mode (full_book vs selection)

#### Frontend - Selection Visual Affordance (Discoverability Enhancement)
- [ ] T058a [P] [US2] Create SelectionPopup component in components/SelectionPopup.tsx (floating button that appears near selected text)
- [ ] T058b [P] [US2] Implement popup positioning logic using Range.getBoundingClientRect() to place button near selection (handle top/bottom/left/right overflow)
- [ ] T058c [P] [US2] Add "Ask AI about this" button to SelectionPopup with icon (message bubble or sparkle icon)
- [ ] T058d [P] [US2] Implement click handler: clicking popup button opens ChatWidget in selection mode with selected text pre-loaded
- [ ] T058e [P] [US2] Handle edge cases: hide popup on scroll, window resize, selection clear, or click outside selection
- [ ] T058f [P] [US2] Add CSS animations for popup (fade in/out, smooth positioning transitions)
- [ ] T058g [P] [US2] Add minimum selection length threshold (e.g., 10 characters) before showing popup to avoid noise
- [ ] T058h [P] [US2] Test popup on mobile devices (touch selection) and adjust positioning for viewport constraints

#### Testing
- [ ] T058 [US2] Manual test: Select text, open chat with Ctrl+K, ask question, verify response only uses selection
- [ ] T058i [US2] Manual test: Select text, verify popup appears near selection, click popup button, verify chat opens in selection mode

**Acceptance Criteria**:
- ✅ When text is selected (>10 chars), a floating "Ask AI" button appears near the selection
- ✅ Clicking the floating button automatically opens chat widget in selection mode with selected text
- ✅ Chat widget shows "selection mode" indicator when opened via floating button
- ✅ Question submitted in selection mode receives response based only on selected text
- ✅ Clearing selection hides the floating button and returns chat to full book mode
- ✅ Selection mode works on code blocks and regular text
- ✅ Floating button repositions correctly on scroll, window resize, and viewport constraints
- ✅ Ctrl+K shortcut still works as alternative way to open chat in selection mode

---

## Phase 5: User Story 3 - Learning Through Suggested Questions (P3)

**Goal**: Show 3-5 suggested starter questions when chat first opens to reduce onboarding friction.

**Why P3**: Nice-to-have UX enhancement. Depends on US1 (core chat working).

**Independent Test**: Open chat as new user, verify 3-5 suggested questions appear, click one, verify it submits automatically.

**Duration Estimate**: 2-3 days

### Tasks

#### Backend - Suggested Questions
- [ ] T059 [P] [US3] Create suggested_questions table in Postgres (question_text, category, display_order)
- [ ] T060 [P] [US3] Seed suggested questions via Alembic migration ("What will I learn in Module 1?", "What are prerequisites?", etc.)
- [ ] T061 [US3] Implement GET /api/suggested-questions endpoint in backend/routers/chat.py (returns 3-5 questions, optionally filtered by category)

#### Frontend - Suggested Questions UI
- [ ] T062 [P] [US3] Create SuggestedQuestions component in components/SuggestedQuestions.tsx (renders clickable chips)
- [ ] T063 [US3] Update ChatWidget to show SuggestedQuestions on first open (hide after user types or clicks)
- [ ] T064 [US3] Implement question chip click handler (auto-submits question)
- [ ] T065 [US3] Store "first visit" flag in localStorage to show different questions for returning users

#### Testing
- [ ] T066 [US3] Manual test: Open chat, verify suggested questions appear, click one, verify auto-submission

**Acceptance Criteria**:
- ✅ First-time users see 3-5 suggested questions when opening chat
- ✅ Clicking a question submits it automatically
- ✅ Suggested questions disappear after user starts typing
- ✅ Returning users see different suggested questions (or none)

---

## Phase 6: User Story 4 - Conversation History and Follow-ups (P3)

**Goal**: Maintain conversation context so users can ask follow-up questions without repeating context.

**Why P3**: Enables natural conversation flow. Depends on US1 (core chat working).

**Independent Test**: Ask "What is ROS 2?", then "How is it different from ROS 1?", verify second response understands "it" refers to ROS 2.

**Duration Estimate**: 3-4 days

### Tasks

#### Backend - Conversation Context
- [ ] T067 [US4] Update RAGService.generate_answer to accept conversation_history parameter (list of previous query/response pairs)
- [ ] T068 [US4] Implement construct_prompt_with_history method in RAGService (includes last 3-5 exchanges in prompt)
- [ ] T069 [US4] Update POST /api/chat to fetch conversation history from DatabaseService based on session_id
- [ ] T070 [US4] Add conversation_history field to chat_sessions table (JSONB array of {role, content} objects)
- [ ] T071 [US4] Update DatabaseService to append new messages to conversation_history on each exchange

#### Frontend - History Management
- [ ] T072 [P] [US4] Update useChat hook to maintain messages array in React state
- [ ] T073 [P] [US4] Persist conversation history to localStorage (with size limit + LRU eviction)
- [ ] T074 [US4] Load conversation history from localStorage on chat widget mount
- [ ] T075 [US4] Implement "Clear History" button in ChatWidget (clears localStorage and backend session)

#### Testing
- [ ] T076 [US4] Manual test: Ask question, then follow-up with pronoun, verify context maintained

**Acceptance Criteria**:
- ✅ Follow-up questions with pronouns ("it", "that") are understood
- ✅ Conversation history persists across page navigation (same session)
- ✅ Conversation history persists across browser close/reopen (localStorage)
- ✅ User can manually clear conversation history

---

## Phase 7: User Story 5 - Response Quality Feedback (P3)

**Goal**: Allow users to rate responses with thumbs up/down and optional text feedback for quality improvement.

**Why P3**: Enables continuous improvement. Depends on US1 (core chat working).

**Independent Test**: Receive chatbot response, click thumbs down, enter feedback text, verify feedback recorded in database.

**Duration Estimate**: 2 days

### Tasks

#### Backend - Feedback Collection
- [ ] T077 [P] [US5] Implement POST /api/feedback endpoint in backend/routers/feedback.py (validate, insert to user_feedback table)
- [ ] T078 [P] [US5] Add unique constraint validation (prevent duplicate feedback for same response)
- [ ] T079 [US5] Implement GET /api/analytics/feedback endpoint for retrieving feedback stats (positive rate, total count)

#### Frontend - Feedback UI
- [ ] T080 [P] [US5] Create FeedbackButtons component in components/FeedbackButtons.tsx (thumbs up/down icons)
- [ ] T081 [US5] Update ChatMessage component to show FeedbackButtons below bot responses
- [ ] T082 [US5] Implement feedback submission (on thumbs down, show optional text input modal)
- [ ] T083 [US5] Show success message after feedback submitted, disable buttons to prevent duplicates

#### Testing
- [ ] T084 [US5] Manual test: Click thumbs up, verify recorded; click thumbs down, enter text, verify recorded

**Acceptance Criteria**:
- ✅ Thumbs up/down buttons appear below each bot response
- ✅ Clicking thumbs down shows optional text feedback input
- ✅ Feedback is recorded in database with response_id, rating, timestamp
- ✅ Duplicate feedback is prevented (buttons disabled after submission)

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Finalize deployment, monitoring, documentation, and polish UX.

**Duration Estimate**: 3-4 days

### Tasks

#### Deployment
- [ ] T085 Create Render Web Service config (root: backend/, build: pip install, start: uvicorn)
- [ ] T086 Configure Render environment variables (OPENAI_API_KEY, QDRANT_URL, DATABASE_URL, CORS_ORIGINS)
- [ ] T087 [P] Update book_frontend/docusaurus.config.ts with production backend URL
- [ ] T088 [P] Build frontend (npm run build) and deploy to GitHub Pages (npm run deploy)

#### Monitoring & Logging
- [ ] T089 [P] Set up Sentry Free Tier for error tracking (backend/config.py Sentry DSN)
- [ ] T090 [P] Add structured logging to RAGService (log query, response_time, source_chunks)

#### Documentation
- [ ] T091 Create README.md in backend/ with setup instructions (reference quickstart.md)
- [ ] T092 Create README.md in book_frontend/src/plugins/rag-chatbot/ with plugin usage

#### Polish
- [ ] T093 [P] Add loading spinner to ChatWidget while waiting for response
- [ ] T094 [P] Add error message display in ChatWidget for API errors (with retry button)
- [ ] T095 [P] Add typing indicator animation ("Bot is typing...")
- [ ] T096 Test on mobile browsers (Chrome, Safari) and fix any responsive issues

**Validation**:
- Backend deployed to Render and accessible
- Frontend deployed to GitHub Pages with chat widget working
- Errors logged to Sentry
- README files complete and accurate
- UX polished (loading states, error handling, mobile-responsive)

---

## Parallel Execution Opportunities

### Phase 1 (Setup) - All tasks parallelizable except T001, T002 (structure first)
```
T001, T002 → [T003, T004, T005, T006] in parallel
          → [T007, T008, T009] in parallel (external services)
          → [T010, T011, T012] in parallel (config files)
```

### Phase 2 (Foundational) - Models → Services in parallel
```
[T013, T014, T015, T016] (models) in parallel
[T017] (schemas) depends on models
[T018, T019, T020] (services) in parallel after schemas
```

### Phase 3 (US1) - Backend and Frontend work streams in parallel
```
Backend: T021-T036 (sequential within, but ingestion T021-T027b can run parallel to service T028-T032)
Frontend: T037-T046 (all parallelizable, different components)
Integration: T047-T048 after both streams complete
```

### Phase 4-7 (US2-US5) - Each user story is independent, can be implemented in parallel by different developers

### Phase 8 (Polish) - Deployment, monitoring, docs can be parallelized

---

## Testing Strategy

**Unit Tests** (if TDD requested):
- Backend services: RAGService, QdrantService, EmbeddingService, AgentService (mock external APIs and sentence-transformers model)
- Pydantic schemas: Validation logic for selection mode
- Database models: Relationships and constraints

**Integration Tests**:
- API endpoints: POST /api/chat (full_book and selection modes), POST /api/feedback
- Content ingestion: End-to-end markdown → Qdrant pipeline

**E2E Tests** (Playwright):
- US1: Open chat, ask question, verify response and citations
- US2: Select text, ask question, verify selection mode
- US3: Open chat, click suggested question
- US4: Ask follow-up question with pronoun
- US5: Submit feedback

**Performance Tests** (Locust):
- 50 concurrent users, <3s p95 response time
- Rate limiting: 10 req/min enforcement

---

## MVP Delivery Plan

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1 only)
**Task Count**: 48 tasks
**Estimate**: 2-3 weeks (1 full-time developer)

**MVP Delivers**:
- ✅ Core RAG chatbot functionality (Full Book Mode)
- ✅ Content ingestion pipeline
- ✅ Chat widget with Ctrl+K shortcut
- ✅ Markdown responses with citations
- ✅ Deployed to Render + GitHub Pages

**Post-MVP Increments**:
1. **Increment 2** (US2 - Selection Mode with Visual Affordance): +19 tasks, +4-5 days
2. **Increment 3** (US3 - Suggested Questions): +8 tasks, +2-3 days
3. **Increment 4** (US4 - Conversation History): +10 tasks, +3-4 days
4. **Increment 5** (US5 - Feedback): +6 tasks, +2 days
5. **Increment 6** (Polish): +6 tasks, +3-4 days

**Full Feature Delivery**: 4-6 weeks (1-2 developers, part-time)

---

## Risk Mitigation

| Risk | Tasks Affected | Mitigation |
|------|---------------|------------|
| OpenAI Agents API rate limits | T031, T036 | Implement exponential backoff in AgentService; monitor usage |
| sentence-transformers model size | T019, T024 | Model cached after first load (~150MB); acceptable for Render |
| Qdrant free tier exceeded | T025, T029 | Monitor chunk count (~15k limit at 768 dims); optimize chunk size |
| Render cold starts | T085 (deployment) | Accept 30s cold start for free tier; warn users in UI |
| Poor answer quality | T031, T048 (testing) | Iterate on prompt engineering with OpenAI Agents; collect feedback (US5) |
| Content ingestion errors | T021-T027b | Robust error handling; verify_chunks.py validation script; incremental re-ingestion with change detection |

---

## Success Metrics (Validation)

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| Response Time | <3s (p95) | Locust load testing; log response_time_ms in database |
| Positive Feedback Rate | >90% | Query user_feedback table: `SELECT AVG(rating='positive')` |
| Selection Mode Success | >85% | Log selection mode queries; track error rate |
| Mobile Compatibility | Works on iOS Safari, Android Chrome | Manual testing on real devices |
| Concurrent Users | 50 without degradation | Locust load test with 50 virtual users |

---

## Next Steps

1. **Review tasks.md** with team for completeness
2. **Start MVP** (Phase 1 + Phase 2 + Phase 3)
3. **Daily standups** to track progress and blockers
4. **Sprint demos** after each user story phase completion
5. **Retrospectives** at MVP and full feature delivery

---

## Related Documents

- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Technology Research](./research.md)
- [Data Model Design](./data-model.md)
- [API Contracts](./contracts/openapi.yaml)
- [Quickstart Guide](./quickstart.md)

---

**Tasks Status**: ✅ READY FOR IMPLEMENTATION
**Generated By**: `/sp.tasks` command
**Estimated Delivery**: 4-6 weeks (1-2 part-time developers)
