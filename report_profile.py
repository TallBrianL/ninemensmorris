import cProfile
import train_infinitely


pr = cProfile.Profile()
pr.enable()

train_infinitely.train_infinitely(200)

pr.disable()

pr.print_stats(sort='time')
