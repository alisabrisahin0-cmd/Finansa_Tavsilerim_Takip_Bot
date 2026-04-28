import datetime
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ⚠️ SADECE TEST İÇİN (sonra kaldır!)
BOT_TOKEN = "BURAYA_TOKEN_YAPISTIR"
MY_CHAT_ID = 915358935

def is_active_hours():
    now = datetime.datetime.now().hour
    return not (0 <= now < 10)

async def analiz_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != MY_CHAT_ID:
        return

    await update.message.reply_text("Analiz başlatıldı...")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("analiz", analiz_komutu))

    print("Bot başlatılıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
