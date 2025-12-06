# Deployment Guide - RAG Chatbot API on Render

This guide walks you through deploying the FastAPI backend to Render.

## Prerequisites

Before deploying, you need:

1. **GitHub account** with this repository
2. **Render account** (free): https://render.com/
3. **OpenAI API key**: https://platform.openai.com/api-keys
4. **Qdrant Cloud account** (free): https://cloud.qdrant.io/

---

## Step 1: Set Up Qdrant (Vector Database)

1. Go to https://cloud.qdrant.io/ and sign up
2. Create a new cluster (free tier available)
3. Note down:
   - **Cluster URL** (e.g., `https://xyz.qdrant.io`)
   - **API Key** (from cluster settings)

4. Create a collection named `book_content`:
   ```bash
   curl -X PUT 'https://YOUR-CLUSTER.qdrant.io/collections/book_content' \
     -H 'api-key: YOUR-API-KEY' \
     -H 'Content-Type: application/json' \
     -d '{
       "vectors": {
         "size": 768,
         "distance": "Cosine"
       }
     }'
   ```

---

## Step 2: Deploy to Render

### Option A: Using render.yaml (Recommended)

1. **Push code to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Add Render deployment config"
   git push origin main
   ```

2. **Connect to Render**:
   - Go to https://dashboard.render.com/
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repository
   - Select this repo
   - Render will auto-detect `render.yaml`

3. **Set Secret Environment Variables**:

   In the Render dashboard, go to your service and set:

   - `OPENAI_API_KEY` = `sk-your-key-here`
   - `QDRANT_URL` = `https://your-cluster.qdrant.io`
   - `QDRANT_API_KEY` = `your-qdrant-api-key`

4. **Deploy**:
   - Click **"Apply"**
   - Render will create:
     - Web service (FastAPI backend)
     - PostgreSQL database
   - Wait for build to complete (~5-10 min)

### Option B: Manual Setup

1. **Create Web Service**:
   - Go to https://dashboard.render.com/
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repo
   - Configure:
     - **Name**: `rag-chatbot-api`
     - **Region**: Oregon (or closest to you)
     - **Branch**: `main`
     - **Root Directory**: `backend`
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Create PostgreSQL Database**:
   - Click **"New +"** → **"PostgreSQL"**
   - **Name**: `rag-chatbot-db`
   - **Plan**: Free
   - Copy the **Internal Database URL**

3. **Add Environment Variables**:

   In your web service settings, add:

   ```
   OPENAI_API_KEY=sk-your-key-here
   OPENAI_CHAT_MODEL=gpt-4o-mini
   OPENAI_TEMPERATURE=0.3
   OPENAI_MAX_TOKENS=1000

   EMBEDDING_MODEL_NAME=BAAI/bge-base-en-v1.5
   EMBEDDING_DEVICE=cpu
   EMBEDDING_BATCH_SIZE=32

   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your-qdrant-api-key
   QDRANT_COLLECTION_NAME=book_content
   QDRANT_VECTOR_SIZE=768

   DATABASE_URL=[paste internal database URL]

   API_HOST=0.0.0.0
   API_VERSION=1.0.0
   ENVIRONMENT=production

   CORS_ORIGINS=https://yourusername.github.io,http://localhost:3000

   RATE_LIMIT_PER_MINUTE=10
   LOG_LEVEL=INFO
   ```

4. **Deploy**:
   - Click **"Create Web Service"**
   - Wait for deployment (~5-10 min)

---

## Step 3: Initialize Database

Once deployed, run database migrations:

1. **Open Render Shell**:
   - Go to your web service in Render
   - Click **"Shell"** tab
   - Run:
     ```bash
     cd backend
     alembic upgrade head
     ```

---

## Step 4: Populate Vector Database

You need to ingest your book content into Qdrant:

1. **Run the ingestion script** (from Render shell or locally):
   ```bash
   # If running locally, set environment variables first
   export QDRANT_URL=https://your-cluster.qdrant.io
   export QDRANT_API_KEY=your-key

   # Run ingestion
   python scripts/ingest_content.py
   ```

2. **Verify ingestion**:
   ```bash
   curl https://YOUR-CLUSTER.qdrant.io/collections/book_content \
     -H 'api-key: YOUR-API-KEY'
   ```

   Should show `points_count > 0`

---

## Step 5: Test Your Deployment

1. **Get your API URL**:
   - Format: `https://rag-chatbot-api.onrender.com`
   - Find in Render dashboard

2. **Test health endpoint**:
   ```bash
   curl https://rag-chatbot-api.onrender.com/api/health
   ```

   Should return:
   ```json
   {
     "status": "healthy",
     "timestamp": "2024-01-15T10:30:00Z"
   }
   ```

3. **Test chat endpoint**:
   ```bash
   curl -X POST https://rag-chatbot-api.onrender.com/api/chat \
     -H "Content-Type: application/json" \
     -d '{
       "query_text": "What is ROS 2?",
       "mode": "full_book"
     }'
   ```

---

## Step 6: Update Frontend

Update your frontend to use the production API:

1. **Update `book_frontend/src/config.js`** (or wherever API URL is configured):
   ```javascript
   const API_BASE_URL = process.env.NODE_ENV === 'production'
     ? 'https://rag-chatbot-api.onrender.com'
     : 'http://localhost:8000';
   ```

2. **Update CORS_ORIGINS** in Render:
   - After deploying frontend, update the backend's `CORS_ORIGINS` env var
   - Add your frontend URL (e.g., `https://yourusername.github.io`)

---

## Monitoring & Maintenance

### View Logs
- Go to Render dashboard → Your service → **"Logs"** tab
- Real-time logs show requests, errors, startup

### Metrics
- Render provides basic metrics (CPU, memory, requests)
- For advanced monitoring, add Sentry:
  ```bash
  # In Render, add env var:
  SENTRY_DSN=https://your-sentry-dsn
  ```

### Free Tier Limitations
- **Web Service**: Spins down after 15 min of inactivity
  - First request after spin-down takes ~30 seconds
  - Upgrade to paid plan ($7/mo) for always-on
- **Database**: 90 days free, then $7/month
- **Bandwidth**: 100 GB/month free

### Cost Optimization
- Start with free tier
- Monitor usage in Render dashboard
- Upgrade individual services as needed

---

## Troubleshooting

### Build Fails
- Check `requirements.txt` has all dependencies
- Verify Python version compatibility
- Check build logs in Render dashboard

### Database Connection Errors
- Ensure `DATABASE_URL` is set correctly
- Check database is in same region as web service
- Verify migrations ran successfully

### CORS Errors
- Update `CORS_ORIGINS` to include your frontend URL
- Check frontend is using correct API URL
- Verify HTTPS (Render auto-provides SSL)

### Rate Limiting Issues
- Adjust `RATE_LIMIT_PER_MINUTE` env var
- Consider upgrading plan for higher limits

### Vector Search Returns No Results
- Verify Qdrant collection exists
- Check ingestion script ran successfully
- Test embeddings are being generated

---

## Next Steps

1. **Set up CI/CD**: Render auto-deploys on git push
2. **Add monitoring**: Integrate Sentry or similar
3. **Custom domain**: Add in Render settings (paid plans)
4. **Scale**: Upgrade plans as traffic grows

---

## Support

- **Render Docs**: https://render.com/docs
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **FastAPI Docs**: https://fastapi.tiangolo.com/

For issues with this deployment, check logs first, then refer to the troubleshooting section above.
