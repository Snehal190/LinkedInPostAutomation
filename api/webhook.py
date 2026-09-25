"""
Vercel serverless entrypoint: Telegram calls this over HTTPS for every new
update (instead of us long-polling). Deployed at /api/webhook.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify  # noqa: E402

import config  # noqa: E402
from pipeline import process_update  # noqa: E402

app = Flask(__name__)


@app.route("/api/webhook", methods=["POST"])
def webhook():
    # Telegram echoes back the secret_token set via setWebhook on every
    # request, so we can reject anything that didn't come from Telegram.
    expected = config.TELEGRAM_WEBHOOK_SECRET
    if expected:
        got = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if got != expected:
            return jsonify(ok=False, error="bad secret token"), 401

    update = request.get_json(force=True, silent=True) or {}
    try:
        process_update(update)
    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        # Still 200 — a 5xx makes Telegram retry the same update repeatedly.
    return jsonify(ok=True)


@app.route("/api/webhook", methods=["GET"])
def health():
    return jsonify(ok=True, service="linkedin-automation-webhook")
