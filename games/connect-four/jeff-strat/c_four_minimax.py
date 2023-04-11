from c_four_tree import *
import random as rng
import numpy as np
import time

class minimaxHeuristic:
    def __init__(self, player, depth):
        self.player = player
        self.depth = depth
        self.generate_new_tree(depth)

    # helper functions
    def generate_new_tree(self, depth):
        self.tree = CFourTree()
        self.tree.recursion_recombining_node_tree(depth)
        self.nodes_by_id = self.tree.nodes_by_id
        self.nodes_by_state = self.tree.nodes_by_state

    def sort_node_by_depth(self, nodes_by_id):
        max_depth = 0
        # finds max depth
        for node in nodes_by_id:
            if max(nodes_by_id[node].depth, max_depth) != max_depth:
                max_depth = nodes_by_id[node].depth
        # sorting
        nodes_by_depth = [[] for _ in range(max_depth + 1)]
        for node in nodes_by_id:
            node_depth = nodes_by_id[node].depth
            nodes_by_depth[node_depth].append(node)
        return nodes_by_depth

    def score_heuristic(self, board):
        # score stuff
        scores = [0, 1, 7, 15, np.inf]
        total_points = 0
        # scores vertical
        if len(board) > 4:
            for i in range(0, len(board) - 3):
                for j in range(0, len(board[0])):
                    subboard = []
                    for a in range(4):
                        subboard.append(board[i+a][j])
                    total_points += scores[subboard.count(1)] * [1, -1][0]
                    total_points += scores[subboard.count(2)] * [1, -1][1]
        # scores horizontal
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                subboard = board[i][j:j+4]
                total_points += scores[subboard.count(1)] * [1, -1][0]
                total_points += scores[subboard.count(2)] * [1, -1][1]
        # scores left diagonal
        if len(board) > 4:
            for i in range(0, len(board) - 4):
                for j in range(0, len(board[0]) - 4):
                    subboard = []
                    for a in range(4):
                        subboard.append(board[i+a][j+a])

                    total_points += scores[subboard.count(1)] * [1, -1][0]
                    total_points += scores[subboard.count(2)] * [1, -1][1]
        # scores right diagonal
        if len(board) > 4:
            for row in range(5, 2, -1):
                for col in range(0, 4):
                    subboard = [board[row][col], board[row-1][col+1],
                                board[row-2][col+2], board[row-3][col+3]]
                    total_points += scores[subboard.count(1)] * [1, -1][0]
                    total_points += scores[subboard.count(2)] * [1, -1][1]

        return total_points

    def add_new_layer(self, starting_node_id):
        self.nodes_by_depth = self.sort_node_by_depth(self.nodes_by_id)
        max_depth = len(self.nodes_by_depth)
        terminal_children = []
        all_children = []
        queue = [starting_node_id]
        # gets terminal children
        while len(queue) != 0:
            if queue[0] in self.nodes_by_depth[max_depth - 1]:
                terminal_children.append(queue[0])
            else:
                for child in self.nodes_by_id[queue[0]].children:
                    if child not in all_children:
                        all_children.append(child)
                        queue.append(child)
            queue.pop(0)
        # all terminal children found
        for child in terminal_children:
            if Game.is_end(self, self.tree.nodes_by_id[child].board) == False:
                last_move = self.tree.nodes_by_id[child].board
                node = self.tree.nodes_by_id[child]
                for i in Game.find_possible_moves(self, last_move):
                    turn = CFourTree.find_player_turn(self, last_move)
                    new_board = copy.deepcopy(last_move)
                    new_board = Game.update_board(self, new_board, i, turn)
                    if str(new_board) in self.tree.nodes_by_state:
                        duplicate_node_id = self.tree.nodes_by_state[str(
                            new_board)]
                        self.tree.nodes_by_id[duplicate_node_id].parents.append(
                            child)
                        node.children.append(duplicate_node_id)
                    else:
                        new_node_id = len(self.tree.nodes_by_id)
                        self.tree.nodes_by_id[new_node_id] = Node(
                            new_node_id, new_board, node.depth + 1)
                        self.tree.nodes_by_state[str(new_board)] = new_node_id
                        self.tree.nodes_by_id[new_node_id].parents.append(
                            child)
                        node.children.append(new_node_id)

    def find_last_move(self, board1, board2):
        for i in range(0, len(board1)):
            if board1[i] != board2[i]:
                for j in range(len(board1[i])):
                    if board1[i][j] != board2[i][j]:
                        return j

    # actual functions

    def fit(self):
        self.nodes_by_id = self.tree.nodes_by_id
        self.nodes_by_state = self.tree.nodes_by_state
        nodes_by_depth = self.sort_node_by_depth(self.nodes_by_id)
        # all heuristic values are appended here
        for state_id in nodes_by_depth[-1]:
            state = self.nodes_by_id[state_id]
            state_board = state.board
            current_node = self.nodes_by_id[self.nodes_by_state[str(
                state.board)]]
            turn = CFourTree.find_player_turn(self, state_board)
            current_node.value = self.score_heuristic(current_node.board)
        for depth in range(len(nodes_by_depth)-2, -1, -1):
            for state_id in nodes_by_depth[depth]:
                state_node = self.nodes_by_id[state_id]
                if len(state_node.children) == 0:
                    turn = CFourTree.find_player_turn(self, state_node.board)
                    state_node.value = self.score_heuristic(state_node.board)
                else:
                    # all minimax-values are appended here
                    turn = CFourTree.find_player_turn(self, state_node.board)
                    children_worth = []

                    for child in state_node.children:
                        children_worth.append(self.nodes_by_id[child].value)
                    state_node.value = max(
                        children_worth) if turn == 1 else min(children_worth)

    def choose_move(self, current_state):
        start = time.time()
        current_state = current_state[::-1]
        # adds layer
        node_id = self.nodes_by_state[str(current_state)]
        if node_id != 0:
            self.add_new_layer(node_id)
            self.add_new_layer(node_id)
        self.fit()
        # gets children
        children = []
        children_value = []
        for child_id in self.nodes_by_id[node_id].children:
            children.append(child_id)
            if self.find_last_move(current_state, self.nodes_by_id[child_id].board) == 3:
                children_value.append(self.nodes_by_id[child_id].value)
            else:
                children_value.append(self.nodes_by_id[child_id].value)

        # for child in range(len(children_value)):
        #     print("-----")
        #     print("child is ", children[child])
        #     print(
        #         "child has " + str(len(self.nodes_by_id[children[child]].children)) + " children")
        #     print("board is ", self.nodes_by_id[children[child]].board)
        #     print("heuristic value is ", children_value[child])

        #     print("-----")

        best_move = max(children_value) if self.player == 1 else min(
            children_value)
        move = children_value.index(best_move)
        best_node_id = self.nodes_by_id[node_id].children[move]
        last_move = self.find_last_move(
            current_state, self.nodes_by_id[best_node_id].board)
        end = time.time()
        if end - start > 1:
            print('jeff', end - start)
        return last_move
