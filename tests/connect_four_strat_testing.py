import sys
sys.path.insert(1, sys.path[0].replace('tests', 'games/connect-four'))
sys.path.insert(1, sys.path[0].replace(
    'tests', 'games/connect-four/celeste-strat'))
sys.path.insert(1, sys.path[0].replace(
    'tests', 'games/connect-four/jeff-strat'))
import random
from c_four_minimax import minimaxHeuristic
from predefined_strat import PredefinedPlayer
from connect_four import Game
from random_player import RandomPlayer
from custom_strat import CustomStrat
from christine import CustomPlayer
from heuristic_minimax_strategy import HeuristicMinimaxStrategy
from last_minute_player import LastMinutePlayer
from input_player import InputPlayer
from random_heuristic_strategy import RandomHeuristicStrategy

end_game = None

toLog = True

first_player = HeuristicMinimaxStrategy(5, True)
# second_player = RandomPlayer()

outcomes = {'Tie': 0, 'c': 0, 'r': 0}
for i in range(2):
    if i % 2 == 0:
        second_player = minimaxHeuristic(2, 5)
        game = Game(first_player, second_player)
        game.run(log=toLog)
        end_game = game.board
        player_order = {'Tie': 'Tie', 1: 'c', 2: 'r'}
    elif i % 2 == 1:
        second_player = minimaxHeuristic(1, 5)
        game = Game(second_player, first_player)
        game.run(log=toLog)
        # assert game.board == end_game
        player_order = {'Tie': 'Tie', 1: 'r', 2: 'c'}
    outcomes[player_order[game.winner]] += 1
    print('game number', i + 1, 'finished')
print(outcomes)
# comment phase
