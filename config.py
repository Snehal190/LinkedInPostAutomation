import os
from dotenv import load_dotenv

load_dotenv()


def _env(name: str, default: str = "") -> str:
    """os.environ.get, but treats a present-but-empty value as unset and
    strips incidental whitespace/quotes.

    Vercel (and other dashboards) can end up storing an env var with an
    empty string, or with surrounding whitespace/quotes from a pasted .env
    blob, either of which silently defeats a plain os.environ.get(name,
    default) or a strict string-equality check downstream.
    """
    value = os.environ.get(name)
    if value is None:
        return default
    value = value.strip().strip('"').strip("'")
    return value or default


TELEGRAM_BOT_TOKEN = _env("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = _env("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = _env("GEMINI_API_KEY")
GEMINI_MODEL = _env("GEMINI_MODEL", "gemini-3.1-pro-preview")

# Optional comma-separated list of keys to rotate through on failure/quota
# errors. Falls back to just GEMINI_API_KEY if unset.
_keys_csv = _env("GEMINI_API_KEYS")
GEMINI_API_KEYS = [k.strip() for k in _keys_csv.split(",") if k.strip()] or (
    [GEMINI_API_KEY] if GEMINI_API_KEY else []
)
POLL_INTERVAL_SECONDS = float(_env("POLL_INTERVAL_SECONDS", "5"))

# Only used by the Vercel webhook path (api/webhook.py), to verify incoming
# requests really came from Telegram. Not needed for local polling.
TELEGRAM_WEBHOOK_SECRET = _env("TELEGRAM_WEBHOOK_SECRET")

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
