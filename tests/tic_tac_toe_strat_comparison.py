import sys
import time
sys.path.insert(1, sys.path[0].replace('tests', 'games/tic-tac-toe'))

from tic_tac_toe import Game
from player import Player
from random_player import RandomPlayer
from custom_strat import strategy as elias_strat
from jeff import *
from ben import ben_strat
from celeste import *
from christine import *
from minimax_strategy import MinimaxStrategy
from heuristic_minimax_strategy import HeuristicMinimaxStrategy


random_player = RandomPlayer()
elias_player = Player(elias_strat)
jeff_player = Player(jeff_strat)
ben_player = Player(ben_strat)
celeste_player = Player(celeste_strat)
christine_player = Player(christine_strat)
bruh = MinimaxStrategy()
bruh2 = MinimaxStrategy()

outcomes = {'Tie': 0, 1: 0, 2: 0}
for i in range(50):
    heuristic_minimax_player = HeuristicMinimaxStrategy(2)
    game = Game(heuristic_minimax_player, random_player)
    game.run()
    outcomes[game.winner] += 1
print(outcomes)


# start_time = time.time()
# outcomes = {'Tie': 0, 'me': 0, 'jeff': 0}
# for i in range(100000):
#     if i % 2 == 0:
#         game = Game(my_player, jeff_player)
#         player_order = {'Tie': 'Tie', 1: 'me', 2: 'jeff'}
#     else:
#         game = Game(jeff_player, my_player)
#         player_order = {'Tie': 'Tie', 1: 'jeff', 2: 'me'}

#     game.run(log=False)
#     outcomes[player_order[game.winner]] += 1
#     if i % 1000 == 0:
#         print(i, time.time() - start_time)
#         start_time = time.time()
# print(outcomes)


# start_time = time.time()
# outcomes = {'Tie': 0, 'me': 0, 'rand': 0}
# for i in range(100000):
#     if i % 2 == 0:
#         game = Game(my_player, random_player)
#         player_order = {'Tie': 'Tie', 1: 'me', 2: 'rand'}
#     else:
#         game = Game(random_player, my_player)
#         player_order = {'Tie': 'Tie', 1: 'rand', 2: 'me'}

#     game.run(log=False)
#     outcomes[player_order[game.winner]] += 1
#     if i % 1000 == 0:
#         print(i, time.time() - start_time)
#         start_time = time.time()
# print(outcomes)
