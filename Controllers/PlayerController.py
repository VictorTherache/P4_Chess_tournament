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


    def add_player_to_tournament(self):
        """
        Add a player to the tournament
        """
        player_table = self.player_model.players_list()
        while len(self.tournament_players) != 8:
            nbr_players_in_tournament = len(self.tournament_players)
            self.tournament_views.add_player(nbr_players_in_tournament)
            choice = input("Entrez un nombre : ")
            if int(choice) == 1: 
                self.choose_player_from_db(player_table)
            if int(choice) == 2:
                self.add_new_player_to_tournament_and_db()
            
    def choose_player_from_db(self, player_table):
        """
        Show the list of players in db and choose
        the player to select
        """
        self.player_views.show_players_list(player_table)
        player_choice = input("Quels joueurs voulez vous ajouter ? :")
        player_chosen = player_table.all()[int(player_choice) - 1]
        if player_chosen not in self.tournament_players:
            return self.tournament_players.append(player_table.all()[int(player_choice) - 1])
        else :
            self.player_views.player_already_added()

    def add_new_player_to_tournament_and_db(self):
        """
        Checks if the player exist in db, if he
        doesn't exist, add it to tournament and db
        """
        players_info = self.player_views.add_player_to_tournament_and_db()
        if (self.player_model.check_players_exists(players_info)):
            self.player_views.player_already_exist()
        else:
            self.player_model.add_new_player_to_db(players_info)
            player_created = self.player_model.get_player_created()
            self.tournament_players.append(player_created)

        