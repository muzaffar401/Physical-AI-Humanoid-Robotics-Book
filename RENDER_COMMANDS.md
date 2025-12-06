# Render Deployment - Quick Commands Reference

## 🚀 Quick Start Commands

### 1. GitHub Repository Push (First Time)

```bash
# Root directory me jao
cd C:\Users\ma940\Desktop\Physical-AI-Humanoid-Robotics-Book

# Changes check karo
git status

# All changes add karo
git add .

# Commit karo
git commit -m "Add Render deployment configuration"

# Push karo
git push origin main
```

### 2. Render Dashboard Setup

**Browser me ye steps follow karo:**

1. **Render Dashboard**: https://dashboard.render.com
2. **New** → **Blueprint** click karo
3. GitHub repository select karo: `Physical-AI-Humanoid-Robotics-Book`
4. **Apply** click karo
5. Environment variables set karo (see below)

### 3. Environment Variables (Render Dashboard me set karo)

Render Dashboard → Your Service → **Environment** → **Add Environment Variable**

**Required Variables:**
```
OPENAI_API_KEY = sk-your-key-here
QDRANT_URL = https://your-cluster.qdrant.io
QDRANT_API_KEY = your-qdrant-key
DATABASE_URL = postgresql://user:pass@host:port/db
```

**Optional (already in render.yaml):**
- OPENAI_CHAT_MODEL = gpt-4o-mini
- CORS_ORIGINS = https://muzaffar401.github.io,http://localhost:3000
- ENVIRONMENT = production

### 4. Deploy Commands

#### Automatic (Recommended)
```bash
# Code push karo - Render automatically deploy karega
git add .
git commit -m "Update backend"
git push origin main
```

#### Manual Deploy (Render Dashboard)
- **Manual Deploy** → **Deploy latest commit**

### 5. Database Setup Commands

#### Option A: Render Shell (After deployment)

Render Dashboard → Service → **Shell** → Open Shell

```bash
cd backend
alembic upgrade head
python scripts/ingest_content.py --source ../book_frontend/docs --create-collection --batch-size 50
```

#### Option B: Local (Qdrant directly)

```bash
cd backend
python scripts/ingest_content.py --source ../book_frontend/docs --create-collection --batch-size 50
```

### 6. Verify Deployment

```bash
# Health check
curl https://rag-chatbot-api.onrender.com/api/health

# Root endpoint
curl https://rag-chatbot-api.onrender.com/

# API docs
# Browser me: https://rag-chatbot-api.onrender.com/docs
```

### 7. View Logs

**Render Dashboard:**
- Service → **Logs** tab

**Or CLI:**
```bash
render logs
```

## 📋 Complete Deployment Checklist

- [ ] Render account created
- [ ] GitHub repository connected
- [ ] Blueprint created from render.yaml
- [ ] Environment variables set (OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, DATABASE_URL)
- [ ] Service deployed successfully
- [ ] Database migrations run (alembic upgrade head)
- [ ] Content ingested (scripts/ingest_content.py)
- [ ] Health check passed (/api/health)
- [ ] API docs accessible (/docs)
- [ ] Frontend API URL updated

## 🔧 Troubleshooting Commands

### Check Service Status
```bash
# Render Dashboard → Service → Status
# Or
render status
```

### View Recent Logs
```bash
# Render Dashboard → Service → Logs
# Or
render logs --tail 100
```

### Restart Service
```bash
# Render Dashboard → Service → Manual Deploy → Deploy latest commit
```

### Test Database Connection
```bash
# Render Shell me
cd backend
python -c "from config import settings; print(settings.database_url)"
```

### Test Qdrant Connection
```bash
# Render Shell me
cd backend
python -c "from services.qdrant_service import QdrantService; q = QdrantService(); print(q.client.get_collections())"
```

## 📝 Environment Variables Template

```bash
# Copy paste karo Render Dashboard me

OPENAI_API_KEY=sk-...
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=1000

QDRANT_URL=https://...
QDRANT_API_KEY=...
QDRANT_COLLECTION_NAME=book_content
QDRANT_VECTOR_SIZE=768

DATABASE_URL=postgresql://...

ENVIRONMENT=production
CORS_ORIGINS=https://muzaffar401.github.io,http://localhost:3000
RATE_LIMIT_PER_MINUTE=10
LOG_LEVEL=INFO
OMP_NUM_THREADS=1
```

## 🎯 Quick Deployment Summary

1. **Push code**: `git push origin main`
2. **Render Dashboard**: New → Blueprint → Select repo
3. **Set env vars**: OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, DATABASE_URL
4. **Deploy**: Automatic ho jayega
5. **Setup DB**: Shell me `alembic upgrade head`
6. **Ingest content**: `python scripts/ingest_content.py ...`
7. **Test**: `curl https://rag-chatbot-api.onrender.com/api/health`

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Service URL**: `https://rag-chatbot-api.onrender.com`
- **API Docs**: `https://rag-chatbot-api.onrender.com/docs`

---

**Note**: Service name `rag-chatbot-api` hai, isliye URL automatically `rag-chatbot-api.onrender.com` hoga.

