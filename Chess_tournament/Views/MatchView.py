class MatchView(object):
    """
    Views of the Round
    """
    def __init__(self):
        """
        Constructor of the class
        """
        pass

    def update_score(self, match):
        print(f"Match entre {match[0][0]['first_name']} {match[0][0]['last_name']}"
              f" et {match[1][0]['first_name']} {match[1][0]['last_name']} \n")

    def update_score_other_rounds(self, match):
        print(f"Match entre {match[0][0]['first_name']} {match[0][0]['last_name']}"
              f" et {match[1][0]['first_name']} {match[1][0]['last_name']}\n")

    def invalide_score(self):
        print("Veuillez rentrer un score valide (1, 0.5 ou 0)\n")

    def error_two_winners(self):
        print("Erreur : Le joueur 2 doit avoir un score de 0 !\n")

    def error_two_loosers(self):
        print("Erreur : Le joueur 2 doit avoir un score de 1 !\n")

    def error_two_draw(self):
        print("Erreur : Le joueur 2 doit avoir un score de 0.5 !\n")
