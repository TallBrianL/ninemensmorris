from game import Game


class NineMenGame(Game):
    board_ref = '''A --- B --- C
                   | D - E - F |
                   | | G H I | |
                   J K L   M N O
                   | | P Q R | |
                   | S - T - U |
                   V --- W --- X'''

    rows = [(0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (9, 10, 11),
            (12, 13, 14),
            (15, 16, 17),
            (18, 19, 20),
            (21, 22, 23)]

    cols = [(0, 9, 21),
            (3, 10, 18),
            (6, 11, 15),
            (1, 4, 7),
            (16, 19, 22),
            (8, 12, 17),
            (5, 13, 20),
            (2, 14, 23)]

    def __init__(self, p1, p2):
        super().__init__(p1, p2)
        self.board = [0 for _ in range(8 * 3)]
        self.player_to_move = 0
        self.num_stones_to_play = [9, 9]

    def is_game_over(self):
        if self.__has_less_than_3_stones():
            return True
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return True

    def get_valid_moves(self):
        stones = self.__get_stone_locations(self.player_to_move)

        if self.num_stones_to_play[self.player_to_move]:
            valid_moves = [i for i, v in enumerate(self.board) if v == 0]

        elif len(stones) > 3:
            # Regular movement phase
            valid_moves = set()
            for stone in stones:
                for move in self.__get_all_moves_for_a_stone(stone):
                    if self.board[move] == 0:
                        valid_moves.add((stone, move))
        else:
            # Flying Dutchmen Phase
            valid_moves = [(stone, move) for move in self.__get_open_locations() for stone in stones]
        return valid_moves

    def take_turn(self, selected_move):
        if self.num_stones_to_play[self.player_to_move] > 0:
            self.__place_piece(selected_move)
        else:
            self.__make_move(selected_move)

    def get_state_string(self):
        board_state = ''.join(str(x) for x in self.board)
        stones_state = ''.join(str(x) for x in self.num_stones_to_play)
        state_string = str(self.player_to_move) + stones_state + board_state
        return state_string

    def __str__(self):
        letter_board = ['.' if x[1] == 0 else str(x[1]) for x in enumerate(self.board)]
        output_str = 'It\'s ' + self.players[self.player_to_move].name + '\'s turn to play:\n' + \
                     self.players[0].name + ' is 1 and has ' + str(self.num_stones_to_play[0]) + ' stones to place\n' + \
                     self.players[1].name + ' is 2 and has ' + str(self.num_stones_to_play[1]) + ' stones to place\n' + \
                     letter_board[0] + ' --- ' + letter_board[1] + ' --- ' + letter_board[2] + '\n' + \
                     '| ' + letter_board[3] + ' - ' + letter_board[4] + ' - ' + letter_board[5] + ' |' + '\n' + \
                     '| | ' + letter_board[6] + ' ' + letter_board[7] + ' ' + letter_board[8] + ' | |' + '\n' + \
                     letter_board[9] + ' ' + letter_board[10] + ' ' + letter_board[11] + '   ' + \
                     letter_board[12] + ' ' + letter_board[13] + ' ' + letter_board[14] + '\n' + \
                     '| | ' + letter_board[15] + ' ' + letter_board[16] + ' ' + letter_board[17] + ' | |' + '\n' + \
                     '| ' + letter_board[18] + ' - ' + letter_board[19] + ' - ' + letter_board[20] + ' |' + '\n' + \
                     letter_board[21] + ' --- ' + letter_board[22] + ' --- ' + letter_board[23]
        return output_str

    def __find_row_and_col(self, pos):
        row = ([any([y == pos for y in x]) for x in self.rows]).index(True)
        col = ([any([y == pos for y in x]) for x in self.cols]).index(True)
        return row, col

    def __is_triple_match(self, list_of_3):
        return self.board[list_of_3[0]] == self.board[list_of_3[1]] and \
               self.board[list_of_3[0]] == self.board[list_of_3[2]]

    def current_player(self):
        return int(self.player_to_move)

    def winner(self):
        return self.__current_opponent()

    def __current_opponent(self):
        return int((self.player_to_move ^ 1) + 1)

    def __capture_piece(self):
        move = self.select_move(self.__get_stone_locations(self.__current_opponent() - 1))
        self.board[move] = 0

    def __new_line_created(self, move):
        row, col = self.__find_row_and_col(move)
        return self.__is_triple_match(self.rows[row]) or self.__is_triple_match(self.cols[col])

    def __place_piece(self, selected_move):
        self.board[selected_move] = self.current_player() + 1
        if self.__new_line_created(selected_move):
            self.__capture_piece()
        self.num_stones_to_play[self.player_to_move] -= 1
        self.player_to_move ^= 1

    def __make_move(self, selected_move):
        self.board[selected_move[1]] = self.current_player() + 1
        self.board[selected_move[0]] = 0
        if self.__new_line_created(selected_move[1]):
            self.__capture_piece()
        self.player_to_move = self.player_to_move ^ 1
        return True

    # Returns the indices of board locations of player's stones
    def __get_stone_locations(self, player_idx):
        return [x[0] for x in enumerate(self.board) if x[1] == player_idx + 1]

    # Returns the indices of empty board locations
    def __get_open_locations(self):
        return [x[0] for x in enumerate(self.board) if x[1] == 0]

    def __get_all_moves_for_a_stone(self, stone):
        moves = set()
        row, col = self.__find_row_and_col(stone)
        moves |= self.get_moves(self.rows[row], stone)
        moves |= self.get_moves(self.cols[col], stone)
        return moves

    @staticmethod
    def get_moves(positions, stone):
        pos = positions.index(stone)
        moves = set()
        if pos == 0:
            moves.add(positions[1])
        elif pos == 1:
            moves.add(positions[0])
            moves.add(positions[2])
        elif pos == 2:
            moves.add(positions[1])
        return moves

    def __has_less_than_3_stones(self):
        stones = self.__get_stone_locations(self.player_to_move)
        num_stones = len(stones) + self.num_stones_to_play[self.player_to_move]
        return num_stones < 3
