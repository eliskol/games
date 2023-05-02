from connect_four_recombining_tree_custom_depth import (
    ConnectFourRecombiningTreeCustomDepth,
)
from connect_four_recombining_tree_custom_depth import Queue
import time
import random


class LastMinutePlayer:
    def __init__(self):
        self.n = 2
        self.generate_tree([[0 for _ in range(7)] for _ in range(6)], self.n)
        self.time = self.propagate_minimax_values()

    def generate_tree(self, board_state, n):
        if (
            not hasattr(self, "tree")
            or board_state == [[0 for _ in range(7)] for _ in range(6)]
            or sum([row.count(1) for row in board_state]) == 1
            or self.n == 1
        ):
            self.tree = ConnectFourRecombiningTreeCustomDepth(board_state, n)
        else:
            self.tree.generate_tree_using_cache(board_state)
        self.node_dict = self.tree.node_dict
        self.terminal_nodes = self.tree.terminal_nodes

    def propagate_minimax_values(self):
        start = time.time()
        game_states_to_propagate = Queue()
        for node in self.terminal_nodes:
            node.minimax_value = {
                1: 1,
                2: -1,
                "Tie": 0,
                None: self.calculate_heuristic_value(node.state),
            }[node.winner]
            # node.minimax_value = self.calculate_heuristic_value(node.state)
            for parent_node in node.parents:
                game_states_to_propagate.enqueue(parent_node.state)
        while game_states_to_propagate.contents != []:
            # tuple because the keys in self.node_dict can't be lists
            game_state_to_propagate = self.tree.deeptuple(
                game_states_to_propagate.dequeue()
            )
            current_node = self.node_dict[game_state_to_propagate]
            if hasattr(current_node, "minimax_value"):
                continue
            proceed = True
            minimax_values_of_children = []
            for child_node in current_node.children:
                if not hasattr(child_node, "minimax_value"):
                    proceed = False
                    break
                minimax_values_of_children.append(child_node.minimax_value)
            if proceed is False:
                continue
            if current_node.turn == 1:
                current_node.minimax_value = max(minimax_values_of_children)
            else:
                current_node.minimax_value = min(minimax_values_of_children)

            for parent_node in current_node.parents:
                if hasattr(parent_node, "minimax_value"):
                    continue
                game_states_to_propagate.enqueue(parent_node.state)
        end = time.time()
        return end - start

    def choose_move(self, board):
        start = time.time()
        # move = random.randrange(0, 7)
        # while 0 not in [board[i][move] for i in range(6)]:
        #     move = random.randrange(0, 7)
        # return move

        self.current_board_state = board
        self.generate_tree(board, self.n)
        self.propagate_minimax_values()

        # in order to look up in self.node_dict; lists aren't hashable
        board = self.tree.deeptuple(board)
        current_node = self.node_dict[board]
        if self.player == 1:
            goal_node = max(current_node.children, key=lambda node: node.minimax_value)
        else:
            goal_node = min(current_node.children, key=lambda node: node.minimax_value)

        for j in range(7):  # check for which column was changed i.e. i want to move in
            if [board[i][j] for i in range(6)] != [
                goal_node.state[i][j] for i in range(6)
            ]:
                end = time.time()
                if end - start >= 1:
                    print(start - end)
                return j

    def calculate_heuristic_value(self, board):
        return 1 - 2 * random.random()
