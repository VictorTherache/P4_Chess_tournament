import sys
sys.path.append("..")
import operator
import itertools
from Models.RoundModel import RoundModel
from Controllers.MatchController import MatchController

class RoundController(object):
    """
    Round's controller : Gets the data from the model and shows
    the views
    """
    def __init__(self):
        """
        Constructor of the class
        """
        super().__init__()
        self.round_model = RoundModel()
        self.match_controller = MatchController()
        self.first_half_list = []
        self.second_half_list = []
        self.round_1_match_list = []
        self.round_list = []
        

    def sort_players_first_round(self, tournament_players):
        """
        Sort the players in 2 list based on their rank
        """
        sorted_players = sorted(tournament_players, key=lambda k: k['rank'], reverse=True) 
        self.first_half_list = sorted_players[:len(sorted_players)//2]
        self.second_half_list = sorted_players[len(sorted_players)//2:]


    def generate_list_for_first_round(self, tournament_players):
        """
        Generate the first round matches of the tournament
        """
        self.sort_players_first_round(tournament_players)
        player_1 = []
        player_2 = []
        j = 0 
        for i in range(1, len(self.first_half_list) + 1):
            """
            Generate matches for the first round
            """
            i = []
            player_1 = []
            player_2 = []
            player_1.extend([self.first_half_list[j], 0])
            player_2.extend([self.second_half_list[j], 0])
            i.extend([player_1, player_2])
            j += 1
            self.match_controller.update_score(i)
            self.round_1_match_list.append(i)
        ranking = self.generate_pairs_for_other_rounds()
        return ranking


    def generate_pairs_for_other_rounds(self):
        """
        Generate the other rounds matches of the tournament
        """
        y = 0
        last_turn = []
        players_rank_end_tournament = []
        for y in range(0, 4):
            re_sort_list = []
            j = 0
            for match in self.round_1_match_list:
                re_sort_list.extend([match[0], match[1]])
            re_sort_list = sorted(re_sort_list, key=lambda x: (x[1], x[0]['rank']), reverse=True)
            j=0
            for first, second in zip(re_sort_list, re_sort_list[1:]):  
                match_list = []
                if(j%2==0):
                    match_list.extend([first, second])
                    self.match_controller.update_score(match_list)
                    last_turn.append(match_list)  
                j+=1  
                y+=1
        for match in last_turn[-4:]:
            players_rank_end_tournament.extend([match[0], match[1]])
        players_rank_end_tournament = sorted(players_rank_end_tournament, key=lambda x: (x[1], x[0]['rank']), reverse=True)
        return players_rank_end_tournament


    def transform_match_list_in_players_list(self, match_list):
        """
        Transform match list into player list
        """
        player_list = []
        for match in match_list:
            player_list.extend([match_list[0], match_list[1]])
        return player_list


    def update_score(self, match):
        """
        Ask the user to enter the result of the matches
        """
        for match in self.round_1_players_list:
            self.match_controller.update_score(match)
