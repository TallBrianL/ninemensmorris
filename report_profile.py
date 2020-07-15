import cProfile
import train_state_dictionary
from games import tictactoe
from games import ninemen

#game = tictactoe.TicTacToe
game = ninemen.NineMenGame

pr = cProfile.Profile()
pr.enable()

train_state_dictionary.train_infinitely(game, 30)

pr.disable()

pr.print_stats(sort='time')
