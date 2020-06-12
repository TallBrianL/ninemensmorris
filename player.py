import random


class Player:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def select_move(self, game):
        valid_moves = game.get_valid_moves()
        return valid_moves[0]


class HumanPlayer(Player):
    def select_move(self, game):
        print(game)
        valid_moves, move_type = game.get_valid_moves()
        print('Select from the following valid moves:')
        for i, x in enumerate(valid_moves):
            print(i, x)
        is_move_valid = False
        move = valid_moves[0]
        while not is_move_valid:
            print(self.name, ' please enter location to ' + move_type + ':')
            user_input = input()
            if len(user_input) > 0:
                move = ord(user_input[0]) - ord('A')
                if 0 <= move <= 23 and move in valid_moves:
                    is_move_valid = True
        return move


class PickFirstMove(Player):
    def select_move(self, valid_moves):
        valid_moves = game.get_valid_moves()
        return valid_moves[0]


class TrainedComputer(Player):
    def __init__(self, name, model):
        self.model = model
        Player.__init__(self, name)

    def select_move(self, game):
        valid_moves = game.get_valid_moves()
        best_score = 0
        best_move_idx = -1
        for idx, move in enumerate(valid_moves):
            possible_state = game.take_action(move)
            if self.model[game.get_state_string()] > best_score:
                best_score = self.model[game.get_state_string()]
                best_move_idx = idx
        return valid_moves[best_move_idx]


class RandomComputer(Player):
    def select_move(self, game):
        valid_moves = game.get_valid_moves()
        move_idx = random.randrange(0, len(valid_moves))
        return valid_moves[move_idx]
