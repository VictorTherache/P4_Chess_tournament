import sys
sys.path.append("..")

from Views.PlayerView import PlayerView
from Views.TournamentView import TournamentView
from Models.PlayerModel import PlayerModel
class PlayerController(object):
    """
    Player's controller : Gets the data from the model and shows
    the the views
    """
    def __init__(self):
        """
        Constructor of the class
        """
        self.player_views = PlayerView()
        self.tournament_views = TournamentView()
        self.player_model = PlayerModel()
        self.tournament_players = []
        # model = PlayerModel()
        # pass

    def add_player_to_tournament(self):
        """
        Add a player to the tournament
        """
        player_table = self.player_model.players_list()
        # self.player_views.show_players_list(player_table)
        # choice = input("Entrez un nombre : ")
        # self.tournament_players.append(player_table.all()[int(choice) - 1])
        while len(self.tournament_players) != 8:
            self.tournament_views.add_player()
            choice = input("Entrez un nombre : ")
            if int(choice) == 1: 
                self.choose_player_from_db(player_table)
                print(self.tournament_players)
            if int(choice) == 2:
                self.add_new_player_to_tournament_and_db()
            
    def choose_player_from_db(self, player_table):
        self.player_views.show_players_list(player_table)
        player_choice = input("Quels joueurs voulez vous ajouter ? :")
        return self.tournament_players.append(player_table.all()[int(player_choice) - 1])

    def add_new_player_to_tournament_and_db(self):
        players_info = self.player_views.add_player_to_tournament_and_db()
        self.player_model.add_new_player_to_db(players_info)
        

# player_c = PlayerController()
# player_c.add_player_to_tournament()
# player_c.add_new_player_to_tournament_and_db()

# controller = TournamentController()
# # print(controller)
# view = TournamentView()
# controller.run_programm(view)