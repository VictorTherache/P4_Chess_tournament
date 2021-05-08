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
        print("Veuillez ajouter huit joueurs au tournoi\n")


    def add_player(self, nbr_players):
        """
        View to add player to the tournament
        """
        print(f"Il y a {nbr_players}/8 joueurs au tournoi. "
                "Voulez vous ajouter un joueur déjà existant (1) "
                "ou en créer un nouveau (2) ?\n")


    def show_players_list(self, player_table):
        """
        Show each player in a single row
        """
        i = 1
        for players in player_table:
            print(f"{players['first_name']} {players['last_name']} {str(i)}") 
            i+= 1



    def player_already_added(self):
        print("Le joueur à déjà été ajouté au tournoi ! Veuillez réessayer")
        

    def player_already_exist(self):
        print("Le joueur à déjà été ajouté à la base de donnée ! Veuillez réessayer")


    def show_tournament_result(self, match_result):
        i = 1
        print("Tournoi terminé !\n")
        print("Voici les résultats : \n")
        for players in match_result:
            if i == 1:
                print(f"{i}er du tournoi : {players[0]['first_name']} {players[0]['last_name']}")
            else:
                print(f"{i}ème du tournoi : {players[0]['first_name']} {players[0]['last_name']}")
            i+=1

    
    def user_choice(self):
        print("\nQue voulez vous faire ?\nTapez 1 pour créer un nouveau tournoi"
                "\nTapez 2 pour afficher un rapport")
        
    def wrong_answer(self):
        print("\nVeuillez taper un autre chiffre")

    def ask_which_report(self):
        print("\n Quel rapport voulez-vous ? :\n"
                "\nTapez 1 pour un rapport sur les joueurs"
                "\nTapez 2 pour un rapport sur tout les joueurs d'un tournoi"
                "\nTapez 3 pour un rapport sur les tournois")


    def invalide_name(self):
        print("\nVeuillez rentrer un nom et un prénom valide (sans numéros"
                "ou caractères spéciaux)")

    def invalide_date_of_birth(self):
        print("\nVeuillez rentrer une date de naissance valide dd/mm/YYYY")

    def invalide_gender(self):
        print("\nVeuillez rentrer un sexe valide (m/f)")

    def invalide_rank(self):
        print("\nVeuillez rentrer un rang valide")