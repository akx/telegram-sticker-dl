import logging
import os

from telegram import Bot

from utils import get_gathered_set_names, get_persistence, get_or_save_sticker_set


def main():
    persistence = get_persistence()
    bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
    for set_name in sorted(get_gathered_set_names(persistence)):
        get_or_save_sticker_set(bot, persistence, set_name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
