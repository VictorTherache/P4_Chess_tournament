import sys
sys.path.append("..")


class PlayerView(object):
    """
    Class of the views related to the players
    """
    def __init__(self):
        """
        Constructor of the method
        """
        self.players_info = []

    def player_already_exist(self):
        print("Le joueur existe déjà, veuillez réessayer")

    def liste_player_alpha(self):
        print("Liste des joueurs par ordre alphabetique : \n")

    def liste_player_rank(self):
        print("Liste des joueurs par rang : \n")

    def show_list_players(self, texttable):
        """
        Show each player in a single row
        """
        print(texttable.draw())

    def show_list_players_by_rank(self, first_name, last_name, rank):
        """
        show sorted players by rank
        """
        print(f"{first_name}"
              f" {last_name}"
              f" | classement : {rank}")
