import player
import game

verbose = False


def play_game(player1, player2):
    game_instance = game.NineMenGame(player1, player2)
    state_list = []

    # Original Placing Stones Phase
    while game_instance.num_stones_to_play[game_instance.player_to_move] > 0:
        if verbose:
            game_instance.display_board()
        game_instance.place_piece()
        state_list.append(game_instance.get_state_num())

    # Secondary Moving Stones Phase
    while game_instance.make_move():
        if verbose:
            game_instance.display_board()
        state_list.append(game_instance.get_state_num())

    # Game Over
    print('Player', game_instance.current_opponent(), 'has won!!! (game took', len(state_list), 'moves.)')
    winner = game_instance.current_opponent()
    return winner, state_list


def print_to_file(file, state_list, winner):
    with open(file, 'a') as f:
        for state in state_list:
            f.write(str(state) + ' ' +
                    # str(state.num_stones_to_play) + ' ' +
                    str(winner) + '\n')


def run_many_games():
    file = "output.txt"
    print("Let's Play")
    prediction = dict()
    p1 = player.Player('Brian', 'computer', 1, prediction)
    for _ in range(100):
        p2 = player.Player('Dani', 'computer', 2, prediction)
        winner, state_list = play_game(p1, p2)
        print_to_file(file, state_list, winner)
        for state in state_list:
            # print(state)
            if state in prediction:
                val, count = prediction[state]
                prediction[state] = (val * count + winner) / (count + 1), count + 1
            else:
                prediction[state] = (winner, 1)
    print("All Done")


run_many_games()
