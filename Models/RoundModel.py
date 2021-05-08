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

    def save_round_in_db(self, pair_of_player):
        """
        saves a list of players pairs in db
        """
        # self.first_round.insert({"p1_first_name": pair_of_player[0]["first_name"],
        #                         "p1_last_name": pair_of_player[0]["last_name"]},
        #                         {"p2_first_name": 'charlie'})

                                #   "p1_last_name": pair_of_player[0]["last_name"],
                                #   "p1_result": ""},
                                # {"p2_first_name": pair_of_player[1]["first_name"],
                                #   "p2_last_name": pair_of_player[1]["last_name"],
                                #   "p2_result": ""})

        # self.player_table.insert({'first_name': players_info[0], 
        #                   'last_name': players_info[1], 
        #                   'age': players_info[2], 
        #                   'gender': players_info[3], 
        #                   'rank': players_info[4]})