import logging
import os
from multiprocessing.pool import Pool

import requests

from utils import get_path_from_fileid, read_jsonl

sess: requests.Session = None


def download_file(url, dest, size):
    if os.path.isfile(dest) and os.stat(dest).st_size == size:
        return False
    global sess
    if not sess:
        sess = requests.Session()
    resp = sess.get(url)
    resp.raise_for_status()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as outf:
        for chunk in resp.iter_content(chunk_size=524288):
            outf.write(chunk)
        print(f"{url} -> {dest}, {outf.tell()}")
    return True


def run_job(row: dict):
    download_file(
        url=(row["url"]),
        dest=(get_path_from_fileid(row["file_id"])),
        size=(row["size"]),
    )


def main():
    jobs = list(read_jsonl("./emoji2.jsonl"))
    print(f"{len(jobs)} jobs to run.")
    with Pool() as pool:
        for result in pool.imap_unordered(run_job, jobs, chunksize=10):
            pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
