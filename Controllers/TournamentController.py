import sys
sys.path.append("..")
from Views.TournamentView import TournamentView
from Views.PlayerView import PlayerView
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
        self.players_controller = PlayerController()
        self.players_view = PlayerView()
        pass

    def run_programm(self, view):
        """
        Run the chess programm
        """
        view.new_tournament()
        answer = input()
        if answer == 'o':
            self.create_tournament(self.tournament_view, self.players_controller)
        else: 
            pass

    def create_tournament(self, tournament_view, players_controller):
        """
        Add players in database for new tournament
        """
        self.players_controller.add_player_to_tournament()



    def press_add_player(self, model, view):
        """
        Show the view to add players to the tournament
        """
        pass

    def press_next_round(self, model, view):
        """
        Display the view for the next round
        """
        pass

    def press_show_report(self, model, view):
        """
        Display the view for the report
        """
        pass


controller = TournamentController()
# print(controller)
view = TournamentView()
controller.run_programm(view)