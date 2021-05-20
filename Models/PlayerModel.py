from tinydb import TinyDB, Query
import sys
from tinydb.operations import delete

class Player(object):
    """
    Player model, create, read, update or delete data from the player
    table
    """
    def __init__(self, first_name, last_name, date_of_birth, gender, rank):
        """
        Constructor of the class
        """
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.rank = rank

    # @classmethod
    def serialize_player(self):
        self.db = TinyDB('Models/db.json')
        self.player_table = self.db.table('player_table')
        self.query = Query()
        serialize_player = {
                'first_name' : self.first_name,
                'last_name' : self.last_name,
                'date_of_birth' : self.date_of_birth,
                'gender' : self.gender,
                'rank' : self.rank
                }
        return serialize_player
    
    
    @classmethod
    def player_list(self):
        """
        Return a table of all the players in database
        """
        self.db = TinyDB('Models/db.json')
        self.player_table = self.db.table('player_table')
        self.query = Query()
        player_table = self.db.table('player_table')
        return player_table
        
    # @classmethod
    def add_to_db(self):
        serialize_player = self.serialize_player()
        self.player_table.insert(serialize_player)

    # @classmethod
    def check_if_player_exists(self):
        """
        Return true if player exist in db
        """
        self.db = TinyDB('Models/db.json')
        self.player_table = self.db.table('player_table')
        self.query = Query()
        if (self.player_table.search(self.query.last_name == self.last_name)
            and self.player_table.search(self.query.first_name == self.first_name)):
            return True

    @classmethod
    def get_players_by_index(self, players_index_list):
        self.db = TinyDB('Models/db.json')
        self.player_table = self.db.table('player_table')
        self.query = Query()
        player_list = []
        for index in players_index_list:
            player = self.player_table.get(doc_id=index)
            player_list.append(player)
        return player_list

    
    @classmethod
    def update_player_rank(self, player_id, new_rank):
        self.db = TinyDB('Models/db.json')
        self.player_table = self.db.table('player_table')
        self.query = Query() 
        # player = self.player_table.get(doc_id=player_id)
        self.player_table.update({'rank' : new_rank}, doc_ids=[player_id])

