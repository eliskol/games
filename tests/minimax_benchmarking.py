import sys
sys.path.insert(1, sys.path[0].replace('tests', 'games/tic-tac-toe'))

from minimax_strategy import MinimaxStrategy

times = []
for i in range(100):
    print(i)
    bruh = MinimaxStrategy()
    times.append(bruh.time)
print(sum(times) / len(times))