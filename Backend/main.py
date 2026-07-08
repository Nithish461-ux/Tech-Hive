from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Form, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import Backend.rag_engine as rag_engine
from Backend.document_loader import load_file, load_url
from Backend.models import ChatRequest, ChatResponse, AddUrlRequest, DocumentInfo
from Backend import seed_knowledge_base


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if rag_engine.is_empty():
            seed_knowledge_base.run()
    except Exception as exc:
        print(f"[startup] Could not seed knowledge base: {exc}")
    yield


app = FastAPI(title="AI Knowledge Assistant API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NOTE: Automatic sample seeding is disabled by default so the app preserves only user-provided documents.
# If you want sample content, run Backend/seed_knowledge_base.py manually.
@app.get("/api/health")
def health():
    return {"status": "ok", "knowledge_base_empty": rag_engine.is_empty()}

@app.get("/api/documents", response_model=list[DocumentInfo])
def get_documents():
    return rag_engine.list_documents()

@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Query the knowledge base for the most relevant snippet
    hits = rag_engine.query(req.query.strip(), top_k=1)
    if not hits:
        raise HTTPException(status_code=404, detail="No relevant information found in knowledge base.")
    top = hits[0]
    return {
        "answer": top["text"],
        "category": top.get("category", "General"),
        "confidence": "low",
        "sources": [{
            "source": top.get("source", "unknown"),
            "category": top.get("category", "General"),
            "snippet": top.get("text", ""),
        }],
        "suggested_actions": []
    }

@app.post("/api/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str | None = Query(None),
    category_form: str | None = Form(None),
):
    category = category or category_form or "General"
    data = await file.read()
    try:
        text = load_file(file.filename, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read file: {e}")
    chunks_added = rag_engine.add_document(source=file.filename, category=category, raw_text=text)
    if chunks_added == 0:
        raise HTTPException(status_code=400, detail="No extractable text found in file.")
    return {"source": file.filename, "category": category, "chunks_added": chunks_added}

@app.post("/api/add-url")
def add_url(req: AddUrlRequest):
    try:
        text = load_url(req.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch URL: {e}")
    chunks_added = rag_engine.add_document(source=req.url, category=req.category, raw_text=text)
    if chunks_added == 0:
        raise HTTPException(status_code=400, detail="No extractable text found at that URL.")
    return {"source": req.url, "category": req.category, "chunks_added": chunks_added}