import sys
sys.path.append("..")
# from Models.PlayerModel import PlayerModel

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

