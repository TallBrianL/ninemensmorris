import random


verbose = False


class Game:
    def __init__(self, p1, p2):
        self.players = (p1, p2)

    def is_game_over(self):
        return True

    def get_valid_moves(self):
        return list()

    def take_turn(self, selected_move):
        return

    def display_board(self):
        return

    def get_state_string(self):
        return

    def play_game(self):
        state_list = []
    
        while not self.is_game_over():
            valid_moves = self.get_valid_moves()
            selected_move = self.select_move(valid_moves)
            self.take_turn(selected_move)
            if verbose:
                print(self)
            state_list.append(self.get_state_string())
    
        # Game Over
        print(self.players[self.winner() -1], 'has won!!! (game took', len(state_list), 'moves.)')
        return self.winner(), state_list

    def select_move(self, valid_moves):
        player = self.players[self.current_player()]
        if player.is_human():
            return self.get_move_human(type, player, valid_moves)
        else:
            return self.get_move_computer(player, valid_moves)

    def get_move_computer(self, player, valid_moves):
        if not player.type == 'learning':
            move_idx = random.randrange(0, len(valid_moves))
        else:
            state = self.get_state_string()
            is_move_valid = False
            while not is_move_valid:
                move_idx = player.prediction(state)
                if move_idx in valid_moves:
                    is_move_valid = True
        return list(valid_moves)[move_idx]

    def get_move_human(self, player, valid_moves):
        self.display_board()
        print('Select from the following valid moves:')
        for i, x in enumerate(valid_moves):
            print(i, x)
        is_move_valid = False
        while not is_move_valid:
            print(player.name, 'Please enter location to ' + type + ':')
            user_input = input()
            if len(user_input) > 0:
                move = ord(user_input[0]) - ord('A')
                if 0 <= move <= 23 and move in valid_moves:
                    is_move_valid = True
        return move