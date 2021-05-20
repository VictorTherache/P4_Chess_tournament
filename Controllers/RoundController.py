import abc
from itertools import repeat, groupby
from operator import itemgetter
from collections import Counter
import sys, os
sys.path.append("..")
import operator
import itertools
from Models.RoundModel import RoundModel
from Controllers.MatchController import MatchController
from Views.RoundView import RoundView
from datetime import datetime

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
        self.time_rounds = [[] for i in repeat(None, 4)]
        self.round_list = [[] for i in repeat(None, 4)] #creation de listes pour les rounds
        self.tuple_match = []
        self.round_instance = []
        self.tournament_id = 0
        self.updated_joined_list = []
        

    def sort_players_first_round(self, tournament_players):
        """
        Sort the players in 2 list based on their rank
        """
        sorted_players = sorted(tournament_players, key=lambda k: k['rank'], reverse=True) 
        self.first_half_list = sorted_players[:len(sorted_players)//2]
        self.second_half_list = sorted_players[len(sorted_players)//2:]


    def make_pairs_first_first_round(self, i, j):
        """
        Returns a list of paired players
        """
        i = []
        first_half_list = []
        second_half_list = []
        first_half_list.extend([self.first_half_list[j]])
        second_half_list.extend([self.second_half_list[j]])
        i = [first_half_list, second_half_list]
        return i




    def generate_pairs_for_first_round(self, tournament_players, number_of_rounds, tournament_id):
        """
        Generate the first round matches of the tournament
        """
        first_half_list = []
        second_half_list = []
        j = 0 
        self.tournament_id = tournament_id
        self.round_number = 1
        self.add_round_time()
        serialized_round = self.create_instances()
        self.sort_players_first_round(tournament_players)
        for i in range(1, len(self.first_half_list) + 1):
            os.system('cls')
            self.round_view.show_round_number(self.round_number)
            i = self.make_pairs_first_first_round(i, j)
            new_score = self.match_controller.update_score(i, 1)
            j += 1
            i[0].extend([new_score[0], 0, 0, 0])
            i[1].extend([new_score[1], 0, 0, 0])
            self.round_list[0].append(i)
        self.add_round_time()
        self.convert_tuple(self.round_number)
        updated_round = self.add_end_time_to_instance()

        self.save_to_db(updated_round, tournament_id)
        ranking = self.generate_matches_other_rounds()
        return ranking


    def convert_tuple(self, round_number):
        """
        Convert a list to tuple
        """
        self.tuple_match = []
        score_index=1
        round_index=0
        match_index=0
        for match in self.round_list[round_number -1]:
            tuple=()
            tuple = tuple + ([match[0][0], match[0][score_index]], [match[1][0], match[1][score_index]])
            self.tuple_match.append(tuple)
            match_index +=1
        score_index+=1
        round_index+=1

        

    def save_to_db(self, serialized_round, tournament_id):
        """
        Saves the round to the db
        """
        RoundModel.save_round_in_db(serialized_round, tournament_id)



    def add_end_time_to_instance(self):
        """
        Add the end time to the round instance
        """
        i=1
        round_index = 0
        serialiazed_round = {
            'name': f"Round 1",
            'start_time': f"{self.time_rounds[round_index][0]}",
            'end_time': f"{self.time_rounds[round_index][1]}",
            'match_list': self.tuple_match
        }
        i+=1
        round_index+=1
        return serialiazed_round  

    def update_instance(self):
        """
        Update the round instance
        """
        i=1
        serialiazed_round = {
            'name': f"Round {self.round_number}",
            'start_time': f"{self.time_rounds[self.round_number-1][0]}",
            'end_time': f"{self.time_rounds[self.round_number-1][1]}",
            'match_list': self.tuple_match
        }
        i+=1
        return serialiazed_round

    
    def add_round_time(self):
        """
        Returns the current time
        """
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.time_rounds[self.round_number -1].append(dt_string)

    def load_match(self, tournament, current_id):
        """
        Load a match and generate the missing rounds
        """
        self.tournament_id = current_id
        players_list = []
        updated_players_list = []
        for rounds in tournament['rounds']:
            for match in rounds['match_list']:
                for players in match:
                    players_list.append(players)
        for index, players in enumerate(players_list):
            for s_index, compared_player in enumerate(players_list):

                if index != s_index:
                    if players[0] == compared_player[0]:
                        players.append(compared_player[1])
            updated_players_list.append(players)
        for players in updated_players_list:
            while len(players) != 5:
                players.append(0)
        i=0
        self.updated_joined_list = updated_players_list
        self.round_number = len(tournament['rounds'])
        ranking = self.generate_matches_other_rounds()
        return ranking

                # i+=1
  
    def generate_matches_other_rounds(self):
        """
        Generate the other rounds matches of the tournament
        """
        j = 0
        for i in range(self.round_number, 4):
            self.round_number += 1
            # self.add_round_time()
            # serialized_round = self.create_instances()
            added_list = []
            joined_player_list = []
            if self.round_list == [[], [], [], []]:
                joined_player_list = self.updated_joined_list
            else:
                joined_player_list = self.joined_player_list()
            added_list = sorted(joined_player_list, 
                                key=lambda x: ((x[1] + x[2] + x[3] + x[4]), 
                                                x[0]['rank']), 
                                reverse=True)  
            match_list = self.generate_pairs_other_rounds(added_list)
            self.add_round_time()
            for match in match_list:
                os.system('cls')
                self.round_view.show_round_number(self.round_number)
                new = self.match_controller.update_score(match, i)
                match[0][i+1] = new[0]
                match[1][i+1] = new[1]
                self.round_list[i].append(match)
            self.add_round_time()
            self.convert_tuple(self.round_number)
            updated_round = self.update_instance()
            self.save_to_db(updated_round, self.tournament_id)
        i=0
        tournament_result = self.get_tournament_result()
        self.clean_rounds()
        return tournament_result


    def get_tournament_result(self):
        """
        Sort the players by the number of their points 
        """
        joined_player_list = []
        joined_player_list = self.joined_player_list()
        added_list = sorted(joined_player_list, 
                            key=lambda x: ((x[1] + x[2] + x[3] + x[4]), 
                                            x[0]['rank']), 
                            reverse=True)  
        return added_list

#     def make_instances(self):
#         """
#         """
#         i=1
#         round_index = 0
#         serialized_round_list = []
# #         self.time_rounds = [['14/05/2021 11:31:32', '14/05/2021 11:31:35'], ['14/05/2021 11:31:35', '14/05/2021 11:31:37'], ['14/05/2021 11:31:37', '14/05/2021 11:31:39'], ['14/05/2021 11:31:39', '14/05/2021 11:31:42']]
# #         self.round_list = [[([{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0]), ([{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 1.0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0]), ([{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 1.0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0]), ([{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0])], [([{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 2.0], [{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 2.0]), ([{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 2.0], [{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0]), ([{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0]), ([{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 2.0])], [([{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 2.0], [{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 2.0]), ([{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 2.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0]), ([{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0]), ([{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0])], [([{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 2.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 2.0]), ([{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 2.0], [{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 2.0]), ([{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0], [{'first_name': 'Lucas', 
# # 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0]), ([{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0])]]
#         for rounds in self.round_list:
#             seriliazed_round = {
#                 'name': f"Round {i}",
#                 'start_time': f"{self.time_rounds[round_index][0]}",
#                 'end_time': f"{self.time_rounds[round_index][1]}",
#                 'match_list': self.round_list[round_index]
#             }
#             serialized_round_list.append(seriliazed_round)
#             i+=1
#             round_index+=1
#         return serialized_round_list

    def create_instances(self):
        """
        Create a new round instance
        """
        i=1
        round_index = self.round_number -1
        seriliazed_round = {
            'name': f"Round 1",
            'start_time': f"{self.time_rounds[round_index][0]}",
            'end_time': "",
            'match_list': ""
        }
        i+=1
        round_index+=1
        return seriliazed_round
            


    def clean_rounds(self):
        """
        Remove the extra scores from the match list 
        """
        score_index=1
        round_index=0
        for rounds in self.round_list:
            match_index=0
            for match in rounds:
                tuple=()
                tuple = tuple + ([match[0][0], match[0][score_index]], [match[1][0], match[1][score_index]])
                self.round_list[round_index][match_index] = tuple
                match_index +=1
            score_index+=1
            round_index+=1


    def joined_player_list(self):
        """
        Create a list of the tournament players
        """
        join_list = []
        for rounds in self.round_list:
            for match in rounds:
                for players in match:
                    join_list.append(players)
        return join_list[-8:]


    def get_players_list(self):
        """
        Get a list of all the players in the tournament
        """
        added_list = []
        for rounds in self.round_list:
            for match in rounds:
                for player in match:
                    i=0
                    player_to_add = player
                    for matches in rounds[i]:
                        for player in matches:
                            self.add_score_for_player(player_to_add, player) 
                    i+=1
        return added_list

    


    def generate_pairs_other_rounds(self, players_list):
        """
        Pair each players of the list to make a unique match list
        """
        match_list = [[] for i in repeat(None, 4)] 
        i=0
        for i in range(0, 4):
            j = 0
            if i == 3:
                match_list[i] = [players_list[0], players_list[1]]
                return match_list
            match_list[i] = [players_list[0], players_list[j+1]]
            while self.check_player_already_played(match_list[i]):
                j+=1
                match_list[i] = [players_list[0], players_list[j+1]]
            del players_list[0]
            del players_list[j]
        return match_list
                

    def check_player_already_played(self, match):
        """
        Check if a player as already played with his opponent
        """
        for rounds in self.round_list:
            if match in rounds:
                return True


    # def transform_match_list_in_players_list(self, match_list):
    #     """
    #     Transform match list into player list
    #     """
    #     player_list = []
    #     for match in match_list:
    #         player_list.extend([match_list[0], match_list[1]])
    #     return player_list


    def update_score(self, match):
        """
        Ask the user to enter the result of the matches
        """
        for match in self.round_1_players_list:
            self.match_controller.update_score(match)



round_c = RoundController()
# round_c.round_list = [[[[{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0, 1.0, 0, 0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0, 1.0, 0, 0]], [[{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 1.0, 1.0, 0, 0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0, 1.0, 0, 0]], [[{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 1.0, 1.0, 0, 0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0, 1.0, 0, 0]], [[{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0, 1.0, 0, 0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0, 1.0, 0, 0]], [[{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0, 0, 0, 0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 0.0, 0, 0, 0]], [[{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 1.0, 0, 0, 0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 0.0, 0, 0, 0]], [[{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': 
# '12/02/1983', 'gender': 'f', 'rank': 1400}, 1.0, 0, 0, 0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 0.0, 0, 0, 0]], [[{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0, 0, 0, 0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 0.0, 0, 0, 0]]], [[[{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0, 1.0, 1.0, 0], [{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 1.0, 1.0, 1.0, 0]], [[{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 1.0, 0.0, 0.0, 0], [{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0, 1.0, 0.0, 0]], [[{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0, 0.0, 1.0, 0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0, 1.0, 1.0, 0]], [[{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0, 0.0, 0.0, 0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0, 0.0, 0.0, 0]], [[{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0, 1.0, 1.0, 0], [{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 1.0, 0.0, 0.0, 0]], [[{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 1.0, 1.0, 1.0, 0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0, 0.0, 1.0, 0]], [[{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0, 1.0, 0.0, 0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0, 0.0, 0.0, 0]], [[{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0, 1.0, 1.0, 0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0, 0.0, 0.0, 0]]], [[[{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0, 1.0, 1.0, 0], [{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0, 1.0, 0.0, 0]], [[{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 1.0, 1.0, 1.0, 0], [{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 1.0, 0.0, 0.0, 0]], [[{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0, 1.0, 1.0, 0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0, 0.0, 0.0, 0]], [[{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0, 0.0, 1.0, 0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0, 0.0, 0.0, 0]]], []]
# round_c.generate_pairs_other_rounds([[{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0, 1.0, 1.0, 0], [{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 1.0, 1.0, 1.0, 0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0, 1.0, 1.0, 0], [{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0, 1.0, 0.0, 0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0, 0.0, 1.0, 0], [{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 1.0, 0.0, 0.0, 0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0, 0.0, 0.0, 0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0, 0.0, 0.0, 0]])
# round_c.generate_pairs_for_first_round([{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, {'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, {'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, {'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, {'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, {'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, {'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, {'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000} ], 4)

# round_c.generate_pairs_other_rounds(4, [[[[{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0, 0, 0, 0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 0.0, 0, 0, 0]], [[{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 0.0, 0, 0, 0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0, 0, 0, 0]], [[{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 0.0, 0, 0, 0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0, 0, 0, 0]], [[{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 0.0, 0, 0, 0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0, 0, 0, 0]]], [], [], []])

# round_c.get_players_list([[[[{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 0.0]], [[{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 0.0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0]], [[{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 0.0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 
# 'm', 'rank': 1050}, 1.0]], [[{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 0.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0]]], [[[{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 
# 'gender': 'm', 'rank': 1203}, 0.0]], [[{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 0.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0]], [[{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 1.0], [{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 0.0]], [[{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 0.0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 2.0]]], [], []])


# ROUND 2
# [[[[{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 0.0]], [[{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 0.0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0]], [[{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 0.0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 
# 'm', 'rank': 1050}, 1.0]], [[{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 0.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0]]], [[[{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 
# 'gender': 'm', 'rank': 1203}, 0.0]], [[{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 0.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0]], [[{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 1.0], [{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 0.0]], [[{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 0.0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 2.0]]], [], []]