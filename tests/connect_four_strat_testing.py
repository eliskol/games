import random
import sys
sys.path.insert(1, sys.path[0].replace('tests', 'games/connect-four'))

from connect_four import Game
from random_player import RandomPlayer
from custom_strat import CustomStrat
from christine import CustomPlayer
from heuristic_minimax_strategy import HeuristicMinimaxStrategy
from last_minute_player import LastMinutePlayer
from input_player import InputPlayer

toLog = False
random_player = RandomPlayer()
random_heuristic_player = HeuristicMinimaxStrategy(4, True)
last_minute_player = LastMinutePlayer()
custom_player = HeuristicMinimaxStrategy(3, False)
custom_player2 = HeuristicMinimaxStrategy(2, False)
input_player = InputPlayer()


outcomes = {'Tie': 0, 'c': 0, 'r': 0}
for i in range(100):
    if i % 2 == 0:
        game = Game(custom_player, custom_player2)
        game.run(log=toLog)
        player_order = {'Tie': 'Tie', 1: 'c', 2: 'r'}
    elif i % 2 == 1:
        game = Game(custom_player2, custom_player)
        game.run(log=toLog)
        player_order = {'Tie': 'Tie', 1: 'r', 2: 'c'}
    outcomes[player_order[game.winner]] += 1
    print('game number', i + 1, 'finished')
print(outcomes)
# comment phase
