from Views import MatchView
import sys
from sys import platform
import os

sys.path.append("..")


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
        self.match_views.update_score(match)
        score_p1 = input(f"Veuillez rentrer le score de "
                         f"{match[0][0]['first_name']} "
                         f"{match[0][0]['last_name']} (1/0.5/0) ")
        score_p2 = input(f"Veuillez rentrer le score de "
                         f"{match[1][0]['first_name']} "
                         f"{match[1][0]['last_name']} (1/0.5/0) ")
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
        if (float(score1) != 1.0 and
                float(score1) != 0.0 and
                float(score1) != 0.5):
            self.clean_console()
            self.match_views.invalide_score()
            input("Appuyer sur entrée pour continuer")
            self.update_score(match, i)
        if (float(score2) != 1.0 and
                float(score2) != 0.0 and
                float(score2) != 0.5):
            self.clean_console()
            self.match_views.invalide_score()
            input("Appuyer sur entrée pour continuer")
            self.update_score(match, i)
        if (float(score1) == 1.0 and float(score2) != 0):
            self.clean_console()
            self.match_views.error_two_winners()
            input("Appuyer sur entrée pour continuer")
            self.update_score(match, i)
        if (float(score1) == 0.0 and float(score2) != 1.0):
            self.clean_console()
            self.match_views.error_two_loosers()
            input("Appuyer sur entrée pour continuer")
            self.update_score(match, i)
        if (float(score1) == 0.5 and float(score2) != 0.5):
            self.clean_console()
            self.match_views.error_two_draw()
            input("Appuyer sur entrée pour continuer")
            self.update_score(match, i)

    def clean_console(self):
        if(platform == 'linux'
           or platform == 'linux2'
           or platform == 'darwin'):
            os.system('clear')
        else:
            os.system('cls')
