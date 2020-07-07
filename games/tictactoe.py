from game import Game
import sys


class TicTacToe(Game):
    game_name = "TicTacToe"

    board_ref = ["A B C",
                 "D E F",
                 "G H I"]

    rows = [(0, 1, 2),
            (3, 4, 5),
            (6, 7, 8)]

    cols = [(0, 3, 6),
            (1, 4, 7),
            (2, 5, 8)]

    diags = [(0, 4, 8),
             (2, 4, 6)]

    def __init__(self, p1, p2):
        super().__init__(p1, p2)

        # board = 0 for empty, 1 for player0, 2 for player1
        self.board = [0 for _ in range(9)]

        # Player to move, 0 based
        self.player_to_move = 0

    @staticmethod
    def __flip_board(board):
        board[0], board[6] = board[6], board[0]
        board[1], board[7] = board[7], board[1]
        board[2], board[8] = board[8], board[2]

    @staticmethod
    def __rotate_board(board):
        board[0], board[2], board[8], board[6] = board[2], board[8], board[6], board[0]
        board[1], board[5], board[7], board[3] = board[5], board[7], board[3], board[1]

    def is_game_over(self):
        if self.__is_triple_match():
            return True
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return True

    def get_valid_moves(self):
        return self.__get_open_locations()

    def get_human_move(self, player_name):
        valid_moves = self.get_valid_moves()
        print(self)
        while True:
            user_input = input(player_name + ', place a stone on the board (q to quit, r to redo):')
            if user_input == 'q':
                sys.exit('User quits')
            elif len(user_input) == 1:
                new_pos = ord(user_input[0]) - ord('A')
                if new_pos in valid_moves:
                    break
                else:
                    print('invalid move, please try again')
        return new_pos

    def get_canonical_state(self):
        board = self.board[:]
        if not self.player_to_move:
            for x in [i for i, v in enumerate(self.board) if v == 1]:
                board[x] = 2
            for x in [i for i, v in enumerate(self.board) if v == 2]:
                board[x] = 1

        best_board = board[:]
        for _1 in range(2):
            for _2 in range(4):
                self.__rotate_board(board)
                if board < best_board:
                    best_board = board[:]
            self.__flip_board(board)
        #return best_board
        return self.board

    POWERS_OF_3 = [3 ** (9 - i) for i in range(9)]

    def get_state_num(self):
        canonical_board = self.get_canonical_state()
        board_state = sum([x*y for x, y in zip(canonical_board, self.POWERS_OF_3)])
        return [board_state, self.player_to_move]

    def get_state_num_after_move(self, move):
        self.take_action(move)
        state_num = self.get_state_num()
        self.invert_action(move)
        return state_num

    def __str__(self):
        letter_board = ['.' if x == 0 else str(x) for x in self.board]
        output_board = self.board_to_string(letter_board)
        canonical_board = self.board_to_string([str(x) for x in self.get_canonical_state()])
        return '\n'.join([x + '   ' + y + '   ' + z for x, y, z in
                          zip(output_board, self.board_ref, canonical_board)])

    @staticmethod
    def board_to_string(board):
        output_board = [board[0] + board[1] + board[2],
                        board[3] + board[4] + board[5],
                        board[6] + board[7] + board[8]]
        return output_board

    def current_player(self):
        return int(self.player_to_move)

    def winner(self):
        if self.__is_triple_match():
            return self.__current_opponent()
        else:
            return .5

    def __current_opponent(self):
        return int((self.player_to_move ^ 1))

    def __is_triple_match(self):
        for group in self.rows:
            if self.board[group[0]] != 0 and \
                    self.board[group[0]] == self.board[group[1]] and \
                    self.board[group[1]] == self.board[group[2]]:
                return True
        for group in self.cols:
            if self.board[group[0]] != 0 and \
                    self.board[group[0]] == self.board[group[1]] and \
                    self.board[group[1]] == self.board[group[2]]:
                return True
        for group in self.diags:
            if self.board[group[0]] != 0 and \
                    self.board[group[0]] == self.board[group[1]] and \
                    self.board[group[1]] == self.board[group[2]]:
                return True
        return False

    def take_action(self, selected_move):
        self.board[selected_move] = self.current_player() + 1
        self.player_to_move = self.player_to_move ^ 1
        return True

    def invert_action(self, selected_move):
        self.player_to_move = self.player_to_move ^ 1
        self.board[selected_move] = 0
        return True

    # Returns the indices of board locations of player's stones
    def __get_stone_locations(self, player_idx):
        return [x[0] for x in enumerate(self.board) if x[1] == player_idx + 1]

    # Returns the indices of empty board locations
    def __get_open_locations(self):
        return [i for i, x in enumerate(self.board) if x == 0]
