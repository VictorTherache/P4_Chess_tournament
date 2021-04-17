from Joueur import Joueur
import operator

class Tournoi(object):

    def __init__(self):
        pass

    def start(self):
        """
        """
        i = 0
        players_list = []
        print("Tournoi créer")
        response = input("Voulez vous ajouter un joueurs au tournoi ? (o/n) :")
        while response == "o":
            # name = input("Nom du joueur : ")
            i = Joueur()
            # i += 1
            players_list.append(i)
            response = input("Voulez vous ajouter un joueurs au tournoi ? (o/n) :")

    def making_first_round(self):
        """
        Return a list of players pairs for the matches
        """
        match_list = []
        round_nbr = "1"
        if round_nbr == "1":
            victor = Joueur("therache", "victor", "22/08/1997", "m", 1302)
            boris = Joueur("grujdalof", "boris", "12/01/1983", "m", 1102)
            john = Joueur("aaaaaa", "john", "12/01/1983", "m", 2000)
            emma = Joueur("zzzzzz", "emma", "12/01/1983", "f", 2100)
            gwen = Joueur("eeeeee", "gwen", "12/01/1983", "m", 900)
            legolas = Joueur("rrrrrr", "legolas", "12/01/1983", "m", 1002)
            patrick = Joueur("tttttt", "patrick", "12/01/1983", "m", 1513)
            marie = Joueur("yyyyyy", "marie", "12/01/1983", "f", 1700)
            players_list = [victor, boris, john, emma, gwen, legolas, 
                            patrick, marie]
            if len(players_list) % 2 == 0:
                first_half_list = []
                second_half_list = []
                new_list = sorted(players_list, key=operator.attrgetter("rank"), reverse=True)
                for i in range(int((len(new_list)))):
                    if i < int((len(new_list)) / 2):
                        first_half_list.append(new_list[i])
                    else : 
                        second_half_list.append(new_list[i])
                for i in range(int((len(first_half_list)))):
                    match_list.append([first_half_list[i], second_half_list[i]])

                # print(match_and_score_list[0])
                return match_list 

    def making_other_rounds(self, match_list):
        # print(match_list)
        match_and_score_list = []
        match_1 = (match_list[0], 1, 0)
        match_2 = (match_list[1], 0, 1)
        match_3 = (match_list[2], 0.5, 0.5)
        match_4 = (match_list[3], 1, 0)
        match_and_score_list.extend([match_1, match_2, match_3, match_4])
        for i in range(0, len(match_and_score_list)):
            if match_and_score_list[i][1] == 1:
                match_list[i][0].tournament_points += 1
                print(match_list[3][0])



            
t = Tournoi()
match_list = t.making_first_round()
other_round = t.making_other_rounds(match_list)
