import player
import ninemen
import pickle
import time

def print_to_file(file, state_list, winner):
    with open(file, 'a') as f:
        for state in state_list:
            f.write(str(state) + ' ' +
                    # str(state.num_stones_to_play) + ' ' +
                    str(winner) + '\n')


def run_infinitely():
    start_time = time.time()
    file = "output.txt"
    print("Let's Play")
    try:
        prediction = pickle.load(open("save.p", "rb"))
    except:
        prediction = dict()
    while True:
        batch_time = time.time()
        player1 = player.Player('Brian', 'computer', 1, prediction)
        player2 = player.Player('Dani', 'computer', 2, prediction)
        players = (player1, player2)
        for iter in range(1000):
            game_instance = ninemen.NineMenGame(player1, player2)
            winner, state_list = game_instance.play_game()
            #print(players[winner-1], 'has won!!! (game took', len(state_list), 'moves.)')
            #print_to_file(file, state_list, winner)
            for state in state_list:
                # print(state)
                if state in prediction:
                    val, count = prediction[state]
                    prediction[state] = (val * count + winner) / (count + 1), count + 1
                else:
                    prediction[state] = (winner, 1)
        print("pickling...")
        pickle.dump(prediction, open( "save.p", "wb" ) )
        print("...pickled")
        print(round(time.time() - start_time), "seconds", round(time.time() - batch_time), "seconds")


run_infinitely()
