from game import Game
import sys


class NineMenGame(Game):
    class Move:
        def __init__(self, old_pos, new_pos, capture):
            self.old_pos = old_pos
            self.new_pos = new_pos
            self.capture = capture

        def __str__(self):
            return str([self.old_pos, self.new_pos, self.capture])

        def __cmp__(self, other):
            return self.old_pos == other.old_pos and self.new_pos == other.new_pos and self.capture == other.capture

        def __eq__(self, other):
            return self.old_pos == other.old_pos and self.new_pos == other.new_pos and self.capture == other.capture

    board_ref = ["A --- B --- C",
                 "| D - E - F |",
                 "| | G H I | |",
                 "J K L   M N O",
                 "| | P Q R | |",
                 "| S - T - U |",
                 "V --- W --- X"]

    rows = [(0,          1,          2),
                (3,      4,     5),
                     (6, 7, 8),
            (9, 10, 11),   (12, 13, 14),
                    (15, 16, 17),
               (18,      19,   20),
            (21,         22,        23)]

    cols = [(0,        9,         21),
               (3,    10,     18),
                  (6, 11, 15),
            (1, 4, 7),   (16, 19, 22),
                  (8, 12, 17),
               (5,    13,     20),
            (2,       14,         23)]

    def __init__(self, p1, p2):
        super().__init__(p1, p2)

        # board = 0 for empty, 1 for player0, 2 for player1
        self.board = [0 for _ in range(8 * 3)]

        # Player to move, 0 based
        self.player_to_move = 0

        self.num_stones_to_play = [9, 9]

    @staticmethod
    def __flip_board(board):
        board[0], board[2] = board[2], board[0]
        board[3], board[5] = board[5], board[3]
        board[6], board[8] = board[8], board[6]
        board[9:14] = reversed(board[9:14])
        board[15], board[17] = board[17], board[15]
        board[18], board[20] = board[20], board[18]
        board[21], board[23] = board[23], board[21]

    @staticmethod
    def __rotate_board(board):
        board[0], board[21], board[23], board[2] = board[21], board[23], board[2], board[0]
        board[1], board[9], board[22], board[14] = board[9], board[22], board[14], board[1]
        board[3], board[18], board[20], board[5] = board[18], board[20], board[5], board[3]
        board[4], board[10], board[19], board[13] = board[10], board[19], board[13], board[4]
        board[6], board[15], board[17], board[8] = board[15], board[17], board[8], board[6]
        board[7], board[11], board[16], board[12] = board[11], board[16], board[12], board[7]

    def is_game_over(self):
        if self.__has_less_than_3_stones():
            return True
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return True

    def get_valid_moves(self):
        stones = self.__get_stone_locations(self.player_to_move)
        valid_moves = list()

        if self.num_stones_to_play[self.player_to_move]:
            for i, v in enumerate(self.board):
                if v == 0:
                    valid_moves.append(self.Move(-1, i, -1))

        elif len(stones) > 3:
            # Regular movement phase
            for stone in stones:
                for move in self.__get_all_moves_for_a_stone(stone):
                    if self.board[move] == 0:
                        valid_moves.append(self.Move(stone, move, -1))
        else:
            # Flying Dutchmen Phase
            for move in self.__get_open_locations():
                for stone in stones:
                    valid_moves.append(self.Move(stone, move, -1))

        valid_moves_with_captures = list()
        for move in valid_moves:
            if self.__is_new_line_created(move, self.player_to_move + 1):
                for capture in self.__get_capturable_stones():
                    valid_moves_with_captures.append(self.Move(move.old_pos, move.new_pos, capture))
            else:
                valid_moves_with_captures.append(move)
        return valid_moves_with_captures

    def __get_capturable_stones(self):
        captures_not_in_mill = list()
        for capture in self.__get_stone_locations(self.__current_opponent()):
            row, col = self.__find_row_and_col(capture)
            is_in_mill = self.__is_triple_match(self.rows[row]) or self.__is_triple_match(self.cols[col])
            if not is_in_mill:
                captures_not_in_mill.append(capture)
        if not captures_not_in_mill:
            captures_not_in_mill = self.__get_stone_locations(self.__current_opponent())
        return captures_not_in_mill

    def get_human_move(self, player_name):
        valid_moves = self.get_valid_moves()

        print(self)
        if self.num_stones_to_play[self.player_to_move]:
            old_pos = -1
            while True:
                user_input = input(player_name + ', place a stone on the board (q to quit, r to redo):')
                if user_input == 'q':
                    sys.exit('User quits')
                elif len(user_input) == 1:
                    new_pos = ord(user_input[0]) - ord('A')
                    if new_pos in [x.new_pos for x in valid_moves]:
                        break
                    else:
                        print('invalid move, please try again')
        else:
            while True:
                user_input = input(player_name + ', choose a stone to move (q to quit):')
                if user_input == 'q':
                    sys.exit('User quits')
                elif len(user_input) == 1:
                    old_pos = ord(user_input[0]) - ord('A')
                    if old_pos in [x.old_pos for x in valid_moves]:
                        break
                    else:
                        print('invalid move, please try again')
            while True:
                user_input = input(player_name + ', choose where to move selected stone (q to quit):')
                if user_input == 'q':
                    sys.exit('User quits')
                elif len(user_input) == 1:
                    new_pos = ord(user_input[0]) - ord('A')
                    if (old_pos, new_pos) in [(x.old_pos, x.new_pos) for x in valid_moves]:
                        break
                    else:
                        print('invalid move, please try again')
        if self.__is_new_line_created(self.Move(old_pos, new_pos, -1), self.player_to_move + 1):
            while True:
                user_input = input(player_name + ', choose which stone to capture (q to quit):')
                if user_input == 'q':
                    sys.exit('User quits')
                elif len(user_input) == 1:
                    capture = ord(user_input[0]) - ord('A')
                    if (old_pos, new_pos, capture) in [(x.old_pos, x.new_pos, x.capture) for x in valid_moves]:
                        break
                    else:
                        print('invalid move, please try again')
        else:
            capture = -1

        return self.Move(old_pos, new_pos, capture)

    def get_canonical_state(self):
        stones_to_play = self.num_stones_to_play[:]
        board = self.board[:]
        if not self.player_to_move:
            stones_to_play.reverse()
            for x in [i for i, v in enumerate(board) if v == 1]:
                board[x] = 2
            for x in [i for i, v in enumerate(board) if v == 2]:
                board[x] = 1

        best_board = board[:]
        for _1 in range(2):
            for _2 in range(4):
                self.__rotate_board(board)
                if board < best_board:
                    best_board = board[:]
            self.__flip_board(board)
        return best_board, stones_to_play

    def get_state_num(self):
        canonical_board, canonical_stones = self.get_canonical_state()
        board_state = sum([x*y for x, y in zip(canonical_board, self.POWERS_OF_3)])
        state_num = board_state * 100 + canonical_stones[0] * 10 + canonical_stones[1]
        return [state_num, self.player_to_move]

    POWERS_OF_3 = [3**(23 - i) for i in range(24)]

    def get_state_num_after_move(self, move):
        self.take_action(move)
        state_num = self.get_state_num()
        self.invert_action(move)
        return state_num

    def __str__(self):
        letter_board = ['.' if x[1] == 0 else str(x[1]) for x in enumerate(self.board)]
        output_header = ['It\'s ' + self.players[self.player_to_move].name + '\'s turn to play:',
                         self.players[0].name + ' is 1 and has ' + str(self.num_stones_to_play[0]) + ' stones to place',
                         self.players[1].name + ' is 2 and has ' + str(self.num_stones_to_play[1]) + ' stones to place']
        output_board = [letter_board[0] + ' --- ' + letter_board[1] + ' --- ' + letter_board[2],
                        '| ' + letter_board[3] + ' - ' + letter_board[4] + ' - ' + letter_board[5] + ' |',
                        '| | ' + letter_board[6] + ' ' + letter_board[7] + ' ' + letter_board[8] + ' | |',
                        letter_board[9] + ' ' + letter_board[10] + ' ' + letter_board[11] + '   ' +
                        letter_board[12] + ' ' + letter_board[13] + ' ' + letter_board[14],
                        '| | ' + letter_board[15] + ' ' + letter_board[16] + ' ' + letter_board[17] + ' | |',
                        '| ' + letter_board[18] + ' - ' + letter_board[19] + ' - ' + letter_board[20] + ' |',
                        letter_board[21] + ' --- ' + letter_board[22] + ' --- ' + letter_board[23]]
        return '\n'.join(output_header + [x + '   ' + y for x, y in zip(output_board, self.board_ref)])

    def __find_row_and_col(self, pos):
        rows = [i for i, x in enumerate(self.rows) if pos in x]
        cols = [i for i, x in enumerate(self.cols) if pos in x]
        return rows[0], cols[0]

    def current_player(self):
        return int(self.player_to_move)

    def winner(self):
        return self.__current_opponent()

    def __current_opponent(self):
        return int((self.player_to_move ^ 1))

    def __is_triple_match(self, list_of_3):
        return self.board[list_of_3[0]] == self.board[list_of_3[1]] and \
               self.board[list_of_3[0]] == self.board[list_of_3[2]]

    def __is_new_line_created(self, move, new_val):
        row, col = self.__find_row_and_col(move.new_pos)
        if move.old_pos != -1:
            self.board[move.old_pos] = 0
        self.board[move.new_pos] = new_val
        is_new_line_created = self.__is_triple_match(self.rows[row]) or self.__is_triple_match(self.cols[col])
        self.board[move.new_pos] = 0
        if move.old_pos != -1:
            self.board[move.old_pos] = new_val
        return is_new_line_created

    def take_action(self, selected_move):

        if selected_move.old_pos == -1:
            # Placing a new stone, remove a stone from the store
            self.num_stones_to_play[self.player_to_move] -= 1
        else:
            # Moving a stone, remove from move origin
            self.board[selected_move.old_pos] = 0

        self.board[selected_move.new_pos] = self.current_player() + 1

        if selected_move.capture != -1:
            # Capture
            self.board[selected_move.capture] = 0

        self.player_to_move = self.player_to_move ^ 1
        return True

    def invert_action(self, selected_move):
        self.player_to_move = self.player_to_move ^ 1

        if selected_move.old_pos == -1:
            # Placing a new stone, remove a stone from the store
            self.num_stones_to_play[self.player_to_move] += 1
        else:
            # Moving a stone, remove from move origin
            self.board[selected_move.old_pos] = self.current_player() + 1

        self.board[selected_move.new_pos] = 0

        if selected_move.capture != -1:
            # Capture
            self.board[selected_move.capture] = self.__current_opponent() + 1

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
        moves |= self.__get_moves(self.rows[row], stone)
        moves |= self.__get_moves(self.cols[col], stone)
        return moves

    @staticmethod
    def __get_moves(positions, stone):
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
