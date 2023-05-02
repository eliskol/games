import pickle
import sys

sys.path.insert(1, sys.path[0].replace("tests", "games/connect-four"))
from heuristic_minimax_strategy import HeuristicMinimaxStrategy
from connect_four_recombining_tree_custom_depth import (
    ConnectFourRecombiningTreeCustomDepth,
)

tree = ConnectFourRecombiningTreeCustomDepth(
    [[0 for _ in range(7)] for _ in range(6)], 4
)  # RecursionError with ply > 3

with open("data.pickle", "wb") as f:
    pickle.dump(tree.node_dict, f, pickle.HIGHEST_PROTOCOL)

with open("data.pickle", "rb") as f:
    node_dict = pickle.load(f)

print(node_dict)
