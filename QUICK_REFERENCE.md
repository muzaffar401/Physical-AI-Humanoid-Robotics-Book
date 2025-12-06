# Quick Reference - Setup & Run Commands

## 🚀 Quick Start (TL;DR)

### Backend Setup (One-time)
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# Create .env file with your API keys (see SETUP_GUIDE.md)
# Then:
alembic upgrade head
python scripts/ingest_content.py --source ../book_frontend/docs --create-collection
```

### Frontend Setup (One-time)
```bash
cd book_frontend
npm install
```

### Running the Project
```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate  # Windows
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd book_frontend
npm start
```

---

## 📝 Essential Commands

### Backend

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Activate virtual env | `venv\Scripts\activate` (Windows)<br>`source venv/bin/activate` (Mac/Linux) |
| Start server | `python main.py` or `uvicorn main:app --reload` |
| Initialize database | `alembic upgrade head` |
| Ingest content | `python scripts/ingest_content.py --source ../book_frontend/docs --create-collection` |
| Verify ingestion | `python scripts/verify_chunks.py` |
| Test health | `curl http://localhost:8000/api/health` |

### Frontend

| Task | Command |
|------|---------|
| Install dependencies | `npm install` |
| Start dev server | `npm start` |
| Build for production | `npm run build` |
| Clear cache | `npm run clear` |
| Deploy to GitHub Pages | `npm run deploy` |

---

## 🔑 Required Environment Variables

Create `backend/.env` with:

```bash
# Required
OPENAI_API_KEY=sk-...
QDRANT_URL=https://...
QDRANT_API_KEY=...
DATABASE_URL=postgresql://...  # Use pooled connection string!

# Optional (have defaults)
OPENAI_CHAT_MODEL=gpt-4o-mini
QDRANT_COLLECTION_NAME=book_content
QDRANT_VECTOR_SIZE=768
CORS_ORIGINS=http://localhost:3000
```

See `SETUP_GUIDE.md` for detailed instructions.

---

## 🌐 URLs

| Service | URL |
|---------|-----|
| Frontend (dev) | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Health Check | http://localhost:8000/api/health |

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | `pip install -r requirements.txt` |
| Port 8000 in use | Change `API_PORT` in `.env` or kill process |
| Can't connect to backend | Check backend is running, verify CORS settings |
| Chat widget not showing | Check browser console, verify plugin in `docusaurus.config.ts` |
| No search results | Run content ingestion script |
| Database error | Verify `DATABASE_URL` uses pooled connection string |

---

## 📚 Full Documentation

- **Complete Setup Guide**: `SETUP_GUIDE.md`
- **Backend README**: `backend/README.md`
- **Frontend README**: `book_frontend/README.md`
- **Quick Start**: `QUICK_START.md`
- **Architecture**: `backend/ARCHITECTURE.md`

---

## 💡 Tips

1. **First run**: Downloads embedding model (~400MB) - takes 3-5 minutes
2. **Development**: Use `--reload` flag for auto-restart
3. **Testing**: Use Swagger UI at `/docs` endpoint
4. **Keyboard shortcut**: Press `Ctrl+K` (or `Cmd+K`) to open chatbot

---

**Need help?** See `SETUP_GUIDE.md` for detailed instructions and troubleshooting.

