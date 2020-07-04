import cProfile
import train_state_dictionary


pr = cProfile.Profile()
pr.enable()

train_state_dictionary.train_infinitely(2000)

pr.disable()

pr.print_stats(sort='time')
