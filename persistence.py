import pickle
import sqlite3
import time
from contextlib import contextmanager


@contextmanager
def get_cursor(name):
    with sqlite3.connect(name) as db:
        c = db.cursor()
        yield c


class Persistence:
    def __init__(self, name):
        self.name = name
        with self.get_cursor() as c:
            c.execute(
                "CREATE TABLE IF NOT EXISTS data (key TEXT, ts INTEGER, val BLOB)"
            )
            c.execute("CREATE UNIQUE INDEX IF NOT EXISTS key_ts ON data (key, ts ASC)")
            c.execute("CREATE INDEX IF NOT EXISTS key ON data (key)")

    def get_cursor(self):
        return get_cursor(self.name)

    def add(self, key, data):
        with self.get_cursor() as c:
            c.execute(
                "INSERT INTO data (key, ts, val) VALUES (?, ?, ?)",
                (
                    key,
                    int(time.clock_gettime(time.CLOCK_MONOTONIC) * 1000),
                    pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL),
                ),
            )

    def list(self, key):
        with self.get_cursor() as c:
            c.execute("SELECT val FROM data WHERE key = ? ORDER BY ts", (key,))
            for row in c:
                yield pickle.loads(row[0])

    def get_last(self, key):
        with self.get_cursor() as c:
            c.execute(
                "SELECT val FROM data WHERE key = ? ORDER BY ts DESC LIMIT 1", (key,)
            )
            for row in c:
                return pickle.loads(row[0])

    def rename(self, old_key, new_key):
        with self.get_cursor() as c:
            c.execute("UPDATE data SET key = ? WHERE key = ?", (new_key, old_key))

    def count(self, key):
        with self.get_cursor() as c:
            c.execute("SELECT COUNT(*) FROM data WHERE key = ?", (key,))
            for row in c:
                return int(row[0])

    def __contains__(self, key):
        return self.count(key) > 0
