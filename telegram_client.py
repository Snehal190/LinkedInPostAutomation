from __future__ import annotations

import requests

import config

_API = "https://api.telegram.org/bot{token}/{method}"


def _call(method: str, **params):
    url = _API.format(token=config.TELEGRAM_BOT_TOKEN, method=method)
    resp = requests.post(url, json=params, timeout=35)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error on {method}: {data}")
    return data["result"]


def get_updates(offset: int | None):
    params = {"timeout": 25}
    if offset is not None:
        params["offset"] = offset
    return _call("getUpdates", **params)


def send_reply(chat_id, text: str, reply_to_message_id: int | None = None):
    params = {"chat_id": chat_id, "text": text}
    if reply_to_message_id is not None:
        params["reply_to_message_id"] = reply_to_message_id
        params["allow_sending_without_reply"] = True
    return _call("sendMessage", **params)


def matches_target_chat(message: dict) -> bool:
    """True if this message came from the configured TELEGRAM_CHAT_ID.

    TELEGRAM_CHAT_ID may be a numeric id (as a string) or an @username.
    """
    chat = message.get("chat", {})
    target = config.TELEGRAM_CHAT_ID.strip()

    target_numeric = target[1:] if target.startswith("-") else target
    if target_numeric.isdigit():
        try:
            return chat.get("id") == int(target)
        except ValueError:
            return False

    username = chat.get("username")
    target_username = target.lstrip("@")
    return bool(username) and username == target_username
