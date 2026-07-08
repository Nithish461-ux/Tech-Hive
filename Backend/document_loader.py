import io
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from docx import Document as DocxDocument

def load_txt_bytes(data: bytes) -> str:
    return data.decode("utf-8", errors="ignore")

def load_pdf_bytes(data: bytes) -> str:
    reader = PdfReader(io.BytesIO(data))
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)

def load_docx_bytes(data: bytes) -> str:
    doc = DocxDocument(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs)

def load_file(filename: str, data: bytes) -> str:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return load_pdf_bytes(data)
    if lower.endswith(".docx"):
        return load_docx_bytes(data)
    return load_txt_bytes(data)

def load_url(url: str, timeout: int = 10) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (AI-Knowledge-Assistant demo bot)"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list:
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == n:
            break
        start = end - overlap
    return chunks