import re
from tinydb import TinyDB, Query
import sys
import datetime
sys.path.append("..")

from Views.TournamentView import TournamentView
from Models.TournamentModel import Tournament
from Models.PlayerModel import Player
from Controllers.RoundController import RoundController
from Controllers.PlayerController import PlayerController


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
        self.player_controller = PlayerController()
        self.db = TinyDB('Models/db.json')
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
        self.start_tournament()
        

    def choose_player_from_db(self, player_table):
        """
        Show the list of players in db and choose
        the player to select
        """
        self.tournament_view.show_players_list(player_table)
        player_choice = input("Quels joueurs voulez vous ajouter ? :")
        player_chosen = player_table.all()[int(player_choice) - 1]
        if player_chosen not in self.tournament_players:
            return self.tournament_players.append(player_chosen)
        else :
            self.tournament_view.player_already_added()

    def add_new_player_to_tournament_and_db(self):
        """
        Checks if the player exist in db, if he
        doesn't exist, add it to tournament and db
        """
        players_info = self.ask_user_input_for_new_player()
        print(players_info)
        if(self.validation_new_player(players_info)):
            transformed_names = self.capitalize_name(players_info[0],
                                                    players_info[1])
            new_player = Player(transformed_names[0], 
                                transformed_names[1], 
                                players_info[2],
                                players_info[3], 
                                int(players_info[4]))
            if(new_player.check_if_player_exists()):
                self.tournament_view.player_already_exist()
            else:
                new_player.add_to_db()
                pick_player = self.player_table.all()[-1]
                self.tournament_players.append(pick_player)

    def validation_new_player(self, new_player):
        if (self.validate_name(new_player[0]) and
            self.validate_name(new_player[1]) and
            self.validate_age(new_player[2]) and
            self.validate_gender(new_player[3]) and
            self.validate_rank(new_player[4])):
            return True
        else:
            self.add_new_player_to_tournament_and_db()
        # first_name = self.validate_name(new_player[0])
        # last_name = self.validate_name(new_player[1])
        # date_of_birth = self.validate_age(new_player[2])
        # gender = self.validate_gender(new_player[3])
        # rank = self.validate_rank(new_player[4])
    
    def validate_name(self, name):
        if(self.contains_special_cha(name)):
            self.tournament_view.invalide_name()
        if(self.contains_number(name)):
            self.tournament_view.invalide_name()
        else:
            return True


    
    def capitalize_name(self, f_name, l_name):
        name_list=[]
        f_name = f_name.lower()
        l_name = l_name.lower()
        name_list.extend([f_name.capitalize(), l_name.capitalize()])
        return name_list

    
    def validate_age(self, date_of_birth):
        format = "%d/%m/%Y"
        try:    
          datetime.datetime.strptime(date_of_birth, format)
        except ValueError:
            self.tournament_view.invalide_date_of_birth()
        else:
            return True


    def validate_gender(self, gender):
        if not((gender == "m") or (gender == "f")):
            self.tournament_view.invalide_gender()
        else:
            return True
        

    
    def validate_rank(self, rank):
        if not rank.isdigit():
            self.tournament_view.invalide_rank()
        else:
            return True

    def contains_number(self, string):
        return any(i.isdigit() for i in string)
            

    def contains_special_cha(self, string):
        return any(not c.isalnum() for c in string)


    def ask_user_input_for_new_player(self):
        """
        View to get players info to add them in the db
        """
        self.players_info = []
        first_name = input("Entrez le prénom du joueur :")
        last_name = input("Entrez le nom du joueur :")
        age = input("Entrez l'âge du joueur :")
        gender = input("Entrez le sexe du joueur (m/f) :")
        rank = input("Entrez le rang du joueur :")
        self.players_info.extend([first_name, last_name, age,
                                 gender, rank])
        return self.players_info



    def start_tournament(self):
        """
        Start the tournament, generates pairs for the rounds and display the final
        result
        """
        self.tournament_players = [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, {'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, {'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, {'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, {'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, {'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, {'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, {'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}]
        match_list = self.round_controller.generate_pairs_for_first_round(
                                            self.tournament_players, 
                                            self.tournament_model.nbr_of_rounds)

        self.end_tournament(match_list)


    def end_tournament(self, match_list):
        """
        Display the tournament results
        """
        self.tournament_view.show_tournament_result(match_list)

    
    def user_choice(self):
        self.tournament_view.user_choice()
        choice = input()
        if int(choice) == 1:
            self.new_tournament()
        if int(choice) == 2:
            self.ask_which_report()
        else:
            self.tournament_view.wrong_answer()
            self.user_choice()
    
    def ask_which_report(self):
        self.tournament_view.ask_which_report()
        choice = input()
        if int(choice) == 1:
            self.player_controller.ask_sort_player_by_what()

# controller = TournamentController()
# # controller.validate_first_name("JEAN")
# controller.start_tournament()
