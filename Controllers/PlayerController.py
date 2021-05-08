import sys
sys.path.append("..")

from Views.PlayerView import PlayerView
from Models.PlayerModel import Player
# from Controllers.TournamentController import TournamentController

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
        # self.tournament_model = TournamentModel()
        # self.tournament_views = TournamentView()
        # self.player_model = Player()
        # self.db = TinyDB('../Models/db.json')
        # self.query = Query()
        # self.player_table = self.db.table('player_table')
        self.tournament_players = []


    # def add_player_to_tournament(self):
    #     """
    #     Add a player to the tournament
    #     """
    #     player_table = self.player_model.players_list()
    #     while len(self.tournament_players) != 8:
    #         nbr_players_in_tournament = len(self.tournament_players)
    #         self.tournament_views.add_player(nbr_players_in_tournament)
    #         choice = input("Entrez un nombre : ")
    #         if int(choice) == 1: 
    #             self.choose_player_from_db(player_table)
    #         if int(choice) == 2:
    #             self.add_new_player_to_tournament_and_db()
            
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

    # def add_new_player_to_tournament_and_db(self):
    #     """
    #     Checks if the player exist in db, if he
    #     doesn't exist, add it to tournament and db
    #     """
    #     players_info = self.player_views.add_player_to_tournament_and_db()
    #     if (self.player_model.check_players_exists(players_info)):
    #         self.player_views.player_already_exist()
    #     else:
    #         self.player_model.add_new_player_to_db(players_info)
    #         player_created = self.player_model.get_player_created()
    #         self.tournament_players.append(player_created)

        
    def show_player_report(self):
        self.player_views.ask_for_player_sort()
        # choice = input()
        # if int(choice) == 1:
        #     pass

    def ask_sort_player_by_what(self):
        choice = input("\nTapez 1 pour classer les joueurs par ordre alphabétique"
                        "\nTapez 2 pour classer les joueurs pas classement")
        if int(choice) == 1:
            self.sort_players_by_alphabetical_order()
        if int(choice) == 2:
            self.sort_player_by_ranking()
    

    def sort_player_by_ranking(self):
        player_list = Player.player_list()
        player_list = player_list.all()
        sorted_list = sorted(player_list, key=lambda k: k['rank'], reverse=True) 
        self.player_views.show_list_players_by_rank(sorted_list)      
    
    
    def sort_players_by_alphabetical_order(self):
        player_list = Player.player_list()
        player_list = player_list.all()
        sorted_list = sorted(player_list, key=lambda k: k['last_name']) 
        self.player_views.show_list_players(sorted_list)


