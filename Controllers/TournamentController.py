from Controllers.PlayerController import PlayerController
from Controllers.RoundController import RoundController
from Models.PlayerModel import Player
from Models.TournamentModel import Tournament
from Views.TournamentView import TournamentView
import re
from tinydb import TinyDB, Query
import sys
import os
import datetime
import time
sys.path.append("..")


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
        self.round_controller = RoundController()
        self.player_controller = PlayerController()
        self.db = TinyDB('Models/db.json')
        self.player_table = self.db.table('player_table')
        self.User = Query()
        self.tournament_players = []
        self.players_index = []
        self.tournament_info = []
        self.tournament_instance = {}
        self.tournament_id = 0

    def start_program(self):
        """
        Initialize the tournament, add players to it
        """
        os.system('cls')
        self.tournament_view.new_tournament()
        player_table = Tournament.players_list()
        user_choice = self.menu_user_choice()
        if int(user_choice) == 1:
            os.system('cls')
            self.add_tournament_info()
            self.create_save_new_tournament_instance()
            self.new_tournament()
        if int(user_choice) == 2:
            self.choose_loading_tournament()
        if int(user_choice) == 3:
            self.ask_which_report()
        if int(user_choice) == 4:
            self.update_player_rank()

    def update_player_rank(self):
        """
        Update the player ranks
        """
        os.system('cls')
        i=1
        self.tournament_view.header_list_player()
        for players in self.player_table:
            self.tournament_view.show_players_list(players['first_name'], 
                                                    players['last_name'],
                                                    i)
            i+=1
        user_choice = input("\nSelectionnez un joueur :")
        player_chosen = self.player_table.all()[int(user_choice) - 1]
        self.tournament_view.display_player_rank(player_chosen)
        updated_rank = input("Nouveau rang : ")
        Player.update_player_rank(player_chosen.doc_id, int(updated_rank))
        os.system('cls')
        self.tournament_view.updated_player_success()
        input("Appuyer sur entrée pour continuer")
        self.start_program()

    def new_tournament(self):
        """
        Ask the users to add players to the tournament
        """
        while len(self.tournament_players) != 8:
            os.system('cls')
            nbr_players_in_tournament = len(self.tournament_players)
            self.tournament_view.add_player(nbr_players_in_tournament)
            choice = input()
            if int(choice) == 1:
                self.choose_player_from_db(self.player_table)
            if int(choice) == 2:
                self.add_new_player_to_tournament_and_db()
        self.update_player_in_db()
        self.start_tournament()

    def create_save_new_tournament_instance(self):
        """
        Create and save the tournament instance
        """
        self.tournament_instance = {
            'name': self.tournament_info[0],
            'place': self.tournament_info[1],
            'date': self.tournament_info[2],
            'rounds': "rounds",
            'player': "players",
            'time_control': self.tournament_info[3],
            'description': self.tournament_info[4]
        }
        Tournament.save_tournament(self.tournament_instance)

    def add_tournament_info(self):
        """
        Ask the user information on the tournament
        """
        self.tournament_view.ask_for_tournament_name()
        name = input()
        self.tournament_view.ask_for_place()
        place = input()
        self.tournament_view.ask_for_date()
        date = input()
        self.tournament_view.ask_for_time_control()
        time_control = input()
        self.tournament_view.ask_for_description()
        description = input()
        self.tournament_info.extend([name,
                                     place,
                                     date,
                                     time_control,
                                     description])

    def choose_loading_tournament(self):
        """
        Display the loading tournaments and ask users which one to choose
        """
        os.system('cls')
        i = 0
        user_choice=1
        tournament_load_list = Tournament.get_loading_tournaments()
        if tournament_load_list:
            self.tournament_view.display_loading_tournaments(
                tournament_load_list[i])
            while int(user_choice) != 4:
                user_choice = input()
                os.system('cls')
                self.tournament_view.display_loading_tournaments(
                    tournament_load_list[i])
                # user_choice = input()
                if int(user_choice) == 2:
                    if tournament_load_list[i] == tournament_load_list[-1]:
                        i -= 1
                    i += 1
                if int(user_choice) == 3:
                    i -= 1
                    if tournament_load_list[i] == tournament_load_list[0]:
                        i += 1
                if int(user_choice) == 1:
                    self.load_tournament_info(tournament_load_list[i])
                    if tournament_load_list[i]['player'] == 'players':
                        self.new_tournament()
                    if tournament_load_list[i]['rounds'] == 'rounds':
                        self.add_players_to_self(tournament_load_list[i])
                        self.start_tournament()
                    else:
                        self.get_tournament_id(self.tournament_info)
                        match_list = self.round_controller.load_match(
                            tournament_load_list[i], self.tournament_id)
                        self.end_tournament(match_list)
                        self.update_players_rank(self.tournament_id)
                        self.start_program()
        else:
            os.system('cls')
            self.tournament_view.no_loading_tournament()
            input("Appuyer sur une entrée pour continuer")
            self.start_program()

                    # self.add_players_to_self(tournament_load_list[i])
                    # self.start_tournament()
        self.start_program()

    def get_tournament_id(self, tournament):
        """
        Get the tournament id
        """
        current_id = Tournament.get_id(tournament)
        self.tournament_id = current_id

    def add_players_to_self(self, tournament):
        """
        Add players in self.tournament_players
        """
        player_list = Player.get_players_by_index(tournament['player'])
        self.tournament_players = player_list

    def load_tournament_info(self, tournament):
        """
        Add tournaments info to self.tournament_info
        """
        self.tournament_info.extend([tournament['name'], tournament['place'],
                                     tournament['date'], tournament['time_control'],
                                     tournament['description']])

    def menu_user_choice(self):
        """
        Ask the user for an action
        """
        self.tournament_view.menu_user_choice()
        user_choice = input()
        return user_choice

    def update_player_in_db(self):
        """
        Update players information in the db
        """
        self.get_players_index()
        Tournament.update_players(self.players_index, self.tournament_info[0])

    def choose_player_from_db(self, player_table):
        """
        Show the list of players in db and choose
        the player to select
        """
        i = 1
        os.system('cls')
        self.tournament_view.header_list_player()
        for players in player_table:
            self.tournament_view.show_players_list(players['first_name'],
                                                    players['last_name'],
                                                    str(i))
            i+= 1
        player_choice = input("\nQuel joueur voulez vous ajouter ? :")
        player_chosen = player_table.all()[int(player_choice) - 1]
        if player_chosen not in self.tournament_players:
            return self.tournament_players.append(player_chosen)
        else:
            self.tournament_view.player_already_added()

    def add_new_player_to_tournament_and_db(self):
        """
        Checks if the player exist in db, if he
        doesn't exist, add it to tournament and db
        """
        players_info = self.ask_user_input_for_new_player()
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

    def ask_user_input_for_new_player(self):
        """
        View to get players info to add them in the db
        """
        self.players_info = []
        first_name = input("Prénom du joueur :")
        last_name = input("Nom du joueur :")
        age = input("Date de naissance du joueur :")
        gender = input("Sexe du joueur (m/f) :")
        rank = input("Rang du joueur :")
        self.players_info.extend([first_name, last_name, age,
                                  gender, rank])
        return self.players_info

    def start_tournament(self):
        """
        Start the tournament, generates pairs for the rounds and display the final
        result
        """
        os.system('cls')
        self.tournament_view.start_tournament()
        tournament_id = self.get_tournament_id(self.tournament_info)
        match_list = self.round_controller.generate_pairs_for_first_round(
            self.tournament_players,
            4, self.tournament_id)
        self.end_tournament(match_list)
        input("Appuyez sur entrée pour continuer")
        os.system('cls')
        self.update_players_rank(self.tournament_id)
        self.start_program()

    def update_players_rank(self, tournament_id):
        """

        """
        players_indexes  =self.get_players_index_from_db(tournament_id)
        for player in players_indexes:
            player_chosen = self.player_table.all()[int(player) - 1]
            self.tournament_view.display_player_rank(player_chosen)
            updated_rank = input("Nouveau rang : ")
            Player.update_player_rank(player, int(updated_rank))
        self.start_program()


    def get_players_index_from_db(self, tournament_id):
        players_indexes = Tournament.get_players_index_from_db(tournament_id)
        return players_indexes

    def end_tournament(self, match_list):
        """
        Display the tournament results
        """
        self.tournament_view.show_tournament_result(match_list)

    def create_tournament_instance(self, rounds):
        tournament = Tournament("Tournoi Hiver",
                                "Mon Garage",
                                "13/05/2021",
                                rounds,
                                self.players_index,
                                "blitz",
                                "description au pif"
                                )
        return tournament

    def get_players_index(self):
        # self.tournament_players = [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, {'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, {'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, {'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, {'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, {'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, {'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, {'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}]
        for players in self.tournament_players:
            player_index = self.player_table.get((self.User.first_name == players['first_name']) &
                                                 (self.User.last_name == players['last_name']))
            self.players_index.append(player_index.doc_id)

    def user_choice(self):
        self.tournament_view.user_choice()
        choice = input()
        if int(choice) == 1:
            self.start_program()
        if int(choice) == 2:
            self.ask_which_report()
        else:
            self.tournament_view.wrong_answer()
            self.user_choice()

    def get_tournament_list(self):
        tournament_list = Tournament.get_tournament_list()
        return tournament_list

    def ask_which_report(self):
        os.system('cls')
        self.tournament_view.ask_which_report()
        choice = input()
        tournament_list = self.get_tournament_list()
        tournament_list = tournament_list.all()
        i = 0
        if int(choice) == 1:
            self.player_controller.ask_sort_player_by_what()
            # input("Appuyer sur une touche pour continuer")
            self.ask_which_report()
        if int(choice) == 2:
            user_choice = 0
            while int(user_choice) != 5:
                os.system('cls')
                self.tournament_view.display_tournament_list(
                    tournament_list[i])
                self.tournament_view.user_choose_tournament_report()
                user_choice = input()
                if int(user_choice) == 1:
                    self.report_tournament_players(tournament_list[i])
                if int(user_choice) == 2:
                    self.report_tournament_rounds(tournament_list[i]['rounds'])
                if int(user_choice) == 3:
                    if tournament_list[i] == tournament_list[-1]:
                        i = 0
                    i += 1
                if int(user_choice) == 4:
                    if tournament_list[i] == tournament_list[0]:
                        i += 1
                    i -= 1
            else:
                self.start_program()
        if int(choice) == 3:
            self.start_program()

    def report_tournament_players(self, tournament):
        os.system('cls')
        self.tournament_view.ask_sort_by_what()
        user_choice = input()
        if int(user_choice) == 1:
            self.get_tournament_players_alphabetical(tournament)
        if int(user_choice) == 2:
            self.get_tournament_players_ranking(tournament)
        self.tournament_view.jump_line()
        input("Appuyer sur entrée pour continuer")

    def report_tournament_rounds(self, tournament_rounds):
        os.system('cls')
        for rounds in tournament_rounds:
            self.tournament_view.show_round(rounds)
        self.tournament_view.ask_to_show_match(rounds)
        user_choice = input()
        os.system('cls')
        if int(user_choice) != 2:
            for rounds in tournament_rounds:
                self.tournament_view.display_round(rounds['name'])
                for match in rounds['match_list']:
                    self.tournament_view.display_match(match)
        input("Appuyer sur entrée pour continuer")

    def get_tournament_players_ranking(self, tournament):
        player_list = Player.player_list()
        sorted_list = sorted(
            player_list, key=lambda k: k['rank'], reverse=True)
        os.system('cls')
        self.tournament_view.display_tournament_players_header()
        for player in sorted_list:
            self.tournament_view.display_player(player)

    def get_tournament_players_alphabetical(self, tournament):
        player_list = Player.player_list()
        sorted_list = sorted(player_list, key=lambda k: k['last_name'])
        os.system('cls')
        self.tournament_view.display_tournament_players_header()
        for player in sorted_list:
            self.tournament_view.display_player(player)

    def validation_new_player(self, new_player):
        if (self.validate_name(new_player[0]) and
            self.validate_name(new_player[1]) and
            self.validate_age(new_player[2]) and
            self.validate_gender(new_player[3]) and
                self.validate_rank(new_player[4])):
            return True
        else:
            self.add_new_player_to_tournament_and_db()

    def validate_name(self, name):
        if(self.contains_special_cha(name)):
            self.tournament_view.invalide_name()
        if(self.contains_number(name)):
            self.tournament_view.invalide_name()
        else:
            return True

    def capitalize_name(self, f_name, l_name):
        name_list = []
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
        if not((gender == "m") 
            or (gender == "f")
            or (gender == "M")
            or (gender == "F") ):
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


controller = TournamentController()
# match_list = ([{'name': 'Round 1', 'start_time': '14/05/2021 11:31:32', 'end_time': '14/05/2021 11:31:35', 'match_list': [([{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0]), ([{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 1.0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0]), ([{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 1.0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0]), ([{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0])]}, {'name': 'Round 2', 'start_time': '14/05/2021 11:31:35', 'end_time': '14/05/2021 11:31:37', 'match_list': [([{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 2.0], [{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 2.0]), ([{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 2.0], [{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0]), ([{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0]), ([{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 2.0])]}, {'name': 'Round 3', 'start_time': '14/05/2021 11:31:37', 'end_time': '14/05/2021 11:31:39', 'match_list': [([{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 2.0], [{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 2.0]), ([{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 2.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 1.0]), ([{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0]), ([{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth':
# '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0])]}, {'name': 'Round 4', 'start_time': '14/05/2021 11:31:39', 'end_time': '14/05/2021 11:31:42', 'match_list': [([{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 2.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 2.0]), ([{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 2.0], [{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 2.0]), ([{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 1.0]), ([{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 1.0], [{'first_name': 'Ozil', 'last_name': 'Bzerut',
# 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0])]}], [[{'first_name': 'Pete', 'last_name': 'Donaldo', 'date_of_birth': '13/02/1979', 'gender': 'm', 'rank': 1753}, 1.0, 1.0, 1.0, 1.0], [{'first_name': 'Ozil', 'last_name': 'Bzerut', 'date_of_birth': '12/05/1985', 'gender': 'm', 'rank': 1050}, 1.0, 1.0, 0.0, 1.0], [{'first_name': 'Emilie', 'last_name': 'Nalie', 'date_of_birth': '12/02/1983', 'gender': 'f', 'rank': 1400}, 0.0, 1.0, 1.0, 0.0], [{'first_name': 'Vicotr', 'last_name': 'Racheter', 'date_of_birth': '22/08/1993', 'gender': 'm', 'rank': 1300}, 0.0, 0.0, 1.0, 1.0], [{'first_name': 'Lucas', 'last_name': 'Peter', 'date_of_birth': '12/04/1993', 'gender': 'm', 'rank': 1203}, 0.0, 0.0, 1.0, 1.0], [{'first_name': 'Gerald', 'last_name': 'Languefoy', 'date_of_birth': '30/03/1983', 'gender': 'm', 'rank': 2000}, 1.0, 0.0, 0.0, 0.0], [{'first_name': 'Joshua', 'last_name': 'Romald', 'date_of_birth': '20/04/1991', 'gender': 'm', 'rank': 1302}, 1.0, 0.0, 0.0, 0.0], [{'first_name': 'Laura', 'last_name': 'Stunie', 'date_of_birth': '12/12/1999', 'gender': 'f', 'rank': 1000}, 0.0, 1.0, 0.0, 0.0]])
# controller.end_tournament(match_list)
# # controller.validate_first_name("JEAN")
