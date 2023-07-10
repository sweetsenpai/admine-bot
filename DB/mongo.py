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


async def text_report_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_message.from_user.name
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id

    user_card = collection.find_one({'user': user})

    if user_card:
        if 'text_date' in user_card.keys():
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
                                                    until_date=datetime.now() + timedelta(days=1),
                                                    revoke_messages=True)
                    return
            else:
                collection.update_one(filter={'user': user},
                                      update={'$set': {'sticker': 1,
                                                       'sticker_date': datetime.now()}})
        else:
            collection.update_one(filter={'user': user},
                                  update={'$set': {'sticker': 1,
                                                   'sticker_date': datetime.now()}})

    else:
        collection.insert_one({'user': user, 'text': 1, 'text_date': datetime.now()})
    user_card = collection.find_one({'user': user})

    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    await context.bot.send_message(chat_id=chat_id, text='{} вынесено {} предупреждений за нецензурную речь,'
                                                   ' третье будет последним!'.format(user_card.get('user'), user_card.get('text')))
    return


async def sticker_report_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_message.from_user.name
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id

    user_card = collection.find_one({'user': user})

    if user_card:
        if 'sticker_date' in user_card:
            delta_time = datetime.now() - user_card.get('sticker_date')
            if delta_time.seconds / 3600 < 1:
                if user_card.get('sticker') < 10:
                    collection.update_one(filter={'user': user}, update={'$inc': {'sticker': 1},
                                                                         '$set': {'sticker_date': datetime.now()}})
                else:
                    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                    await context.bot.send_message(chat_id=chat_id, text='{} получил бан на час за '
                                                                         'спам стикерами.'.format(user_card.get('user')))
                    await context.bot.banChatMember(chat_id=update.effective_message.chat_id,
                                                    user_id=update.effective_message.from_user.id,
                                                    until_date=datetime.now() + timedelta(hours=1),
                                                    revoke_messages=True)
                    return
            else:
                collection.update_one(filter={'user': user},
                                      update={'$set': {'sticker': 1,
                                                       'sticker_date': datetime.now()}})
        else:
            collection.update_one(filter={'user': user},
                                  update={'$set': {'sticker': 1,
                                                   'sticker_date': datetime.now()}})
    else:
        collection.insert_one({'user': user, 'text': 1, 'text_date': datetime.now()})
    user_card = collection.find_one({'user': user})
    if user_card.get('sticker') >= 7:
        warnings_left = 10 - user_card.get('sticker')
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await context.bot.send_message(chat_id=chat_id, text='{} вынесено  предупреждение за cпам стикерами, в течении часа больше 10 стикеров.\n'
                                                             'Осталось стикеров до бана: {}'.format(user_card.get('user'), warnings_left))

    return

