from tic_tac_toe_recombining_tree import TicTacToeRecombiningTree
from tic_tac_toe_recombining_tree import Queue


class MinimaxStrategy:
    def __init__(self):
        self.generate_tree()
        self.propagate_minimax_values()

    def generate_tree(self):
        self.tree = TicTacToeRecombiningTree()
        self.node_dict = self.tree.node_dict
        self.terminal_state_nodes = self.tree.terminal_state_nodes

    def propagate_minimax_values(self):
        game_states_to_propagate = Queue()
        for node in self.terminal_state_nodes:
            node.minimax_value = {1: 1, 2: -1, 'Tie': 0}[node.winner]
            for parent_node in node.parents:
                game_states_to_propagate.enqueue(parent_node.state)
        while game_states_to_propagate.contents != []:
            game_state_to_propagate = tuple(game_states_to_propagate.dequeue()) #tuple because the keys in self.node_dict can't be lists
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

    def choose_move(self, board):
        board = tuple(board) # in order to look up in self.node_dict; lists aren't hashable
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
