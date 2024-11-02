import os
from dotenv import load_dotenv

def get_base_path():
    load_dotenv()
    base_path = os.getenv('DB_FILE_PATH')
    if not base_path:
        raise Exception("No base path provided")
    return base_path

def get_images_path():
    load_dotenv()
    images_path = os.getenv('IMAGES_PATH')
    if not images_path:
        raise Exception("No images path provided")
    return images_path