# RAG Chatbot Backend - Complete Flow Overview

## High-Level Architecture

The backend is a **RAG (Retrieval-Augmented Generation) chatbot system** built with FastAPI that answers questions about the Physical AI & Humanoid Robotics Book. It combines:
- **Vector Search** (Qdrant) for finding relevant book content
- **LLM Generation** (OpenAI GPT-4o-mini) for creating answers
- **PostgreSQL** (Neon) for storing conversation history and analytics

## Technology Stack

```
FastAPI (REST API)
├── OpenAI API (Embeddings + Chat Completions)
├── Qdrant Cloud (Vector Database)
├── PostgreSQL/Neon (Relational Database)
└── Pydantic (Validation) + SQLAlchemy (ORM)
```

**Key Dependencies** (requirements.txt:1-41):
- `fastapi[all]` - REST API framework
- `openai` - OpenAI SDK for embeddings/chat
- `qdrant-client` - Vector search client
- `sqlalchemy` + `psycopg` - PostgreSQL ORM
- `slowapi` - Rate limiting
- `markdown-it-py` + `langchain-text-splitters` - Content ingestion

## Complete Request Flow

### 1. Chat Query Flow (Primary Flow)

```
┌─────────────┐
│   Client    │
│  (Frontend) │
└──────┬──────┘
       │ POST /api/chat
       │ { query_text, mode, selected_text?, session_id? }
       ▼
┌──────────────────────────────────────────────────────┐
│  FastAPI Server (main.py:28-77)                      │
│  ┌─────────────────────────────────────────────┐    │
│  │ Middleware Layer                            │    │
│  │ • CORS (allow frontend origin)              │    │
│  │ • Rate Limiting (10 req/min)                │    │
│  │ • Sentry Error Tracking (optional)          │    │
│  └─────────────────────────────────────────────┘    │
│                                                      │
│  ┌─────────────────────────────────────────────┐    │
│  │ Router: chat.py:23-130                      │    │
│  │                                             │    │
│  │ Step 1: Session Management                  │    │
│  │ • Get or create chat session                │    │
│  │ • Track conversation continuity             │    │
│  └──────────────────┬──────────────────────────┘    │
│                     ▼                                │
│  ┌─────────────────────────────────────────────┐    │
│  │ Step 2: RAG Pipeline                        │    │
│  │ rag_service.generate_answer()               │    │
│  └──────────────────┬──────────────────────────┘    │
└───────────────────┬─┴──────────────────────────┘
                    │
                    ▼
```

### 2. RAG Service Pipeline (services/rag_service.py:122-204)

```
┌──────────────────────────────────────────────────────┐
│  Mode Check: full_book vs selection                  │
└──────────┬────────────────────────┬──────────────────┘
           │                        │
           │ FULL_BOOK MODE         │ SELECTION MODE
           ▼                        ▼
    ┌──────────────┐         ┌──────────────┐
    │ 1. Embed     │         │ Use selected │
    │    Query     │         │ text as      │
    │              │         │ context      │
    │ OpenAI API   │         │ (no search)  │
    │ text-        │         └──────┬───────┘
    │ embedding-   │                │
    │ 3-small      │                │
    └──────┬───────┘                │
           │                        │
           ▼                        │
    ┌──────────────┐                │
    │ 2. Semantic  │                │
    │    Search    │                │
    │              │                │
    │ Qdrant       │                │
    │ Vector DB    │                │
    │ • Top 10     │                │
    │ • Score>0.7  │                │
    └──────┬───────┘                │
           │                        │
           ▼                        │
    ┌──────────────┐                │
    │ 3. Construct │                │
    │    Prompt    │                │
    │              │                │
    │ System msg + │                │
    │ Context (5   │                │
    │ chunks) +    │                │
    │ User query   │                │
    └──────┬───────┘                │
           │                        │
           └────────┬───────────────┘
                    ▼
           ┌─────────────────┐
           │ 4. Generate     │
           │    Response     │
           │                 │
           │ OpenAI Chat     │
           │ gpt-4o-mini     │
           │ temp=0.3        │
           │ max_tokens=1000 │
           └────────┬────────┘
                    │
                    ▼
```

### 3. Database Storage & Response (chat.py:64-116)

```
┌────────────────────────────────────────┐
│  database_service CRUD Operations      │
│                                        │
│  Step 3: Save User Query               │
│  • query_text                          │
│  • mode (full_book/selection)          │
│  • selected_text (if applicable)       │
│  • session_id linkage                  │
│                                        │
│  Step 4: Save Chat Response            │
│  • response_text (markdown)            │
│  • source_chunks (top 5, JSONB)        │
│  • response_time_ms                    │
│  • token_usage                         │
│                                        │
│  Step 5: Format & Return               │
│  • response_id                         │
│  • response_text                       │
│  • source_chunks[] (with citations)    │
│  • response_time_ms                    │
│  • session_id                          │
└────────────┬───────────────────────────┘
             │
             ▼
      ┌──────────┐
      │  Client  │
      │ Response │
      └──────────┘
```

## Data Flow Components

### OpenAI Service (services/openai_service.py)

**Responsibilities:**
1. **Text Embedding** (openai_service.py:27-48)
   - Convert text to 1536-dim vectors
   - Model: `text-embedding-3-small`
   - Used for: Query embedding, content ingestion

2. **Chat Completion** (openai_service.py:85-125)
   - Generate responses from messages
   - Model: `gpt-4o-mini`
   - Temperature: 0.3 (consistent, factual)
   - Max tokens: 1000

3. **Batch Embedding** (openai_service.py:50-83)
   - Process multiple texts efficiently
   - Batch size: 100 texts/request
   - Rate limiting: 0.5s delay between batches

### Qdrant Service (services/qdrant_service.py)

**Responsibilities:**
1. **Collection Management** (qdrant_service.py:30-78)
   - Collection: `book_content`
   - Vector size: 1536 (matches OpenAI embeddings)
   - Distance metric: Cosine similarity
   - Payload indices: `module_number`, `chapter_number`

2. **Semantic Search** (qdrant_service.py:80-144)
   - Input: Query vector (1536-dim)
   - Filters: Optional module/chapter filters
   - Score threshold: 0.7 (configurable)
   - Returns: Top 10 chunks with metadata

3. **Upsert Operations** (qdrant_service.py:146-176)
   - Batch insert chunks with embeddings
   - Used during content ingestion

**Chunk Metadata Structure:**
```json
{
  "chunk_id": "uuid",
  "content_text": "actual text content",
  "module_number": 1,
  "chapter_number": 3,
  "section_title": "Custom Messages",
  "public_url": "https://...",
  "score": 0.89
}
```

### Database Service (services/database_service.py)

**PostgreSQL Schema (models/database.py:40-136):**

```
chat_sessions
├── session_id (UUID, PK)
├── user_identifier (text, nullable)
├── start_timestamp
├── last_activity_timestamp
└── message_count

user_queries
├── query_id (UUID, PK)
├── session_id (FK → chat_sessions)
├── query_text (text)
├── query_timestamp
├── mode (full_book | selection)
├── selected_text (text, nullable)
└── embedding (JSONB, nullable)

chat_responses
├── response_id (UUID, PK)
├── query_id (FK → user_queries)
├── response_text (text)
├── source_chunks (JSONB)
├── generation_timestamp
├── response_time_ms
├── model_used (default: gpt-4o-mini)
└── token_usage (JSONB)

user_feedback
├── feedback_id (UUID, PK)
├── response_id (FK → chat_responses)
├── rating (positive | negative)
├── feedback_text (text, nullable)
└── feedback_timestamp
```

**CRUD Operations:**
- `create_session()` - New conversation
- `create_query()` - Save user question
- `create_response()` - Save AI answer
- `create_feedback()` - Save user rating
- `get_session_history()` - Retrieve conversation

## API Endpoints

### 1. Health Check
**GET /api/health** (routers/health.py)
```json
Response: {
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-12-03T..."
}
```

### 2. Session Management
**POST /api/session** (routers/session.py)
```json
Request: { "user_identifier": "string (optional)" }
Response: {
  "session_id": "uuid",
  "created_at": "timestamp"
}
```

### 3. Chat (Main RAG Endpoint)
**POST /api/chat** (routers/chat.py:23-130)
```json
Request: {
  "query_text": "How do I create a ROS 2 node?",
  "mode": "full_book",
  "selected_text": null,
  "session_id": "uuid (optional)"
}

Response: {
  "response_id": "uuid",
  "response_text": "To create a ROS 2 node...",
  "source_chunks": [
    {
      "chunk_id": "uuid",
      "module_number": 1,
      "chapter_number": 2,
      "section_title": "Your First ROS 2 Node",
      "url": "https://...",
      "score": 0.89
    }
  ],
  "response_time_ms": 1850,
  "session_id": "uuid"
}
```

### 4. Feedback
**POST /api/feedback** (routers/feedback.py)
```json
Request: {
  "response_id": "uuid",
  "rating": "positive",
  "feedback_text": "Very helpful!"
}

Response: {
  "feedback_id": "uuid",
  "message": "Feedback recorded successfully"
}
```

**GET /api/analytics/feedback**
```json
Response: {
  "total_count": 100,
  "positive_count": 85,
  "negative_count": 15,
  "positive_rate": 85.0
}
```

## Content Ingestion Flow (scripts/ingest_content.py)

```
┌────────────────────┐
│ Markdown Files     │
│ (book_frontend/    │
│  docs/*)           │
└────────┬───────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 1. Parse Markdown               │
│    • Extract frontmatter (YAML) │
│    • Extract sections           │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 2. Chunk Content                │
│    • LangChain RecursiveText    │
│      CharacterTextSplitter      │
│    • Chunk size: ~500 tokens    │
│    • Overlap: 50 tokens         │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 3. Generate Embeddings          │
│    • OpenAI text-embedding-3-   │
│      small                      │
│    • Batch processing (100)     │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 4. Store in Qdrant              │
│    • Upsert vectors + metadata  │
│    • Create collection if new   │
└─────────────────────────────────┘
```

## Configuration Management (config.py:10-61)

**Environment Variables (.env):**
```bash
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=1000

# Qdrant
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=...
QDRANT_COLLECTION_NAME=book_content
QDRANT_VECTOR_SIZE=1536

# Database
DATABASE_URL=postgresql://user:pass@host/db

# API Server
API_HOST=localhost
API_PORT=8000
CORS_ORIGINS=http://localhost:3000

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10

# Optional
SENTRY_DSN=...
LOG_LEVEL=INFO
```

## Error Handling Flow

```
Try Block
├── HTTPException (400, 404) → Pass through
├── ValueError → 400 Bad Request
└── Generic Exception → 500 Internal Server Error
    └── Log to Sentry (if configured)
```

## Performance Characteristics

**Response Time Breakdown:**
- Embedding generation: ~200ms
- Vector search: ~100-300ms
- LLM generation: ~1000-2000ms
- Database operations: ~50-100ms
- **Total: ~1500-2500ms**

**Rate Limits:**
- 10 requests/minute per IP (configurable)
- OpenAI rate limits apply (tier-based)

## Key Files Reference

| File | Lines | Purpose |
|------|-------|---------|
| `main.py` | 1-77 | FastAPI app initialization, middleware, routers |
| `config.py` | 10-61 | Environment configuration with pydantic-settings |
| `routers/chat.py` | 23-130 | Chat endpoint logic and request handling |
| `routers/session.py` | - | Session creation endpoint |
| `routers/health.py` | - | Health check endpoint |
| `routers/feedback.py` | - | Feedback submission and analytics |
| `services/rag_service.py` | 122-204 | RAG pipeline orchestration |
| `services/qdrant_service.py` | 80-144 | Vector search operations |
| `services/openai_service.py` | 27-125 | OpenAI API integration |
| `services/database_service.py` | 17-265 | PostgreSQL CRUD operations |
| `models/database.py` | 40-136 | SQLAlchemy ORM models |
| `models/schemas.py` | 12-158 | Pydantic validation schemas |
| `scripts/ingest_content.py` | - | Content ingestion script |
| `scripts/verify_chunks.py` | - | Verification script |

## Architecture Patterns

### 1. Service Layer Pattern
All business logic is encapsulated in service classes:
- `RAGService` - Orchestrates RAG pipeline
- `QdrantService` - Handles vector operations
- `OpenAIService` - Manages API calls
- `DatabaseService` - Handles CRUD operations

### 2. Dependency Injection
FastAPI's dependency injection system is used for:
- Database sessions (`get_db`)
- Rate limiting (`limiter`)
- Request validation (Pydantic models)

### 3. Singleton Pattern
Service instances are created once and reused:
```python
rag_service = RAGService()
qdrant_service = QdrantService()
openai_service = OpenAIService()
database_service = DatabaseService()
```

### 4. Repository Pattern
Database operations are abstracted through `DatabaseService`, separating data access from business logic.

## Security Features

1. **Rate Limiting**: 10 requests/minute per IP (configurable)
2. **CORS Protection**: Only allowed origins can access API
3. **Input Validation**: Pydantic schemas validate all inputs
4. **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
5. **Environment Variables**: Secrets managed via `.env` file
6. **Error Masking**: Generic error messages in production

## Monitoring & Observability

1. **Logging**: Structured logging with Python's `logging` module
2. **Error Tracking**: Optional Sentry integration
3. **Performance Metrics**: Response time tracking in database
4. **Feedback Analytics**: User satisfaction metrics
5. **Health Check**: `/api/health` endpoint for monitoring

## Deployment Architecture

```
┌─────────────────┐
│   Render.com    │
│   (Web Service) │
└────────┬────────┘
         │
         ├─────────► OpenAI API (embeddings + chat)
         │
         ├─────────► Qdrant Cloud (vector search)
         │
         └─────────► Neon PostgreSQL (conversation storage)
```

**Environment**: Production
**Build Command**: `pip install -r requirements.txt`
**Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Database Migrations

Using Alembic for schema versioning:
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Summary

This backend implements a production-ready RAG system with:
- **Modular architecture** with clear separation of concerns
- **Comprehensive error handling** and validation
- **Performance optimization** through batching and caching
- **Analytics tracking** for continuous improvement
- **Scalable design** ready for horizontal scaling
- **Production monitoring** with health checks and error tracking

The system processes user queries by embedding them, searching for relevant book content in Qdrant, constructing context-aware prompts, generating responses with OpenAI, and storing everything in PostgreSQL for analytics and conversation continuity.
