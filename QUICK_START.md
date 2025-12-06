# RAG Chatbot - Quick Start Guide

**Feature**: 005-rag-chatbot
**Status**: Technology stack migration completed
**Date**: 2025-12-04

## What's Been Done

The RAG Chatbot implementation has been successfully updated to match the tasks.md specification:

### Technology Stack Migrated ✅

**Before:**
- OpenAI text-embedding-3-small (1536 dimensions, costs $0.0001/1K tokens)
- Standard OpenAI SDK for chat completions
- Qdrant configured for 1536-dimensional vectors

**After (Current):**
- **Sentence Transformers** (BAAI/bge-base-en-v1.5, 768 dimensions, FREE)
- **OpenAI Agents Python SDK** for LLM responses
- Qdrant configured for 768-dimensional vectors

### Files Created/Updated ✅

1. **backend/requirements.txt** - Updated with sentence-transformers, openai-agents, torch
2. **backend/config.py** - Updated for 768 dimensions + sentence-transformers config
3. **backend/.env.template** - Updated for new tech stack
4. **backend/services/embedding_service.py** - NEW: Local embeddings (768 dims)
5. **backend/services/agent_service.py** - NEW: OpenAI Agents SDK integration

### Compatible Services ✅

6. **backend/services/qdrant_service.py** - Already uses config.qdrant_vector_size (now 768)

## Benefits of This Migration

- ✅ **Zero embedding costs** - sentence-transformers runs locally
- ✅ **Faster embeddings** - No network latency
- ✅ **Privacy** - Text never leaves server for embeddings
- ✅ **Offline capable** - Embeddings work without internet
- ✅ **High quality** - BAAI/bge-base-en-v1.5 is state-of-the-art

## Next Steps to Complete Implementation

### 1. Update Integration Layer (Priority: HIGH)

The new services need to be integrated into the RAG pipeline:

**File**: `backend/services/rag_service.py`

**Required changes:**
```python
# OLD imports (remove these):
from services.openai_service import openai_service

# NEW imports (add these):
from services.embedding_service import embedding_service
from services.agent_service import agent_service

# Update embed_query method:
# OLD: embedding = await openai_service.embed_text(query_text)
# NEW: embedding = embedding_service.embed_text(query_text)  # Note: sync, not async

# Update generate_answer method:
# OLD: result = await openai_service.generate_response(messages, ...)
# NEW: result = await agent_service.generate_response(system_instructions, user_message, context)
```

### 2. Review Database Models (Priority: MEDIUM)

**File**: `backend/models/database.py`

Check if `user_queries` table has vector column:
```python
# If present, update from:
embedding VECTOR(1536)
# To:
embedding VECTOR(768)
```

If changed, create Alembic migration.

### 3. Clean Up Obsolete Code (Priority: LOW)

**Delete**: `backend/services/openai_service.py` - No longer needed

### 4. Create .gitignore (Priority: LOW)

**File**: `backend/.gitignore`

```
venv/
.env
__pycache__/
.pytest_cache/
*.pyc
.DS_Store
*.log
.coverage
htmlcov/
```

### 5. User Setup Tasks (Required)

**Qdrant Cloud** (T007):
- Create collection `book_content`
- **IMPORTANT**: Set vector size to **768** (not 1536)
- Set distance metric to Cosine
- Copy URL and API key to `.env`

**Neon Postgres** (T008):
- Create database
- **IMPORTANT**: Use pooled connection string (with `-pooler` suffix)
- Copy connection string to `.env`

## Running the Backend

### Quick Start (Simplest)

Navigate to backend directory and run:
```bash
cd D:\spec-driven-dev\physical_ai_and_humanoid_robotics\backend
python main.py
```

This will start the server in the foreground (you'll see logs in terminal, Ctrl+C to stop).

### Background Mode (Recommended)

Run in background with logs:
```bash
cd D:\spec-driven-dev\physical_ai_and_humanoid_robotics\backend
python main.py > backend.log 2>&1 &
```

Check if it's running:
```bash
netstat -ano | findstr ":8000"
```

View logs:
```bash
cat backend/backend.log
# or
tail -f backend/backend.log  # Follow logs in real-time
```

### Using Uvicorn Directly

```bash
cd backend
uvicorn main:app --reload --host localhost --port 8000
```

The `--reload` flag auto-restarts on code changes (good for development).

### Check Backend Status

Test if backend is running:
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{"status":"healthy","version":"1.0.0","timestamp":"2025-12-04T12:22:21.509108"}
```

Available endpoints:
- **API Root**: http://localhost:8000/
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health

### Stop the Backend

Find the process ID:
```bash
netstat -ano | findstr ":8000"
```

Kill it (replace PID with your actual process ID):
```bash
taskkill /F /PID 12336
```

### Startup Times

- **First run**: Takes 3-5 minutes (downloads ML model from HuggingFace, ~400MB)
- **Subsequent runs**: Takes 30-60 seconds (model already cached)

## Installation & Testing

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Note**: First install will download BAAI/bge-base-en-v1.5 model (~400MB).

### Test Embedding Service

```python
from services.embedding_service import embedding_service

# Test single embedding
emb = embedding_service.embed_text("This is a test")
print(f"Embedding dimensions: {len(emb)}")  # Should be 768

# Test batch embeddings
embs = embedding_service.embed_batch(["test1", "test2", "test3"])
print(f"Batch size: {len(embs)}, Dims: {len(embs[0])}")  # 3 embeddings, 768 dims each
```

### Test Agent Service

```python
import asyncio
from services.agent_service import agent_service

async def test():
    result = await agent_service.generate_response(
        system_instructions="You are a helpful assistant",
        user_message="Say hello"
    )
    print(f"Response: {result['response_text']}")
    print(f"Tokens: {result['token_usage']['total_tokens']}")

asyncio.run(test())
```

## Architecture Diagram

```
User → Docusaurus Frontend
       ↓
     FastAPI Backend (main.py)
       ↓
     RAG Service (rag_service.py)
       ├─→ EmbeddingService (sentence-transformers, 768 dims, LOCAL)
       ├─→ QdrantService (768-dim vectors, Qdrant Cloud)
       ├─→ AgentService (OpenAI Agents SDK, gpt-4o-mini, API)
       └─→ DatabaseService (Neon Postgres)
```

## Performance Impact

**Startup Time:**
- First time: +2-3 seconds (model loading)
- Subsequent: Model cached in memory

**Memory Usage:**
- +400MB RAM for embedding model
- Acceptable for most deployments

**Response Time:**
- Embeddings: Faster (no network latency)
- LLM responses: Same (still using OpenAI API)

**Cost:**
- Embeddings: $0 (was ~$0.0001/1K tokens)
- LLM: ~$0.15/$0.60 per 1M tokens (unchanged)

## Troubleshooting

### Import Error: No module named 'agents'
```bash
pip install openai-agents
```

### Import Error: No module named 'sentence_transformers'
```bash
pip install sentence-transformers torch
```

### Pydantic Version Conflict
Requirements.txt now specifies `pydantic>=2.10,<3.0` for openai-agents compatibility.

### Model Download Issues
If model download fails, manually download from HuggingFace:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-base-en-v1.5')
```

## Summary

✅ **Completed:**
- Technology stack migrated to sentence-transformers + OpenAI Agents SDK
- Configuration updated for 768 dimensions
- New services created and tested
- Requirements fixed for dependency compatibility

⚠️ **Remaining:**
- Update rag_service.py to use new services
- Review database models for vector dimensions
- User setup: Qdrant (768 dims) + Neon Postgres
- Delete obsolete openai_service.py

**Estimated Time to Complete**: 30-60 minutes

---

**Questions?** See IMPLEMENTATION_STATUS.md for detailed progress.
