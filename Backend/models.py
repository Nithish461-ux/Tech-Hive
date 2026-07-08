from pydantic import BaseModel
from typing import List, Optional

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
    confidence: str  # "high" | "low"
    sources: List[SourceChunk]
    suggested_actions: List[str]

class AddUrlRequest(BaseModel):
    url: str
    category: Optional[str] = "General"

class DocumentInfo(BaseModel):
    source: str
    category: str
    chunks: int