from tinydb import TinyDB, Query
from Models import Player

player = Player()

db = TinyDB('db.json')
User = Query()
player_table = db.table('player_table')

# player_table.insert({'first_name': 'victor', 'last_name': 'therache', 
#                      'age': 23, 'gender': 'male', 'rank': 1300})
# player_table.insert({'first_name': 'johnathan', 'last_name': 'putchine', 
#                      'age': 28, 'gender': 'male', 'rank': 1100})
# player_table.insert({'first_name': 'Josephine', 'last_name': 'Mithey', 
#                      'age': 23, 'gender': 'female', 'rank': 1800})
# player_table.insert({'first_name': 'Dominique', 'last_name': 'Bleu', 
#                      'age': 33, 'gender': 'male', 'rank': 3000})
# player_table.insert({'first_name': 'Vincent', 'last_name': 'Dequerio', 
#                      'age': 58, 'gender': 'male', 'rank': 1500})
# player_table.insert({'first_name': 'Elias', 'last_name': 'Velipini', 
#                      'age': 17, 'gender': 'male', 'rank': 900})
# player_table.insert({'first_name': 'Catherine', 'last_name': 'Solaire', 
#                      'age': 48, 'gender': 'female', 'rank': 1250})
# player_table.insert({'first_name': 'Zlatan', 'last_name': 'Ibrahimovic', 
#                      'age': 36, 'gender': 'male', 'rank': 1100})
            