import os
import sys
sys.path.append("..")

from Views import MatchView
# from Models import MatchModel

class MatchController(object):
    """
    Match's controller : Gets the data from the model and shows
    the views
    """
    def __init__(self):
        """
        Constructor of the class
        """
        self.match_views = MatchView.MatchView()


    def update_score(self, match, i):
        """
        Take the results of the match the user entered
        """
        match_list = []
        self.match_views.update_score(match)
        score_p1 = input(f"Veuillez rentrer le score de {match[0][0]['first_name']} {match[0][0]['last_name']} (1/0.5/0) ")
        score_p2 = input(f"Veuillez rentrer le score de {match[1][0]['first_name']} {match[1][0]['last_name']} (1/0.5/0) ")
        self.validate_score(score_p1, score_p2, match, i)
        new_score = float(score_p1)
        new_score2 = float(score_p2) 
        return new_score, new_score2


        
    def update_score_other_rounds(self, match):
        """
        Display the message to ask the user for matches result
        """
        self.match_views.update_score(match)


    def validate_score(self, score1, score2, match, i):
        print(float(score1))
        if (float(score1) != 1.0 and
            float(score1) != 0.0 and
            float(score1) != 0.5):
            os.system('cls')
            self.match_views.invalide_score()
            input("Appuyer sur entrée pour continuer")
            self.update_score(match, i)
        if (float(score2) != 1.0 and
            float(score2) != 0.0 and
            float(score2) != 0.5):
            os.system('cls')
            self.match_views.invalide_score()
            input("Appuyer sur entrée pour continuer")
            self.update_score(match, i)
        if (float(score1) == 1.0 and float(score2) != 0):
            os.system('cls')
            self.match_views.error_two_winners()
            input("Appuyer sur entrée pour continuer")
            self.update_score(match, i)
        if (float(score1) == 0.0 and float(score2) != 1.0):
            os.system('cls')
            self.match_views.error_two_loosers()
            input("Appuyer sur entrée pour continuer")
            self.update_score(match, i)
        if (float(score1) == 0.5 and float(score2) != 0.5):
            os.system('cls')
            self.match_views.error_two_draw()
            input("Appuyer sur entrée pour continuer")
            self.update_score(match, i)

    # def add_score_to_first_rounds_match(self):
    #     """
    #     Ask the user to put score to the first round matches
    #     """
    #     for match in self.match_model.get_first_round():
    #         player_1 = f"{match['pair_of_players'][0]['first_name']} {match['pair_of_players'][0]['last_name']}"
    #         player_2 = f"{match['pair_of_players'][1]['first_name']} {match['pair_of_players'][1]['last_name']}"
    #         self.match_views.show_match(player_1, player_2)
    #         score_player_1 = input(f"Rentrez le score de {player_1} : ")
    #         score_player_2 = input(f"Rentrez le score de {player_2} : ")

