import json
import logging
import os

from telegram import Bot

from utils import (
    get_gathered_set_names,
    get_persistence,
    ensure_file,
    get_or_save_sticker_set,
)


def expand_set_files(bot, persistence, set_data):
    for sticker in set_data["stickers"]:
        file_id = sticker["file_id"]
        file = ensure_file(bot, persistence, file_id)
        yield {
            "set_name": set_data["name"],
            "set_title": set_data["title"],
            "emoji": sticker["emoji"],
            "file_id": file_id,
            "url": file["file_path"],
            "size": file["file_size"],
        }


def main():
    persistence = get_persistence()
    bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
    for set_name in sorted(get_gathered_set_names(persistence)):
        set_data = get_or_save_sticker_set(bot, persistence, set_name)
        for datum in expand_set_files(bot, persistence, set_data):
            print(json.dumps(datum))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
