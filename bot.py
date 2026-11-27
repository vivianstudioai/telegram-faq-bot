"""Telegram FAQ bot - answers customer questions from your own FAQ file.

Vivian Studio - https://www.freelancer.com/u/vivianstudioai
"""
import json
import logging
import os
import re
from difflib import get_close_matches
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

FAQ_PATH = Path(os.getenv("FAQ_PATH", "faq.json"))
UNANSWERED_LOG = Path(os.getenv("UNANSWERED_LOG", "unanswered.jsonl"))
MATCH_CUTOFF = float(os.getenv("MATCH_CUTOFF", "0.55"))

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
log = logging.getLogger("faq-bot")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s?]", "", text.lower())).strip()


def load_faq() -> dict:
    with open(FAQ_PATH, encoding="utf-8") as f:
        return json.load(f)


FAQ = load_faq()
# Map every normalized question/alias to its answer.
INDEX = {}
for item in FAQ["entries"]:
    for q in [item["question"], *item.get("aliases", [])]:
        INDEX[normalize(q)] = item["answer"]


def find_answer(text: str):
    q = normalize(text)
    if q in INDEX:
        return INDEX[q]
    close = get_close_matches(q, INDEX.keys(), n=1, cutoff=MATCH_CUTOFF)
    return INDEX[close[0]] if close else None


def log_unanswered(update: Update, text: str) -> None:
    record = {"user_id": update.effective_user.id, "text": text}
    with open(UNANSWERED_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(FAQ["welcome_message"])


async def answer(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    reply = find_answer(text)
    if reply is None:
        log_unanswered(update, text)
        reply = FAQ["fallback_message"]
    await update.message.reply_text(reply)


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]  # from @BotFather
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
    log.info("Bot running. Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
