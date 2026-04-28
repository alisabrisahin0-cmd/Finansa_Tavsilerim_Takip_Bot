import os
import logging
import yfinance as yf
import pandas_ta as ta
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Loglama ayarları
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Takip Sepeti
SEPET = {
    "ALTIN": "GC=F",
    "GUMUS": "SI=F",
    "BIST100": "XU100.IS",
    "NASDAQ": "^IXIC"
}

# Analiz Fonksiyonu
def analiz_motoru(sembol):
    try:
        df = yf.download(sembol, period="6mo", interval="1d", progress=False)
        if df.empty: return "Veri çekilemedi."

        # Teknik Göstergeler
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['SMA20'] = ta.sma(df['Close'], length=20)
        
        last_price = float(df['Close'].iloc[-1])
        last_rsi = float(df['RSI'].iloc[-1])
        sma20 = float(df['SMA20'].iloc[-1])
        
        # Hacim Analizi (Patlama kontrolü)
        avg_vol = df['Volume'].tail(10).mean()
        last_vol = df['Volume'].iloc[-1]
        hacim_durumu = "Güçlü" if last_vol > avg_vol * 1.5 else "Zayıf"

        # Stratejik Yorum
        if last_rsi > 70:
            yorum = f"⚠️ **Doygunluk!** RSI çok yüksek. Kar satışı makul olabilir. Geri alım için {sma20:.2f} seviyesi beklenebilir."
        elif last_rsi < 35:
            yorum = "💎 **Fırsat!** Herkes korkarken toplama bölgesi olabilir. Arkası dolu bir dönüş beklenebilir."
        else:
            yorum = "☕ **Makul Bölge.** Şu an için büyük bir sapma yok, trendi izle."

        return f"Fiyat: {last_price:.2f}\nRSI: {last_rsi:.1f}\nHacim: {hacim_durumu}\n💡 {yorum}"
    except Exception as e:
        return f"Analiz hatası: {e}"

# Komutlar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Ben senin Finansal Strateji Botunum. Bana bir varlık sorabilirsin (Örn: Gümüş ne olur?) veya /sepet yazarak genel durumu görebilirsin.")

async def sepet_goster(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mesaj = "📊 **GÜNLÜK STRATEJİ SEPETİ**\n\n"
    for isim, sembol in SEPET.items():
        analiz = analiz_motoru(sembol)
        mesaj += f"**{isim}**\n{analiz}\n\n---\n"
    await update.message.reply_text(mesaj, parse_mode="Markdown")

# Soru-Cevap Mantığı
async def mesaj_isleyici(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if "gümüş" in text or "gumus" in text:
        res = analiz_motoru(SEPET["GUMUS"])
        await update.message.reply_text(f"🥈 **Gümüş Analizim:**\n\n{res}", parse_mode="Markdown")
    elif "altın" in text or "altin" in text:
        res = analiz_motoru(SEPET["ALTIN"])
        await update.message.reply_text(f"🥇 **Altın Analizim:**\n\n{res}", parse_mode="Markdown")
    elif "bist" in text:
        res = analiz_motoru(SEPET["BIST100"])
        await update.message.reply_text(f"🇹🇷 **BIST 100 Analizim:**\n\n{res}", parse_mode="Markdown")
    else:
        await update.message.reply_text("Bunu henüz listeme almadım ama /sepet komutuyla genel durumu görebilirsin.")

if __name__ == '__main__':
    # Railway'den TOKEN'ı alıyoruz
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sepet", sepet_goster))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_isleyici))

    app.run_polling()
