"""
Watches a Telegram chat/channel for new "thoughts", turns each one into a
LinkedIn post in Meera Pillai's voice via Gemini, and replies with the draft
immediately in the same Telegram chat.

Run:
    python main.py
"""

import sys
import time

import config
import state_store
import telegram_client
from gemini_client import draft_linkedin_post


def extract_message(update: dict):
    """A Telegram update is either a regular message or a channel post."""
    return update.get("message") or update.get("channel_post")


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
            "(e.g. a photo with no caption) — nothing to draft from."
        )
        return

    print(f"[thought] {text[:80]!r}...")
    try:
        post = draft_linkedin_post(text)
    except Exception as exc:
        print(f"[error] Gemini draft failed: {exc}", file=sys.stderr)
        telegram_client.send_reply(
            message["chat"]["id"],
            f"Couldn't draft a post for that one — {exc}",
            reply_to_message_id=message.get("message_id"),
        )
        return

    telegram_client.send_reply(
        message["chat"]["id"],
        post,
        reply_to_message_id=message.get("message_id"),
    )
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
