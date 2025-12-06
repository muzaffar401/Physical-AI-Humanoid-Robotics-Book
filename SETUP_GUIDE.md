
## 📋 Project Overview

This project consists of:

1. **Backend** (`backend/`): FastAPI REST API with RAG (Retrieval-Augmented Generation) chatbot
   - Uses Sentence Transformers for local embeddings (768 dimensions)
   - Uses OpenAI Agents SDK for LLM responses
   - Uses Qdrant Cloud for vector database
   - Uses Neon Postgres for data persistence

2. **Frontend** (`book_frontend/`): Docusaurus website with integrated RAG chatbot
   - React/TypeScript
   - Chatbot plugin with keyboard shortcut (Ctrl+K / Cmd+K)
   - Connects to backend API

## 🔧 Prerequisites

Before starting, ensure you have:

### Required Software
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 20+** ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/downloads))

### Required Accounts & API Keys

1. **OpenAI API Key** (Required)
   - Sign up at https://platform.openai.com/
   - Create an API key in your dashboard
   - You'll need a paid account (pay-as-you-go)

2. **Qdrant Cloud Account** (Required)
   - Sign up at https://cloud.qdrant.io/
   - Create a free cluster
   - Get your cluster URL and API key
   - **Important**: Create a collection named `book_content` with:
     - Vector size: **768** (not 1536!)
     - Distance metric: **Cosine**

3. **Neon Postgres Database** (Required)
   - Sign up at https://neon.tech/
   - Create a free database
   - **Important**: Use the **pooled connection string** (ends with `-pooler`)
   - Copy the connection string

---

## 🚀 Step-by-Step Setup

### Step 1: Clone and Navigate to Project

```bash
# If you haven't cloned yet
git clone <your-repo-url>
cd Physical-AI-Humanoid-Robotics-Book
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: First install will download the BAAI/bge-base-en-v1.5 model (~400MB), which may take 3-5 minutes.

#### 2.3 Create Environment File

Create a `.env` file in the `backend/` directory:

```bash
# Windows (PowerShell)
New-Item -Path .env -ItemType File

# Mac/Linux
touch .env
```

#### 2.4 Configure Environment Variables

Edit `backend/.env` and add the following (replace with your actual values):

```bash
# OpenAI API (Required)
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=1000

# Sentence Transformers (Local embeddings - no API key needed)
EMBEDDING_MODEL_NAME=BAAI/bge-base-en-v1.5
EMBEDDING_DEVICE=cpu
EMBEDDING_BATCH_SIZE=32

# Qdrant Cloud (Required)
QDRANT_URL=https://your-cluster-id.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_COLLECTION_NAME=book_content
QDRANT_VECTOR_SIZE=768

# Neon Postgres Database (Required - use pooled connection string!)
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# API Server Configuration
API_HOST=localhost
API_PORT=8000
API_VERSION=1.0.0
ENVIRONMENT=development

# CORS (Allow frontend to connect)
CORS_ORIGINS=http://localhost:3000

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10

# Logging
LOG_LEVEL=INFO
```

**Important Notes:**
- Use the **pooled connection string** from Neon (contains `-pooler` in the hostname)
- Qdrant collection must have **768 dimensions** (not 1536)
- CORS_ORIGINS should match your frontend URL

#### 2.5 Initialize Database

```bash
# Run database migrations
alembic upgrade head

# If migrations don't exist, create tables directly
python -c "from models.database import init_db; init_db()"
```

#### 2.6 Ingest Book Content

This step populates the vector database with book content:

```bash
# Ingest all markdown files from the book
python scripts/ingest_content.py \
  --source ../book_frontend/docs \
  --create-collection \
  --batch-size 50
```

**What this does:**
- Reads all `.md` and `.mdx` files from `book_frontend/docs/`
- Splits them into chunks
- Generates embeddings using Sentence Transformers
- Uploads to Qdrant Cloud

**Expected output:**
- ~10,000-15,000 chunks created
- Takes 5-15 minutes depending on content size

#### 2.7 Verify Content Ingestion

```bash
python scripts/verify_chunks.py
```

This will:
- Check collection health
- Run a sample query
- Display results

#### 2.8 Start Backend Server

```bash
# Option 1: Run directly
python main.py

# Option 2: Use uvicorn (recommended for development)
uvicorn main:app --reload --host localhost --port 8000
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000
```

**Test the backend:**
```bash
# In another terminal
curl http://localhost:8000/api/health
```

You should see:
```json
{"status":"healthy","version":"1.0.0","timestamp":"..."}
```

**Backend API Endpoints:**
- API Root: http://localhost:8000/
- API Docs (Swagger): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/api/health

---

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend Directory

```bash
# From project root
cd book_frontend
```

#### 3.2 Install Dependencies

```bash
npm install
```

This installs:
- Docusaurus and plugins
- React and TypeScript
- Chatbot plugin dependencies

#### 3.3 Configure Backend API URL (Optional)

If your backend is running on a different URL, edit `src/plugins/rag-chatbot/api/chatClient.ts`:

```typescript
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://your-production-backend-url.com'  // Change this
  : 'http://localhost:8000';  // Default for development
```

#### 3.4 Start Development Server

```bash
npm start
```

**Expected output:**
```
[INFO] Starting the development server...
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

The browser should automatically open to http://localhost:3000

---

## 🎯 Running the Complete Project

### Development Mode

1. **Terminal 1 - Backend:**
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   uvicorn main:app --reload --port 8000
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd book_frontend
   npm start
   ```

3. **Open Browser:**
   - Navigate to http://localhost:3000
   - Press `Ctrl+K` (or `Cmd+K` on Mac) to open the chatbot
   - Ask a question like "What is ROS 2?"

### Testing the Chatbot

1. **Open Chat**: Press `Ctrl+K` or click the chat bubble button
2. **Ask Questions**:
   - "What is ROS 2?"
   - "How do I create a custom message?"
   - "Explain URDF"
   - "What are the prerequisites for Module 1?"
3. **Check Citations**: Click on source links to navigate to book chapters
4. **Provide Feedback**: Use 👍 or 👎 buttons below responses

---

## 🐛 Troubleshooting

### Backend Issues

#### "ModuleNotFoundError: No module named 'X'"
```bash
# Ensure virtual environment is activated
cd backend
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### "Connection refused" or "Cannot connect to Qdrant"
- Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Check Qdrant Cloud dashboard: https://cloud.qdrant.io/
- Ensure collection exists with 768 dimensions

#### "Database connection error"
- Verify `DATABASE_URL` in `.env`
- Use the **pooled connection string** from Neon (contains `-pooler`)
- Test connection: `psql $DATABASE_URL` (if psql is installed)

#### "OpenAI API error"
- Verify `OPENAI_API_KEY` is correct
- Check your OpenAI account has credits
- Verify API key permissions in OpenAI dashboard

#### "Model download failed" (Sentence Transformers)
```bash
# Manually download the model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-base-en-v1.5')"
```

#### Backend won't start
```bash
# Check if port 8000 is already in use
# Windows
netstat -ano | findstr ":8000"

# Mac/Linux
lsof -i :8000

# Kill the process if needed, or change API_PORT in .env
```

### Frontend Issues

#### "Chat widget not appearing"
1. Check browser console for errors (F12)
2. Verify plugin is in `docusaurus.config.ts`:
   ```typescript
   plugins: [
     path.resolve(__dirname, './src/plugins/rag-chatbot/index.js'),
   ],
   ```
3. Clear cache and restart:
   ```bash
   npm run clear
   npm start
   ```

#### "Cannot connect to backend"
1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check `API_BASE_URL` in `chatClient.ts`
3. Verify CORS settings in backend `config.py`:
   ```python
   cors_origins: str = "http://localhost:3000"
   ```

#### "npm install fails"
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### "TypeScript errors"
```bash
# Check TypeScript version
npm list typescript

# Reinstall if needed
npm install --save-dev typescript@~5.6.2
```

### Content Ingestion Issues

#### "No chunks found"
- Verify source path: `--source ../book_frontend/docs`
- Check that markdown files exist in `book_frontend/docs/`
- Ensure files have `.md` or `.mdx` extension

#### "Qdrant collection error"
- Verify collection exists in Qdrant Cloud
- Check vector size is **768** (not 1536)
- Try recreating collection:
  ```bash
  python scripts/ingest_content.py --source ../book_frontend/docs --create-collection --force
  ```

#### "Embedding generation slow"
- First run downloads model (~400MB) - be patient
- Subsequent runs use cached model
- Consider using GPU: set `EMBEDDING_DEVICE=cuda` in `.env` (if GPU available)

---

## 📊 Verification Checklist

Use this checklist to verify your setup:

### Backend
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with all required variables
- [ ] Database initialized (`alembic upgrade head`)
- [ ] Content ingested (`python scripts/ingest_content.py`)
- [ ] Backend server running (`python main.py` or `uvicorn main:app`)
- [ ] Health check passes: `curl http://localhost:8000/api/health`

### Frontend
- [ ] Node.js 20+ installed
- [ ] Dependencies installed (`npm install`)
- [ ] Development server starts (`npm start`)
- [ ] Website loads at http://localhost:3000
- [ ] Chatbot widget appears (press Ctrl+K)

### Integration
- [ ] Chatbot can connect to backend
- [ ] Can send a query and receive a response
- [ ] Citations appear and are clickable
- [ ] Feedback buttons work

---

## 🚢 Production Deployment

### Backend Deployment (Render)

1. **Create Web Service on Render:**
   - Go to https://dashboard.render.com/
   - New → Web Service
   - Connect GitHub repo
   - Configure:
     - **Root Directory**: `backend`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Set Environment Variables:**
   - Add all variables from your `.env` file
   - Update `CORS_ORIGINS` to include production frontend URL

3. **Deploy:**
   - Render will auto-deploy on git push
   - Wait for build to complete (~5-10 minutes)

### Frontend Deployment (GitHub Pages)

1. **Update Backend URL:**
   ```typescript
   // src/plugins/rag-chatbot/api/chatClient.ts
   const API_BASE_URL = 'https://your-backend.onrender.com';
   ```

2. **Build and Deploy:**
   ```bash
   npm run build
   npm run deploy
   ```

---

## 📚 Additional Resources

- **Backend Documentation**: `backend/README.md`
- **Frontend Documentation**: `book_frontend/README.md`
- **Architecture Details**: `backend/ARCHITECTURE.md`
- **Quick Start**: `QUICK_START.md`
- **Implementation Status**: `IMPLEMENTATION_STATUS.md`

---

## 💡 Tips

1. **First Run**: The first time you run the backend, it will download the embedding model (~400MB). This takes 3-5 minutes. Subsequent runs are much faster.

2. **Development**: Use `--reload` flag with uvicorn for auto-restart on code changes:
   ```bash
   uvicorn main:app --reload
   ```

3. **Testing**: Use the Swagger UI at http://localhost:8000/docs to test API endpoints directly.

4. **Logs**: Check backend logs in the terminal for debugging. Frontend logs appear in browser console (F12).

5. **Content Updates**: If you update book content, re-run the ingestion script:
   ```bash
   python scripts/ingest_content.py --source ../book_frontend/docs --force
   ```

---

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review error messages in terminal/browser console
3. Verify all environment variables are set correctly
4. Check that all services (Qdrant, Neon, OpenAI) are accessible
5. Review the documentation files in the project

---

**Happy coding! 🚀**

