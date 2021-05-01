class MatchView(object):
    """
    Views of the Round
    """
    def __init__(self):
        """
        Constructor of the class
        """
        pass

    def show_match(self, player_1, player_2):
        print('\n')
        print(f"\n Match entre {player_1} "
              f"et {player_2} ! ") 

    def update_score(self, match):
        print(f"Match entre {match[0][0]['first_name']} {match[0][0]['last_name']}"
              f" et {match[1][0]['first_name']} {match[1][0]['last_name']} \n")
    
    def update_score_other_rounds(self, match):
        print(f"Match entre {match[0][0]['first_name']} {match[0][0]['last_name']}"
              f" et {match[1][0]['first_name']} {match[1][0]['last_name']}\n")    
