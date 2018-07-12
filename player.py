import random


class Player:
    def __init__(self, name, type, number):
        self.name = name
        self.type = type
        self.number = number

    def is_human(self):
        return self.type == 'human'

    def get_move(self, valid_moves):
        if self.is_human():
            return self.get_move_human(valid_moves)
        else:
            return self.get_move_computer(valid_moves)

    def get_move_computer(self, valid_moves):
        is_move_valid = False
        while not is_move_valid:
            move = random.randint(0, 23)
            if move in valid_moves:
                is_move_valid = True
        return move

    def get_move_human(self, player, valid_moves):
        is_move_valid = False
        while not is_move_valid:
            print('Player', player, 'please enter location to MOVE to:')
            user_input = input()
            if len(user_input) > 0:
                move = ord(user_input[0]) - ord('A')
                if 0 <= move <= 23 and move in valid_moves:
                    is_move_valid = True
        return move


