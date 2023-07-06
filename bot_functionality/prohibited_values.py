from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from admine_bot.DB.mongo import text_massage_report
from datetime import datetime
from admine_bot.DB.db_bilder import session, Words


async def message_moderation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text.split(' ')
    for word in text:
        if session.query(Words).where(Words.word == word.lower()).all():

            await text_massage_report(update, context)
            break

    return

