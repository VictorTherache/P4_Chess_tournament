class TournamentView(object):

    def new_tournament(self):
        """
        Contains the view of a new tournament
        """
        print("Bienvenue sur ChessTournament, le logiciel"
                "pour créer et gérer ses tournois d'échecs."
                "Voulez-vous créer un nouveau tournoi ? o/n")
        # pass

    def add_player(self):
        """
        View to add player to the tournament
        """
        print("Veuillez ajouter 8 joueurs au tournoi"
                "Voulez vous ajouter un joueur déjà existant (1) "
                "ou en créer un nouveau (2) ?")


    def display_round(self, model):
        """
        Display the tournament round
        """
        pass

    def enter_round_result(self, model):
        """
        At the end of a round, results must be updated 
        """
        pass


    def update_players_rank(self, model):
        """
        Update the players rank
        """
        pass

    def display_report(self, model):
        """
        Display the tournament report
        """
        pass