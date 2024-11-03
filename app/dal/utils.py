from contextlib import contextmanager
import sqlite3
import base64
import os
from PIL import Image

from config.env_loader import get_base_path, get_thumbnails_path

db_path = get_base_path()
th_path = get_thumbnails_path()

# utility func to establish a connection with database, prevents database lock
@contextmanager
def get_db_conn():

    conn = sqlite3.connect(db_path, timeout=10)
    try:
        yield conn
    finally:
        conn.close()

def save_thumbnail(img_path, filename) -> None:
    th_size = (120, 90)
    im = Image.open(img_path)

    im.thumbnail(size=th_size, resample=Image.Resampling.BILINEAR)
    im.save(f'{th_path}{filename}')

# thumbnail base64 encode
def get_th_base64(filename) -> str:
    if filename is None:
        return ""
    file_path = os.path.join(th_path, filename)
    with open(file_path, 'rb') as th:
        th_base64 = base64.b64encode(th.read()).decode('utf-8')
    return th_base64

