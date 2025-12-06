# Feature Specification: Integrated RAG Chatbot for Physical AI Book

**Feature Branch**: `005-rag-chatbot`
**Created**: 2025-12-03
**Status**: Draft
**Priority**: High
**Estimated Effort**: 4-6 weeks (1-2 developers, part-time)

---

## Executive Summary

Build and integrate a Retrieval-Augmented Generation (RAG) chatbot within the Physical AI and Humanoid Robotics Docusaurus book website. The chatbot enables readers to ask natural language questions about book content and receive contextual answers with citations. Key features include full-book semantic search, text selection mode for targeted queries, conversation history, suggested questions, and user feedback mechanisms.

**Technology Stack**:
- **Backend**: FastAPI (Python 3.11+)
- **LLM**: OpenAI Agents Python SDK with gpt-4o-mini
- **Embeddings**: Hugging Face sentence-transformers (BAAI/bge-base-en-v1.5)
- **Vector DB**: Qdrant Cloud Free Tier
- **Relational DB**: Neon Serverless Postgres
- **Frontend**: Docusaurus Plugin (React)
- **Deployment**: Render (backend) + GitHub Pages (frontend)

**Value Proposition**: Enhance learning experience by providing instant, contextual answers to reader questions, reducing friction in knowledge discovery, and enabling interactive exploration of robotics concepts.

**Technical Approach**:
- **Embeddings**: Local sentence-transformers model (BAAI/bge-base-en-v1.5) generates 768-dimensional vectors for semantic search, eliminating OpenAI embedding API costs
- **Agent Framework**: OpenAI Agents Python SDK provides robust conversation management, agent orchestration, and structured response generation
- **Database**: Neon Serverless Postgres with automatic connection pooling optimized for serverless deployments, ensuring efficient connection management at zero infrastructure cost

---

## User Scenarios & Testing

### User Story 1 - Quick Content Search (Priority: P1)

**As a** book reader
**I want to** ask natural language questions about ROS 2, robotics, or AI concepts
**So that** I can quickly find relevant information without manually searching through chapters

**Why this priority**: This is the core value proposition of the RAG chatbot - instant, semantic search across all book content. Without this, the feature has no value. It's the foundation for all other user stories and represents the minimum viable product.

**Independent Test**: Can be fully tested by opening the book website, pressing Ctrl+K, typing "How do I create a custom ROS 2 message?", and receiving a response with citations that link to actual chapters. Delivers immediate value: faster knowledge discovery than manual chapter navigation.

**Acceptance Scenarios**:

1. **Given** I open the book website
   **When** I press `Ctrl+K` (Windows/Linux) or `Cmd+K` (Mac)
   **Then** the chat widget opens with an empty input field

2. **Given** the chat widget is open
   **When** I type "How do I create a custom ROS 2 message?" and press Enter
   **Then** I receive a response within 3 seconds containing:
   - A natural language answer synthesized from book content
   - 2-5 clickable citations linking to relevant chapters (e.g., "Module 1, Chapter 1.3")
   - Proper markdown formatting (code blocks, lists, bold/italic)

3. **Given** I receive a response with citations
   **When** I click a citation link (e.g., "[Module 1, Chapter 1.3]")
   **Then** the browser navigates to the exact chapter page

4. **Given** I ask a question unrelated to the book content (e.g., "What's the weather?")
   **When** the system searches for relevant chunks
   **Then** I receive a polite response: "I couldn't find relevant information in the book. Please ask about Physical AI, ROS 2, or Humanoid Robotics topics covered in this book."

**Definition of Done**:
- [ ] Chat widget opens/closes with keyboard shortcuts
- [ ] Queries return responses in <3s (p95)
- [ ] Responses include 2-5 citations with working links
- [ ] Out-of-scope queries return appropriate fallback message
- [ ] Unit tests cover query processing, embedding, retrieval, generation
- [ ] E2E test verifies full flow (open widget → query → response → citation click)

---

### User Story 2 - Selection Mode Queries (Priority: P2)

**As a** book reader
**I want to** select text on a page and ask questions specifically about that selection
**So that** I can get clarification on specific paragraphs, code snippets, or diagrams without providing full context

**Why this priority**: This feature significantly enhances user experience by enabling contextual queries, but the chatbot still provides value without it (via US1). It's a natural extension that makes the tool more powerful for learners who need clarification on specific content.

**Independent Test**: Can be tested independently by selecting a paragraph of text on any chapter page, pressing Ctrl+K, asking "Explain this in simpler terms", and receiving a response that explicitly references the selected content. Delivers value: targeted help without manual context-switching or copy-pasting.

**Acceptance Scenarios**:

1. **Given** I am reading Chapter 1.2 (Publishers & Subscribers)
   **When** I highlight the paragraph explaining `rclpy.spin(node)` and press `Ctrl+K`
   **Then** the chat widget opens with a visual indicator showing "Selection Mode" and the selected text preview (first 100 chars)

2. **Given** I am in selection mode
   **When** I type "Explain this in simpler terms" and submit
   **Then** I receive a response that:
   - References the selected text explicitly (e.g., "The selected code demonstrates...")
   - Provides a simplified explanation
   - Includes citations to related chapters if applicable

3. **Given** I select a Python code block and ask "What does this function do?"
   **When** the query is processed
   **Then** the response includes:
   - Line-by-line explanation of the code
   - Purpose and inputs/outputs
   - Relevant ROS 2 concepts (e.g., "This is a publisher node...")

4. **Given** I am in selection mode
   **When** I clear my selection or press Escape
   **Then** the chat widget switches back to "Full Book Mode"

**Definition of Done**:
- [ ] Text selection triggers selection mode indicator
- [ ] Selected text is embedded and used as context for retrieval
- [ ] Responses reference the selected content explicitly
- [ ] Selection mode can be toggled/cleared
- [ ] Unit tests verify selection mode logic
- [ ] E2E test: select text → open chat → query → contextual response

---

### User Story 3 - Suggested Questions (Priority: P3)

**As a** book reader
**I want to** see suggested questions related to my current chapter
**So that** I can explore topics I might not have thought to ask about

**Why this priority**: This is a "nice-to-have" feature that enhances discoverability but isn't essential for core functionality. Users can still ask questions manually (US1 and US2 provide full value). It helps with onboarding and exploration but can be deferred if resources are limited.

**Independent Test**: Can be tested by opening the chat widget while viewing Chapter 1.5 (URDF) and verifying that 3-5 contextually relevant suggested questions appear (e.g., "What is a URDF file?", "How do I create joints?"). Clicking a suggestion should submit it as a query. Delivers value: reduced friction for users who aren't sure what to ask.

**Acceptance Scenarios**:

1. **Given** I open the chat widget while viewing Chapter 1.5 (URDF)
   **When** the widget loads
   **Then** I see 3-5 suggested questions like:
   - "What is a URDF file?"
   - "How do I create a robot arm with joints?"
   - "How does RViz2 use URDF files?"

2. **Given** I see suggested questions
   **When** I click "What is a URDF file?"
   **Then** the question is automatically submitted and I receive a response

3. **Given** I am in selection mode
   **When** the widget loads
   **Then** suggested questions are context-aware (e.g., "Explain this code snippet", "What are the prerequisites?")

**Definition of Done**:
- [ ] Suggested questions appear in the chat widget
- [ ] Questions are context-aware (based on current chapter)
- [ ] Clicking a suggestion submits it as a query
- [ ] Unit tests verify suggestion generation logic
- [ ] E2E test: open widget → click suggestion → receive response

---

### User Story 4 - Conversation History (Priority: P3)

**As a** book reader
**I want to** see my previous questions and answers in the same session
**So that** I can refer back to earlier explanations and build on previous queries

**Why this priority**: While valuable for multi-turn conversations, most interactions are single-query searches (US1). This enhances the experience for users who need to ask follow-up questions, but isn't critical for core functionality. Can be added after MVP launch based on user feedback.

**Independent Test**: Can be tested by asking 3 questions in succession, verifying all Q&A pairs appear in chronological order, then closing and reopening the browser tab to confirm session persistence via localStorage. Delivers value: continuity for complex learning sessions without losing context.

**Acceptance Scenarios**:

1. **Given** I have asked 3 questions in the current session
   **When** I open the chat widget
   **Then** I see all 3 Q&A pairs in chronological order (oldest at top)

2. **Given** I have a conversation history
   **When** I ask a follow-up question (e.g., "Can you explain that in more detail?")
   **Then** the system uses previous context to generate a relevant response

3. **Given** I close and reopen the browser tab
   **When** I open the chat widget
   **Then** my session history persists (using `session_id` stored in localStorage)

4. **Given** I want to start fresh
   **When** I click "New Conversation" button
   **Then** the chat history clears and a new `session_id` is generated

**Definition of Done**:
- [ ] Chat widget displays conversation history
- [ ] Session persistence via localStorage
- [ ] Follow-up queries use conversation context
- [ ] "New Conversation" button clears history and creates new session
- [ ] Unit tests verify session management
- [ ] E2E test: multi-turn conversation → close tab → reopen → history persists

---

### User Story 5 - Response Feedback (Priority: P3)

**As a** book reader
**I want to** rate responses with thumbs up/down and provide optional text feedback
**So that** the system can improve over time and authors can identify content gaps

**Why this priority**: This is a data collection feature that benefits future iterations but doesn't impact core user value. It's useful for measuring success and identifying areas for improvement, but can be added post-MVP. Feedback loops are important for long-term quality but not essential for launch.

**Independent Test**: Can be tested by receiving a response, clicking thumbs up (or thumbs down with optional text feedback), and verifying the feedback is stored in the database with the correct response linkage. Prevents duplicate feedback. Delivers value: enables continuous improvement and content gap analysis.

**Acceptance Scenarios**:

1. **Given** I receive a response
   **When** the response is displayed
   **Then** I see thumbs up/down buttons below the response

2. **Given** I click thumbs up
   **When** the feedback is submitted
   **Then** the button highlights green and a "Thank you!" message appears briefly

3. **Given** I click thumbs down
   **When** the modal opens
   **Then** I see a textarea asking "What went wrong?" with a submit button

4. **Given** I submit negative feedback with text
   **When** the feedback is recorded
   **Then** the data is stored in Postgres with `response_id`, `rating='negative'`, and `feedback_text`

5. **Given** I have already rated a response
   **When** I try to rate it again
   **Then** the buttons are disabled with a message "Feedback already submitted"

**Definition of Done**:
- [ ] Thumbs up/down buttons appear on all responses
- [ ] Positive feedback: one-click submission
- [ ] Negative feedback: optional text modal
- [ ] Feedback stored in Postgres with response linkage
- [ ] Duplicate feedback prevention (one rating per response per session)
- [ ] Unit tests verify feedback submission logic
- [ ] E2E test: submit positive/negative feedback → verify in database

---

### Edge Cases

1. **Empty query**: User submits empty string → Return HTTP 400 "Query text cannot be empty"
2. **Very long query**: User submits 1500-character query → Truncate to 1000 chars with warning message
3. **Selection mode without selected text**: User sets `mode='selection'` but `selected_text` is null → Return HTTP 400 "Selected text required for selection mode"
4. **No relevant chunks found**: Query embedding returns 0 chunks with similarity ≥0.7 → Return fallback response "I couldn't find relevant information in the book..."
5. **Invalid session_id**: User provides non-UUID session_id → Return HTTP 400 "Invalid session_id format"
6. **Expired session**: Session older than 30 days → Create new session (optional cleanup job)
7. **OpenAI Agents API rate limit**: OpenAI Agents SDK returns 429 → Retry with exponential backoff (max 3 retries), then return HTTP 503 "Service temporarily unavailable"
8. **Qdrant connection failure**: Qdrant unreachable → Return HTTP 503 with retry suggestion
9. **Malformed markdown in response**: LLM generates invalid markdown → Sanitize with markdown parser before returning
10. **Concurrent feedback submissions**: Two clients submit feedback for same response simultaneously → Use database constraint to prevent duplicates

---

## Requirements

### Functional Requirements

#### Content Ingestion (FR-001 to FR-006)

- **FR-001**: The system SHALL parse all `.md` and `.mdx` files in `book_frontend/docs/` directory
- **FR-002**: The system SHALL chunk content using recursive character splitting with 500-1000 token chunks and 100-token overlap
- **FR-003**: The system SHALL extract metadata from each chunk: `module_number`, `chapter_number`, `section_title`, `file_path`, `public_url`
- **FR-004**: The system SHALL embed each chunk using Hugging Face sentence-transformers model `BAAI/bge-base-en-v1.5` (768 dimensions), utilizing batch encoding via `model.encode()` for efficiency
- **FR-005**: The system SHALL upsert chunks to Qdrant Cloud collection `book_content` with vector + payload
- **FR-006**: The system SHALL support incremental re-ingestion (detect changed files, re-embed only changed content)

#### Query Processing (FR-007 to FR-012)

- **FR-007**: The system SHALL accept queries via REST API endpoint `POST /api/chat` with JSON payload: `query_text`, `mode`, `selected_text`, `session_id`
- **FR-008**: The system SHALL validate `query_text` (max 1000 chars) and `selected_text` (max 5000 chars if provided)
- **FR-009**: The system SHALL embed the query using Hugging Face sentence-transformers model `BAAI/bge-base-en-v1.5`
- **FR-010**: The system SHALL search Qdrant for up to 5 most similar chunks (cosine similarity ≥ 0.7), returning fewer if insufficient chunks meet the threshold
- **FR-011**: For selection mode (`mode='selection'`), the system SHALL embed and prioritize the selected text in retrieval
- **FR-012**: The system SHALL fall back to "no relevant content found" if no chunks meet similarity threshold

#### Response Generation (FR-013 to FR-018)

- **FR-013**: The system SHALL construct a prompt with: user query, retrieved chunks, system instructions (answer concisely, cite sources, use markdown)
- **FR-014**: The system SHALL use OpenAI Agents Python SDK to generate responses with model `gpt-4o-mini` and `temperature=0.3`, leveraging the Agent and Runner classes for conversation management
- **FR-015**: The system SHALL return a JSON response with: `response_id`, `response_text`, `source_chunks[]`, `response_time_ms`, `session_id`
- **FR-016**: Each `source_chunk` SHALL include: `chunk_id`, `module_number`, `chapter_number`, `section_title`, `url`, `score`
- **FR-017**: The system SHALL enforce p95 response time <3 seconds (measured end-to-end from FastAPI request receipt to final response sent, including embedding generation, vector search, and LLM response generation)
- **FR-018**: The system SHALL support streaming responses using OpenAI Agents SDK's async iteration capabilities (optional, post-MVP)

#### Session Management (FR-019 to FR-021)

- **FR-019**: The system SHALL create a new `session_id` (UUID) via `POST /api/session` if not provided
- **FR-020**: The system SHALL persist sessions in Neon Serverless Postgres `chat_sessions` table with: `session_id`, `user_identifier`, `start_timestamp`, `last_activity_timestamp`, `message_count`, utilizing Neon's automatic connection pooling
- **FR-021**: The system SHALL update `last_activity_timestamp` on every query in the session

#### Feedback Collection (FR-022 to FR-024)

- **FR-022**: The system SHALL accept feedback via `POST /api/feedback` with: `response_id`, `rating` (positive/negative), `feedback_text` (optional)
- **FR-023**: The system SHALL store feedback in Neon Serverless Postgres `user_feedback` table with timestamp
- **FR-024**: The system SHALL prevent duplicate feedback (one rating per `response_id` per `session_id`)

#### Rate Limiting & Security (FR-025 to FR-028)

- **FR-025**: The system SHALL enforce rate limit of 10 requests/minute per IP address using slowapi
- **FR-026**: The system SHALL return HTTP 429 with `Retry-After` header when rate limit exceeded
- **FR-027**: The system SHALL validate all inputs (Pydantic schemas) and return HTTP 400 for validation errors
- **FR-028**: The system SHALL NOT expose internal errors; return generic HTTP 500 with error tracking (Sentry/logging)

### Key Entities

#### 1. Book Content Chunk
**Stored in**: Qdrant Cloud (`book_content` collection)

- **chunk_id** (UUID): Primary key (Qdrant point ID)
- **vector** (float[768]): Embedding from BAAI/bge-base-en-v1.5
- **content_text** (string): Raw markdown/text content (500-1000 tokens)
- **module_number** (integer): Module number (e.g., 1 for Module 1)
- **chapter_number** (integer): Chapter number (e.g., 2 for Chapter 1.2)
- **section_title** (string): Human-readable section title
- **file_path** (string): Relative path (e.g., docs/module-1/chapter-1-2.md)
- **public_url** (string): Full URL to chapter on GitHub Pages
- **token_count** (integer): Token count of content_text

#### 2. Chat Session
**Stored in**: Neon Serverless Postgres (`chat_sessions` table)
**Note**: Neon provides automatic connection pooling via PgBouncer for serverless environments

- **session_id** (UUID): Primary key
- **user_identifier** (string): Optional anonymous user ID
- **start_timestamp** (timestamptz): Session creation time
- **last_activity_timestamp** (timestamptz): Last query time in session
- **message_count** (integer): Total queries in session

#### 3. User Query
**Stored in**: Neon Serverless Postgres (`user_queries` table)

- **query_id** (UUID): Primary key
- **session_id** (UUID): Foreign key to chat_sessions
- **query_text** (string): User's question
- **query_timestamp** (timestamptz): Query submission time
- **mode** (string): 'full_book' or 'selection'
- **selected_text** (string): Text selection (if mode='selection')

#### 4. Chat Response
**Stored in**: Neon Serverless Postgres (`chat_responses` table)

- **response_id** (UUID): Primary key
- **query_id** (UUID): Foreign key to user_queries
- **response_text** (text): Generated markdown answer
- **source_chunk_ids** (UUID[]): Array of chunk_ids used
- **response_time_ms** (integer): Generation time (milliseconds)
- **model_version** (string): OpenAI model used (e.g., gpt-4o-mini)
- **response_timestamp** (timestamptz): Response generation time

#### 5. User Feedback
**Stored in**: Neon Serverless Postgres (`user_feedback` table)

- **feedback_id** (UUID): Primary key
- **response_id** (UUID): Foreign key to chat_responses
- **rating** (string): 'positive' or 'negative'
- **feedback_text** (text): Optional text feedback
- **feedback_timestamp** (timestamptz): Feedback submission time

#### 6. Content Metadata (Optional)
**Stored in**: Neon Serverless Postgres (`content_metadata` table) - for tracking ingestion

- **file_path** (string): Primary key
- **last_ingested_at** (timestamptz): Last ingestion timestamp
- **chunk_count** (integer): Number of chunks generated
- **file_hash** (string): MD5 hash (for incremental ingestion)

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: 90% of user queries return responses within 3 seconds (p95 latency)
- **SC-002**: Selection mode accuracy: 85% of users successfully ask questions about selected text
- **SC-003**: Citation accuracy: 95% of citation links navigate to correct chapter pages
- **SC-004**: User satisfaction: >90% positive feedback rate (thumbs up / total feedback)
- **SC-005**: Content coverage: All 12+ book chapters successfully ingested into Qdrant (500+ chunks)
- **SC-006**: Zero exposure of API keys or secrets in client-side code or logs
- **SC-007**: Rate limiting: 100% of requests exceeding 10/min receive HTTP 429 with proper Retry-After header
- **SC-008**: Error handling: All 5xx errors logged with trace IDs; generic messages returned to users
- **SC-009**: Accessibility: Chat widget meets WCAG 2.1 AA standards (keyboard navigation, ARIA labels, screen reader support)
- **SC-010**: Mobile responsiveness: Chat widget fully functional on viewport widths 320px-768px
- **SC-011**: Concurrent users: System supports 50 concurrent chat sessions without degradation
- **SC-012**: Incremental ingestion: Re-ingestion of 1 changed chapter completes in <2 minutes
- **SC-013**: Free-tier compliance: Monthly costs stay within $0 (Qdrant, Neon, Render, Hugging Face models are free) + ~$10-15 (OpenAI Agents API usage)
- **SC-014**: Test coverage: Backend unit test coverage ≥80%, frontend component test coverage ≥70%

---

## Additional Context

### Assumptions

1. **Content stability**: Book content is updated infrequently (1-2 times/month); incremental re-ingestion is sufficient
2. **Anonymous users**: No authentication required; users are anonymous with optional session persistence
3. **English only**: All book content and queries are in English; no i18n/l10n required for MVP
4. **Static deployment**: Frontend is static site on GitHub Pages; no server-side rendering
5. **Free-tier constraints**: System operates within free-tier limits of Qdrant (1GB), Neon (0.5GB), Render (750 hrs/month)
6. **Single book**: System serves one book only; no multi-tenancy or multiple book support
7. **Docusaurus 3.x**: Frontend uses Docusaurus 3.1.0 with plugin architecture
8. **Python 3.11+**: Backend requires Python 3.11 or higher for type hints and async features
9. **Desktop-first**: Primary use case is desktop browsers (laptop/desktop); mobile is secondary
10. **No real-time collaboration**: Each user's session is independent; no shared chat rooms
11. **Embedding model**: Uses Hugging Face sentence-transformers model `BAAI/bge-base-en-v1.5` (768 dimensions) for semantic embeddings
12. **Agent framework**: OpenAI Agents Python SDK provides agent orchestration, conversation management, and response generation
13. **Database pooling**: Neon Serverless Postgres provides automatic connection pooling for serverless environments

### Dependencies

**External Services**:
- OpenAI API: Requires API key with access to `gpt-4o-mini` model for OpenAI Agents Python SDK
- Hugging Face: Sentence-transformers library for embedding generation (`BAAI/bge-base-en-v1.5` model)
- Qdrant Cloud: Free-tier account with 1GB storage (https://cloud.qdrant.io/)
- Neon Serverless Postgres: Free-tier serverless Postgres database with connection pooling (https://neon.tech/)
- Render: Free-tier web service for backend deployment (https://render.com/)
- GitHub Pages: Static site hosting for Docusaurus frontend

**Internal Services**:
- Book Frontend: Docusaurus site in `book_frontend/` directory
- Book Content: Markdown/MDX files in `book_frontend/docs/` directory

**Development Tools**:
- Python 3.11+: Backend runtime
- Node.js 18+: Frontend build tooling
- Git: Version control

**Libraries**:
- Backend: FastAPI, OpenAI Agents Python SDK, sentence-transformers, qdrant-client, SQLAlchemy, psycopg, Pydantic, slowapi
- Frontend: React, react-markdown, react-syntax-highlighter, Docusaurus

### Out of Scope (Not in MVP)

1. **User authentication**: No login, registration, or user accounts
2. **Advanced conversation features**: No multi-turn reasoning, no memory beyond current session
3. **Voice input/output**: No speech recognition or text-to-speech
4. **Multilingual support**: English only
5. **Admin dashboard**: No analytics UI or content management interface
6. **A/B testing**: No experimentation framework
7. **Custom LLM fine-tuning**: Use OpenAI models as-is
8. **Real-time collaboration**: No shared sessions or multiplayer features
9. **Advanced search filters**: No date ranges, module filtering, or advanced search operators
10. **Export/share responses**: No PDF export, sharing links, or response bookmarking

---

## Implementation Phases (See tasks.md)

- **Phase 1**: Project Setup & Infrastructure (12 tasks)
- **Phase 2**: Foundational Backend Services (8 tasks)
- **Phase 3**: US1 - Full Book Search (28 tasks) ← MVP Milestone
- **Phase 4**: US2 - Selection Mode (14 tasks)
- **Phase 5**: US3 - Suggested Questions (10 tasks)
- **Phase 6**: US4 - Conversation History (8 tasks)
- **Phase 7**: US5 - Feedback System (8 tasks)
- **Phase 8**: Deployment & Monitoring (8 tasks)

**MVP Scope**: Phases 1-3 (48 tasks) = Core RAG chatbot with full-book search

---

## Cross-References

- **Planning Documents**: `specs/005-rag-chatbot/plan.md` (architecture decisions)
- **Research**: `specs/005-rag-chatbot/research.md` (technology selection)
- **Data Model**: `specs/005-rag-chatbot/data-model.md` (schemas)
- **API Contracts**: `specs/005-rag-chatbot/contracts/openapi.yaml` (REST API spec)
- **Quickstart**: `specs/005-rag-chatbot/quickstart.md` (developer guide)
- **Tasks**: `specs/005-rag-chatbot/tasks.md` (implementation tasks)

---

**Next Steps**: Run `/sp.implement` to begin task execution following the red-green-refactor cycle.
