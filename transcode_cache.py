import logging
import os
from multiprocessing.pool import Pool
from pathlib import Path

from PIL import Image

from utils import get_path_from_fileid, read_jsonl


def run_job(row: dict):
    path = get_path_from_fileid(row["file_id"])
    if not os.path.exists(path):
        return False
    filename = os.path.basename(row["url"])
    basename, ext = os.path.splitext(filename)
    dest_basename = f"{row['set_name']}_{row['emoji']}_{basename}"
    if ext == ".webp":
        dest_path = Path("stickers") / row["set_name"] / (dest_basename + ".png")
        if not dest_path.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            img = Image.open(path)
            img.save(dest_path)
            print(row["set_name"], row["emoji"], img.size, img.mode, "->", dest_path)
    else:
        print(f"Unsupported extension {ext} for {dest_basename}.")


def main():
    jobs = list(read_jsonl("./emoji2.jsonl"))
    print(f"{len(jobs)} jobs to run.")
    with Pool() as pool:
        for result in pool.imap_unordered(run_job, jobs, chunksize=10):
            pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
