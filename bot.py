import datetime
import asyncio
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# LOG
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ENV (ÖNEMLİ)
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
MY_CHAT_ID = int(os.getenv("CHAT_ID", "0"))

def is_active_hours():
    now = datetime.datetime.now().hour
    return not (0 <= now < 10)

# KOMUT
async def analiz_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != MY_CHAT_ID:
        return

    await update.message.reply_text(
        "Analiz başlatıldı...\nSonuçlar hazırlanıyor."
    )

# SAAT KONTROL TASK
async def saat_kontrol():
    while True:
        if not is_active_hours():
            print("Pasif saatler (00:00-10:00)")
        await asyncio.sleep(60)

async def main():
    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_TOKEN bulunamadı!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("analiz", analiz_komutu))

    print(f"Bot aktif. CHAT_ID: {MY_CHAT_ID}")

    # Arka plan görev
    asyncio.create_task(saat_kontrol())

    # TEK VE DOĞRU ÇALIŞMA ŞEKLİ
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
