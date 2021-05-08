from itertools import repeat
import sys
sys.path.append("..")
import operator
import itertools
from Models.RoundModel import RoundModel
from Controllers.MatchController import MatchController
from Views.RoundView import RoundView

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
        # self.round_model = RoundModel()
        self.match_controller = MatchController()
        self.round_view = RoundView()
        self.first_half_list = []
        self.second_half_list = []
        self.round_1_match_list = []
        self.round_number = 1
        self.total_rounds =  []
        

    def sort_players_first_round(self, tournament_players):
        """
        Sort the players in 2 list based on their rank
        """
        sorted_players = sorted(tournament_players, key=lambda k: k['rank'], reverse=True) 
        self.first_half_list = sorted_players[:len(sorted_players)//2]
        self.second_half_list = sorted_players[len(sorted_players)//2:]


    def make_pairs_first_first_round(self, i, j):
        i = ()
        first_half_list = []
        second_half_list = []
        first_half_list.extend([self.first_half_list[j], 0])
        second_half_list.extend([self.second_half_list[j], 0])
        i = (first_half_list, second_half_list)
        return i


    def generate_pairs_for_first_round(self, tournament_players, number_of_rounds):
        """
        Generate the first round matches of the tournament
        """
        first_half_list = []
        second_half_list = []
        j = 0 
        round_list = [[] for i in repeat(None, number_of_rounds)] #creation de listes pour les rounds
        self.sort_players_first_round(tournament_players)
        self.round_view.show_round_number(self.round_number)
        for i in range(1, len(self.first_half_list) + 1):
            i = self.make_pairs_first_first_round(i, j)
            new_score = self.match_controller.update_score(i, 1)
            j += 1
            i[0][1] = new_score[0]
            i[1][1] = new_score[1]
            round_list[0].append(i)
            self.round_1_match_list.append(i)
        ranking = self.generate_pairs_for_other_rounds(number_of_rounds, round_list)
        return ranking
    


    def generate_pairs_for_other_rounds(self, number_of_rounds, round_list):
        """
        Generate the other rounds matches of the tournament
        """
        # round_list[0].append(self.round_1_match_list)
        print(f"SELF {self.round_1_match_list}")
        print(f"ROUND LIST {round_list[0]}")
        j = 0
        for i in range(1, 3):
            all_players = []
            for match in self.round_1_match_list:
                all_players.extend([match[0], match[1]])
            all_players = sorted(all_players, key=lambda x: (x[i], x[0]['rank']), reverse=True)   
            pair_players = list(zip(all_players, all_players[1:] + all_players[:1]))
            self.round_number += 1
            self.round_view.show_round_number(self.round_number)
            for paired_players in pair_players:
                if(j%2==0):
                    new = self.match_controller.update_score(paired_players, i)
                    paired_players[0].append(new[0])
                    paired_players[1].append(new[1])
                    round_list[i].append(paired_players)
                j+=1
        self.clean_rounds_list(round_list)
    


    def clean_rounds_list(self, round_list):
        """
        Modify the round list to be cleaner (remove the excessive points)
        """
        i=1
        for rounds in round_list:
            for match in rounds:
                for player in match:
                    print(player)



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



