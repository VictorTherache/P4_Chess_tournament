from tinydb import TinyDB, Query
import sys


class Player(object):
    """
    Player model, create, read, update or delete data from the player
    table
    """
    def __init__(self, first_name, last_name, date_of_birth, gender, rank):
        """
        Constructor of the class
        """
        self.db = TinyDB('../Models/db.json')
        self.player_table = self.db.table('player_table')
        self.query = Query()
        self.first_name = first_name 
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.rank = rank

    def serialize_player(self):
        serialize_player = {
                'first_name' : self.first_name,
                'last_name' : self.last_name,
                'date_of_birth' : self.date_of_birth,
                'gender' : self.gender,
                'rank' : self.rank
                }
        return serialize_player
    

    def add_to_db(self):
        serialize_player = self.serialize_player()
        self.player_table.insert(serialize_player)


    def check_if_player_exists(self):
        """
        Return true if player exist in db
        """
        if (self.player_table.search(self.query.last_name == self.last_name)
            and self.player_table.search(self.query.first_name == self.first_name)):
            return True
