"""
Simplified demo backend for testing frontend
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI(title="AI Knowledge Assistant API (Demo)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data storage
mock_knowledge_base = [
    {
        "source": "Academics Guide 2024",
        "category": "Academics",
        "text": "Our institution offers 50+ undergraduate and postgraduate programs. Core subjects include Science, Commerce, and Arts streams.",
        "chunks": 3
    },
    {
        "source": "Admissions FAQ",
        "category": "Admissions",
        "text": "Admission is based on merit and entrance exam scores. Application deadline is usually in June.",
        "chunks": 2
    },
    {
        "source": "Exam Schedule",
        "category": "Exams",
        "text": "Mid-term exams: October, End-semester exams: December. Minimum attendance required: 75%",
        "chunks": 2
    },
    {
        "source": "Library Information",
        "category": "Library",
        "text": "Library hours: 8 AM - 8 PM weekdays, 10 AM - 5 PM weekends. We have 50,000+ books and digital resources.",
        "chunks": 2
    },
    {
        "source": "Hostel Guidelines",
        "category": "Hostel & Campus Life",
        "text": "Hostel curfew is 10 PM on weekdays and 11 PM on weekends. Campus has sports facilities, gym, and mess.",
        "chunks": 2
    },
    {
        "source": "Scholarship Programs",
        "category": "Scholarships & Fees",
        "text": "Merit scholarships up to 100% tuition available. Other schemes: SC/ST scholarships, sports scholarships, need-based aid.",
        "chunks": 3
    },
    {
        "source": "Career Services",
        "category": "Placements & Career",
        "text": "100+ companies recruit from our campus. Average placement package: 6-12 LPA. Career counseling available.",
        "chunks": 2
    }
]

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"

class SourceChunk(BaseModel):
    source: str
    category: str
    snippet: str

class ChatResponse(BaseModel):
    answer: str
    category: str
    confidence: str
    sources: List[SourceChunk]
    suggested_actions: List[str]

class DocumentInfo(BaseModel):
    source: str
    category: str
    chunks: int

class AddUrlRequest(BaseModel):
    url: str
    category: Optional[str] = "General"

@app.get("/api/health")
def health():
    return {"status": "ok", "knowledge_base_empty": len(mock_knowledge_base) == 0}

@app.get("/api/documents", response_model=List[DocumentInfo])
def get_documents():
    return [
        DocumentInfo(source=doc["source"], category=doc["category"], chunks=doc["chunks"])
        for doc in mock_knowledge_base
    ]

@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    query = req.query.strip().lower()
    
    # Simple keyword matching for demo
    matching_docs = []
    keywords = set(query.split())
    
    for doc in mock_knowledge_base:
        doc_text = (doc["source"] + " " + doc["text"]).lower()
        matches = sum(1 for kw in keywords if kw in doc_text)
        if matches > 0:
            matching_docs.append((doc, matches))
    
    if not matching_docs:
        return ChatResponse(
            answer="I don't have information about that topic in the knowledge base yet. Please upload relevant documents or contact your institution's help desk.",
            category="General",
            confidence="low",
            sources=[],
            suggested_actions=["Upload a document", "Try a different question", "Contact the help desk"]
        )
    
    # Sort by relevance
    matching_docs.sort(key=lambda x: x[1], reverse=True)
    top_docs = matching_docs[:3]
    
    # Categorize the question
    question_lower = query
    if any(word in question_lower for word in ["exam", "test", "score"]):
        category = "Exams"
    elif any(word in question_lower for word in ["course", "subject", "class", "program"]):
        category = "Academics"
    elif any(word in question_lower for word in ["apply", "admission", "enroll", "register"]):
        category = "Admissions"
    elif any(word in question_lower for word in ["fee", "scholarship", "financial", "cost"]):
        category = "Scholarships & Fees"
    elif any(word in question_lower for word in ["place", "job", "career", "package", "recruit"]):
        category = "Placements & Career"
    elif any(word in question_lower for word in ["hostel", "dorm", "curfew", "campus", "room"]):
        category = "Hostel & Campus Life"
    elif any(word in question_lower for word in ["library", "book", "resource", "borrow"]):
        category = "Library"
    else:
        category = "General"
    
    # Build answer
    answer_parts = []
    for doc, _ in top_docs:
        answer_parts.append(f"Based on {doc['source']}: {doc['text']}")
    
    answer = "\n\n".join(answer_parts) if answer_parts else "I found some relevant information in our knowledge base."
    
    sources = [
        SourceChunk(
            source=doc["source"],
            category=doc["category"],
            snippet=doc["text"][:200]
        )
        for doc, _ in top_docs
    ]
    
    suggested_actions = [
        "Ask about admission requirements",
        "Learn about scholarships",
        "Check placement statistics"
    ]
    
    return ChatResponse(
        answer=answer,
        category=category,
        confidence="high" if len(top_docs) > 0 else "low",
        sources=sources,
        suggested_actions=suggested_actions
    )

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...), category: str = "General"):
    # Demo: just accept the file
    content = await file.read()
    return {
        "source": file.filename,
        "category": category,
        "chunks_added": max(1, len(content.decode("utf-8", errors="ignore")) // 800)
    }

@app.post("/api/add-url")
def add_url(req: AddUrlRequest):
    # Demo: just accept the URL
    return {
        "source": req.url,
        "category": req.category,
        "chunks_added": 3
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
