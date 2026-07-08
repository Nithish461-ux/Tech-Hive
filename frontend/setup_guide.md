# AI Knowledge Assistant - Setup Guide

## ✅ Code Improvements Completed

Your project has been cleaned up and improved with:

- **Better error handling** in backend and frontend
- **Improved validation** for API key, files, and URLs
- **Enhanced logging** for debugging
- **Documentation** added to all API endpoints
- **Better user feedback** with clearer error messages
- **Fixed API URL routing** (frontend → backend connection)
- **Code organization** and consistency improvements

## 🚀 Quick Start (3 Steps)

### Step 1: Set Your Anthropic API Key

1. Open `Backend/.env`
2. Get your API key from https://console.anthropic.com/
3. Add your key:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   ```

### Step 2: Install Dependencies

```bash
cd Backend
pip install -r requirements.txt
cd ..
```

### Step 3: Start the Application

```bash
python run.py
```

This will start:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📋 Features Working

### Chat Questions
- Ask questions about your knowledge base
- Get AI-powered answers with source citations
- Receive suggested next actions

### File Uploads
- Upload `.txt`, `.pdf`, and `.docx` files
- Automatic text extraction and indexing
- Organize by categories (Academics, Exams, Library, etc.)

### Website Integration
- Add content from any website URL
- Automatic web scraping and indexing
- Full text extraction

## 🔧 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/health` | Check if backend is running |
| `GET` | `/api/documents` | List indexed documents |
| `POST` | `/api/chat` | Send a question |
| `POST` | `/api/upload` | Upload a document file |
| `POST` | `/api/add-url` | Add a website URL |

## 🐛 Troubleshooting

### "Backend offline" message
- Make sure `run.py` is running
- Check that port 8000 is not in use
- Look for error messages in the terminal

### Questions not working
- Ensure ANTHROPIC_API_KEY is set in `Backend/.env`
- Upload or add some documents first (knowledge base is empty initially)
- Check that backend is running (`http://localhost:8000/docs`)

### Uploads not working
- Make sure file format is `.txt`, `.pdf`, or `.docx`
- File must contain readable text
- Check terminal for specific error messages

### "Cannot connect to server"
- Verify both servers are running
- Frontend should be at http://localhost:3000
- Backend should be at http://localhost:8000

## 📝 Example Usage

1. **Add a document**:
   - Click "+ Add knowledge source" button
   - Upload a PDF or TXT file
   - Select the appropriate category
   - Wait for indexing to complete

2. **Ask a question**:
   - Type your question in the chat box
   - Press Send or click Enter
   - The AI will search your knowledge base and respond

3. **Add a website**:
   - Click "+ Add knowledge source" button
   - Switch to "Live website" tab
   - Enter a URL
   - The system will fetch and index the content

## 🎯 Next Steps

- Upload your education documents
- Test with various questions
- Monitor terminal for logs and debugging info
- Check API docs at http://localhost:8000/docs for more details

---

**Backend**: Python + FastAPI + ChromaDB + Claude AI
**Frontend**: React + Vite + Tailwind CSS
**Database**: Vector embeddings with Chroma
