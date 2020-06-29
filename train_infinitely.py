import player
import ninemen
import pickle
import time
import os
from tqdm import tqdm
import sys


def train_infinitely(total_iteration_target):
    total_iteration_count = 0
    iterations_per_cycle = 100
    start_time = time.time()
    save_file = "save.p"
    print("Let's Play")
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
        player1 = player.TrainedComputer('Brian', prediction)
        player2 = player.TrainedComputer('Dani', prediction)
        print('players loaded', end=" ")
        winner_sum = 0
        print('playing games')
        for _ in tqdm(range(iterations_per_cycle)):
            game_instance = ninemen.NineMenGame(player1, player2)
            winner_idx, state_list = game_instance.play_game()
            winner_sum += winner_idx
            for state, active_player in state_list:
                score = int(winner_idx == active_player)
                if state in prediction:
                    val, count = prediction[state]
                    prediction[state] = (val * count + score) / (count + 1), count + 1
                else:
                    prediction[state] = (score, 1)
            total_iteration_count += 1
        print("winner ", str(winner_sum / iterations_per_cycle), " in ", str(len(state_list)), " moves; pickling...",
              end="")
        pickle.dump(prediction, open(save_file, "wb"))
        print("pickled", save_file, os.stat(save_file).st_size / 1e6, "MB",
              round(time.time() - start_time), "seconds", round(time.time() - batch_time), "seconds")


if __name__ == "__main__":
    train_infinitely(float('inf'))
