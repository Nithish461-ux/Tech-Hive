import json
import anthropic
from openai import OpenAI
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, OPENAI_API_KEY, OPENAI_MODEL
from config import DEV_MOCK
import rag_engine
from typing import List

# Initialize clients conditionally
_anthropic_client = None
if ANTHROPIC_API_KEY:
    try:
        _anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    except Exception:
        _anthropic_client = None

if OPENAI_API_KEY:
    try:
        _openai_client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        _openai_client = None
else:
    _openai_client = None

CATEGORIES = [
    "Academics", "Admissions", "Exams", "Library",
    "Hostel & Campus Life", "Scholarships & Fees", "Placements & Career", "General"
]

def classify_intent(question: str) -> str:
    prompt = f"""Classify the following student/staff question into exactly ONE of these categories:
{', '.join(CATEGORIES)}

Question: "{question}"

Reply with ONLY the category name, nothing else."""
    # Try OpenAI first, then Anthropic as a fallback
    try:
        if OPENAI_API_KEY and _openai_client:
            try:
                resp = _openai_client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=60,
                )
                label = resp.choices[0].message.content.strip()
                return label if label in CATEGORIES else "General"
            except Exception as e:
                msg = str(e).lower()
                # If error is quota/invalid key related, allow fallback to Anthropic
                if not ("quota" in msg or "insufficient" in msg or "invalid_api_key" in msg or "incorrect api key" in msg):
                    return "General"

        if _anthropic_client:
            try:
                resp = _anthropic_client.messages.create(
                    model=CLAUDE_MODEL,
                    max_tokens=20,
                    messages=[{"role": "user", "content": prompt}],
                )
                label = resp.content[0].text.strip()
                return label if label in CATEGORIES else "General"
            except Exception:
                return "General"
    except Exception:
        return "General"

def build_context_block(hits: list) -> str:
    blocks = []
    for i, h in enumerate(hits, start=1):
        blocks.append(f"[Source {i}: {h['source']} | Category: {h['category']}]\n{h['text']}")
    return "\n\n".join(blocks)

SYSTEM_PROMPT = """You are the AI Knowledge Assistant for an educational institution.
You help students, employees, and visitors find accurate answers instantly instead of
digging through scattered handbooks, portals, and PDFs.

Rules you must follow:
1. Answer ONLY using the information in the provided context. Do not invent facts.
2. If the context does not contain the answer, say clearly: "I couldn't find this in the
   knowledge base yet" and suggest who the user could contact instead.
3. Be concise, warm, and practical - like a helpful campus staff member, not a search engine.
4. When you use a fact from a source, mention it naturally (e.g. "According to the Exam Policy...").
5. After the answer, on a new line starting with "ACTIONS:", output a JSON array of 1-3 short
   suggested next-step actions the user might want (e.g. ["Draft an email to admissions",
   "Show the full scholarship list", "Set a reminder for the exam date"]). If none make sense,
   output an empty array []."""

def answer_question(question: str) -> dict:
    category = classify_intent(question)
    hits = rag_engine.query(question)

    # Development mock: return a simple canned answer when enabled
    if DEV_MOCK:
        answer_text = "This is a mock answer for development. Enable a real LLM key to get live answers."
        sources = [
            {"source": h["source"], "category": h["category"], "snippet": h["text"][:220]}
            for h in hits[:3]
        ]
        return {
            "answer": answer_text,
            "category": category,
            "confidence": "low",
            "sources": sources,
            "suggested_actions": ["Upload more documents", "Check admin"]
        }

    if not hits:
        return {
            "answer": (
                "The knowledge base is empty right now, so I have nothing to search. "
                "Upload a document or add a website source first."
            ),
            "category": category,
            "confidence": "low",
            "sources": [],
            "suggested_actions": ["Upload a document", "Add a website URL"],
        }

    context = build_context_block(hits)
    user_prompt = f"""Context from the knowledge base:

{context}

---
Question: {question}"""

    def try_openai(messages: List[dict], max_tokens: int = 1000) -> str:
        if not (_openai_client and OPENAI_API_KEY):
            raise RuntimeError("OpenAI client not configured")
        resp = _openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()

    def try_anthropic(prompt: str, max_tokens: int = 700) -> str:
        if not (_anthropic_client and ANTHROPIC_API_KEY):
            raise RuntimeError("Anthropic client not configured")
        resp = _anthropic_client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()

    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        raw = None
        # Try OpenAI first
        if _openai_client and OPENAI_API_KEY:
            try:
                raw = try_openai(messages, max_tokens=1000)
            except Exception as e:
                emsg = str(e).lower()
                # If error suggests quota/invalid key, try Anthropic as fallback
                if _anthropic_client and ("quota" in emsg or "insufficient" in emsg or "invalid_api_key" in emsg or "incorrect api key" in emsg):
                    raw = try_anthropic(user_prompt, max_tokens=700)
                else:
                    raise

        # If OpenAI not configured or returned nothing, try Anthropic
        if raw is None and _anthropic_client and ANTHROPIC_API_KEY:
            try:
                raw = try_anthropic(user_prompt, max_tokens=700)
            except Exception as e:
                emsg = str(e).lower()
                # try falling back to OpenAI if Anthropic reports low credit
                if _openai_client and ("credit" in emsg or "your credit balance" in emsg or "low to access" in emsg):
                    raw = try_openai(messages, max_tokens=1000)
                else:
                    raise

        if raw is None:
            raise RuntimeError("No LLM response obtained from OpenAI or Anthropic")
    except Exception as e:
        # Return a structured error response instead of raising, so the API can
        # send a deterministic JSON back to the frontend.
        return {
            "answer": f"Error: {str(e)}",
            "category": category,
            "confidence": "low",
            "sources": [],
            "suggested_actions": [],
            "_error": True,
            "_error_msg": str(e),
        }

    answer_text = raw
    actions = []
    if "ACTIONS:" in raw:
        answer_text, actions_part = raw.split("ACTIONS:", 1)
        answer_text = answer_text.strip()
        try:
            actions = json.loads(actions_part.strip())
            if not isinstance(actions, list):
                actions = []
        except json.JSONDecodeError:
            actions = []

    confidence = "low" if "couldn't find" in answer_text.lower() or "could not find" in answer_text.lower() else "high"

    sources = [
        {"source": h["source"], "category": h["category"], "snippet": h["text"][:220]}
        for h in hits
    ]

    return {
        "answer": answer_text,
        "category": category,
        "confidence": confidence,
        "sources": sources,
        "suggested_actions": actions,
    }

