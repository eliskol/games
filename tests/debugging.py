from connect_four_recombining_tree_custom_depth import *
from heuristic_minimax_strategy import HeuristicMinimaxStrategy
from predefined_strat import PredefinedStrat
from connect_four import Game

predefined = PredefinedStrat([i % 7 for i in range(100)])
bruh2 = HeuristicMinimaxStrategy(2)
bruh3 = HeuristicMinimaxStrategy(4)
game = Game(predefined, bruh2)
game.run(log=True)
# bruh.terminal_nodes = sorted(bruh.terminal_nodes, key=lambda node: node.minimax_value)
# for node in bruh.terminal_nodes:
#     print(node.minimax_value)
#     for row in reversed(node.state):
#         print(row)
#     print()

for state in bruh2.node_dict:
    node2 = bruh2.node_dict[state]
    node3 = bruh3.node_dict[state]
    print((node2.minimax_value, node3.minimax_value) if node2.minimax_value != node3.minimax_value else "same")