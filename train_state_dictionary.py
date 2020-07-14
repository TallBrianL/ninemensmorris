import player
import pickle
import time
import os
from tqdm import tqdm
from games.ninemen import NineMenGame
from games.tictactoe import TicTacToe

def train_infinitely(game, total_iteration_target):
    total_iteration_count = 0
    start_time = time.time()
    save_file = game.game_name + ".pickle"
    print("Let's Play", game.game_name)
    try:
        # prediction is chances the player whose turn it is will win
        prediction = pickle.load(open(save_file, "rb"))
        print('model loaded', end=" ")
    except:
        print('cannot open', save_file)
        print('creating a new prediction dictionary')
        prediction = dict()
    while total_iteration_count < total_iteration_target:
        batch_time = time.time()
        player1 = player.TrainedComputer('Dani', prediction, total_iteration_count)
        player2 = player.RandomComputer('Brian')
        iterations_per_cycle = 1000
        if 0:
            player1 = player.Human('Dani')
            player2 = player.Human('Brian')
            iterations_per_cycle = 1
        print('players loaded', end=" ")
        winner_sum = 0
        winner_tally = {0:0, 1:0, .5:0}
        print('playing games')
        for _ in tqdm(range(iterations_per_cycle)):
            game_instance = game(player1, player2)
            winner_idx, state_list = game_instance.play_game()
            winner_sum += winner_idx
            winner_tally[winner_idx] += 1
            for state, active_player in state_list:
                if winner_idx == .5:
                    score = winner_idx
                else:
                    score = int(winner_idx == active_player)
                if state in prediction:
                    val, count = prediction[state]
                    prediction[state] = (val + score) / 2, count + 1
                else:
                    prediction[state] = (score, 1)
            total_iteration_count += 1
        time.sleep(0.1)
        print("winner tally", winner_tally, end=" ")
        p = [x for x, y in prediction.values()]
        print([len([x for x in p if y[0] < x < y[1]]) for y in [(0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1)]])
        print("pickling...", end="")
        pickle.dump(prediction, open(save_file, "wb"))
        print("pickled", save_file, os.stat(save_file).st_size / 1e6, "MB",
              round(time.time() - start_time), "seconds", round(time.time() - batch_time), "seconds")


if __name__ == "__main__":
    game1 = TicTacToe
    game2 = NineMenGame
    train_infinitely(game2, float('inf'))
