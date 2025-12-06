# RAG Chatbot Plugin for Docusaurus

Intelligent chatbot for the Physical AI & Humanoid Robotics Book powered by RAG (Retrieval-Augmented Generation).

## Features

- 🔍 **Semantic Search**: Finds relevant content using vector embeddings
- 💬 **Natural Conversations**: Powered by OpenAI GPT-4o-mini
- 📚 **Source Citations**: Every answer includes links to book chapters
- ⌨️ **Keyboard Shortcut**: Press `Ctrl+K` (or `⌘K` on Mac) to toggle chat
- 💾 **Persistent History**: Conversations saved in browser localStorage
- 👍 **User Feedback**: Thumbs up/down to improve responses
- 🌓 **Dark Mode Support**: Automatically adapts to Docusaurus theme
- 📱 **Mobile Responsive**: Works on desktop, tablet, and mobile

## Installation

### 1. Install Dependencies

```bash
cd book_frontend
npm install react-markdown @docusaurus/ExecutionEnvironment
```

### 2. Configure Backend API

Edit `src/plugins/rag-chatbot/api/chatClient.ts`:

```typescript
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://your-backend-url.onrender.com'  // Replace with your backend URL
  : 'http://localhost:8000';
```

### 3. Enable Plugin in Docusaurus Config

Edit `docusaurus.config.ts` and add the plugin:

```typescript
const config: Config = {
  // ... existing config

  plugins: [
    './src/plugins/rag-chatbot',
  ],

  // ... rest of config
};
```

Add this after the `presets` section and before `themeConfig`.

### 4. Start Development Server

```bash
npm start
```

The chat widget should appear in the bottom-right corner. Press `Ctrl+K` to open it.

## Backend Setup

The chatbot requires a backend API. See `backend/README.md` for setup instructions.

### Quick Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure .env with API keys
cp .env.template .env
# Edit .env: OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, DATABASE_URL

# Initialize database
alembic upgrade head

# Ingest book content
python scripts/ingest_content.py --source ../book_frontend/docs --create-collection

# Start server
uvicorn main:app --reload
```

## Usage

### Opening the Chat

- **Keyboard Shortcut**: Press `Ctrl+K` (Windows/Linux) or `⌘K` (Mac)
- **Click Button**: Click the chat bubble button in the bottom-right corner

### Asking Questions

Type your question in the input box and press Enter or click "Send".

**Example Questions:**
- "What is ROS 2?"
- "How do I create a custom message?"
- "What are the prerequisites for Module 1?"
- "Explain URDF"

### Providing Feedback

Click the 👍 or 👎 buttons below assistant responses to rate answer quality.

### Clearing History

Click the trash icon (🗑️) in the chat header to clear all conversation history.

## Architecture

```
Frontend (React/TypeScript)
├── components/
│   ├── ChatWidget.tsx       # Main container
│   ├── ChatMessage.tsx      # Message display
│   ├── ChatInput.tsx        # User input
│   ├── CitationLink.tsx     # Source citations
│   └── FeedbackButtons.tsx  # Rating buttons
├── hooks/
│   ├── useChat.ts           # State management
│   └── useKeyboard.ts       # Keyboard shortcuts
├── api/
│   └── chatClient.ts        # Backend API client
└── styles/
    └── chat.module.css      # Responsive styling

Backend (Python/FastAPI)
└── See backend/README.md for details
```

## Customization

### Styling

Edit `styles/chat.module.css` to customize colors, sizes, and animations.

### API Endpoint

Change the backend URL in `api/chatClient.ts`:

```typescript
const API_BASE_URL = 'https://your-custom-backend.com';
```

### Keyboard Shortcut

Modify the key combination in `hooks/useKeyboard.ts`:

```typescript
const isModifierPressed = event.ctrlKey || event.metaKey;
const isKPressed = event.key === 'k' || event.key === 'K';
```

### Welcome Message

Edit the empty state in `components/ChatWidget.tsx`:

```tsx
<div className="chat-empty-state">
  <p>Your custom welcome message</p>
  {/* ... */}
</div>
```

## Troubleshooting

### Chat Widget Not Appearing

1. Check browser console for errors
2. Verify plugin is registered in `docusaurus.config.ts`
3. Ensure dependencies are installed: `npm install`
4. Clear cache: `npm run clear && npm start`

### Backend Connection Errors

1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check CORS configuration in backend `config.py`
3. Verify `API_BASE_URL` in `chatClient.ts` matches backend URL

### No Search Results

1. Verify content is ingested: `python backend/scripts/verify_chunks.py`
2. Check Qdrant connection in backend logs
3. Ensure OpenAI API key is valid

## Performance

- **Initial Load**: ~50KB (gzipped)
- **API Response Time**: <3s (p95)
- **Messages Stored**: Last 50 in localStorage (~10KB)
- **Mobile Performance**: Optimized for 3G networks

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

Part of the Physical AI & Humanoid Robotics Book project.

## Support

For issues or questions:
- Backend: See `backend/README.md`
- Frontend: Check browser console for errors
- API: Test endpoints at `http://localhost:8000/docs`
