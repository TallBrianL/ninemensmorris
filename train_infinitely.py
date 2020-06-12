import player
import ninemen
import pickle
import time
import os


def train_infinitely():
    iterations = 1000
    start_time = time.time()
    save_file = "save.p"
    print("Let's Play")
    try:
        prediction = pickle.load(open(save_file, "rb"))
    except:
        print('cannot open', save_file)
        print('creating a new prediction dictionary')
        prediction = dict()
    while True:
        batch_time = time.time()
        player1 = player.RandomComputer('Brian')
        player2 = player.RandomComputer('Dani')
        for _ in range(iterations):
            game_instance = ninemen.NineMenGame(player1, player2)
            winner, state_list = game_instance.play_game()
            for state in state_list:
                if state in prediction:
                    val, count = prediction[state]
                    prediction[state] = (val * count + winner) / (count + 1), count + 1
                else:
                    prediction[state] = (winner, 1)
        print("pickling...")
        pickle.dump(prediction, open(save_file, "wb"))
        print("...pickled", save_file, os.stat(save_file).st_size / 1e6, "MB")
        print(round(time.time() - start_time), "seconds", round(time.time() - batch_time), "seconds")


if __name__ == "__main__":
    train_infinitely()
