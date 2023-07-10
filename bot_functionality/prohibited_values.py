from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from admine_bot.DB.mongo import text_report_db
from datetime import datetime
from admine_bot.DB.db_bilder import session, Words


async def text_moderation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text.split(' ')
    for word in text:
        if session.query(Words).where(Words.word == word.lower()).all():

            await text_report_db(update, context)
            break

    return

