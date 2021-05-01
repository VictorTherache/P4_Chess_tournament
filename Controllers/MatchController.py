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


    def update_score(self, match):
        """
        Take the results of the match the user entered
        """
        self.match_views.update_score(match)
        score_p1 = input(f"Veuillez rentrer le score de {match[0][0]['first_name']} {match[0][0]['last_name']} (1/0.5/0) ")
        score_p2 = input(f"Veuillez rentrer le score de {match[1][0]['first_name']} {match[1][0]['last_name']} (1/0.5/0) ")
        match[0][1] = float(match[0][1]) + float(score_p1) 
        match[1][1] = float(match[1][1]) + float(score_p2) 
        
    def update_score_other_rounds(self, match):
        """
        Display the message to ask the user for matches result
        """
        self.match_views.update_score(match)

    def add_score_to_first_rounds_match(self):
        """
        Ask the user to put score to the first round matches
        """
        for match in self.match_model.get_first_round():
            player_1 = f"{match['pair_of_players'][0]['first_name']} {match['pair_of_players'][0]['last_name']}"
            player_2 = f"{match['pair_of_players'][1]['first_name']} {match['pair_of_players'][1]['last_name']}"
            self.match_views.show_match(player_1, player_2)
            score_player_1 = input(f"Rentrez le score de {player_1} : ")
            score_player_2 = input(f"Rentrez le score de {player_2} : ")

