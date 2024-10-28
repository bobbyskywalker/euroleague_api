from contextlib import contextmanager
import sqlite3

from config.env_loader import get_base_path

db_path = get_base_path()

@contextmanager
def get_db_conn():

    conn = sqlite3.connect(db_path, timeout=10)  # database lock fix
    try:
        yield conn
    finally:
        conn.close()
