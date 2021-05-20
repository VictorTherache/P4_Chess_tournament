from tinydb import TinyDB, Query
import sys

class RoundModel(object):
    """
    Round model, create, read, update or delete data from the round
    table
    """
    def __init__(self, name, starting_time, end_time, match_list):
        """
        Constructor of the class
        """
        # self.db = TinyDB('../Models/db.json')
        # self.first_round = self.db.table('first_round')
        # self.query = Query()
        self.name = name
        self.starting_time = starting_time
        self.end_time = end_time
        self.match_list = match_list

    def get_matches_list(self):
        """
        Returns the list of the matches
        """
        pass

    @classmethod
    def save_round_in_db(self, serialized_round, tournament_id):
        """
        saves a list of players pairs in db
        """
        rounds_list =[]
        self.db = TinyDB('Models/db.json')
        self.query = Query()
        self.tournament_table = self.db.table('tournament_table')
        tournament = self.tournament_table.get(doc_id=tournament_id)
        if (tournament['rounds'] == 'rounds'):
            rounds_list.append(serialized_round)
            self.tournament_table.update({'rounds': rounds_list}, doc_ids=[tournament_id])
        else:
            rounds_list = tournament['rounds']
            rounds_list.append(serialized_round)
            self.tournament_table.update({'rounds': rounds_list}, doc_ids=[tournament_id])
