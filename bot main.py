from passwords import token
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
from bot_functionality.prohibited_values import text_moderation, img_moderation
from DB.mongo import sticker_report_db
from bot_functionality.settings import seting_keyboard

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    application = Application.builder().token(token).build()
#    application.add_handler(MessageHandler(filters.TEXT, text_moderation))
    application.add_handler(MessageHandler(filters.Sticker.ALL, sticker_report_db))
    application.add_handler((MessageHandler(filters.PHOTO, img_moderation)))
    application.add_handler((CommandHandler('settings', seting_keyboard)))
    application.run_polling()


if __name__ == '__main__':
    main()
