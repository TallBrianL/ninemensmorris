import random
import math


class Player:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def select_move(self, game):
        valid_moves = game.get_valid_moves()
        return valid_moves[0]


class Debug(Player):
    def select_move(self, game):
        print(game)
        valid_moves = game.get_valid_moves()
        print('Select from the following valid moves:')
        for i, x in enumerate(valid_moves):
            print(i, x)
        move_idx = -1
        while move_idx not in range(len(valid_moves)):
            try:
                print(self.name, ' please select move by index:')
                move_idx = int(input())
            except:
                move_idx = -1
        return valid_moves[move_idx]


class Human(Player):
    def select_move(self, game):
        return game.get_human_move(self.name)


class PickFirstMoveComputer(Player):
    def select_move(self, game):
        valid_moves = game.get_valid_moves()
        return valid_moves[0]


class TrainedComputer(Player):
    def __init__(self, name, model, randomness):
        self.model = model
        self.randomness = randomness
        Player.__init__(self, name)

    def select_move(self, game):
        valid_moves = game.get_valid_moves()
        best_score = 1
        best_move = valid_moves[0]
        for move in valid_moves:
            state = game.get_state_num_after_move(move)
            try:
                modeled_score = abs(self.model[state[0]][0])
            except:
                modeled_score = .5
            modeled_score = modeled_score + \
                            (random.random() - .5) / .5 * self.randomness
            if modeled_score < best_score:
                best_score = modeled_score
                best_move = move
        return best_move


class RandomComputer(Player):
    def select_move(self, game):
        valid_moves = game.get_valid_moves()
        move_idx = random.randrange(0, len(valid_moves))
        return valid_moves[move_idx]
