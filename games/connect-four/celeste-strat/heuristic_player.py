from c4_tree import *
import random


class HeuristicPlayer:
    def __init__(self, ply):
        self.ply = ply

    def choose_move(self, board):
        tree = C4HeuristicTree(board, self.ply)
        tree.assign_heuristic_values(tree.root)

        board_node = tree.root

        if board == [[0, 0, 0, 0, 0, 0] for i in range(6)]:
            return 5

        children_heuristic_values_dict = {
            tree.get_board_tuple(children.game_state): children.heuristic_value
            for children in board_node.children
        }

        if len(children_heuristic_values_dict) == 0:
            return random.choice(board_node.remaining_columns())

        if board_node.upcoming_player == 1:
            best_move_board = list(
                max(
                    children_heuristic_values_dict,
                    key=children_heuristic_values_dict.get,
                )
            )
        else:
            best_move_board = list(
                min(
                    children_heuristic_values_dict,
                    key=children_heuristic_values_dict.get,
                )
            )

        current_board = board_node.game_state

        best_move_index = 4
        for i in range(6):
            for j in range(7):
                if current_board[i][j] != best_move_board[i][j]:
                    best_move_index = j
                    return best_move_index
