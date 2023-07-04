from passwords import token
import telegram.error
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler,filters
from telegram import Update
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    application = Application.builder().token(token).build()
    application.run_polling()


if __name__ == '__main__':
    main()
