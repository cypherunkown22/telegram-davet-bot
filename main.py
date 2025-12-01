import os
import pandas as pd
import asyncio
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Senin bilgiler (değiştirme!)
BOT_TOKEN = "8307000762:AAGieOxDk4bIqMUeLFhwj33oqanCeWkmB1Q"
ADMIN_ID = 8164418645

MESAJ = (
    "Merhaba, yeni açılan kanalımıza hepinizi bekliyoruz ❤️\n\n"
    "Kanal linki: https://t.me/tradingmarrket"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Yetkisiz giriş 🚫")
        return
    await update.message.reply_text(
        "Selam patron 👑\n\n"
        "CSV dosyasını at (içinde sadece user ID'ler satır satır olsun)\n"
        "Hemen herkese davet yollayayım 🚀"
    )

async def handle_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.document or not update.message.document.file_name.lower().endswith('.csv'):
        await update.message.reply_text("Kanka sadece .csv dosyası at 🥲")
        return

    await update.message.reply_text("Dosya alındı, başlıyorum... ☕")

    file = await update.message.document.get_file()
    await file.download_to_drive("users.csv")

    try:
        df = pd.read_csv("users.csv", header=None, dtype=str)
        user_ids = df.iloc[:, 0].str.strip().tolist()
        await update.message.reply_text(f"{len(user_ids)} kişi bulundu, gönderiyorum...")
    except Exception as e:
        await update.message.reply_text(f"CSV bozuk → {str(e)[:100]}")
        return

    success = 0
    fail = 0

    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=MESAJ, disable_web_page_preview=True)
            success += 1
            await update.message.reply_text(f"✅ {uid}")
        except:
            fail += 1

        await asyncio.sleep(random.uniform(3, 7))  # Ban yememek için yavaş yavaş

    await update.message.reply_text(
        f"💥 BİTTİ KANKA! 💥\n\n"
        f"Gönderilen: {success}\n"
        f"Olmayan/engelleyen: {fail}\n\n"
        f"Kanalın dolsun aslanım ❤️"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL & filters.ChatType.PRIVATE, handle_csv))
    print("Bot aktif, CSV bekliyor 👑")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
