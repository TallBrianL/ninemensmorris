verbose = False


def play_game(game_instance):
    state_list = []

    while not game_instance.is_game_over():
        game_instance.take_turn()
        if verbose:
            game_instance.display_board()
        state_list.append(game_instance.get_state_num())

    # Game Over
    print('Player', game_instance.current_opponent(), 'has won!!! (game took', len(state_list), 'moves.)')
    winner = game_instance.current_opponent()
    return winner, state_list
