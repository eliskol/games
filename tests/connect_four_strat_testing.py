from random import Random, random
import sys
sys.path.insert(1, sys.path[0].replace('tests', 'games/connect-four'))

from connect_four import Game
from random_player import RandomPlayer
from custom_strat import CustomStrat
from christine import CustomPlayer


random_player = RandomPlayer()
custom_player = CustomStrat()
outcomes = {'Tie': 0, 'c': 0, 'r': 0}
for i in range(10000):
    if i % 2 == 0:
        game = Game(custom_player, random_player)
        game.run()
        player_order = {'Tie': 'Tie', 1: 'c', 2: 'r'}
    elif i % 2 == 1:
        game = Game(random_player, custom_player)
        game.run()
        player_order = {'Tie': 'Tie', 1: 'r', 2: 'c'}
    outcomes[player_order[game.winner]] += 1
print(outcomes)