import sys
import time
sys.path.insert(1, sys.path[0].replace('tests', 'games/tic-tac-toe'))

from tic_tac_toe import Game
from custom_strat import strategy
from jeff import *
from player import Player
from random_player import RandomPlayer

my_player = Player(strategy)
jeff_player = Player(jeff_strat)
random_player = RandomPlayer()

start_time = time.time()
outcomes = {'Tie': 0, 'me': 0, 'jeff': 0}
for i in range(100000):
    if i % 2 == 0:
        game = Game(my_player, jeff_player)
        player_order = {'Tie': 'Tie', 1: 'me', 2: 'jeff'}
    else:
        game = Game(jeff_player, my_player)
        player_order = {'Tie': 'Tie', 1: 'jeff', 2: 'me'}

    game.run(log=False)
    outcomes[player_order[game.winner]] += 1
    if i % 1000 == 0:
        print(i, time.time() - start_time)
        start_time = time.time()
print(outcomes)


start_time = time.time()
outcomes = {'Tie': 0, 'me': 0, 'rand': 0}
for i in range(100000):
    if i % 2 == 0:
        game = Game(my_player, random_player)
        player_order = {'Tie': 'Tie', 1: 'me', 2: 'rand'}
    else:
        game = Game(random_player, my_player)
        player_order = {'Tie': 'Tie', 1: 'rand', 2: 'me'}

    game.run(log=False)
    outcomes[player_order[game.winner]] += 1
    if i % 1000 == 0:
        print(i, time.time() - start_time)
        start_time = time.time()
print(outcomes)
