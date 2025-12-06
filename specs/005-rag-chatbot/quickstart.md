# Quickstart Guide: RAG Chatbot Development

**Feature**: Integrated RAG Chatbot for Physical AI Book
**Last Updated**: 2025-12-03

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Backend Development](#backend-development)
4. [Frontend Development](#frontend-development)
5. [Content Ingestion](#content-ingestion)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts
- **OpenAI API**: Create account at https://platform.openai.com/
- **Qdrant Cloud**: Sign up for free tier at https://cloud.qdrant.io/
- **Neon Postgres**: Create free database at https://neon.tech/
- **Render** (for deployment): https://render.com/

### Required Software
- **Python 3.11+**: Download from https://www.python.org/
- **Node.js 18+**: Download from https://nodejs.org/
- **Git**: Download from https://git-scm.com/
- **VS Code** (recommended): https://code.visualstudio.com/

### Environment Variables Template

Create `.env` file in project root:
```bash
# OpenAI API
OPENAI_API_KEY=sk-...

# Qdrant Cloud
QDRANT_URL=https://xxx-yyy.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key

# Neon Postgres
DATABASE_URL=postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/chatbot

# API Configuration
API_HOST=localhost
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,https://muhammad-aneeq.github.io

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10
```

---

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/Muhammad-Aneeq/Physical-AI-Humanoid-Robotics-Book.git
cd Physical-AI-Humanoid-Robotics-Book
git checkout 005-rag-chatbot
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run database migrations
cd backend
alembic upgrade head

# Start development server
uvicorn main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup
```bash
# Navigate to book frontend
cd book_frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will be available at `http://localhost:3000`

---

## Backend Development

### Project Structure
```
backend/
├── main.py                 # FastAPI app entry point
├── routers/
│   ├── chat.py            # Chat endpoints
│   ├── feedback.py        # Feedback endpoints
│   └── health.py          # Health check
├── services/
│   ├── rag_service.py     # RAG logic (embed, search, generate)
│   ├── qdrant_service.py  # Qdrant vector DB client
│   └── openai_service.py  # OpenAI API client
├── models/
│   ├── database.py        # SQLAlchemy models
│   └── schemas.py         # Pydantic request/response models
├── config.py              # Configuration management
└── requirements.txt       # Python dependencies
```

### Key Dependencies
```txt
fastapi[all]==0.109.0
uvicorn[standard]==0.27.0
openai==1.10.0
qdrant-client==1.7.0
sqlalchemy==2.0.25
psycopg[binary]==3.1.16
pydantic==2.5.3
slowapi==0.1.9
python-dotenv==1.0.0
```

### Running Tests
```bash
# Unit tests
pytest tests/unit -v

# Integration tests (requires services running)
pytest tests/integration -v

# Coverage report
pytest --cov=backend --cov-report=html
```

---

## Frontend Development

### Project Structure
```
book_frontend/src/plugins/rag-chatbot/
├── index.tsx              # Plugin registration
├── components/
│   ├── ChatWidget.tsx     # Main chat UI
│   ├── ChatMessage.tsx    # Message bubble
│   ├── ChatInput.tsx      # Input with keyboard shortcuts
│   ├── SelectionDetector.tsx  # Text selection handler
│   └── FeedbackButtons.tsx    # Thumbs up/down
├── hooks/
│   ├── useChat.ts         # Chat state management
│   ├── useSelection.ts    # Text selection hook
│   └── useKeyboard.ts     # Keyboard shortcut handler
├── api/
│   └── chatClient.ts      # Backend API client
└── styles/
    └── chat.module.css    # Component styles
```

### Key Dependencies
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-markdown": "^9.0.1",
    "react-syntax-highlighter": "^15.5.0",
    "@docusaurus/core": "^3.1.0",
    "@docusaurus/preset-classic": "^3.1.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "typescript": "^5.3.0"
  }
}
```

### Testing Frontend
```bash
# Run Jest tests
npm test

# E2E tests with Playwright
npm run test:e2e
```

---

## Content Ingestion

### Ingestion Script
```bash
# Navigate to backend
cd backend

# Run ingestion script
python scripts/ingest_content.py --source ../book_frontend/docs --collection book_content
```

### Ingestion Process
1. **Scan** `book_frontend/docs/` for `.md`/`.mdx` files
2. **Parse** markdown and extract metadata (module, chapter)
3. **Chunk** content (500-1000 tokens, 100-token overlap)
4. **Embed** chunks using OpenAI `text-embedding-3-small`
5. **Upsert** to Qdrant with metadata

### Re-ingestion (Content Updates)
```bash
# Full re-ingestion (clears existing collection)
python scripts/ingest_content.py --source ../book_frontend/docs --force

# Incremental update (only changed files)
python scripts/ingest_content.py --source ../book_frontend/docs --incremental
```

---

## Testing

### Manual Testing Checklist

**Backend API**:
- [ ] Health check: `curl http://localhost:8000/api/health`
- [ ] Create session: `POST /api/session`
- [ ] Full book query: `POST /api/chat` with `mode=full_book`
- [ ] Selection query: `POST /api/chat` with `mode=selection`
- [ ] Submit feedback: `POST /api/feedback`

**Frontend**:
- [ ] Open chat with Ctrl+K (Cmd+K on Mac)
- [ ] Type question and submit
- [ ] Verify response appears with citations
- [ ] Click citation link (navigates to correct page)
- [ ] Select text on page, ask question
- [ ] Verify selection mode indicator
- [ ] Click thumbs up/down
- [ ] Test on mobile browser

### Automated Test Suites

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd book_frontend
npm test

# E2E tests
npm run test:e2e
```

---

## Deployment

### Backend Deployment (Render)

1. **Create Web Service** on Render
   - Repository: Link GitHub repo
   - Branch: `005-rag-chatbot`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables** (Render Dashboard)
   - Add all variables from `.env` template
   - Use Render's secret management

3. **Deploy**
   - Render auto-deploys on push to branch
   - Monitor logs for startup

### Frontend Deployment (GitHub Pages)

```bash
# Build Docusaurus site
cd book_frontend
npm run build

# Deploy to GitHub Pages
npm run deploy
```

Site will be available at: https://muhammad-aneeq.github.io/Physical-AI-Humanoid-Robotics-Book/

---

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**:
```bash
pip install -r backend/requirements.txt
```

**Problem**: `qdrant_client.exceptions.UnexpectedResponse: Unexpected Response: 401 (Unauthorized)`
**Solution**: Check `QDRANT_API_KEY` in `.env`

**Problem**: Database connection error
**Solution**:
```bash
# Test connection
psql $DATABASE_URL
# If fails, regenerate connection string in Neon dashboard
```

### Frontend Issues

**Problem**: Chat widget doesn't appear
**Solution**: Check browser console for errors; verify plugin is registered in `docusaurus.config.ts`

**Problem**: CORS error when calling backend
**Solution**: Add frontend origin to `CORS_ORIGINS` env variable

### Content Ingestion Issues

**Problem**: `OpenAI RateLimitError`
**Solution**: Wait 60 seconds; consider batching smaller chunks

**Problem**: Some chapters missing from search
**Solution**: Check ingestion logs for parsing errors; verify file paths

---

## Development Workflow

1. **Feature branch**: Create from `005-rag-chatbot`
2. **Local testing**: Backend + frontend running concurrently
3. **Commit**: Use conventional commits (`feat:`, `fix:`, `docs:`)
4. **PR**: Submit for review
5. **Deploy**: Auto-deploys on merge to main

## Useful Commands

```bash
# Backend
uvicorn main:app --reload --port 8000  # Start dev server
pytest -v                               # Run tests
alembic revision --autogenerate -m "msg"  # Create migration
alembic upgrade head                    # Run migrations

# Frontend
npm start                               # Start dev server
npm run build                           # Production build
npm test                                # Run tests

# Content
python scripts/ingest_content.py --source ../book_frontend/docs  # Ingest content
python scripts/verify_chunks.py        # Verify ingestion
```

## Additional Resources

- **OpenAPI Docs**: http://localhost:8000/docs (Swagger UI)
- **Qdrant Dashboard**: https://cloud.qdrant.io/
- **Neon Dashboard**: https://console.neon.tech/
- **Render Dashboard**: https://dashboard.render.com/

---

**Next Steps**: After local setup, proceed to Phase 2 (`/sp.tasks`) to generate implementation tasks.
