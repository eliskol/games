from connect_four_recombining_tree_custom_depth import ConnectFourRecombiningTreeCustomDepth
from connect_four_recombining_tree_custom_depth import Queue
import time
import random


class RandomHeuristicStrategy:
    def __init__(self, n):
        self.generate_tree([[0 for _ in range(7)] for _ in range(6)], n)
        self.time = self.propagate_minimax_values()
        self.n = n

    def generate_tree(self, board_state, n):
        if (not hasattr(self, "tree")) or board_state == [[0 for _ in range(7)] for _ in range(6)] or sum([row.count(1) for row in board_state]) == 1 != sum([row.count(2) for row in board_state]) or self.n == 1:
            self.tree = ConnectFourRecombiningTreeCustomDepth(board_state, n)
        else:
            self.tree.generate_tree_using_cache(board_state)
        self.node_dict = self.tree.node_dict
        self.terminal_nodes = self.tree.terminal_nodes

    def propagate_minimax_values(self):
        for node in self.node_dict.values():
            node.minimax_value = 1 - 2 * random.random()
        return

    def choose_move(self, board):
        start = time.time()

        self.current_board_state = board
        self.generate_tree(board, self.n)
        self.propagate_minimax_values()

        # if board == [[0 for _ in range(7)] for _ in range(6)]:
        #     return 3
        # elif sum([row.count(1) for row in board]) == 1 != sum([row.count(2) for row in board]):
        #     return 2

        # in order to look up in self.node_dict; lists aren't hashable
        board = self.tree.deeptuple(board)
        current_node = self.node_dict[board]
        if self.player == 1:
            goal_node = max(current_node.children,
                            key=lambda node: node.minimax_value)
        else:
            goal_node = min(current_node.children,
                            key=lambda node: node.minimax_value)

        for j in range(7):  # check for which column was changed i.e. i want to move in
            if [board[i][j] for i in range(6)] != [goal_node.state[i][j] for i in range(6)]:
                end = time.time()
                if end - start >= 1:
                    print(end - start)
                return j
