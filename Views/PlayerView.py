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

    def ask_for_player_sort(self):
        print("Tapez 1 pour classer les joueurs par ordre alphabétique"
                "\nTapez 2 pour classer les joueurs par rangs")

    def show_list_players(self, players_list):
        """
        Show each player in a single row
        """
        i = 1
        for players in players_list:
            print(f"{players['first_name']} {players['last_name']}") 
            i+= 1

    def show_list_players_by_rank(self, players_list):
        """
        show sorted players by rank
        """
        i = 1
        for players in players_list:
            print(f"{players['first_name']}"
                  f" {players['last_name']}" 
                  f" | classement : {players['rank']}") 
            i+= 1