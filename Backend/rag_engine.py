import re
import uuid
try:
    import chromadb
except Exception:
    chromadb = None
    _chroma_error = Exception('chromadb not available')

try:
    from sentence_transformers import SentenceTransformer
    _embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
except Exception:
    # Simple fallback embedder returning zero vectors
    class _FallbackEmbedder:
        def encode(self, texts, show_progress_bar=False):
            # Return a list of zero vectors of length 768 for each text
            return [[0.0] * 768 for _ in texts]
    _embedder = _FallbackEmbedder()

from Backend.config import CHROMA_DIR, EMBEDDING_MODEL_NAME, TOP_K_RESULTS
from Backend.document_loader import chunk_text

if chromadb:
    _client = chromadb.PersistentClient(path=CHROMA_DIR)
    _collection = _client.get_or_create_collection(name="knowledge_base")
else:
    # Simple in‑memory mock collection with minimal API used by the code
    class _MockCollection:
        def __init__(self):
            self.store = []
        def add(self, ids, embeddings, documents, metadatas):
            for i, doc in enumerate(documents):
                self.store.append({
                    "id": ids[i],
                    "embedding": embeddings[i] if embeddings else None,
                    "document": doc,
                    "metadata": metadatas[i] if metadatas else {}
                })
        def count(self):
            return len(self.store)
        def query(self, query_embeddings, n_results):
            # Return first n_results entries (no similarity scoring)
            docs = [item["document"] for item in self.store[:n_results]]
            metas = [item["metadata"] for item in self.store[:n_results]]
            dists = [0.0 for _ in range(n_results)]
            return {"documents": [docs], "metadatas": [metas], "distances": [dists]}
        def get(self):
            return {"metadatas": [item["metadata"] for item in self.store]}
    _collection = _MockCollection()

def embed(texts: list) -> list:
    vectors = _embedder.encode(texts, show_progress_bar=False)
    if hasattr(vectors, "tolist"):
        return vectors.tolist()
    return vectors

def add_document(source: str, category: str, raw_text: str) -> int:
    chunks = chunk_text(raw_text)
    if not chunks:
        return 0
    embeddings = embed(chunks)
    ids = [f"{source}-{uuid.uuid4().hex[:8]}-{i}" for i in range(len(chunks))]
    metadatas = [{"source": source, "category": category} for _ in chunks]
    _collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
    return len(chunks)

def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    stopwords = {"the", "a", "an", "is", "are", "to", "for", "and", "or", "of", "in", "on", "with", "what", "how", "why", "when", "who", "do", "does", "did", "can", "be", "must", "this", "that", "those", "these"}
    return [token for token in tokens if token not in stopwords and len(token) > 1]


def _keyword_score(question: str, text: str) -> float:
    q_tokens = set(_tokenize(question))
    d_tokens = _tokenize(text)
    if not q_tokens:
        return 0.0
    overlap = sum(1 for token in d_tokens if token in q_tokens)
    return float(overlap)


def query(question: str, top_k: int = TOP_K_RESULTS) -> list:
    if _collection.count() == 0:
        return []

    if chromadb is None:
        ranked = []
        for item in getattr(_collection, "store", []):
            score = _keyword_score(question, item.get("document", ""))
            ranked.append((score, item))
        ranked.sort(key=lambda entry: entry[0], reverse=True)
        hits = []
        for _, item in ranked[:min(top_k, len(ranked))]:
            meta = item.get("metadata", {})
            hits.append({
                "text": item.get("document", ""),
                "source": meta.get("source", "unknown"),
                "category": meta.get("category", "General"),
                "distance": 0.0,
            })
        return hits

    q_embedding = embed([question])[0]
    results = _collection.query(
        query_embeddings=[q_embedding],
        n_results=min(top_k, _collection.count()),
    )
    hits = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]
    for doc, meta, dist in zip(docs, metas, dists):
        hits.append({
            "text": doc,
            "source": meta.get("source", "unknown"),
            "category": meta.get("category", "General"),
            "distance": dist,
        })
    return hits

def list_documents() -> list:
    if _collection.count() == 0:
        return []
    everything = _collection.get()
    summary = {}
    for meta in everything.get("metadatas", []):
        source = meta.get("source", "unknown")
        category = meta.get("category", "General")
        key = (source, category)
        summary[key] = summary.get(key, 0) + 1
    return [
        {"source": src, "category": cat, "chunks": count}
        for (src, cat), count in summary.items()
    ]

def is_empty() -> bool:
    return _collection.count() == 0