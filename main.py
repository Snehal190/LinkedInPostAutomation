"""
Watches a Telegram chat/channel for new "thoughts". Each one is first run
through the LinkedIn post qualifier rubric; if it qualifies, it's turned into
a LinkedIn post in Meera Pillai's voice via Gemini and replied back
immediately. If it doesn't qualify, the bot replies saying so instead of
drafting anything.

Run:
    python main.py
"""

import sys
import time

import config
import state_store
import telegram_client
from gemini_client import draft_linkedin_post
from qualifier import evaluate_thought


def extract_message(update: dict):
    """A Telegram update is either a regular message or a channel post."""
    return update.get("message") or update.get("channel_post")


def build_discard_reply(result) -> str:
    score = f"{result.score}/8" if result.score is not None else "unscored"
    reason = result.to_strengthen or "Doesn't clear the bar on enough metrics."
    return (
        f"This can be ignored for LinkedIn post (score {score}).\n\n{reason}"
    )


def process_update(update: dict):
    message = extract_message(update)
    if not message:
        return

    if not telegram_client.matches_target_chat(message):
        return

    text = message.get("text") or message.get("caption")
    if not text:
        print(
            f"[skip] update {update['update_id']} has no text/caption "
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

    try:
        post = draft_linkedin_post(text, angle=result.angle)
    except Exception as exc:
        print(f"[error] Gemini draft failed: {exc}", file=sys.stderr)
        telegram_client.send_reply(
            chat_id,
            f"Qualified (score {result.score}/8) but couldn't draft a post — {exc}",
            reply_to_message_id=reply_id,
        )
        return

    telegram_client.send_reply(chat_id, post, reply_to_message_id=reply_id)
    print("[done] draft sent back to Telegram.")


def main():
    config.require_keys()
    state = state_store.load()
    print("Listening for new thoughts on Telegram... (Ctrl+C to stop)")

    while True:
        try:
            updates = telegram_client.get_updates(state.get("offset"))
        except Exception as exc:
            print(f"[error] Telegram poll failed: {exc}", file=sys.stderr)
            time.sleep(config.POLL_INTERVAL_SECONDS)
            continue

        for update in updates:
            process_update(update)
            state["offset"] = update["update_id"] + 1
            state_store.save(state)

        if not updates:
            time.sleep(config.POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
