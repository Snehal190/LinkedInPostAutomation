"""
Core per-update logic: qualify a thought, look up news, draft a LinkedIn post
in Meera Pillai's voice, and reply on Telegram. Shared by the local long-poll
runner (main.py) and the Vercel webhook handler (api/webhook.py) — the two
delivery mechanisms Telegram supports, which are mutually exclusive on
Telegram's side (setting a webhook disables getUpdates, and vice versa).
"""

import sys

import news_client
import telegram_client
from gemini_client import draft_linkedin_post
from qualifier import evaluate_thought


def extract_message(update: dict):
    """A Telegram update is either a regular message or a channel post."""
    return update.get("message") or update.get("channel_post")


def build_discard_reply(result) -> str:
    score = f"{result.score}/8" if result.score is not None else "unscored"
    reason = result.to_strengthen or "Doesn't clear the bar on enough metrics."
    return f"This can be ignored for LinkedIn post (score {score}).\n\n{reason}"


def process_update(update: dict):
    message = extract_message(update)
    if not message:
        return

    if not telegram_client.matches_target_chat(message):
        return

    text = message.get("text") or message.get("caption")
    if not text:
        print(
            f"[skip] update {update.get('update_id')} has no text/caption "
            "(e.g. a photo with no caption) — nothing to evaluate."
        )
        return

    chat_id = message["chat"]["id"]
    reply_id = message.get("message_id")

    print(f"[thought] {text[:80]!r}...")
    try:
        result = evaluate_thought(text)
    except Exception as exc:
        print(f"[error] Qualifier failed: {exc}", file=sys.stderr)
        telegram_client.send_reply(
            chat_id,
            f"Couldn't evaluate that one — {exc}",
            reply_to_message_id=reply_id,
        )
        return

    if result.verdict is None:
        print("[warn] Qualifier output didn't parse — sending raw rubric for review.")
        telegram_client.send_reply(chat_id, result.raw_text, reply_to_message_id=reply_id)
        return

    print(f"[qualifier] verdict={result.verdict} score={result.score}/8")

    if result.verdict == "DISCARD":
        telegram_client.send_reply(
            chat_id, build_discard_reply(result), reply_to_message_id=reply_id
        )
        print("[done] marked as skip, no draft made.")
        return

    news_item = None
    try:
        query = news_client.extract_keywords(text)
        print(f"[news] keywords: {query!r}")
        news_item = news_client.fetch_top_news(query)
        if news_item:
            print(f"[news] found: {news_item.headline!r} ({news_item.source})")
        else:
            print("[news] no relevant article found.")
    except Exception as exc:
        print(f"[warn] News lookup failed, drafting without it: {exc}", file=sys.stderr)

    try:
        post, news_used = draft_linkedin_post(text, angle=result.angle, news_item=news_item)
    except Exception as exc:
        print(f"[error] Gemini draft failed: {exc}", file=sys.stderr)
        telegram_client.send_reply(
            chat_id,
            f"Qualified (score {result.score}/8) but couldn't draft a post — {exc}",
            reply_to_message_id=reply_id,
        )
        return

    if news_used and news_item:
        post += news_client.build_verify_footer(news_item)
        print("[news] used in draft — verify footer attached.")

    telegram_client.send_reply(chat_id, post, reply_to_message_id=reply_id)
    print("[done] draft sent back to Telegram.")
