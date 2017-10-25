import random


class Player:
    def __init__(self):
        self.num_stones_to_play = 9


def is_human(player):
    return False


def get_move(player, valid_moves):
    if is_human(player):
        return get_move_human(player, valid_moves)
    else:
        return get_move_computer(valid_moves)


def get_move_computer(valid_moves):
    is_move_valid = False
    while not is_move_valid:
        move = random.randint(0, 23)
        if move in valid_moves:
            is_move_valid = True
    return move


def get_move_human(player, valid_moves):
    is_move_valid = False
    while not is_move_valid:
        print('Player', player, 'please enter location to MOVE to:')
        user_input = input()
        if len(user_input) > 0:
            move = ord(user_input[0]) - ord('A')
            if 0 <= move <= 23 and move in valid_moves:
                is_move_valid = True
    return move


class NineMenGame:
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

    def find_row_and_col(self, pos):
        row = ([any([y == pos for y in x]) for x in self.rows]).index(True)
        col = ([any([y == pos for y in x]) for x in self.cols]).index(True)
        return row, col

    def is_triple_match(self, list_of_3):
        return self.board[list_of_3[0]] == self.board[list_of_3[1]] and \
               self.board[list_of_3[0]] == self.board[list_of_3[2]]

    def __init__(self):
        self.board = [0 for _ in range(ord('A'), ord('A') + 8 * 3)]
        self.player_to_move = 0
        self.players = (Player(), Player())
        print('board init')

    def display_board(self):
        print('')
        print('It is', self.current_player(), 'turn to play:')
        letter_board = [chr(x[0] + ord('A')) if x[1] == 0 else x[1] for x in enumerate(self.board)]
        letter_board = ['.' if x[1] == 0 else x[1] for x in enumerate(self.board)]
        print('Stones to place, player 1:', self.players[0].num_stones_to_play,
              'player 2:', self.players[1].num_stones_to_play)
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
        move = get_move(self.current_player(), self.get_stones(self.current_opponent()))
        print('====PLAYER', self.current_player(), 'captures piece', move, '!====')
        self.board[move] = 0

    def new_line_created(self, move):
        row, col = self.find_row_and_col(move)
        return self.is_triple_match(self.rows[row]) or self.is_triple_match(self.cols[col])

    def place_piece(self):
        move = get_move(self.current_player(), self.get_open_locations())
        self.board[move] = self.current_player()
        if self.new_line_created(move):
            self.capture_piece()
        self.players[self.player_to_move].num_stones_to_play -= 1
        self.player_to_move = self.player_to_move ^ 1

    def make_move(self):
        valid_moves = []
        while valid_moves == []:
            stone = get_move(self.current_player(), self.get_stones(self.current_player()))
            valid_moves = self.get_valid_moves([stone])
        move = get_move(self.current_player(), valid_moves)
        self.board[move] = self.current_player()
        self.board[stone] = 0
        if self.new_line_created(move):
            self.capture_piece()
        print('Player', self.current_player(), 'moved from', stone, 'to', move, '.')
        self.player_to_move = self.player_to_move ^ 1

    def get_stones(self, player):
        return [x[0] for x in enumerate(self.board) if x[1] == player]

    def get_open_locations(self):
        return [x[0] for x in enumerate(self.board) if x[1] == 0]

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

    def get_valid_moves(self, stones=None):
        moves = set()
        if len(self.get_stones(self.current_player())) > 3:
            if stones is None:
                stones = self.get_stones(self.current_player())
            for stone in stones:
                row, col = self.find_row_and_col(stone)
                moves |= self.get_moves(self.rows[row], stone)
                moves |= self.get_moves(self.cols[col], stone)
            valid_moves = [move for move in moves if self.board[move] == 0]
        else:
            valid_moves = self.get_open_locations()
        return valid_moves

    def has_lost(self):
        stones = self.get_stones(self.current_player())
        num_stones = len(stones)
        moves = self.get_valid_moves()
        num_moves = len(moves)
        return num_stones < 3 or num_moves == 0

    def play_game(self):
        while self.players[self.player_to_move].num_stones_to_play > 0:
            self.display_board()
            self.place_piece()
        num_moves = 0
        while not self.has_lost():
            self.display_board()
            self.make_move()
            num_moves += 1
        print('Player', self.current_player(), 'has lost :(')
        print('Player', self.current_opponent(), 'has won!!! (game took', num_moves, 'moves.)')


print("Let's Play")
game1 = NineMenGame()
game1.play_game()
print("All Done")
