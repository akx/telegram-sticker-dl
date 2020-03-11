import hashlib
import json
from pathlib import Path

from telegram import Bot

from persistence import Persistence


def get_gathered_set_names(persistence: Persistence):
    sets = set()
    for gs in persistence.list("gathered_stickers"):
        if isinstance(gs, str):
            gs = json.loads(gs)
        set_name = gs.get("set_name")
        if set_name:
            sets.add(set_name)
    return sets


def get_persistence(name="./tsdl.sqlite3") -> Persistence:
    return Persistence(name)


def ensure_file(bot: Bot, persistence: Persistence, file_id: str) -> dict:
    f_key = f"file:{file_id}"
    file_data = persistence.get_last(f_key)
    if file_data is None:
        print(f"Retrieving file {file_id}")
        file = bot.get_file(file_id=file_id)
        file_data = file.to_dict()
        persistence.add(f_key, file_data)
    return file_data


def get_or_save_sticker_set(bot, persistence, set_name):
    p_key = f"set:{set_name}"
    if p_key not in persistence:
        print(set_name)
        sticker_set = bot.get_sticker_set(name=set_name)
        data = sticker_set.to_dict()
        persistence.add("sets", data)
        persistence.add(p_key, data)
    return data


def get_path_from_fileid(file_id):
    file_id_hash = hashlib.md5(file_id.encode()).hexdigest()
    dest_path = Path("downloads") / file_id_hash[:2] / file_id_hash[:4] / file_id_hash
    return dest_path


def read_jsonl(filename):
    with open(filename, "r") as infp:
        for row in infp:
            yield json.loads(row)
