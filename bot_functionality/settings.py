from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from admine_bot.DB.mongo import text_report_db, flood_report_db, img_report_db


async def seting_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button_names = ['Сквернословие', 'Флуд', 'Флуд картинками', 'Флуд стикерами']
    buttons_list = []
    for index, button in enumerate(button_names):
        buttons_list.append([InlineKeyboardButton(
            text=button,
            callback_data=index
        )])
    await update.effective_message.reply_text(text='Выберете параметр который хотите изменить',
                                              reply_markup=InlineKeyboardMarkup(buttons_list))
    return

