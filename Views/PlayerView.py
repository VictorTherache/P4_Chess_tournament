import sys
sys.path.append("..")
from Models.PlayerModel import PlayerModel

class PlayerView(object):
    """
    Class of the views related to the players
    """
    def __init__(self):
        """
        Constructor of the method
        """
        self.player_model = PlayerModel()
        self.players_info = []
        # print(player_model)

    def show_players_list(self, player_table):
        """
        Contains the view of a new tournament
        """
        print('Quels joueurs souhaitez vous ajouter ? :')
        i = 1
        for players in player_table:
            print(players['first_name'] + " " + str(i)) 
            i+= 1
        # .players_list())

    def add_player_to_tournament_and_db(self):
        """
        View to get players info to add them in the db
        """
        last_name = input("Entrez le nom du joueur :")
        first_name = input("Entrez le prénom du joueur :")
        age = input("Entrez l'âge du joueur :")
        gender = input("Entrez le sexe du joueur (m/f) :")
        rank = input("Entrez le rang du joueur :")
        self.players_info.extend([last_name, first_name, age,
                                 gender, rank])
        return self.players_info



player_view = PlayerView()
# player_view.show_players_list()