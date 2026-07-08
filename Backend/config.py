import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).with_name(".env")
load_dotenv(dotenv_path)
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_store")
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "4"))
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Optional OpenAI fallback
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-16k")

# Development mock mode: set to 'true' to return canned responses for testing
DEV_MOCK = os.getenv("DEV_MOCK", "false").lower() in ("1", "true", "yes")

if not ANTHROPIC_API_KEY and not OPENAI_API_KEY:
    print(
        "[WARNING] No LLM API key found (ANTHROPIC_API_KEY or OPENAI_API_KEY). "
        "Add one to Backend/.env before running the server."
    )