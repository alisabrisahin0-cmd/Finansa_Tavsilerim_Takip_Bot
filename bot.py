import datetime
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# 1. LOGLAMA AYARI: Botun çalışmasını ve hataları terminalden izleyebilirsin
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- AYARLAR ---
# Güncellediğin Token ve CHAT_ID
BOT_TOKEN = "8798725584:AAEJy2sB39ldN50KlOVXKpUnvmGhXobEjTM" 
MY_CHAT_ID = 915358935

# 2. SAAT KONTROLÜ FONKSİYONU
def is_active_hours():
    """Gece 00:00 ile 10:00 arası False döner, bu saatlerde bot çalışmaz."""
    now = datetime.datetime.now().hour
    if 0 <= now < 10:
        return False
    return True

# 3. ANALİZ KOMUTU (Piyasa yorumu için taslak)
async def analiz_komutu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Sadece senin mesajlarına yanıt verir
    if update.effective_chat.id != MY_CHAT_ID:
        return

    await update.message.reply_text(
        "Teknik ve Temel Analiz süreci başlatıldı...\n"
        "Günlük piyasa yorumu ve derin düşünme sonuçları birazdan iletilecek."
    )
    # Buraya ileride analiz yapan Python fonksiyonlarını bağlayabiliriz.

async def main():
    # Uygulamayı oluştur
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # /analiz komutunu kaydet
    app.add_handler(CommandHandler("analiz", analiz_komutu))

    print(f"Bot aktif. CHAT_ID: {MY_CHAT_ID} için çalışıyor.")

    while True:
        if is_active_hours():
            try:
                print(f"[{datetime.datetime.now()}] Aktif saatler: Bot başlatılıyor.")
                
                await app.initialize()
                await app.start()
                await app.updater.start_polling()

                # Aktif saatler bitene kadar çalışmaya devam et
                while is_active_hours():
                    await asyncio.sleep(60)

                # Saat 00:00 olduğunda güvenli kapatma
                print(f"[{datetime.datetime.now()}] Saat 00:00: Kota koruması için bot durduruluyor.")
                await app.updater.stop()
                await app.stop()
                await app.shutdown()

            except Exception as e:
                print(f"Bağlantı hatası: {e}")
                await asyncio.sleep(60)
        else:
            # Uyku modu (10 dakikada bir kontrol eder)
            await asyncio.sleep(600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot kapatıldı.")
