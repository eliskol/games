import sys
sys.path.insert(1, sys.path[0].replace('tests', 'games/connect-four'))
sys.path.insert(1, sys.path[0].replace(
    'tests', 'games/connect-four/celeste-strat'))
sys.path.insert(1, sys.path[0].replace(
    'tests', 'games/connect-four/jeff-strat'))
from random_heuristic_strategy import RandomHeuristicStrategy
from input_player import InputPlayer
from last_minute_player import LastMinutePlayer
from heuristic_minimax_strategy import HeuristicMinimaxStrategy
from christine import CustomPlayer
from custom_strat import CustomStrat
from random_player import RandomPlayer
from connect_four import Game
from predefined_strat import PredefinedPlayer
from c_four_minimax import minimaxHeuristic
import random

end_game = None

toLog = True

first_player = HeuristicMinimaxStrategy(5)
# second_player = HeuristicMinimaxStrategy(5)

# trying to figure out why predefined player wins here
# thinking its bc minimax values are off

outcomes = {'Tie': 0, 'c': 0, 'r': 0}
for i in range(2):
    if i % 2 == 0:
        second_player = minimaxHeuristic(2, 3)
        game = Game(first_player, second_player)
        game.run(log=toLog)
        end_game = game.board
        player_order = {'Tie': 'Tie', 1: 'c', 2: 'r'}
    elif i % 2 == 1:
        second_player = minimaxHeuristic(1, 3)
        game = Game(second_player, first_player)
        game.run(log=toLog)
        # assert game.board == end_game
        player_order = {'Tie': 'Tie', 1: 'r', 2: 'c'}
    outcomes[player_order[game.winner]] += 1
    print('game number', i + 1, 'finished')
print(outcomes)
# comment phase
