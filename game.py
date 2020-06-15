verbose = False


class Game:
    def __init__(self, p1, p2):
        self.players = (p1, p2)

    def is_game_over(self):
        return True

    def get_valid_moves(self):
        return list()

    def take_action(self, selected_move):
        return

    def display_board(self):
        return

    def get_state_string(self):
        return

    def winner(self):
        return -1

    def current_player(self):
        return self.players[0]

    def play_game(self):
        state_list = []
        move_count = 0
    
        while not self.is_game_over() and move_count < 100:
            valid_moves = self.get_valid_moves()
            selected_move = self.players[self.current_player()].select_move(self)
            self.take_action(selected_move)
            if verbose:
                print(self)
            state_list.append(self.get_state_string())
            move_count += 1
    
        # Game Over
        return self.winner(), state_list
