from Controllers import TournamentController

if __name__=='__main__':
    try:
        controller = TournamentController.TournamentController()
        controller.start_program()
    except(KeyboardInterrupt):
        pass



