from tinydb import TinyDB, Query
# from TournamentModel import TournamentModel

class PlayerModel(object):
    """
    Player model, create, read, update or delete data from the player
    table
    """
    def __init__(self):
        """
        Constructor of the class
        """
        self.db = TinyDB('../Models/db.json')
    # def get_player_id(self, TournamentModel):
    #     pass

    # def get_last_name(self, TournamentModel, id):
    #     """
    #     Returns the last name of the player
    #     """
    #     pass

    # def set_last_name(self, TournamentModel, id):
    #     """
    #     Set the last name of the player
    #     """
    #     pass

    # def get_date_of_birth(self, TournamentModel, id):
    #     """
    #     Returns the date of birth of the player
    #     """
    #     pass

    
    # def set_date_of_birth(self, TournamentModel, id):
    #     """
    #     Sets the date of birth of the player
    #     """
    #     pass

    # def get_gender(self, TournamentModel, id):
    #     """
    #     Returns the gender of the player
    #     """
    #     pass

    # def set_gender(self, TournamentModel, id):
    #     """
    #     Sets the gender of the player
    #     """
    #     pass

    # def get_rank(self, TournamentModel, id):
    #     """
    #     Returns the rank of the player
    #     """
    #     pass

    # def set_rank(self, TournamentModel, id):
    #     """
    #     Sets the rank of the player
    #     """
    #     pass


    def add_new_player_to_db(self, players_info):
        
        pass

    def players_list(self):
        player_table = self.db.table('player_table')
        # for players in player_table:
        #     print(players)
        return player_table

# player = PlayerModel()
# player.players_list()
# player_table = db.table('player_table')

