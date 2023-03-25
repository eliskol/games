from connect_four_recombining_tree_custom_depth import ConnectFourRecombiningTreeCustomDepth
from connect_four_recombining_tree_custom_depth import Queue
import time
import random


class HeuristicMinimaxStrategy:
    def __init__(self, n, random=False):
        self.random = random
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
            if self.random:
                node.minimax_value = 1 - 2 * random.random()
            else:
                node.minimax_value = {
1: 9999, 2: -9999, 'Tie': 0, None: self.calculate_heuristic_value(node.state)}[node.winner]
            # node.minimax_value = self.calculate_heuristic_value(node.state)
            for parent_node in node.parents:
                game_states_to_propagate.enqueue(parent_node.state)
        while game_states_to_propagate.contents != []:
            # tuple because the keys in self.node_dict can't be lists
            game_state_to_propagate = self.tree.deeptuple(game_states_to_propagate.dequeue())
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

        # if board == [[0 for _ in range(7)] for _ in range(6)] or sum([row.count(1) for row in board]) == 1:  # i should check if i should only go middle if the other player hasn't yet
            # return 3  # middle is the best starting move apparently
        # move = random.randrange(0, 7)
        # while 0 not in [board[i][move] for i in range(6)]:
        #     move = random.randrange(0, 7)
        # return move

        self.propagate_minimax_values()

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

    def calculate_heuristic_value(self, board):
        heuristic_value = 0
        indexes = [[i, j] for i in range(6) for j in range(7)]

        filled_in_spaces = [[i, j]
                            for [i, j] in indexes if board[i][j] != 0]

        for [i, j] in filled_in_spaces:

            # checking horizontally:
            if j <= 4:
                if board[i][j] == board[i][j + 1] == board[i][j + 2]:  # three in a row
                    if j <= 3 and board[i][j + 3] == 0 or j >= 1 and board[i][j - 1] == 0:
                        heuristic_value += {1: 0.9, 2: -0.9}[board[i][j]]
            if j <= 5:
                if board[i][j] == board[i][j + 1]:  # two in a row
                    if j <= 4 and board[i][j + 2] == 0 or j >= 1 and board[i][j - 1] == 0:
                        heuristic_value += {1: 0.3, 2: -0.3}[board[i][j]]

            if j <= 6:
                if j <= 5 and board[i][j + 1] == 0 or j >= 1 and board[i][j - 1] == 0:
                    heuristic_value += {1: 0.1, 2: -0.1}[board[i][j]]

            # checking vertically:
            if i <= 2:
                if board[i][j] == board[i + 1][j] == board[i + 2][j] and board[i + 3][j] == 0: # three in a row
                    heuristic_value += {1: 0.9, 2: -0.9}[board[i][j]]
                elif board[i][j] == board[i + 1][j] and board[i + 2][j] == 0: # two in a row
                    heuristic_value += {1: 0.3, 2: -0.3}[board[i][j]]
                elif board[i + 1][j] == 0:
                    heuristic_value += {1: 0.1, 2: -0.1}[board[i][j]]
        return heuristic_value


# game_state = [[0 for _ in range(7)] for _ in range(5)]
# game_state.insert(0, [1, 1, 0, 0, 0, 2, 2])

# bruh = HeuristicMinimaxStrategy(2)
# bruh.tree = ConnectFourRecombiningTreeCustomDepth(game_state, 2)
# # bruh.generate_tree(game_state, bruh.n)

# game_state = [[0 for _ in range(7)] for _ in range(5)]
# game_state.insert(0, [1, 1, 1, 0, 2, 2, 2])

# print(bruh.choose_move(game_state))