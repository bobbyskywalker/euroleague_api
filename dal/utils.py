from contextlib import contextmanager
import sqlite3

db_path = '../euroleague.db'

@contextmanager
def get_db_conn():
    
    conn = sqlite3.connect(
        db_path, timeout=10
    ) # database lock fix
    try:
        yield conn
    finally:
        conn.close()


