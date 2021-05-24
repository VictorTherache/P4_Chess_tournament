class TournamentView(object):

    def __init__(self):
        """
        Constructor of the method
        """
        self.players_info = []

    def new_tournament(self):
        """
        Contains the view of a new tournament
        """
        print("\n"
              "   ___ _\n"
              "  / __\ |__   ___  ___ ___                                  \n"
              " / /  | '_ \ / _ \/ __/ __|                                 \n"
              "/ /___| | | |  __/\__ \__ \                                 \n"
              "\____/|_| |_|\___||___/___/                             _   \n"
              "/__   \___  _   _ _ __ _ __   __ _ _ __ ___   ___ _ __ | |_ \n"
              "  / /\/ _ \| | | | '__| '_ \ / _` | '_ ` _ \ / _ \ '_ \| __|\n"
              " / / | (_) | |_| | |  | | | | (_| | | | | | |  __/ | | | |_ \n"
              " \/___\___/ \__,_|_|  |_| |_|\__,_|_| |_| |_|\___|_| |_|\__|\n"
              "  /___\_ __ __ _  __ _ _ __ (_)___  ___ _ __                \n"
              " //  // '__/ _` |/ _` | '_ \| / __|/ _ \ '__|               \n"
              "/ \_//| | | (_| | (_| | | | | \__ \  __/ |                  \n"
              "\___/ |_|  \__, |\__,_|_| |_|_|___/\___|_|                  \n"
              "           |___/                                            \n"
              "\n"
              )

    def add_player(self, nbr_players):
        """
        View to add player to the tournament
        """
        print(f"Il y a {nbr_players}/8 joueurs au tournoi. "
              "Voulez vous ajouter un joueur déjà existant (1) "
              "ou en créer un nouveau (2) ?\n")

    def menu_user_choice(self):
        print("1 : Lancer un nouveau tournoi\n"
              "2 : Charger un tournoi\n"
              "3 : Afficher un rapport\n"
              "4 : Mettre à jour le rang d'un joueur\n"
              "5 : Supprimer un joueur\n"
              "6 : Ajouter un nouveau joueur\n"
              "7 : Quitter le programme"
              )

    def show_players_list(self, texttable):
        """
        Show each player in a single row
        """
        print(texttable.draw())

    def header_list_player(self):
        print("\n\n\nListe des joueurs : \n")

    def player_already_added(self):
        print("Le joueur à déjà été ajouté au tournoi ! Veuillez réessayer")

    def player_already_exist(self):
        print("Le joueur à déjà été ajouté à la base de donnée ! Veuillez réessayer")

    def voice_les_resultats(self):
        print("\n\nTournoi terminé !\n")
        print("Voici les résultats : \n")

    def tournament_result(self, texttable):
        print(texttable.draw())

    def first_of_the_tournament(self, first_name, last_name, i):
        print(f"{i}er du tournoi : {first_name} {last_name}")

    def other_places_of_the_tournament(self, first_name, last_name, i):
        print(f"{i}ème du tournoi : {first_name} {last_name}")

    def user_choice(self):
        print("\n\n1 : Créer un nouveau tournoi"
              "\n2 : Afficher un rapport")

    def wrong_answer(self):
        print("\nVeuillez taper un autre chiffre")

    def ask_which_report(self):
        print("\n Quel rapport voulez-vous ? :\n"
              "\n 1 : Rapport sur les joueurs"
              "\n 2 : Rapport sur les tournois"
              "\n 3 : Revenir en arrière"
              )

    def invalide_name(self):
        print("\nVeuillez rentrer un nom et un prénom valide (sans numéros"
              "ou caractères spéciaux)")

    def invalide_date_of_birth(self):
        print("\nVeuillez rentrer une date de naissance valide dd/mm/YYYY")

    def invalide_gender(self):
        print("\nVeuillez rentrer un sexe valide (m/f)")

    def invalide_rank(self):
        print("\nVeuillez rentrer un rang valide")

    def display_tournament_list(self, tournament):
        print(f"Nom du tournoi : {tournament['name']}\n"
              f"Lieu : {tournament['place']}\n"
              f"Date :{tournament['date']}\n"
              f"Mode de jeu : {tournament['time_control']}\n"
              f"Description : {tournament['description']}\n\n"
              )

    def user_choose_tournament_report(self):
        print(
              "1 : Afficher les joueurs de ce tournoi\n"
              "2 : Afficher les rounds\n"
              "3 : Tournoi suivant\n"
              "4 : Tournoi précedent\n"
              "5 : Retour au menu\n"
              )

    def ask_sort_by_what(self):
        print("\n1 : Classer les joueurs par ordre alphabétique"
              "\n2 : Classer les joueurs par rang")

    def show_round(self, texttable):
        print(texttable.draw())

    def ask_to_show_match(self, rounds):
        print("1 : Afficher les matchs de ce tournoi\n"
              "2 : Revenir en arriere"
              )

    def display_round(self, round_name):
        print(f"\n{round_name}\n")

    def display_match(self, texttable):
        print(texttable.draw())

    def display_loading_tournaments(self, texttable):
        print(texttable.draw())

    def ask_user_loading_tournament_input(self):
        print("\n1 : Reprendre ce tournoi\n"
              "2 : Tournoi suivant\n"
              "3 : Tournoi précèdent\n"
              "4 : Retour au menu\n"
              )

    def new_tournament_header(self):
        print("\n\nCréation du nouveau tournoi\n")

    def ask_for_tournament_name(self):
        print("Nom du tournoi : ")

    def ask_for_place(self):
        print("Lieu : ")

    def ask_for_date(self):
        print("Date : ")

    def ask_for_time_control(self):
        print("Blitz, Bullet ou coup rapide :")

    def ask_for_description(self):
        print("Description : ")

    def display_tournament_players_header(self):
        print("Liste des joueurs ayant participé au tournoi :\n")

    def display_player(self, player):
        print(f"- {player['first_name']} {player['last_name']} | classement : {player['rank']}")

    def display_player_rank(self, player):
        print(f"Rang actuel de {player['first_name']} {player['last_name']} :"
              f" {player['rank']}"
              )

    def no_loading_tournament(self):
        print("Aucun tournoi en cours")

    def jump_line(self):
        print("\n")

    def add_player_sucess(self):
        print("\n\n\nLe joueur à bien été ajouté !")

    def delete_player_success(self):
        print("\n\n\nLe joueur à bien été supprimé ! ")

    def updated_player_success(self):
        print('\n\n\nLe joueur à bien été mis à jour !')

    def start_tournament(self):
        print('Début du tournoi\n')

    def no_tournament(self):
        print("Aucun tournois sauvegardés")

    def add_player_header(self):
        print("\n\nAjout des joueurs au tournoi\n")

    def add_new_player(self):
        print("\n\n\nAjouter un nouveau joueur")
