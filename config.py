import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-pro-preview")

# Optional comma-separated list of keys to rotate through on failure/quota
# errors. Falls back to just GEMINI_API_KEY if unset.
_keys_csv = os.environ.get("GEMINI_API_KEYS", "")
GEMINI_API_KEYS = [k.strip() for k in _keys_csv.split(",") if k.strip()] or (
    [GEMINI_API_KEY] if GEMINI_API_KEY else []
)
POLL_INTERVAL_SECONDS = float(os.environ.get("POLL_INTERVAL_SECONDS", "5"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "data", "state.json")
SKILL_DIR = os.path.join(BASE_DIR, "skills", "meera-pillai-voice")
QUALIFIER_SKILL_DIR = os.path.join(BASE_DIR, "skills", "meera-linkedin-post-qualifier")


def require_keys():
    """Raise a clear error naming exactly which secrets are still missing."""
    missing = [
        name
        for name, value in (
            ("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
            ("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID),
            ("GEMINI_API_KEY", GEMINI_API_KEY),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing required .env values: "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill them in."
        )
