# Telegram FAQ Bot

A production-ready Telegram chatbot that answers customer questions from **your own FAQ file** - no code changes needed to update answers. Built by [Vivian Studio](https://www.freelancer.com/u/vivianstudioai).

The same bot we deploy for restaurants, clinics, and online stores. It answers instantly from your knowledge base, and politely says when it doesn't know - logging every unanswered question so you can grow your FAQ over time.

## Features

- **Answers from your file** - edit `faq.json`, restart, done. No coding.
- **Smart matching** - handles rephrased questions ("when are you open?" vs "opening hours") with alias lists plus fuzzy matching.
- **Honest fallback** - a polite, editable message when no answer matches, instead of guessing.
- **Unanswered-question log** - every miss is appended to `unanswered.jsonl` so you know exactly what to add next.
- **Single dependency** - just `python-telegram-bot`. Runs anywhere Python runs.

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env   # paste your token from @BotFather
python bot.py
```

Message your bot on Telegram - `/start`, then ask anything from `faq.json`.

## Customize

| Setting | Where | Default |
| --- | --- | --- |
| Questions & answers | `faq.json` -> `entries` | sample restaurant FAQ |
| Welcome message | `faq.json` -> `welcome_message` | - |
| Fallback message | `faq.json` -> `fallback_message` | - |
| Match strictness | `MATCH_CUTOFF` env var (0.0-1.0) | `0.55` |

Add a new answer: append an entry to `entries` with a `question`, optional `aliases`, and an `answer`. Restart the bot.

## Deploy

Runs fine on Render, Railway, a VPS, or a Raspberry Pi. For always-on hosting, wrap `python bot.py` in systemd, Docker, or your platform's worker process.

## License

MIT - see [LICENSE](LICENSE).
