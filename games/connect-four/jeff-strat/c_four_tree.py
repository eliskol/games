from c_four import *
import copy
"""
README FOR FORMATTING:
    boards are stored as a 6 7 entry array
    children and parents are stored in ID's
    for recombining, nodes are in order of DFS
"""


class CFourTree:

    def find_player_turn(self, board):
        # index 0 is p1, index 1 is p2
        moves_by_player = [0, 0]
        for row in board:
            for index in row:
                if index == 1:
                    moves_by_player[0] += 1
                elif index == 2:
                    moves_by_player[1] += 1
        return 1 if moves_by_player[0] == moves_by_player[1] else 2

    def recursion_recombining_node_tree(self, remaining_depth=6, node_id=0):
        if node_id == 0:
            self.nodes_by_id = {}
            self.nodes_by_id[0] = Node(
                0, [[0 for i in range(7)] for i in range(6)])
            self.nodes_by_state = {}
            self.nodes_by_state[str([[0 for i in range(7)]
                                    for i in range(6)])] = 0
        board = copy.deepcopy(self.nodes_by_id[node_id].board)
        if remaining_depth != 0 and Game.is_end(self, board) == False:
            # setup stuff
            node = self.nodes_by_id[node_id]
            last_state = copy.copy(node.board)
            player_to_move = self.find_player_turn(last_state)
            # children
            for possible_move in Game.find_possible_moves(self, last_state):
                possible_state = Game.update_board(self, copy.deepcopy(
                    last_state), possible_move, player_to_move)
                if str(possible_state) not in self.nodes_by_state:
                    new_id = len(self.nodes_by_id)
                    self.nodes_by_id[new_id] = Node(
                        new_id, possible_state, node.depth + 1)
                    self.nodes_by_state[str(possible_state)] = new_id
                    self.nodes_by_id[new_id].parents.append(node_id)
                    self.nodes_by_id[node_id].children.append(new_id)
                    self.recursion_recombining_node_tree(
                        remaining_depth-1, new_id)

                else:
                    # deal with all of the parent remapping here
                    duplicate_id = self.nodes_by_state[str(possible_state)]
                    self.nodes_by_id[duplicate_id].parents.append(node_id)
                    node.children.append(duplicate_id)


class Node:
    def __init__(self, node_id, board, depth=0):
        self.id = node_id
        self.board = board
        self.parents = []
        self.children = []
        self.depth = depth
