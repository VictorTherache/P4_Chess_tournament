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
        print("Bienvenue sur ChessTournament, le logiciel "
                "pour créer et gérer ses tournois d'échecs. "
                " Veuillez ajouter huit joueurs au tournoi\n")


    def add_player(self, nbr_players):
        """
        View to add player to the tournament
        """
        print(f"Il y a {nbr_players}/8 joueurs au tournoi. "
                "Voulez vous ajouter un joueur déjà existant (1) "
                "ou en créer un nouveau (2) ?\n")


    def show_players_list(self, player_table):
        """
        Contains the view of a new tournament
        """
        i = 1
        for players in player_table:
            print(f"{players['first_name']} {players['last_name']} {str(i)}") 
            i+= 1


    def add_player_to_tournament_and_db(self):
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