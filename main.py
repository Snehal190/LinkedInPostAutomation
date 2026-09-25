"""
Local runner: long-polls Telegram for new thoughts and feeds each one to
pipeline.process_update.

This is the local-dev / run-on-your-own-machine path. In production
(Vercel), Telegram delivers updates via a webhook to api/webhook.py instead
of this polling loop — the two are mutually exclusive on Telegram's side, so
don't run this at the same time a webhook is registered (setWebhook).

Run:
    python main.py
"""

import sys
import time

import config
import state_store
import telegram_client
from pipeline import process_update


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
