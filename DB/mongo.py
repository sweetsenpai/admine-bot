import pymongo
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db_ban = myclient['ban_db']
try:
    collection = db_ban.create_collection('bans')
except pymongo.errors.CollectionInvalid:
    collection = db_ban.bans


async def text_massage_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_message.from_user.name
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id

    user_card = collection.find_one({'user': user})

    if user_card:
        delta_time = datetime.now() - user_card.get('text_date')
        if delta_time.days < 1:
            if user_card.get('text') < 2:
                collection.update_one(filter={'user': user}, update={'$inc': {'text': 1},
                                                                     '$set': {'text_date': datetime.now()}})
            else:
                await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                await context.bot.send_message(chat_id=chat_id, text='{} получил бан на сутки за '
                                                               'нецензурную речь.'.format(user_card.get('user')))
                await context.bot.banChatMember(chat_id=update.effective_message.chat_id,
                                                user_id=update.effective_message.from_user.id,
                                                until_date=datetime.now() + timedelta(minutes=1.5),
                                                revoke_messages=True)
                return
        else:
            collection.update_one(filter={'user': user},
                                  update={'$set': {'text': 1,
                                                   'text_date': datetime.now()}})

    else:
        collection.insert_one({'user': user, 'text': 1, 'text_date': datetime.now()})
    user_card = collection.find_one({'user': user})

    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    await context.bot.send_message(chat_id=chat_id, text='{} вынесено {} предупреждений за нецензурную речь,'
                                                   ' третье будет последним!'.format(user_card.get('user'), user_card.get('text')))
    return



