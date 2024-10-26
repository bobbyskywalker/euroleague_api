import sqlite3
from inserts.player_class import Player



# algorithm:

# create a player in player table
# find ids of player team and season in order to create playerTeam record
# create playerTeam record
# create playerStats record base of class passed info and player team id
class PlayerInsert:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def insert(self, player_data: Player):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute()
        

