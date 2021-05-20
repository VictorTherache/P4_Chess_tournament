from Controllers import TournamentController
import time
if __name__=='__main__':
    try:
        controller = TournamentController.TournamentController()
        controller.start_program()
    except(KeyboardInterrupt):
        print("Erreur de saisie")
        time.sleep(1.2)
        exec(open("main.py").read())
    except(ValueError):
        print("Erreur de saisie")
        time.sleep(1.2)
        exec(open("main.py").read())



