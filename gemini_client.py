from __future__ import annotations

import requests

import config
from voice_skill import load_voice_prompt

_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)

_INSTRUCTION_SUFFIX = """

---

You are drafting a LinkedIn post from a raw thought Meera jotted down on
Telegram. Turn that thought into a single LinkedIn post in her voice,
following the "LinkedIn post" format spec and the argument arc above as
closely as the thought allows — but do not force beats that don't fit a
short thought. Output ONLY the finished post text: no preamble, no
"Here's a draft", no markdown formatting, no quotation marks around it. If
the thought is missing a fact you'd need to invent, use a bracketed
[DATA NEEDED: ...] placeholder inline rather than making it up, and still
return only the post text (placeholders and all).
"""


def generate(system_prompt: str, user_text: str, temperature: float = 0.8) -> str:
    """Low-level Gemini call, shared by drafting and qualifying.

    Rotates across config.GEMINI_API_KEYS on auth/quota failures (401/403/429)
    so a revoked or exhausted key doesn't take the whole pipeline down.
    """
    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_text}],
            }
        ],
        "generationConfig": {
            "temperature": temperature,
        },
    }

    url = _ENDPOINT.format(model=config.GEMINI_MODEL)
    keys = config.GEMINI_API_KEYS or [config.GEMINI_API_KEY]

    last_error = None
    for i, key in enumerate(keys):
        resp = requests.post(url, params={"key": key}, json=payload, timeout=60)
        # 401/403 = bad/revoked key, 429 = quota exhausted — try the next key.
        if resp.status_code in (401, 403, 429):
            last_error = RuntimeError(
                f"Gemini key #{i + 1} failed ({resp.status_code}): {resp.text[:200]}"
            )
            continue
        resp.raise_for_status()
        data = resp.json()
        try:
            candidate = data["candidates"][0]
            parts = candidate["content"]["parts"]
            return "".join(p.get("text", "") for p in parts).strip()
        except (KeyError, IndexError) as exc:
            raise RuntimeError(f"Unexpected Gemini response shape: {data}") from exc

    raise last_error or RuntimeError("No Gemini API keys configured.")


def draft_linkedin_post(thought: str, angle: str | None = None) -> str:
    system_prompt = load_voice_prompt() + _INSTRUCTION_SUFFIX
    user_text = f"Raw thought:\n\n{thought}"
    if angle:
        user_text += f"\n\nThe angle to write it from:\n\n{angle}"
    return generate(system_prompt, user_text)
