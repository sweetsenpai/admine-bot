from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from admine_bot.DB.db_bilder import session, Words


async def message_moderation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.effective_message.text.split(' ')
    for word in text:
        print(word.lower())
        if session.query(Words).where(Words.word == word.lower()).all():
            print('____________________________________')
            chat_id = update.effective_message.chat_id
            message_id = update.effective_message.message_id
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            await context.bot.send_message(chat_id=chat_id, text='ТАК нельзя!!!!')
            break

    return
