from Views.PlayerView import PlayerView
from Models.PlayerModel import Player
import sys
from sys import platform
import os
from texttable import Texttable
sys.path.append("..")


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
        self.tournament_players = []

    def choose_player_from_db(self, player_table):
        """
        Show the list of players in db and choose
        the player to select
        """
        self.player_views.show_players_list(player_table)
        player_choice = input("\nQuel joueur voulez vous ajouter ? :")
        player_chosen = player_table.all()[int(player_choice) - 1]
        if player_chosen not in self.tournament_players:
            return self.tournament_players.append(
                player_table.all()[int(player_choice) - 1])
        else:
            self.player_views.player_already_added()
            input("Appuyez sur entrée pour continuer")

    def ask_sort_player_by_what(self):
        """
        Asks the user how to sort the players
        """
        self.clean_console()
        choice = input("\n\n\n1 : Classer les joueurs par ordre alphabétique"
                       "\n2 : Classer les joueurs par rang")
        self.clean_console()
        if int(choice) == 1:
            self.sort_players_by_alphabetical_order()
        if int(choice) == 2:
            self.sort_player_by_ranking()
        input("\nAppuyer sur entrée pour continuer")

    def sort_player_by_ranking(self):
        """
        Sort a players list by ranking
        """
        t = Texttable()
        texttable_list = []
        headers = ["Prénom", "Nom", "Date de naissance",
                   "Genre", "Rang"]
        player_list = Player.player_list()
        player_list = player_list.all()
        sorted_list = sorted(player_list,
                             key=lambda
                             k: k['rank'],
                             reverse=True)
        self.player_views.liste_player_rank()
        for players in sorted_list:
            texttable_list.append([players['first_name'],
                                   players['last_name'],
                                   players['date_of_birth'],
                                   players['gender'],
                                   players['rank']])
        texttable_list.insert(0, headers)
        t.add_rows(texttable_list)
        self.player_views.show_list_players(t)

    def sort_players_by_alphabetical_order(self):
        """
        Sort a players list by alphabetical order
        """
        t = Texttable()
        texttable_list = []
        player_list = Player.player_list()
        player_list = player_list.all()
        sorted_list = sorted(player_list, key=lambda k: k['last_name'])
        headers = ["Prénom", "Nom", "Date de naissance",
                   "Genre", "Rang"]
        self.player_views.liste_player_alpha()
        for players in sorted_list:
            texttable_list.append([players['first_name'],
                                   players['last_name'],
                                   players['date_of_birth'],
                                   players['gender'],
                                   players['rank']])
        texttable_list.insert(0, headers)
        t.add_rows(texttable_list)
        self.player_views.show_list_players(t)

    def clean_console(self):
        if(platform == 'linux'
           or platform == 'linux2'
           or platform == 'darwin'):
            os.system('clear')
        else:
            os.system('cls')
