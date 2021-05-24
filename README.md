# P2_Therache_Victor
## Table des matières
1. [Information générale](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)

### Information générale
***
Ce programme permet de gérer des tournois d'échecs de 8 joueurs, création des tournois, sauvegarde, chargement et génération de rapports sur les joueurs, les tournois, les rounds et les matchs.
### Screenshot
![Image text](https://i.ibb.co/LC80vpd/banniere-op.png)
## Technologies
***
Technologie utilisé :
* [Python 64bit](https://www.python.org/downloads/release/python-391/): Version 3.9.1
* [tinydb](https://tinydb.readthedocs.io/en/latest/index.html)
* flake8-html(https://pypi.org/project/flake8-html/)


## Installation
***
Pour installer le programme, entrez ces commandes dans un terminal :
```
Sur Windows : 
$ git clone https://github.com/VictorTherache/P4_chess_tournament.git
$ cd P4_chess_tournament
$ pip3 install -r requirements.txt 
$ cd Chess_tournament
$ py main.py
```
```
Sur Linux/Mac : 
$ git clone https://github.com/VictorTherache/P4_chess_tournament.git
$ cd P4_chess_tournament
$ cd Chess_tournament
$ pip3 install -r requirements.txt 
$ cd Chess_tournament
$ python main.py
```
## Créer un rapport flake8
***
Pour créer un rapport flake8, tapez la commande ci-dessous dans le dossier P4_chess_tournament:
```
$ flake8 Chess_tournament --format=html --htmldir=flake-report --max-line-lengt=119
```
[Remarque] : flake8 va générer le warning suivant :  invalid escape sequence à cause du texte ASCII contenu dans le fichier Tournamentview.
***
Merci d'avoir téléchargé ce projet :) 
