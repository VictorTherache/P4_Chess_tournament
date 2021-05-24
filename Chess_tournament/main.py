import os
from sys import platform
from Controllers import TournamentController
import time


if __name__ == '__main__':
    try:
        controller = TournamentController.TournamentController()
        controller.start_program()
    except(KeyboardInterrupt):
        print("Erreur de saisie")
        time.sleep(1.2)
        if(platform == 'linux'
           or platform == 'linux2'
           or platform == 'darwin'):
            os.system('clear')
        else:
            os.system('cls')
        exec(open("main.py").read())
    except(ValueError):
        print("Erreur de saisie")
        time.sleep(1.2)
        exec(open("main.py").read())
