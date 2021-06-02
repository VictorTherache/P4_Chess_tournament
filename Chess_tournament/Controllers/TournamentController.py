from Controllers.PlayerController import PlayerController
from Controllers.RoundController import RoundController
from Models.PlayerModel import Player
from Models.TournamentModel import Tournament
from Views.TournamentView import TournamentView
from Views.PlayerView import PlayerView
from tinydb import TinyDB, Query
import sys
from sys import platform
import os
import datetime
import time
from texttable import Texttable
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
        self.player_views = PlayerView()
        self.db = TinyDB('Models/db.json')
        self.player_table = self.db.table('player_table')
        self.tournament_table = self.db.table('tournament_table')
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
        self.clean_console()
        self.tournament_view.new_tournament()
        user_choice = self.menu_user_choice()
        if int(user_choice) == 1:
            self.clean_console()
            self.add_tournament_info()
            self.create_save_new_tournament_instance()
            self.new_tournament()
        if int(user_choice) == 2:
            self.choose_loading_tournament()
        if int(user_choice) == 3:
            self.ask_which_report()
        if int(user_choice) == 4:
            self.update_player_rank()
        if int(user_choice) == 5:
            self.add_new_player_to_tournament_and_db()
            self.tournament_view.add_player_sucess()
            input("Appuyer sur entrée pour continuer")
            self.start_program()
        if int(user_choice) == 6:
            self.delete_player()
        if int(user_choice) == 7:
            self.delete_tournament()
        if int(user_choice) == 8:
            self.close_program()

    def add_tournament_info(self):
        """
        Ask the user information on the tournament
        """
        self.tournament_view.new_tournament_header()
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

    def new_tournament(self):
        """
        Ask the users to add players to the tournament
        """
        self.tournament_players = []
        self.players_index = []
        while len(self.tournament_players) != 8:
            self.clean_console()
            self.tournament_view.add_player_header()
            nbr_players_in_tournament = len(self.tournament_players)
            self.tournament_view.add_player(nbr_players_in_tournament)
            choice = input()
            if int(choice) == 1:
                self.choose_player_from_db(self.player_table)
            if int(choice) == 2:
                self.add_new_player_to_tournament_and_db()
        self.update_player_in_db()
        self.start_tournament()

    def choose_loading_tournament(self):
        """
        Display the loading tournaments and ask users which one to choose
        """
        self.clean_console()
        i = 0
        user_choice = 1
        tournament_load_list = Tournament.get_loading_tournaments()
        while int(user_choice) != 4:
            t = Texttable()
            texttable_list = []
            headers = ["Nom du tournoi", "Lieu", "Date", "Contrôle du temps", "Description"]
            if tournament_load_list:
                texttable_list.append([tournament_load_list[i]['name'],
                                       tournament_load_list[i]['place'],
                                       tournament_load_list[i]['date'],
                                       tournament_load_list[i]['time_control'],
                                       tournament_load_list[i]['description']])
                texttable_list.insert(0, headers)
                t.add_rows(texttable_list)
                self.tournament_view.display_loading_tournaments(t)
                self.tournament_view.ask_user_loading_tournament_input()
                user_choice = input()
                self.clean_console()
                if int(user_choice) == 2:
                    if(len(tournament_load_list) == 0):
                        i -= 1
                    else:
                        if tournament_load_list[i] == tournament_load_list[-1]:
                            i -= 1
                    i += 1
                if int(user_choice) == 3:
                    i -= 1
                    if len(tournament_load_list) == 0:
                        i += 1
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
                self.clean_console()
                self.tournament_view.no_loading_tournament()
                input("Appuyer sur une entrée pour continuer")
                self.start_program()
        self.start_program()

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

    def update_player_rank(self):
        """
        Update the player ranks
        """
        self.clean_console()
        i = 1
        t = Texttable()
        texttable_list = []
        headers = ["Id", "Prénom", "Nom", "Date de naissance",
                   "Genre", "Rang"]
        self.tournament_view.header_list_player()
        for players in self.player_table:
            texttable_list.append([i,
                                   players['first_name'],
                                   players['last_name'],
                                   players['date_of_birth'],
                                   players['gender'],
                                   players['rank']
                                   ])
            i += 1
        texttable_list.insert(0, headers)
        t.add_rows(texttable_list)
        self.tournament_view.show_players_list(t)
        user_choice = input("\nSelectionnez un joueur :")
        player_chosen = self.player_table.all()[int(user_choice) - 1]
        self.tournament_view.display_player_rank(player_chosen)
        updated_rank = input("Nouveau rang : ")
        Player.update_player_rank(player_chosen.doc_id, int(updated_rank))
        self.clean_console()
        self.tournament_view.updated_player_success()
        input("Appuyer sur entrée pour continuer")
        self.start_program()

    def delete_player(self):
        """
        Delete the selected player
        """
        self.clean_console()
        i = 1
        t = Texttable()
        texttable_list = []
        headers = ["Id", "Prénom", "Nom", "Date de naissance",
                   "Genre", "Rang"]
        self.tournament_view.header_list_player()
        for players in self.player_table:
            texttable_list.append([i,
                                   players['first_name'],
                                   players['last_name'],
                                   players['date_of_birth'],
                                   players['gender'],
                                   players['rank']
                                   ])
            i += 1
        texttable_list.insert(0, headers)
        t.add_rows(texttable_list)
        self.tournament_view.show_players_list(t)
        user_choice = input("\nSelectionnez un joueur à supprimer:")
        player_chosen = self.player_table.all()[int(user_choice) - 1]
        Player.delete_player(player_chosen.doc_id)
        self.clean_console()
        self.tournament_view.delete_player_success()
        input("Appuyer sur entrée pour continuer")
        self.start_program()

    def delete_tournament(self):
        """
        Delete the selected tournament
        """
        self.clean_console()
        i = 1
        t = Texttable()
        texttable_list = []
        headers = ["Id", "Nom", "Lieu", "Date",
                   "Time control", "Description"]
        for tournament in self.tournament_table:
            texttable_list.append([i,
                                   tournament['name'],
                                   tournament['place'],
                                   tournament['date'],
                                   tournament['time_control'],
                                   tournament['description']
                                   ])
            i += 1
        texttable_list.insert(0, headers)
        t.add_rows(texttable_list)
        if len(self.tournament_table) == 0:
            input("\n\n\nAucun tournoi trouvé, appuyez sur"
                         " entrée pour continuer")
            self.start_program()
        self.tournament_view.header_list_tournament()
        self.tournament_view.show_players_list(t)
        user_choice = input("\nSelectionnez un tournoi à supprimer:")
        tournament_chosen = self.tournament_table.all()[int(user_choice) - 1]
        Tournament.delete_tournament(tournament_chosen.doc_id)
        self.clean_console()
        self.tournament_view.delete_tournament_success()
        input("Appuyer sur entrée pour continuer")
        self.start_program()



    def close_program(self):
        sys.exit(0)

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
        self.clean_console()
        self.tournament_view.header_list_player()
        t = Texttable()
        texttable_list = []
        headers = ["Id", "Prénom", "Nom", "Date de naissance",
                   "Genre", "Rang"]
        for players in player_table:
            texttable_list.append([i,
                                   players['first_name'],
                                   players['last_name'],
                                   players['date_of_birth'],
                                   players['gender'],
                                   players['rank']
                                   ])
            i += 1
        texttable_list.insert(0, headers)
        t.add_rows(texttable_list)
        self.tournament_view.show_players_list(t)
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
        self.clean_console()
        self.tournament_view.add_new_player()
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
        age = input("Date de naissance du joueur (dd/mm/yyyy) :")
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
        self.clean_console()
        self.tournament_view.start_tournament()
        self.get_tournament_id(self.tournament_info)
        match_list = self.round_controller.generate_pairs_for_first_round(
            self.tournament_players,
            4, self.tournament_id)
        self.end_tournament(match_list)
        input("Appuyez sur entrée pour continuer")
        self.clean_console()
        self.update_players_rank(self.tournament_id)
        self.start_program()

    def update_players_rank(self, tournament_id):
        """
        At the end of a tournament asks the user to
        update the players rank
        """
        players_indexes = self.get_players_index_from_db(tournament_id)
        players_list = Player.get_players_by_index(players_indexes)
        i = 0
        for player in players_list:
            self.clean_console()
            self.tournament_view.display_player_rank(player)
            updated_rank = input("Nouveau rang : ")
            Player.update_player_rank(players_indexes[i], int(updated_rank))
            i += 1
        self.start_program()

    def get_players_index_from_db(self, tournament_id):
        players_indexes = Tournament.get_players_index_from_db(tournament_id)
        return players_indexes

    def end_tournament(self, match_list):
        """
        Display the tournament results
        """
        self.clean_console()
        self.tournament_view.voice_les_resultats()
        t = Texttable()
        texttable_list = []
        headers = ["Position", "Joueur"]
        i = 1
        for player in match_list:
            if i == 1:
                join_player = [player[0]["first_name"], player[0]["last_name"]]
                texttable_list.append(["1 er", ' '.join(join_player)])
            else:
                join_player = [player[0]["first_name"], player[0]["last_name"]]
                texttable_list.append([f"{str(i)} ème", ' '.join(join_player)])
            i += 1
        texttable_list.insert(0, headers)
        t.add_rows(texttable_list)
        self.tournament_view.tournament_result(t)

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
        for players in self.tournament_players:
            player_index = self.player_table.get((self.User.first_name == players['first_name']) &
                                                 (self.User.last_name == players['last_name']))
            self.players_index.append(player_index.doc_id)

    def get_tournament_list(self):
        tournament_list = Tournament.get_tournament_list()
        return tournament_list

    def ask_which_report(self):
        self.clean_console()
        self.tournament_view.ask_which_report()
        choice = input()
        tournament_list = self.get_tournament_list()
        tournament_list = tournament_list.all()
        i = 0
        if int(choice) == 1:
            self.player_controller.ask_sort_player_by_what()
            self.ask_which_report()
        if int(choice) == 2:
            if tournament_list != []:
                user_choice = 0
                while int(user_choice) != 5:
                    self.clean_console()
                    t = Texttable()
                    texttable_list = []
                    headers = ["Nom du tournoi", "Lieu", "Date", "Contrôle du temps", "Description"]
                    if tournament_list:
                        texttable_list.append([tournament_list[i]['name'],
                                            tournament_list[i]['place'],
                                            tournament_list[i]['date'],
                                            tournament_list[i]['time_control'],
                                            tournament_list[i]['description']])
                        texttable_list.insert(0, headers)
                        t.add_rows(texttable_list)
                    self.tournament_view.display_loading_tournaments(t)
                    self.tournament_view.user_choose_tournament_report()
                    user_choice = input()
                    if int(user_choice) == 1:
                        self.report_tournament_players(tournament_list[i])
                    if int(user_choice) == 2:
                        self.report_tournament_rounds(tournament_list[i]['rounds'])
                    if int(user_choice) == 3:
                        if len(tournament_list) != 1:
                            if tournament_list[i] == tournament_list[-1]:
                                i = 0
                            i += 1
                    if int(user_choice) == 4:
                        if len(tournament_list) != 1:
                            if tournament_list[i] == tournament_list[0]:
                                i += 1
                            i -= 1
                else:
                    self.start_program()
            else:
                self.tournament_view.no_tournament()
                time.sleep(2)
                self.start_program()
        if int(choice) == 3:
            self.start_program()

    def report_tournament_players(self, tournament):
        self.clean_console()
        self.tournament_view.ask_sort_by_what()
        user_choice = input()
        if int(user_choice) == 1:
            self.get_tournament_players_alphabetical(tournament)
        if int(user_choice) == 2:
            self.get_tournament_players_ranking(tournament)
        self.tournament_view.jump_line()
        input("Appuyer sur entrée pour continuer")

    def report_tournament_rounds(self, tournament_rounds):
        self.clean_console()
        t = Texttable()
        texttable_list = []
        headers = ["Round number",
                   "Heure de début",
                   "Heure de fin"]
        for rounds in tournament_rounds:
            texttable_list.append([rounds["name"],
                                  rounds["start_time"],
                                  rounds["end_time"]])
        texttable_list.insert(0, headers)
        t.add_rows(texttable_list)
        self.tournament_view.show_round(t)
        self.tournament_view.ask_to_show_match(rounds)
        user_choice = input()
        self.clean_console()
        if int(user_choice) != 2:
            headers = ["Joueur 1", "Joueur 2", "Score 1", "Score 2"]
            for rounds in tournament_rounds:
                self.tournament_view.display_round(rounds['name'])
                t = Texttable()
                texttable_list = []
                for match in rounds['match_list']:
                    name_player1 = [match[0][0]['first_name'],
                                    match[0][0]['last_name']]
                    name_player2 = [match[1][0]['first_name'],
                                    match[1][0]['last_name']]
                    texttable_list.append([' '.join(name_player1),
                                           ' '.join(name_player2),
                                           match[0][1],
                                           match[1][1]
                                           ])
                texttable_list.insert(0, headers)
                t.add_rows(texttable_list)
                self.tournament_view.display_match(t)
        input("Appuyer sur entrée pour continuer")

    def get_tournament_players_ranking(self, tournament):
        player_list = Player.get_players_by_index(tournament['player'])
        t = Texttable()
        headers = ["Prénom", "Nom", "Date de naissance",
                   "Genre", "Rang"]
        texttable_list = []
        sorted_list = sorted(
            player_list, key=lambda k: k['rank'], reverse=True)
        self.clean_console()
        self.tournament_view.display_tournament_players_header()
        for player in sorted_list:
            texttable_list.append([player['first_name'],
                                   player['last_name'],
                                   player['date_of_birth'],
                                   player['gender'],
                                   player['rank']])
        texttable_list.insert(0, headers)
        t.add_rows(texttable_list)
        self.player_views.show_list_players(t)

    def get_tournament_players_alphabetical(self, tournament):
        player_list = Player.get_players_by_index(tournament['player'])
        sorted_list = sorted(player_list, key=lambda k: k['last_name'])
        self.clean_console()
        t = Texttable()
        headers = ["Prénom", "Nom", "Date de naissance",
                   "Genre", "Rang"]
        texttable_list = []
        self.tournament_view.display_tournament_players_header()
        for player in sorted_list:
            texttable_list.append([player['first_name'],
                                   player['last_name'],
                                   player['date_of_birth'],
                                   player['gender'],
                                   player['rank']])
        texttable_list.insert(0, headers)
        t.add_rows(texttable_list)
        self.player_views.show_list_players(t)

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
                or (gender == "F")):
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

    def clean_console(self):
        if(platform == 'linux'
           or platform == 'linux2'
           or platform == 'darwin'):
            os.system('clear')
        else:
            os.system('cls')


controller = TournamentController()
