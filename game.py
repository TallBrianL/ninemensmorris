import random


class NineMenGame:
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
        self.board = [0 for _ in range(8 * 3)]
        self.player_to_move = 0
        self.players = (p1, p2)
        self.num_stones_to_play = [9, 9]
        # print(self.board_ref)

    def get_state_num(self):
        board_state = sum([x**3 * y for x, y in enumerate(self.board)])
        stones_state = sum([x**10 * y for x, y in enumerate(self.num_stones_to_play)])
        return board_state, stones_state, self.player_to_move

    def find_row_and_col(self, pos):
        row = ([any([y == pos for y in x]) for x in self.rows]).index(True)
        col = ([any([y == pos for y in x]) for x in self.cols]).index(True)
        return row, col

    def is_triple_match(self, list_of_3):
        return self.board[list_of_3[0]] == self.board[list_of_3[1]] and \
               self.board[list_of_3[0]] == self.board[list_of_3[2]]

    def display_board(self):
        print('')
        print('It is', self.current_player(), 'turn to play:')
        # letter_board = [chr(x[0] + ord('A')) if x[1] == 0 else x[1] for x in enumerate(self.board)]
        letter_board = ['.' if x[1] == 0 else x[1] for x in enumerate(self.board)]
        print('Stones to place, player 1:', self.num_stones_to_play[0],
              'player 2:', self.num_stones_to_play[1])
        print(letter_board[0], '---', letter_board[1], '---', letter_board[2])
        print('|', letter_board[3], '-', letter_board[4], '-', letter_board[5], '|')
        print('| |', letter_board[6], letter_board[7], letter_board[8], '| |')
        print(letter_board[9], letter_board[10], letter_board[11], ' ',
              letter_board[12], letter_board[13], letter_board[14])
        print('| |', letter_board[15], letter_board[16], letter_board[17], '| |')
        print('|', letter_board[18], '-', letter_board[19], '-', letter_board[20], '|')
        print(letter_board[21], '---', letter_board[22], '---', letter_board[23])

    def current_player(self):
        return int(self.player_to_move + 1)

    def current_opponent(self):
        return int((self.player_to_move ^ 1) + 1)

    def capture_piece(self):
        move = self.select_move(self.get_stone_locations(self.current_opponent()))
        # print('====PLAYER', self.current_player(), 'captures piece', move, '!====')
        self.board[move] = 0

    def new_line_created(self, move):
        row, col = self.find_row_and_col(move)
        return self.is_triple_match(self.rows[row]) or self.is_triple_match(self.cols[col])

    def place_piece(self):
        #self.display_board()
        move = self.select_move(self.get_open_locations())
        self.board[move] = self.current_player()
        if self.new_line_created(move):
            self.capture_piece()
        self.num_stones_to_play[self.player_to_move] -= 1
        self.player_to_move ^= 1

    def make_move(self):
        if self.has_less_than_3_stones():
            return False
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return False
        move = self.select_move(valid_moves)
        self.board[move[1]] = self.current_player()
        self.board[move[0]] = 0
        if self.new_line_created(move[1]):
            self.capture_piece()
        self.player_to_move = self.player_to_move ^ 1
        return True

    # Returns the indices of board locations of player's stones
    def get_stone_locations(self, player):
        return [x[0] for x in enumerate(self.board) if x[1] == player]

    # Returns the indices of empty board locations
    def get_open_locations(self):
        return [x[0] for x in enumerate(self.board) if x[1] == 0]

    def get_all_moves_for_a_stone(self, stone):
        moves = set()
        row, col = self.find_row_and_col(stone)
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

    def get_valid_moves(self):
        stones = self.get_stone_locations(self.current_player())

        if len(stones) > 3:
            # Regular movement phase
            valid_moves = set()
            for stone in stones:
                for move in self.get_all_moves_for_a_stone(stone):
                    if self.board[move] == 0:
                        valid_moves.add((stone, move))
        else:
            # Flying Dutchmen Phase
            valid_moves = [(stone, move) for move in self.get_open_locations() for stone in stones]
        return valid_moves

    def has_less_than_3_stones(self):
        stones = self.get_stone_locations(self.current_player())
        num_stones = len(stones)
        return num_stones < 3

    def select_move(self, valid_moves):
        player = self.players[self.current_player() - 1]
        if player.is_human():
            return self.get_move_human(type, player, valid_moves)
        else:
            return self.get_move_computer(player, valid_moves)

    def get_move_computer(self, player, valid_moves):
        if not player.type == 'learning':
            move_idx = random.randrange(0, len(valid_moves))
        else:
            state = self.get_state_num()
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
