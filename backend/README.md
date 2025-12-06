# RAG Chatbot Backend

REST API backend for the Physical AI & Humanoid Robotics Book RAG chatbot.

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.template .env
# Edit .env with your API keys and configuration
```

### 2. Configure Environment Variables

Edit `.env` with your credentials:

```bash
# OpenAI API
OPENAI_API_KEY=sk-your-key-here

# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-key-here

# Neon Postgres
DATABASE_URL=postgresql://user:pass@host/db

# API Configuration
API_HOST=localhost
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### 3. Initialize Database

```bash
# Run migrations
alembic upgrade head

# Or create tables directly (development)
python -c "from models.database import init_db; init_db()"
```

### 4. Ingest Book Content

```bash
# Ingest markdown files from book_frontend/docs
python scripts/ingest_content.py \
  --source ../book_frontend/docs \
  --create-collection \
  --batch-size 50

# Verify ingestion
python scripts/verify_chunks.py
```

### 5. Run Development Server

```bash
# Start FastAPI server
uvicorn main:app --reload --port 8000

# Or run directly
python main.py
```

API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env.template           # Environment variables template
├── alembic.ini             # Alembic configuration
├── alembic/
│   ├── env.py              # Alembic environment
│   └── versions/           # Database migrations
├── models/
│   ├── database.py         # SQLAlchemy ORM models
│   └── schemas.py          # Pydantic request/response models
├── services/
│   ├── qdrant_service.py   # Qdrant vector DB client
│   ├── openai_service.py   # OpenAI API client
│   ├── rag_service.py      # RAG orchestration logic
│   └── database_service.py # Database CRUD operations
├── routers/
│   ├── health.py           # Health check endpoint
│   ├── session.py          # Session management
│   ├── chat.py             # Chat endpoints (main RAG)
│   └── feedback.py         # User feedback endpoints
├── scripts/
│   ├── ingest_content.py   # Content ingestion script
│   └── verify_chunks.py    # Verification script
└── tests/
    ├── unit/               # Unit tests
    └── integration/        # Integration tests
```

## API Endpoints

### Health Check
- `GET /api/health` - API health status

### Session Management
- `POST /api/session` - Create new chat session

### Chat
- `POST /api/chat` - Send query and get response
  - Supports `full_book` and `selection` modes
  - Returns response with source citations

### Feedback
- `POST /api/feedback` - Submit thumbs up/down feedback
- `GET /api/analytics/feedback` - Get feedback statistics

## Development

### Running Tests

```bash
# Unit tests
pytest tests/unit -v

# Integration tests (requires services running)
pytest tests/integration -v

# Coverage report
pytest --cov=. --cov-report=html
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Content Re-ingestion

```bash
# Full re-ingestion (clears existing)
python scripts/ingest_content.py \
  --source ../book_frontend/docs \
  --force

# Incremental update (only changed files)
# Note: Implement file modification time tracking for this
```

## Deployment

### Deploy to Render

1. Create Web Service on Render
2. Set environment variables in Render dashboard
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy from GitHub (auto-deploys on push)

### Environment Variables (Production)

Set these in Render dashboard:
- `OPENAI_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`
- `DATABASE_URL` (from Neon)
- `CORS_ORIGINS` (production frontend URL)
- `ENVIRONMENT=production`
- `SENTRY_DSN` (optional, for error tracking)

## Troubleshooting

### Database Connection Errors

```bash
# Test connection
psql $DATABASE_URL

# If fails, regenerate in Neon dashboard
```

### Qdrant Connection Errors

```bash
# Verify credentials
# Check QDRANT_URL and QDRANT_API_KEY in .env
```

### OpenAI Rate Limits

```bash
# Reduce batch size in ingestion
python scripts/ingest_content.py --batch-size 25
```

### Import Errors

```bash
# Ensure you're in the backend directory
cd backend

# Activate virtual environment
source venv/bin/activate
```

## Monitoring

- **Logs**: Check console output or Render logs
- **Sentry**: Error tracking (if configured)
- **Qdrant Dashboard**: https://cloud.qdrant.io/
- **Neon Dashboard**: https://console.neon.tech/

## License

Part of the Physical AI & Humanoid Robotics Book project.
