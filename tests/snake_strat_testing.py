import sys

sys.path.insert(1, sys.path[0].replace("tests", "games/snake"))

from snake import Game
from ben import BenStrat
from basic_winner_strat import Winner as MyStrat


totals = {"score": 0, "moves": 0}
# beginning = time.time()
for i in range(199):
    ben = BenStrat()
    game = Game(ben)
    result = game.run_game(log=True)
    totals["score"] += result["score"]
    totals["moves"] += result["moves"]
    if i % 50 == 0:
        print(i)
# time_taken = time.time() - beginning
# print('total time taken:', time_taken)
# print('avg time per game:', time_taken / 1000)

averages = {"score": totals["score"] / 100, "moves": totals["moves"] / 100}
print(averages)
# print('moves per second:', averages['moves'] / (time_taken / 1000))
