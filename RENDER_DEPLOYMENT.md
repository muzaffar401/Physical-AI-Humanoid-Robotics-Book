# Render Deployment Guide - Backend API

## Prerequisites

1. **Render Account**: https://render.com (Sign up karo)
2. **GitHub Repository**: Code already GitHub par hona chahiye
3. **API Keys Ready**:
   - OpenAI API Key
   - Qdrant Cloud URL & API Key
   - PostgreSQL Database URL (Neon ya Render PostgreSQL)

## Step 1: Render Account Setup

### 1.1 Render Dashboard me jao
- https://dashboard.render.com
- Login/Sign up karo

### 1.2 GitHub Connect Karo
- **Account Settings** → **GitHub** → **Connect GitHub**
- Repository access grant karo

## Step 2: Create Web Service (Using Render Dashboard)

### Option A: Using render.yaml (Recommended - Automatic)

1. **New** → **Blueprint** click karo
2. GitHub repository select karo: `Physical-AI-Humanoid-Robotics-Book`
3. Render automatically `render.yaml` detect karega
4. **Apply** click karo
5. Environment variables set karo (Step 3 dekho)

### Option B: Manual Setup (Without render.yaml)

1. **New** → **Web Service** click karo
2. GitHub repository connect karo
3. Settings configure karo:

```
Name: rag-chatbot-api
Region: Oregon (or nearest)
Branch: main (or master)
Root Directory: backend
Environment: Python 3
Build Command: pip install --upgrade pip && pip install torch==2.5.0 --index-url https://download.pytorch.org/whl/cpu && pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 300
```

## Step 3: Environment Variables Set Karo

Render Dashboard me **Environment** section me ye variables add karo:

### Required Variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=1000

# Qdrant Vector Database
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=book_content
QDRANT_VECTOR_SIZE=768

# PostgreSQL Database
DATABASE_URL=postgresql://user:password@host:port/database

# Application Settings
ENVIRONMENT=production
CORS_ORIGINS=https://muzaffar401.github.io,http://localhost:3000
RATE_LIMIT_PER_MINUTE=10
LOG_LEVEL=INFO

# Performance (for free tier)
OMP_NUM_THREADS=1
```

### Optional Variables:

```bash
# Sentry Error Tracking (optional)
SENTRY_DSN=your-sentry-dsn-here

# Embedding Model Settings
EMBEDDING_MODEL_NAME=BAAI/bge-base-en-v1.5
EMBEDDING_DEVICE=cpu
EMBEDDING_BATCH_SIZE=16
```

## Step 4: Deploy Karo

### Automatic Deployment (Recommended)

1. Code push karo GitHub par:
```bash
cd C:\Users\ma940\Desktop\Physical-AI-Humanoid-Robotics-Book
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

2. Render automatically detect karega aur deploy start karega
3. **Events** tab me progress dekh sakte ho

### Manual Deploy (If needed)

Render Dashboard me:
- **Manual Deploy** → **Deploy latest commit**

## Step 5: Database Setup

### 5.1 Database Migrations Run Karo

Render me **Shell** access karke:

```bash
# Render Dashboard → Service → Shell
cd backend
alembic upgrade head
```

Ya phir **Post Deploy Script** add karo `render.yaml` me (optional):

```yaml
postDeployCommand: cd backend && alembic upgrade head
```

### 5.2 Content Ingest Karo (First Time)

**Important**: Pehli baar deploy ke baad content ingest karna hoga.

Render Shell me:
```bash
cd backend
python scripts/ingest_content.py \
  --source ../book_frontend/docs \
  --create-collection \
  --batch-size 50
```

Ya phir local se run karo (Qdrant cloud me directly):
```bash
cd backend
python scripts/ingest_content.py \
  --source ../book_frontend/docs \
  --create-collection \
  --batch-size 50
```

## Step 6: Verify Deployment

### 6.1 Health Check

API URL check karo:
```
https://your-service-name.onrender.com/
```

Expected response:
```json
{
  "name": "RAG Chatbot API",
  "version": "1.0.0",
  "environment": "production",
  "docs": "/docs",
  "health": "/api/health"
}
```

### 6.2 API Documentation

- **Swagger UI**: `https://your-service-name.onrender.com/docs`
- **ReDoc**: `https://your-service-name.onrender.com/redoc`

### 6.3 Test Endpoints

```bash
# Health check
curl https://your-service-name.onrender.com/api/health

# Create session
curl -X POST https://your-service-name.onrender.com/api/session

# Test chat
curl -X POST https://your-service-name.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test-123", "query": "What is ROS 2?", "mode": "full_book"}'
```

## Step 7: Update Frontend Configuration

Frontend me API URL update karo:

`book_frontend/src/plugins/rag-chatbot/api/chatClient.ts` me:

```typescript
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://your-service-name.onrender.com'
  : 'http://localhost:8000';
```

## Troubleshooting

### Build Fail Ho Raha Hai

1. **Logs Check Karo**: Render Dashboard → **Logs** tab
2. Common issues:
   - Dependencies install nahi ho rahi
   - Python version mismatch
   - Memory limit exceeded (free tier)

### Service Start Nahi Ho Raha

1. **Start Command** check karo:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 300
   ```

2. **Environment Variables** verify karo
3. **Health Check Path** check karo: `/`

### Database Connection Error

1. `DATABASE_URL` verify karo
2. Database publicly accessible hai?
3. SSL connection required? Add `?sslmode=require` to URL

### Qdrant Connection Error

1. `QDRANT_URL` aur `QDRANT_API_KEY` check karo
2. Qdrant cluster active hai?
3. Network access allowed?

### Slow Startup (First Time)

- First startup me model download hoga (BAAI/bge-base-en-v1.5)
- 5-10 minutes lag sakte hain
- **Logs** me progress dekh sakte ho

## Render CLI Commands (Optional)

Agar aap CLI use karna chahte ho:

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Deploy service
render deploy

# View logs
render logs

# Check status
render status
```

## Cost Optimization (Free Tier)

1. **Auto-sleep**: Free tier services 15 min inactivity ke baad sleep ho jate hain
2. **First request slow**: Sleep se wake up me 30-60 seconds lag sakte hain
3. **Upgrade option**: Paid plan me always-on available hai

## Monitoring

1. **Logs**: Render Dashboard → **Logs** tab
2. **Metrics**: CPU, Memory usage
3. **Events**: Deploy history
4. **Sentry**: Error tracking (if configured)

## Next Steps

1. ✅ Service deployed
2. ✅ Database migrations run
3. ✅ Content ingested
4. ✅ Frontend API URL updated
5. ✅ Testing complete

## Support

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Community**: https://community.render.com

---

**Deployment URL Format**: `https://rag-chatbot-api.onrender.com` (service name se automatically generate hota hai)

