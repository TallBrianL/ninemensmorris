import player
import ninemen


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
    player1 = player.Player('Brian', 'computer', 1, prediction)
    for _ in range(100):
        player2 = player.Player('Dani', 'computer', 2, prediction)
        game_instance = ninemen.NineMenGame(player1, player2)
        winner, state_list = game_instance.play_game()
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
