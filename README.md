# LinkedIn Automation

Watches a Telegram chat/channel for new "thoughts", drafts a LinkedIn post in
Meera Pillai's voice using the Gemini API, and replies with the draft
immediately in the same Telegram thread — ready to copy into LinkedIn.

## How it works

1. `main.py` long-polls the Telegram Bot API (`getUpdates`) for new messages
   in the configured chat/channel.
2. Each new message's text (the "thought") is sent to Gemini, with the
   `skills/meera-pillai-voice` skill (voice rules + brand facts + exemplars)
   loaded as the system instruction.
3. Gemini's draft is sent straight back to Telegram as a reply to the
   original message.

No LinkedIn API is involved — this produces a ready-to-paste draft, it
doesn't publish to LinkedIn itself.

## Setup

1. **Create a Telegram bot**: message [@BotFather](https://t.me/BotFather),
   `/newbot`, and copy the token it gives you.
2. **Connect it to your channel/chat:**
   - Channel: add the bot as an **admin** of the channel with "Post messages"
     permission (so it can reply there). Set `TELEGRAM_CHAT_ID` to the
     channel's `@username`, or its numeric id if it's private.
   - Private group or DM: add the bot, then set `TELEGRAM_CHAT_ID` to that
     chat's numeric id (send a message and check
     `https://api.telegram.org/bot<token>/getUpdates` to find it).
3. **Get a Gemini API key** at https://aistudio.google.com/apikey.
4. ```bash
   cd "LinkedIn Automation"
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # fill in TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GEMINI_API_KEY in .env
   python main.py
   ```

Leave it running (e.g. in a terminal tab, `tmux`, or as a background
process) — it checks for new messages every few seconds and drops the draft
back into the chat as soon as it's ready.

## Project structure

```
main.py                          Poll loop: Telegram -> Gemini -> Telegram reply
config.py                        Loads .env, validates required keys
telegram_client.py                Telegram Bot API (getUpdates / sendMessage)
gemini_client.py                  Gemini API call + posting instructions
voice_skill.py                    Loads the Meera Pillai voice skill into a prompt
state_store.py                    Persists the Telegram update offset (data/state.json)
skills/meera-pillai-voice/        The voice skill (SKILL.md + reference docs)
```

## Notes

- Only text messages (or photo captions) are turned into drafts; anything
  without text is skipped with a log line.
- If Gemini can't draft something (missing data, API error), the bot replies
  with the error instead of failing silently, so you always know it saw the
  message.
- `data/state.json` tracks which Telegram updates have been processed, so
  restarting the script won't re-draft old messages.
