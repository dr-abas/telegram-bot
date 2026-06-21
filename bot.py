import logging
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# -----------------------------
# تنظیمات ربات
# -----------------------------
TOKEN = "8916404735:AAEBIheA87H_tWdyNl4JB7fRta5Zm66A_4U"
TARGET_CHANNEL = "@mohre_akhar"     # کانالی که فایل‌ها باید ارسال شوند
MY_CHANNEL_LINK = "@mohre_akhar"    # لینک کانال خودت
ADMINS = {8741862420}               # ادمین‌ها (آیدی عددی)

# -----------------------------
# لاگ‌گیری
# -----------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# -----------------------------
# حذف لینک‌ها ولی نگه داشتن کلمات
# -----------------------------
def remove_links_keep_words(text: str) -> str:
    if not text:
        return ""

    # حذف لینک‌ها
    cleaned = re.sub(r'https?://\S+', '', text)
    cleaned = re.sub(r'www\.\S+', '', cleaned)

    # حذف فاصله‌های اضافی
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned

# -----------------------------
# چک کردن ادمین بودن
# -----------------------------
def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

# -----------------------------
# /start
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if is_admin(user_id):
        await update.message.reply_text("ادمین عزیز، ربات روشنه. فایل بفرست.")
    else:
        await update.message.reply_text("شما ادمین نیستید.")

# -----------------------------
# هندلر فایل‌ها
# -----------------------------
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_id = message.from_user.id

    # فقط ادمین‌ها اجازه دارند
    if not is_admin(user_id):
        await message.reply_text("شما ادمین نیستید.")
        return

    caption = message.caption if message.caption else ""
    cleaned_caption = remove_links_keep_words(caption)

    # اضافه کردن لینک کانال خودت
    final_caption = f"{cleaned_caption}\n\n{MY_CHANNEL_LINK}"

    # -----------------------------
    # ارسال فایل به کانال مقصد
    # -----------------------------
    if message.video:
        file_id = message.video.file_id
        await context.bot.send_video(
            chat_id=TARGET_CHANNEL,
            video=file_id,
            caption=final_caption
        )

    elif message.document:
        file_id = message.document.file_id
        await context.bot.send_document(
            chat_id=TARGET_CHANNEL,
            document=file_id,
            caption=final_caption
        )

    else:
        await message.reply_text("فقط فایل یا ویدیو بفرست.")

# -----------------------------
# اجرای ربات
# -----------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_file))

    app.run_polling()

if __name__ == "__main__":
    main()