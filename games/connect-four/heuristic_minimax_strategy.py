from connect_four_recombining_tree_custom_depth import ConnectFourRecombiningTreeCustomDepth
from connect_four_recombining_tree_custom_depth import Queue
import time


class HeuristicMinimaxStrategy:
    def __init__(self, n):
        self.generate_tree([0 for _ in range(9)], n)
        self.time = self.propagate_minimax_values()
        self.n = n

    def generate_tree(self, board_state, n=9):
        if not hasattr(self, "tree"):
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
                1: 1, 2: -1, 'Tie': 0, None: self.calculate_heuristic_value(node.state)}[node.winner]
            for parent_node in node.parents:
                game_states_to_propagate.enqueue(parent_node.state)
        while game_states_to_propagate.contents != []:
            # tuple because the keys in self.node_dict can't be lists
            game_state_to_propagate = tuple(game_states_to_propagate.dequeue())
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
        self.current_board_state = board
        if board != [0 for _ in range(9)]:
            self.generate_tree(board)
            self.propagate_minimax_values()

        # in order to look up in self.node_dict; lists aren't hashable
        board = tuple(board)
        current_node = self.node_dict[board]
        if self.player == 1:
            goal_node = max(current_node.children,
                            key=lambda node: node.minimax_value)
        else:
            goal_node = min(current_node.children,
                            key=lambda node: node.minimax_value)

        for i in range(9):
            if board[i] != goal_node.state[i]:
                return i

    def calculate_heuristic_value(self, board):
        total = 0
        for i in [0, 3, 6]:  # rows
            if board[i] == board[i + 1] != 0 and board[i + 2] == 0:
                # add 1 if its player 1, subtract 1 if its player 2
                total += {1: 1, 2: -1}[board[i]]
            if board[i + 1] == board[i + 2] != 0 and board[i] == 0:
                total += {1: 1, 2: -1}[board[i + 1]]  # see above comment
            if board[i] == board[i + 2] != 0 and board[i + 1] == 0:
                total += {1: 1, 2: -1}[board[i]]  # see above comment
        for i in [0, 1, 2]:  # cols
            if board[i] == board[i + 3] != 0 and board[i + 6] == 0:
                total += {1: 1, 2: -1}[board[i]]  # see above above comment
            if board[i + 3] == board[i + 6] != 0 and board[i] == 0:
                total += {1: 1, 2: -1}[board[i + 3]]  # see above comment
            if board[i] == board[i + 6] != 0 and board[i + 3] == 0:
                total += {1: 1, 2: -1}[board[i]]  # see above comment

        # diagonal
        if board[0] == board[4] != 0 and board[8] == 0:
            total += {1: 1, 2: -1}[board[0]]  # see above above comment
        if board[4] == board[8] != 0 and board[0] == 0:
            total += {1: 1, 2: -1}[board[4]]  # see above comment
        if board[0] == board[8] != 0 and board[4] == 0:
            total += {1: 1, 2: -1}[board[0]]  # see above comment

        # anti-diagonal
        if board[2] == board[4] != 0 and board[6] == 0:
            total += {1: 1, 2: -1}[board[2]]  # see above comment
        if board[2] == board[6] != 0 and board[4] == 0:
            total += {1: 1, 2: -1}[board[2]]  # see above comment
        if board[4] == board[8] != 0 and board[0] == 0:
            total += {1: 1, 2: -1}[board[4]]  # see above comment

        total /= 8
        if total == 0.5:
            return 0
        return 1 if total > 0.5 else 2
