verbose = False


def play_game(game_instance):
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
