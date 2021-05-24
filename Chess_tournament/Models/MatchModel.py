from tinydb import TinyDB, Query


class Match(object):
    """
    Match model, create, read, update or delete data from the match
    table
    """
    def __init__(self):
        """
        Constructor of the class
        """
        self.db = TinyDB('Models/db.json')
        self.first_round = self.db.table('first_round')
        self.query = Query()

    def get_first_round(self):
        """
        Return each matchs of the first round
        """
        return self.first_round.iter()
