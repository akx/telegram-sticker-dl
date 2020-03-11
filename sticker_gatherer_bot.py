import logging
import os

from telegram.ext import MessageHandler, Updater

from utils import get_persistence

logging.basicConfig(level=logging.INFO)

persistence = get_persistence()


def echo(update, context):
    print(vars(context))
    print(vars(update))
    try:
        sticker = update.message.sticker
    except Exception as exc:
        sticker = None

    if sticker:
        persistence.add("gathered_stickers", sticker.to_dict())
        print("OK!", sticker.set_name)


if __name__ == "__main__":
    bot = Updater(token=(os.environ["TELEGRAM_TOKEN"]), use_context=True)
    echo_handler = MessageHandler(filters=None, callback=echo)
    bot.dispatcher.add_handler(echo_handler)
    bot.start_polling(0.1)
