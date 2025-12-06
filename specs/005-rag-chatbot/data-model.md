# Data Model: RAG Chatbot

**Feature**: Integrated RAG Chatbot for Physical AI Book
**Date**: 2025-12-03
**Phase**: 1 - Data Model Design

## Overview

This document defines the data entities, schemas, and relationships for the RAG chatbot system. The system uses two data stores:
1. **Qdrant (Vector DB)**: Book content chunks with embeddings for semantic search
2. **Neon Postgres (Relational DB)**: Chat sessions, queries, responses, and feedback

---

## 1. Vector Database Schema (Qdrant)

### Collection: `book_content`

**Purpose**: Store book content chunks with embeddings for semantic search.

**Vector Configuration**:
```python
{
  "vectors": {
    "size": 1536,  # Matches text-embedding-3-small dimensions
    "distance": "Cosine"  # Cosine similarity for text embeddings
  }
}
```

**Payload Schema**:
| Field | Type | Description | Indexed |
|-------|------|-------------|---------|
| `chunk_id` | string (UUID) | Unique identifier for chunk | Primary key |
| `content_text` | string | Actual text content of the chunk | Full-text |
| `module_number` | integer | Module number (1-4) | Yes |
| `chapter_number` | integer | Chapter number within module | Yes |
| `section_title` | string | Section heading/title | No |
| `file_path` | string | Relative path to source markdown file | No |
| `public_url` | string | Full URL to published page (for citations) | No |
| `token_count` | integer | Approximate token count (for context window management) | No |
| `last_updated` | timestamp | When this chunk was last updated | No |

**Indexes**:
```python
# Create payload indices for filtered search
collection.create_payload_index("module_number", field_schema="integer")
collection.create_payload_index("chapter_number", field_schema="integer")
```

**Example Document**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "vector": [0.023, -0.15, ...],  # 1536 dimensions
  "payload": {
    "chunk_id": "550e8400-e29b-41d4-a716-446655440000",
    "content_text": "ROS 2 uses a publish-subscribe pattern...",
    "module_number": 1,
    "chapter_number": 2,
    "section_title": "Your First ROS 2 Node - Publishers & Subscribers",
    "file_path": "docs/module-1/chapter-1-2-pubsub.md",
    "public_url": "https://muhammad-aneeq.github.io/Physical-AI-Humanoid-Robotics-Book/docs/module-1/chapter-1-2-pubsub",
    "token_count": 847,
    "last_updated": "2025-12-03T10:00:00Z"
  }
}
```

---

## 2. Relational Database Schema (Postgres)

### Table: `chat_sessions`

**Purpose**: Track conversation sessions (browser sessions or user sessions).

**Schema**:
```sql
CREATE TABLE chat_sessions (
  session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_identifier TEXT,  -- Anonymous session ID or user email (if auth added later)
  start_timestamp TIMESTAMPTZ DEFAULT NOW(),
  last_activity_timestamp TIMESTAMPTZ DEFAULT NOW(),
  message_count INTEGER DEFAULT 0,

  CONSTRAINT message_count_positive CHECK (message_count >= 0)
);

CREATE INDEX idx_sessions_last_activity ON chat_sessions(last_activity_timestamp DESC);
CREATE INDEX idx_sessions_user ON chat_sessions(user_identifier) WHERE user_identifier IS NOT NULL;
```

**Lifecycle**:
- Created when user first opens chat widget
- Updated on every message exchange (last_activity_timestamp, message_count)
- Sessions older than 30 days with no activity may be archived/deleted

---

### Table: `user_queries`

**Purpose**: Store all user questions and their metadata.

**Schema**:
```sql
CREATE TABLE user_queries (
  query_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
  query_text TEXT NOT NULL,
  query_timestamp TIMESTAMPTZ DEFAULT NOW(),
  mode TEXT NOT NULL CHECK (mode IN ('full_book', 'selection')),
  selected_text TEXT,  -- NULL if mode='full_book'; populated if mode='selection'
  embedding VECTOR(1536),  -- Optional: for hybrid search (requires pgvector extension)

  CONSTRAINT selected_text_required_for_selection CHECK (
    (mode = 'full_book' AND selected_text IS NULL) OR
    (mode = 'selection' AND selected_text IS NOT NULL)
  )
);

CREATE INDEX idx_queries_session ON user_queries(session_id, query_timestamp DESC);
CREATE INDEX idx_queries_timestamp ON user_queries(query_timestamp DESC);
CREATE INDEX idx_queries_mode ON user_queries(mode);
```

**Example Row**:
```json
{
  "query_id": "660e8400-e29b-41d4-a716-446655440001",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "query_text": "How do I create a custom ROS 2 message?",
  "query_timestamp": "2025-12-03T14:30:00Z",
  "mode": "full_book",
  "selected_text": null,
  "embedding": null
}
```

---

### Table: `chat_responses`

**Purpose**: Store generated responses and their metadata for analytics.

**Schema**:
```sql
CREATE TABLE chat_responses (
  response_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  query_id UUID NOT NULL REFERENCES user_queries(query_id) ON DELETE CASCADE,
  response_text TEXT NOT NULL,
  source_chunks JSONB,  -- Array of {chunk_id, score, module, chapter, url}
  generation_timestamp TIMESTAMPTZ DEFAULT NOW(),
  response_time_ms INTEGER,  -- Time taken to generate response
  model_used TEXT DEFAULT 'gpt-4o-mini',
  token_usage JSONB,  -- {prompt_tokens, completion_tokens, total_tokens}

  CONSTRAINT response_time_positive CHECK (response_time_ms > 0)
);

CREATE INDEX idx_responses_query ON chat_responses(query_id);
CREATE INDEX idx_responses_timestamp ON chat_responses(generation_timestamp DESC);
CREATE INDEX idx_responses_time ON chat_responses(response_time_ms);  -- For performance analysis
```

**Example Row**:
```json
{
  "response_id": "770e8400-e29b-41d4-a716-446655440002",
  "query_id": "660e8400-e29b-41d4-a716-446655440001",
  "response_text": "To create a custom ROS 2 message, you need to...",
  "source_chunks": [
    {
      "chunk_id": "550e8400-e29b-41d4-a716-446655440000",
      "score": 0.89,
      "module": 1,
      "chapter": 3,
      "url": "https://..."
    }
  ],
  "generation_timestamp": "2025-12-03T14:30:02Z",
  "response_time_ms": 1850,
  "model_used": "gpt-4o-mini",
  "token_usage": {
    "prompt_tokens": 1200,
    "completion_tokens": 350,
    "total_tokens": 1550
  }
}
```

---

### Table: `user_feedback`

**Purpose**: Track user satisfaction ratings (thumbs up/down) and optional text feedback.

**Schema**:
```sql
CREATE TABLE user_feedback (
  feedback_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  response_id UUID NOT NULL REFERENCES chat_responses(response_id) ON DELETE CASCADE,
  rating TEXT NOT NULL CHECK (rating IN ('positive', 'negative')),
  feedback_text TEXT,  -- Optional user-provided explanation
  feedback_timestamp TIMESTAMPTZ DEFAULT NOW(),

  -- Prevent duplicate feedback for the same response
  CONSTRAINT unique_feedback_per_response UNIQUE (response_id)
);

CREATE INDEX idx_feedback_response ON user_feedback(response_id);
CREATE INDEX idx_feedback_rating ON user_feedback(rating);
CREATE INDEX idx_feedback_timestamp ON user_feedback(feedback_timestamp DESC);
```

**Example Row**:
```json
{
  "feedback_id": "880e8400-e29b-41d4-a716-446655440003",
  "response_id": "770e8400-e29b-41d4-a716-446655440002",
  "rating": "positive",
  "feedback_text": null,
  "feedback_timestamp": "2025-12-03T14:32:00Z"
}
```

---

## 3. Entity Relationships (ER Diagram)

```
chat_sessions (1) ──< (N) user_queries
                           │
                           └──< (1) chat_responses
                                     │
                                     └──< (0..1) user_feedback

book_content (Qdrant) ←──(referenced in)──  chat_responses.source_chunks (JSONB)
```

**Relationship Details**:
1. **chat_sessions → user_queries**: One session has many queries (1:N)
2. **user_queries → chat_responses**: One query has exactly one response (1:1)
3. **chat_responses → user_feedback**: One response has at most one feedback (1:0..1)
4. **book_content → chat_responses**: Chunks are referenced in responses via JSONB (loose coupling)

**Cascade Behavior**:
- Deleting a session cascades to queries, responses, and feedback
- Deleting a query cascades to response and feedback
- Deleting a response cascades to feedback

---

## 4. Data Access Patterns

### Pattern 1: Answer User Query (Full Book Mode)

1. **Generate embedding** for user query using OpenAI API
2. **Search Qdrant** for top 5-10 most similar chunks:
   ```python
   results = qdrant_client.search(
       collection_name="book_content",
       query_vector=query_embedding,
       limit=10,
       score_threshold=0.7,  # Minimum similarity
       with_payload=True
   )
   ```
3. **Construct prompt** with retrieved chunks + query
4. **Generate response** using OpenAI chat completion
5. **Insert records**:
   - `user_queries` (query_text, mode='full_book')
   - `chat_responses` (response_text, source_chunks, response_time_ms)

### Pattern 2: Answer User Query (Selection Mode)

1. **No vector search**: Use selected_text directly as context
2. **Construct prompt**: "Based on this text: {selected_text}, answer: {query}"
3. **Generate response** using OpenAI
4. **Insert records**:
   - `user_queries` (query_text, mode='selection', selected_text)
   - `chat_responses` (response_text, source_chunks=null)

### Pattern 3: Track Feedback

1. **User clicks thumbs up/down** on a response
2. **Insert record** into `user_feedback` (response_id, rating)
3. **Optional**: If thumbs down, prompt for text feedback

### Pattern 4: Analytics - Response Quality

```sql
SELECT
  ROUND(AVG(CASE WHEN rating = 'positive' THEN 1.0 ELSE 0.0 END) * 100, 2) AS positive_rate,
  COUNT(*) AS total_feedback
FROM user_feedback;
```

### Pattern 5: Analytics - Popular Topics

```sql
SELECT
  module_number,
  chapter_number,
  COUNT(*) AS query_count
FROM user_queries q
JOIN chat_responses r ON q.query_id = r.query_id
WHERE r.source_chunks IS NOT NULL
GROUP BY module_number, chapter_number
ORDER BY query_count DESC
LIMIT 10;
```

---

## 5. Validation Rules

### Input Validation (Pydantic Models)

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
from uuid import UUID

class ChatQueryRequest(BaseModel):
    query_text: str = Field(..., min_length=1, max_length=1000)
    mode: Literal["full_book", "selection"]
    selected_text: Optional[str] = Field(None, max_length=5000)
    session_id: Optional[UUID] = None

    @field_validator('selected_text')
    def validate_selected_text(cls, v, info):
        mode = info.data.get('mode')
        if mode == 'selection' and not v:
            raise ValueError("selected_text required for selection mode")
        if mode == 'full_book' and v:
            raise ValueError("selected_text must be null for full_book mode")
        return v

class ChatResponse(BaseModel):
    response_id: UUID
    response_text: str
    source_chunks: list[dict]  # [{chunk_id, score, module, chapter, url}]
    response_time_ms: int
```

### Database Constraints

- `message_count` must be non-negative
- `response_time_ms` must be positive
- `rating` must be 'positive' or 'negative'
- `mode` must be 'full_book' or 'selection'
- `selected_text` required if mode='selection'
- Unique feedback per response (no duplicate ratings)

---

## 6. Indexing Strategy

### Qdrant Indexes
- **Payload indexes**: `module_number`, `chapter_number` for filtered search
- **Full-text index**: `content_text` (built-in, no config needed)

### Postgres Indexes
- **Foreign keys**: Auto-indexed by Postgres
- **Timestamp columns**: Indexed for date-range queries
- **User identifier**: Partial index (only non-null values)
- **Response time**: Indexed for performance analytics

---

## 7. Data Retention Policy

| Table | Retention Period | Rationale |
|-------|------------------|-----------|
| `chat_sessions` | 30 days inactive | Purge abandoned sessions to save storage |
| `user_queries` | 1 year | Retain for long-term analytics |
| `chat_responses` | 1 year | Tied to queries; cascade delete |
| `user_feedback` | 1 year | Retain for quality analysis |
| `book_content` (Qdrant) | Indefinite | Core knowledge base; update on content changes |

**Archival Strategy**:
- After 30 days of inactivity, archive `chat_sessions` to cold storage (S3/Glacier)
- Implement automatic cleanup job (monthly cron)

---

## 8. Migration Scripts

### Initial Migration (V1)

```sql
-- Enable pgvector extension (if using hybrid search)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create tables in order (respecting foreign keys)
CREATE TABLE chat_sessions (...);
CREATE TABLE user_queries (...);
CREATE TABLE chat_responses (...);
CREATE TABLE user_feedback (...);

-- Create indexes
CREATE INDEX idx_sessions_last_activity ON chat_sessions(...);
-- ... (see individual table definitions)

-- Seed data (optional: sample suggested questions)
INSERT INTO suggested_questions (question_text, category) VALUES
  ('What will I learn in Module 1?', 'onboarding'),
  ('What are the prerequisites for this course?', 'onboarding'),
  ('How do I create a custom ROS 2 message?', 'technical');
```

---

## 9. Testing Data Model

### Unit Tests (Pydantic Validation)

```python
def test_chat_query_validation_full_book():
    query = ChatQueryRequest(
        query_text="What is ROS 2?",
        mode="full_book",
        selected_text=None
    )
    assert query.mode == "full_book"
    assert query.selected_text is None

def test_chat_query_validation_selection_missing_text():
    with pytest.raises(ValueError, match="selected_text required"):
        ChatQueryRequest(
            query_text="Explain this",
            mode="selection",
            selected_text=None
        )
```

### Integration Tests (Database)

```python
async def test_cascade_delete_session():
    # Create session → query → response → feedback
    session_id = await create_test_session()
    query_id = await create_test_query(session_id)
    response_id = await create_test_response(query_id)
    feedback_id = await create_test_feedback(response_id)

    # Delete session
    await delete_session(session_id)

    # Verify cascade
    assert await get_query(query_id) is None
    assert await get_response(response_id) is None
    assert await get_feedback(feedback_id) is None
```

---

## Summary

This data model supports:
- ✅ Two query modes (full_book, selection)
- ✅ Semantic search with metadata filtering
- ✅ Conversation history tracking
- ✅ User feedback collection
- ✅ Performance and quality analytics
- ✅ Data retention and archival
- ✅ Input validation and database constraints

**Next Steps**: Generate API contracts in `contracts/` directory.
