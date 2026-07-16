import os
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# នាំចូលមុខងារ Database ដែលយើងបានបង្កើតនៅឯកសារ database.py
from database import init_db

# ទាញយកទិន្នន័យពីឯកសារ .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Samy Construction")

# រៀបចំប្រព័ន្ធកត់ត្រា (Logging) សម្រាប់តាមដានសកម្មភាព និងកំហុស
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_main_menu() -> ReplyKeyboardMarkup:
    """បង្កើត Menu Keyboard សម្រាប់ផ្ទាំងខាងក្រោម"""
    keyboard = [
        ["👷 Attendance", "📋 Projects"],
        ["📝 Daily Report", "📦 Materials"],
        ["💰 Expenses", "📊 Reports"],
        ["👤 My Profile", "⚙️ Admin"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ដំណើរការនៅពេលអ្នកប្រើប្រាស់បញ្ជា /start"""
    user = update.effective_user
    
    welcome_text = (
        f"🏗 **{COMPANY_NAME}**\n\n"
        f"Welcome {user.first_name}!\n\n"
        "Samy Construction Management System"
    )

    await update.message.reply_text(
        text=welcome_text,
        reply_markup=get_main_menu(),
        parse_mode="Markdown" # អនុញ្ញាតឱ្យអក្សរដិត (Bold) ដំណើរការ
    )

def main() -> None:
    """មុខងារចម្បងសម្រាប់បញ្ជា Bot ឱ្យដើរ"""
    # ពិនិត្យមើលថាតើមាន Token ឬអត់
    if not BOT_TOKEN or BOT_TOKEN == "ដាក់_TOKEN_ថ្មីរបស់អ្នកនៅទីនេះ":
        logger.error("រកមិនឃើញ BOT_TOKEN ទេ! សូមពិនិត្យមើលឯកសារ .env របស់អ្នកម្តងទៀត។")
        return

    # រៀបចំ Database មុនពេល Bot ចាប់ផ្តើម
    init_db()

    # បង្កើតកម្មវិធី Bot
    app = Application.builder().token(BOT_TOKEN).build()

    # បន្ថែមការបញ្ជា (Command Handlers)
    app.add_handler(CommandHandler("start", start))

    # ចាប់ផ្តើម Bot
    logger.info("Bot កំពុងដំណើរការ... (ចុច Ctrl+C ដើម្បីបញ្ឈប់)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()