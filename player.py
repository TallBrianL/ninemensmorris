class Player:
    def __init__(self, name, player_type, number, prediction):
        self.name = name
        # should be "human", "learning", or other
        self.type = player_type
        self.number = number
        self.prediction = prediction

    def __str__(self):
        return self.name

    def is_human(self):
        return self.type == 'human'
