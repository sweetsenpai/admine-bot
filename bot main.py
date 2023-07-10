from passwords import token
import telegram.error
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update
import logging
from bot_functionality.prohibited_values import text_moderation
from DB.mongo import sticker_report_db


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    application = Application.builder().token(token).build()
    application.add_handler(MessageHandler(filters.TEXT, text_moderation))
    application.add_handler(MessageHandler(filters.Sticker.ALL, sticker_report_db))
    application.run_polling()


if __name__ == '__main__':
    main()
