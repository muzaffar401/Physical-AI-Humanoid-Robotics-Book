# Research: RAG Chatbot Technology Stack

**Feature**: Integrated RAG Chatbot for Physical AI Book
**Date**: 2025-12-03
**Phase**: 0 - Research & Technology Selection

## Executive Summary

This research document consolidates technology decisions for building a Retrieval-Augmented Generation (RAG) chatbot embedded in the Docusaurus Physical AI book website. All decisions prioritize free-tier compatibility, ease of integration, and proven RAG patterns.

---

## 1. Backend Framework: FastAPI

**Decision**: Use FastAPI (Python 3.11+) for the backend REST API and WebSocket server.

**Rationale**:
- **Async-first**: Native async/await support for concurrent requests and streaming responses
- **Type safety**: Pydantic models enforce request/response validation
- **WebSocket support**: Built-in for real-time streaming chat responses
- **OpenAPI**: Auto-generated API documentation
- **Ecosystem**: Excellent integration with OpenAI SDK, Qdrant, SQLAlchemy
- **Performance**: Fast enough for free-tier workloads (handles 1000+ req/s)

**Alternatives Considered**:
- **Flask**: Lacks native async support; requires extensions for WebSockets
- **Django**: Overkill for API-only backend; heavier than needed
- **Node.js (Express)**: Viable, but Python ecosystem better for AI/ML integrations

**Best Practices**:
- Use FastAPI dependency injection for database/service instances
- Structure as `routers/` for endpoints, `services/` for business logic, `models/` for data
- Enable CORS middleware for Docusaurus frontend origin
- Use Pydantic v2 for validation performance

---

## 2. LLM Integration: OpenAI SDK with gpt-4o-mini

**Decision**: Use OpenAI Python SDK with `gpt-4o-mini` for chat completions and `text-embedding-3-small` for embeddings.

**Rationale**:
- **Cost-effective**: gpt-4o-mini is 60% cheaper than GPT-4, sufficient for Q&A
- **Streaming**: Native streaming support for progressive response display
- **Embeddings**: text-embedding-3-small is optimized for semantic search (1536 dimensions)
- **Reliability**: OpenAI has 99.9% uptime SLA
- **Context window**: 128k tokens supports large book chunks

**Alternatives Considered**:
- **OpenAI ChatKit SDK**: Not officially released; stick with standard SDK
- **Anthropic Claude**: More expensive; no free tier
- **Open-source models (Llama 3)**: Requires hosting infrastructure (exceeds free-tier scope)

**Configuration**:
```python
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# For embeddings
embedding_model = "text-embedding-3-small"
embedding_dimensions = 1536

# For chat
chat_model = "gpt-4o-mini"
temperature = 0.3  # Lower for factual answers
max_tokens = 1000
```

**Best Practices**:
- Use async client for non-blocking I/O
- Implement exponential backoff for rate limit errors
- Cache embeddings to avoid redundant API calls
- Set temperature=0.3 for factual, deterministic answers

---

## 3. Vector Database: Qdrant Cloud Free Tier

**Decision**: Use Qdrant Cloud Free Tier (1GB storage) for vector search.

**Rationale**:
- **Free tier**: 1GB storage sufficient for ~10-15k book chunks
- **Performance**: Sub-100ms search latency for k-NN queries
- **Python SDK**: Native async support, integrates with FastAPI
- **Filtering**: Supports metadata filtering (by module, chapter)
- **Managed**: No ops burden; HTTPS API

**Alternatives Considered**:
- **Pinecone**: Free tier limited to 1 index, 100k vectors (sufficient but less flexible)
- **Weaviate Cloud**: Free tier deprecated; self-hosting required
- **Chroma**: Requires self-hosting; no managed free tier

**Schema Design**:
```python
# Collection: book_content
{
  "vectors": {
    "size": 1536,  # text-embedding-3-small
    "distance": "Cosine"
  },
  "payload_schema": {
    "chunk_id": "keyword",
    "content_text": "text",
    "module_number": "integer",
    "chapter_number": "integer",
    "section_title": "keyword",
    "file_path": "keyword",
    "public_url": "keyword",
    "token_count": "integer"
  }
}
```

**Best Practices**:
- Use cosine similarity for text embeddings
- Create payload indices on module_number, chapter_number for filtered search
- Batch upsert chunks (100 at a time) for efficient ingestion
- Use scroll API for paginated retrieval during ingestion

---

## 4. Relational Database: Neon Serverless Postgres

**Decision**: Use Neon Serverless Postgres Free Tier for chat history and analytics.

**Rationale**:
- **Free tier**: 0.5GB storage, 10GB transfer/month (sufficient for MVP)
- **Serverless**: Auto-scales to zero when idle; no ops burden
- **PostgreSQL**: Full SQL support, JSONB for flexible schemas
- **Branching**: Git-like database branching for dev/staging/prod
- **Integration**: Works with SQLAlchemy, psycopg3

**Alternatives Considered**:
- **Supabase**: Similar offering, but Neon has better cold-start performance
- **PlanetScale (MySQL)**: Free tier deprecated
- **SQLite**: Insufficient for multi-user concurrent writes

**Schema Design**:
```sql
CREATE TABLE chat_sessions (
  session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_identifier TEXT,  -- Anonymous or tracked
  start_timestamp TIMESTAMPTZ DEFAULT NOW(),
  last_activity_timestamp TIMESTAMPTZ DEFAULT NOW(),
  message_count INTEGER DEFAULT 0
);

CREATE TABLE user_queries (
  query_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES chat_sessions(session_id),
  query_text TEXT NOT NULL,
  query_timestamp TIMESTAMPTZ DEFAULT NOW(),
  mode TEXT CHECK (mode IN ('full_book', 'selection')),
  selected_text TEXT,  -- NULL if full_book mode
  embedding VECTOR(1536)  -- pgvector extension
);

CREATE TABLE chat_responses (
  response_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  query_id UUID REFERENCES user_queries(query_id),
  response_text TEXT NOT NULL,
  source_chunks JSONB,  -- Array of chunk_ids used
  generation_timestamp TIMESTAMPTZ DEFAULT NOW(),
  response_time_ms INTEGER,
  model_used TEXT
);

CREATE TABLE user_feedback (
  feedback_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  response_id UUID REFERENCES chat_responses(response_id),
  rating TEXT CHECK (rating IN ('positive', 'negative')),
  feedback_text TEXT,
  feedback_timestamp TIMESTAMPTZ DEFAULT NOW()
);
```

**Best Practices**:
- Use pgvector extension for hybrid search (vector + SQL filters)
- Index on session_id, query_timestamp for analytics queries
- Use JSONB for flexible source_chunks storage
- Enable connection pooling (pg_bouncer built into Neon)

---

## 5. Frontend Integration: Docusaurus Plugin (React Component)

**Decision**: Build a custom React component wrapped in a Docusaurus plugin for the chat interface.

**Rationale**:
- **Native integration**: Docusaurus uses React; no framework mismatch
- **Theming**: Inherits Docusaurus theme (light/dark mode)
- **Positioning**: Can use portal to render chat widget globally
- **Keyboard shortcuts**: React hooks for Ctrl+K/Cmd+K detection

**Component Structure**:
```
book_frontend/
└── src/
    └── plugins/
        └── rag-chatbot/
            ├── index.tsx           # Plugin registration
            ├── ChatWidget.tsx      # Main chat UI
            ├── ChatMessage.tsx     # Message component
            ├── ChatInput.tsx       # Input with keyboard shortcuts
            ├── SelectionDetector.tsx  # Text selection handler
            └── api/
                └── chatClient.ts   # Backend API client
```

**Alternatives Considered**:
- **Iframe embed**: Isolates widget but complicates text selection detection
- **Web Component**: Browser support issues; React integration awkward
- **Third-party chat widget**: Inflexible; doesn't support selection mode

**Best Practices**:
- Use React Context for chat state management
- Implement virtual scrolling for long conversation histories (react-window)
- Use `react-markdown` for rendering chatbot responses with code highlighting
- Store chat history in localStorage (with size limit + LRU eviction)

---

## 6. Content Ingestion: Python Script with Markdown Parser

**Decision**: Build a Python CLI script using `markdown-it-py` to parse and chunk Markdown files.

**Rationale**:
- **Markdown parsing**: markdown-it-py is fast and CommonMark-compliant
- **Chunking strategy**: Recursive character splitting with overlap (LangChain TextSplitter)
- **Metadata extraction**: Parse frontmatter (YAML) for module/chapter metadata
- **Idempotent**: Can re-run to update chunks when content changes

**Chunking Strategy**:
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # ~750 tokens
    chunk_overlap=100,  # Maintain context across boundaries
    separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],  # Respect markdown structure
    length_function=len,
    keep_separator=True
)
```

**Best Practices**:
- Split on markdown headings first to preserve semantic boundaries
- Extract code blocks separately; embed with surrounding text as context
- Strip HTML comments and frontmatter before chunking
- Track file modification times to avoid re-processing unchanged files

---

## 7. Deployment: Render Free Tier (Backend) + GitHub Pages (Frontend)

**Decision**: Deploy FastAPI backend on Render Free Tier; Docusaurus frontend on GitHub Pages.

**Rationale**:
- **Backend (Render)**:
  - Free tier: 750 hours/month (sufficient for demo/MVP)
  - Auto-deploys from GitHub on push to main
  - HTTPS included
  - Spins down after 15 min inactivity (cold start ~30s acceptable for MVP)
- **Frontend (GitHub Pages)**:
  - Already hosting Docusaurus book
  - Free static hosting with custom domain support

**Alternatives Considered**:
- **Railway**: Similar to Render; recent free tier changes make it less attractive
- **Fly.io**: More complex setup; better for production scale
- **Vercel (backend)**: Serverless functions have cold starts; FastAPI WebSockets problematic

**Deployment Architecture**:
```
User → GitHub Pages (Docusaurus + Chat UI)
       ↓ HTTPS
     Render (FastAPI Backend)
       ↓
     Qdrant Cloud (Vectors) + Neon Postgres (Relational) + OpenAI API (LLM)
```

**Best Practices**:
- Use environment variables for API keys (Render secrets)
- Configure CORS to allow requests only from book domain
- Implement health check endpoint (`/api/health`) for monitoring
- Use Render's build cache to speed up deployments

---

## 8. Rate Limiting & Security

**Decision**: Use `slowapi` (FastAPI-compatible) for rate limiting + input sanitization.

**Rationale**:
- **Rate limiting**: Prevent abuse of free-tier APIs (OpenAI, Qdrant)
- **Input sanitization**: Prevent injection attacks (SQL, prompt injection)
- **CORS**: Restrict API access to book domain only

**Configuration**:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat_endpoint(request: Request, query: ChatQuery):
    # Sanitize input
    sanitized_query = bleach.clean(query.text, strip=True)
    ...
```

**Best Practices**:
- Use IP-based rate limiting (get_remote_address)
- Return 429 (Too Many Requests) with Retry-After header
- Log rate limit violations for abuse monitoring
- Use `bleach` library to sanitize user input before LLM submission

---

## 9. Monitoring & Observability

**Decision**: Use free-tier observability tools for MVP.

**Tools**:
- **Application monitoring**: Render built-in logs + metrics
- **Error tracking**: Sentry Free Tier (5k events/month)
- **Analytics**: Plausible Analytics Free Trial or simple custom events to Postgres

**Rationale**:
- Render provides basic CPU/memory metrics and log aggregation
- Sentry catches Python exceptions and provides stack traces
- Plausible is privacy-friendly; no cookies

**Best Practices**:
- Log all API errors with request context (query, session_id)
- Track response times and token usage per query
- Monitor OpenAI API quota usage to avoid surprises
- Set up Sentry alerts for error spikes

---

## 10. Context7 MCP Integration

**Decision**: Use Context7 MCP for fetching up-to-date documentation during development/maintenance.

**Usage**:
- **When**: During system maintenance or adding new technologies
- **What**: Fetch latest docs for OpenAI API, FastAPI, Qdrant, Neon Postgres
- **How**: MCP tools (`mcp__context7__resolve-library-id`, `mcp__context7__get-library-docs`)

**Best Practices**:
- Use mode='code' for API references, mode='info' for conceptual guides
- Cache documentation locally to avoid repeated MCP calls
- Update documentation links in quickstart.md when dependencies change

---

## Summary Table

| Component | Technology | Rationale | Free Tier Limits |
|-----------|-----------|-----------|------------------|
| Backend API | FastAPI (Python 3.11+) | Async, type-safe, WebSocket support | N/A (open-source) |
| LLM | OpenAI gpt-4o-mini + text-embedding-3-small | Cost-effective, reliable, streaming | Pay-as-you-go (~$0.50/1M tokens) |
| Vector DB | Qdrant Cloud | Managed, fast, free tier sufficient | 1GB storage (~15k chunks) |
| Relational DB | Neon Serverless Postgres | Serverless, free tier, full SQL | 0.5GB storage, 10GB transfer/month |
| Frontend | Docusaurus Plugin (React) | Native integration, theming | N/A (client-side) |
| Hosting (Backend) | Render Free Tier | Auto-deploy, HTTPS, easy setup | 750 hours/month, cold starts |
| Hosting (Frontend) | GitHub Pages | Already hosting book | Free static hosting |
| Rate Limiting | slowapi | FastAPI-compatible, simple | N/A (open-source) |
| Monitoring | Render logs + Sentry Free | Basic observability | 5k Sentry events/month |

---

## Next Steps

1. **Phase 1**: Design data models, API contracts, quickstart guide
2. **Phase 2**: Generate implementation tasks from plan
3. **Implementation**: Red-green-refactor cycle per task
