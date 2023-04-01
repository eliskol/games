from connect_four_recombining_tree_custom_depth import ConnectFourRecombiningTreeCustomDepth, Node
from connect_four_recombining_tree_custom_depth import Queue
import time


class HeuristicMinimaxStrategy:
    def __init__(self, n, old=False):
        self.old = old
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
        start = time.time()
        game_states_to_propagate = Queue()
        for node in self.terminal_nodes:
            node.minimax_value = {
                1: 9999, 2: -9999, 'Tie': 0}[node.winner] if node.winner is not None else (
                    self.calculate_heuristic_value(node.state) if not self.old else self.old_calculate_heuristic_value(node.state))
            for parent_node in node.parents:
                game_states_to_propagate.enqueue(parent_node.state)
        while game_states_to_propagate.contents != []:
            # tuple because the keys in self.node_dict can't be lists
            game_state_to_propagate = self.tree.deeptuple(
                game_states_to_propagate.dequeue())
            current_node = self.node_dict[game_state_to_propagate]
            if hasattr(current_node, 'minimax_value'):
                continue
            proceed = True
            minimax_values_of_children = []
            for child_node in current_node.children:
                if not hasattr(child_node, 'minimax_value'):
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
                if hasattr(parent_node, 'minimax_value'):
                    continue
                game_states_to_propagate.enqueue(parent_node.state)
        end = time.time()
        return end - start

    def choose_move(self, board):
        start = time.time()

        self.current_board_state = board
        self.generate_tree(board, self.n)
        self.propagate_minimax_values()

        if board == [[0 for _ in range(7)] for _ in range(6)]:
            self.player = 1
            return 3
        elif sum([row.count(1) for row in board]) == 1 != sum([row.count(2) for row in board]):
            self.player = 2
            return 2

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

    def calculate_heuristic_value(self, board: list[list[int]]):
        heuristic_value = 0
        for i in range(6):
            for j in range(4):
                horizontal = board[i][j:j + 4]
                if (horizontal.count(1) == 3 or horizontal.count(2) == 3) and horizontal.count(0) == 1:
                    heuristic_value += {3: 0.9, 0: -0.9}[horizontal.count(1)]
                elif (horizontal.count(1) == 2 or horizontal.count(2) == 2) and horizontal.count(0) == 2:
                    heuristic_value += {2: 0.3, 0: -0.3}[horizontal.count(1)]
                elif (horizontal.count(1) == 1 or horizontal.count(2) == 1) and horizontal.count(0) == 3:
                    heuristic_value += {1: 0.1, 0: -0.1}[horizontal.count(1)]
            # for j in range(5):
            #     horizontal = board[i][j:j + 3]
            #     if (horizontal.count(1) == 2 or horizontal.count(2) == 2) and horizontal.count(0) == 1:
            #         heuristic_value += {2: 0.3, 0: -0.3}[horizontal.count(1)]
            # for j in range(6):
            #     horizontal = board[i][j:j + 2]
            #     if (horizontal.count(1) == 1 or horizontal.count(2) == 1) and horizontal.count(0) == 1:
            #         heuristic_value += {1: 0.1, 0: -0.1}[horizontal.count(1)]
        for j in range(7):
            for i in range(3):
                vertical = [board[i + k][j] for k in range(4)]
                if (vertical.count(1) == 3 or vertical.count(2) == 3) and vertical[-1] == 0:
                    heuristic_value += {3: 0.9, 0: -0.9}[vertical.count(1)]
                elif (vertical.count(1) == 2 or vertical.count(2) == 2) and vertical[-2] == 0:
                    heuristic_value += {2: 0.3, 0: -0.3}[vertical.count(1)]
                elif (vertical.count(1) == 1 or vertical.count(2) == 1) and vertical[-3] == 0:
                    heuristic_value += {1: 0.1, 0: -0.1}[vertical.count(1)]
            # for i in range(4):
            #     vertical = [board[i + k][j] for k in range(3)]
            #     if (vertical.count(1) == 2 or vertical.count(2) == 2) and vertical[-1] == 0:
            #         heuristic_value += {2: 0.3, 0: -0.3}[vertical.count(1)]
            # for i in range(5):
            #     vertical = [board[i + k][j] for k in range(2)]
            #     if (vertical.count(1) == 1 or vertical.count(2) == 1) and vertical[-1] == 0:
            #         heuristic_value += {1: 0.1, 0: -0.1}[vertical.count(1)]
        for i in range(0, 3):
            for j in range(0, 4):
                positive_diagonal = [board[i + k][j + k] for k in range(4)]
                negative_diagonal = [board[5 - (i + k)][j + k] for k in range(4)]
                if positive_diagonal.count(0) == 0 and (positive_diagonal.count(1) == 0 or positive_diagonal.count(2) == 0):
                    heuristic_value += {True: [0, 0.1, 0.3, 0.9][positive_diagonal.count(1)], False: [0, -0.1, -0.3, -0.9][positive_diagonal.count(2)]}[
                        positive_diagonal.count(2) == 0]  # what is wrong with me
                if negative_diagonal.count(0) == 0 and (negative_diagonal.count(1) == 0 or negative_diagonal.count(2) == 0):
                    heuristic_value += {True: [0, 0.1, 0.3, 0.9][negative_diagonal.count(1)], False: [0, -0.1, -0.3, -0.9][negative_diagonal.count(2)]}[
                        negative_diagonal.count(2) == 0]  # what is wrong with me
        return heuristic_value

    def old_calculate_heuristic_value(self, board: list[list[int]]):
        heuristic_value = 0
        for i in range(6):
            for j in range(4):
                horizontal = board[i][j:j + 4]
                if (horizontal.count(1) == 3 or horizontal.count(2) == 3) and horizontal.count(0) == 1:
                    heuristic_value += {3: 0.9, 0: -0.9}[horizontal.count(1)]
            for j in range(5):
                horizontal = board[i][j:j + 3]
                if (horizontal.count(1) == 2 or horizontal.count(2) == 2) and horizontal.count(0) == 1:
                    heuristic_value += {2: 0.3, 0: -0.3}[horizontal.count(1)]
            for j in range(6):
                horizontal = board[i][j:j + 2]
                if (horizontal.count(1) == 1 or horizontal.count(2) == 1) and horizontal.count(0) == 1:
                    heuristic_value += {1: 0.1, 0: -0.1}[horizontal.count(1)]
        for j in range(7):
            for i in range(3):
                vertical = [board[i + k][j] for k in range(4)]
                if (vertical.count(1) == 3 or vertical.count(2) == 3) and vertical[-1] == 0:
                    heuristic_value += {3: 0.9, 0: -0.9}[vertical.count(1)]
            for i in range(4):
                vertical = [board[i + k][j] for k in range(3)]
                if (vertical.count(1) == 2 or vertical.count(2) == 2) and vertical[-1] == 0:
                    heuristic_value += {2: 0.3, 0: -0.3}[vertical.count(1)]
            for i in range(5):
                vertical = [board[i + k][j] for k in range(2)]
                if (vertical.count(1) == 1 or vertical.count(2) == 1) and vertical[-1] == 0:
                    heuristic_value += {1: 0.1, 0: -0.1}[vertical.count(1)]
        for i in range(0, 3):
            for j in range(0, 4):
                positive_diagonal = [board[i + k][j + k] for k in range(4)]
                negative_diagonal = [
                    board[5 - (i + k)][j + k] for k in range(4)]
                if positive_diagonal.count(0) == 0 and (positive_diagonal.count(1) == 0 or positive_diagonal.count(2) == 0):
                    heuristic_value += {True: [0, 0.1, 0.3, 0.9, 9999][positive_diagonal.count(1)], False: [0, -0.1, -0.3, -0.9, -9999][positive_diagonal.count(2)]}[
                        positive_diagonal.count(2) == 0]  # what is wrong with me
                if negative_diagonal.count(0) == 0 and (negative_diagonal.count(1) == 0 or negative_diagonal.count(2) == 0):
                    heuristic_value += {True: [0, 0.1, 0.3, 0.9, 9999][negative_diagonal.count(1)], False: [0, -0.1, -0.3, -0.9, -9999][negative_diagonal.count(2)]}[
                        negative_diagonal.count(2) == 0]  # what is wrong with me
        return heuristic_value
