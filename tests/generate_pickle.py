import sys
sys.path.insert(1, sys.path[0].replace('tests', 'games/connect-four'))
sys.path.insert(1, sys.path[0].replace(
    'tests', 'games/connect-four/celeste-strat'))
sys.path.insert(1, sys.path[0].replace(
    'tests', 'games/connect-four/jeff-strat'))
from random_heuristic_strategy import RandomHeuristicStrategy
from last_minute_player import LastMinutePlayer
from heuristic_minimax_strategy import HeuristicMinimaxStrategy
from random_player import RandomPlayer
from connect_four import Game
from predefined_strat import PredefinedPlayer

# first_player = HeuristicMinimaxStrategy(4, False)
second_player = HeuristicMinimaxStrategy(3, True)
# second_player = PredefinedPlayer([(n + 3) % 7 for n in range(100)])
game = Game(first_player, second_player)
game.run(log=True)
