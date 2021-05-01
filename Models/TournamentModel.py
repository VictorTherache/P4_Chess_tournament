from tinydb import TinyDB, Query
import sys
from Views import TournamentView

class Tournament(object):
    """
    Tournament model, create, read, update or delete data from the tournament
    table
    """
    def __init__(self):
        """
        Constructor of the class
        """
        self.tournament_views = TournamentView
        self.db = TinyDB('../Models/db.json')
        self.query = Query()
        self.player_table = self.db.table('player_table')
        # self.name = name 
        # self.place = place 
        # self.date = date 
        # self.nbr_of_rounds = 4
        # self.rounds = rounds
        # self.players = players
        # self.time_control = time_control
        # self.description = description


    def players_list(self):
        """
        Return a table of all the players in database
        """
        player_table = self.db.table('player_table')
        return player_table

