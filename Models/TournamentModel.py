from abc import abstractproperty
from tinydb import TinyDB, Query
import sys

from tinydb.queries import where
from Views import TournamentView

class Tournament(object):
    """
    Tournament model, create, read, update or delete data from the tournament
    table
    """
    def __init__(self, name, place, date, rounds, players, time_control, description):
        """
        Constructor of the class
        """
        self.tournament_views = TournamentView

        self.name = name
        self.place = place
        self.date = date
        self.nbr_of_rounds = 4
        self.rounds = rounds
        self.players = players
        self.time_control = time_control
        self.description = description

    @classmethod
    def players_list(self):
        """
        Return a table of all the players in database
        """
        self.db = TinyDB('Models/db.json')
        self.query = Query()
        player_table = self.db.table('player_table')
        return player_table

    
    @classmethod
    def save_tournament(self, tournament):
        self.db = TinyDB('Models/db.json')
        self.query = Query()
        self.tournament_table = self.db.table('tournament_table')
        
        self.tournament_table.insert(tournament)
    

    @classmethod
    def get_current_instance(self):
        self.db = TinyDB('Models/db.json')
        self.query = Query()
        self.tournament_table = self.db.table('tournament_table')
        return self.tournament_table.all()[-1]
        
    @classmethod
    def update_players(self, players_index, name):
        self.db = TinyDB('Models/db.json')
        self.query = Query()
        self.tournament_table = self.db.table('tournament_table') 
        self.tournament_table.update({'player': players_index}, where('name')== name)


    @classmethod
    def get_tournament_list(self):
        self.db = TinyDB('Models/db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.query = Query()
        tournament_table = self.db.table('tournament_table')
        return tournament_table

    @classmethod
    def serialize_tournament(self, tournament_instance):
        serialize_tournament = {
            'name': tournament_instance.name,
            'place': tournament_instance.place,
            'date': tournament_instance.date,
            'rounds': tournament_instance.rounds,
            'player': tournament_instance.players,
            'time_control': tournament_instance.time_control,
            'description': tournament_instance.description
        }
        return serialize_tournament

    @classmethod
    def get_loading_tournaments(self):
        loading_tournament_list = []
        self.db = TinyDB('Models/db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.query = Query()
        all_tournaments = self.tournament_table.all()
        for tournament in all_tournaments:
            if(tournament['player'] == 'players' or
               tournament['rounds'] == 'rounds'):
                loading_tournament_list.append(tournament)
            if(len(tournament['rounds']) < 4):
                loading_tournament_list.append(tournament)
        return loading_tournament_list
    @classmethod      
    
    def get_id(self, tournament):
        self.db = TinyDB('Models/db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.query = Query()
        tournament = self.tournament_table.get(self.query.name == tournament[0])
        return tournament.doc_id
    
    @classmethod
    def get_players_index_from_db(self, tournament_id):
        self.db = TinyDB('Models/db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.query = Query()
        tournament = self.tournament_table.get(doc_id=tournament_id)
        return tournament['player']

