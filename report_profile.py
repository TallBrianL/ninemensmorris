import cProfile
import train_infinitely


pr = cProfile.Profile()
pr.enable()

train_infinitely.train_infinitely()

pr.disable()

pr.print_stats(sort='time')
