import os
import subprocess
import logging

from db.db_creator.src.scrape_data import get_teams_jsons, get_player_jsons
from db.db_creator.src.create_db import create_tables
from db.db_creator.src.fill_db import fill_database
from config.env_loader import get_base_path

def create_database():
    print("downloading data...")
    get_teams_jsons()
    get_player_jsons()
    print("creating database...")
    create_tables()
    print("filling tables...")
    db_status = fill_database()
    if db_status == False:
        print("database creation failed!")
        return -1
    else:
        print("database created!")
    print("cleaning up...")
    subprocess.run(["rm -rf players_data"], shell=True)
    subprocess.run(["rm -rf teams_data"], shell=True)
    subprocess.run(["rm -rf __pycache__"], shell=True)
    subprocess.run(["rm -rf src/__pycache__"], shell=True)
    print("done!\ndb name: euroleague.db")

def delete_db():
    db_path = get_base_path()
    if os.path.exists(db_path):
        os.remove(db_path)
        logging.info("-> Database deleted <-")
    else:
        logging.info("-> Database not found <-")