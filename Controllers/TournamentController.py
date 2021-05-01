from tinydb import TinyDB, Query
import sys
sys.path.append("..")
from Views.TournamentView import TournamentView
from Models.TournamentModel import Tournament
from Models.PlayerModel import Player
from Controllers.RoundController import RoundController


class TournamentController(object):
    """
    Tournament's controller : Gets the data from the model and shows
    the views
    """
    def __init__(self):
        """
        Constructor of the class
        """
        self.tournament_view = TournamentView()
        self.tournament_model = Tournament()
        self.round_controller = RoundController()
        self.db = TinyDB('../Models/db.json')
        self.player_table = self.db.table('player_table')
        self.tournament_players = []


    def new_tournament(self):
        """
        Initialize the tournament, add players to it
        """
        self.tournament_view.new_tournament()
        player_table = self.tournament_model.players_list()
        while len(self.tournament_players) != 8:
            nbr_players_in_tournament = len(self.tournament_players)
            self.tournament_view.add_player(nbr_players_in_tournament)
            choice = input("Entrez un nombre : ")
            if int(choice) == 1: 
                self.choose_player_from_db(player_table)
            if int(choice) == 2:
                self.add_new_player_to_tournament_and_db()
        self.generate_pairs_first_round()
        

    def choose_player_from_db(self, player_table):
        """
        Show the list of players in db and choose
        the player to select
        """
        self.tournament_view.show_players_list(player_table)
        player_choice = input("Quels joueurs voulez vous ajouter ? :")
        player_chosen = player_table.all()[int(player_choice) - 1]
        if player_chosen not in self.tournament_players:
            return self.tournament_players.append(player_table.all()[int(player_choice) - 1])
        else :
            self.tournament_view.player_already_added()

    def add_new_player_to_tournament_and_db(self):
        """
        Checks if the player exist in db, if he
        doesn't exist, add it to tournament and db
        """
        players_info = self.tournament_view.add_player_to_tournament_and_db()
        new_player = Player(players_info[0], players_info[1], players_info[2],
                            players_info[3], players_info[4])
        if(new_player.check_if_player_exists()):
            self.tournament_view.player_already_exist()
        else:
            new_player.add_to_db()
            self.tournament_players.append(new_player)

    def generate_pairs_first_round(self):
        """
        Generate first round matches of the tournament
        """
        match_list = self.round_controller.generate_list_for_first_round(self.tournament_players)
        self.end_tournament(match_list)

    def end_tournament(self, match_list):
        """
        Display the tournament results
        """
        self.tournament_view.show_tournament_result(match_list)


controller = TournamentController()
controller.new_tournament()
