import cProfile
import train_state_dictionary
from games import tictactoe

game = tictactoe.TicTacToe

pr = cProfile.Profile()
pr.enable()

train_state_dictionary.train_infinitely(game, float('inf'))

pr.disable()

pr.print_stats(sort='time')
