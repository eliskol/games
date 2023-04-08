import copy
import time
import random

# update check win states bc storing the rows and columns now
#COMBINE THE LOOPS FOR HORIZONTAL AND VERTICAL
class C4Node:

    def __init__(self, game_state):
        self.game_state = game_state
        self.rows = [game_state[i] for i in range(len(game_state))]
        self.columns = [[rows[i] for rows in game_state] for i in range(7)]

        self.diagonals = None #DEFINE DIAGOANLS

        self.upcoming_player = self.upcoming_player()
        self.winner = self.check_win_states()
        self.parents = []
        self.children = []
        self.depth = 0
        self.heuristic_value = None

    def upcoming_player(self):
        upcoming_player = 2
        flattened_board = sum(self.game_state, [])
        if flattened_board.count(1) == flattened_board.count(2):
            upcoming_player = 1
        return upcoming_player

    def print(self):
        for i in range(6):
            print(self.game_state[i])

    def check_win_states(self):
        # horizontal
        for i in range(4):
            for j in range(6):
                if self.game_state[j][i] == self.game_state[j][i+1] == self.game_state[j][i+2] == self.game_state[j][i+3] != 0:
                    return self.game_state[j][i]

        # vertical
        for i in range(7):
            for j in range(3):
                if self.game_state[j][i] == self.game_state[j+1][i] == self.game_state[j+2][i] == self.game_state[j+3][i] != 0:
                    return self.game_state[j][i]

        # positive diagonals
        for i in range(4):
            for j in range(3):
                if self.game_state[j][i] == self.game_state[j+1][i+1] == self.game_state[j+2][i+2] == self.game_state[j+3][i+3] != 0:
                    return self.game_state[j][i]

        # negative diagonals
        for i in range(4):
            for j in range(3, 6):
                if self.game_state[j][i] == self.game_state[j-1][i+1] == self.game_state[j-2][i+2] == self.game_state[j-3][i+3] != 0:
                    return self.game_state[j][i]

       # tie
        flat_list = []
        for rows in self.game_state:
            for i in range(len(rows)):
                flat_list.append(rows[i])

        if 0 not in flat_list:
            return 'Tie'

    def remaining_columns(self):
        #only need to check if the top element is zero
        open_columns = [i for i in range(7) if self.game_state[-1][i] == 0]
        return open_columns

        return open_columns

    def copy_of_copies(self):
        new_copy = [row.copy() for row in self.game_state]
        return new_copy

    def classify_horizontals(self):
        self.horizontal_three_of_a_kinds = []
        self.horizontal_two_of_a_kinds = []

        for horizontal in self.rows:
            for i in range(4):
                #2220
                if horizontal[0 + i] == horizontal[1 + i] == horizontal[2+i] != 0 and horizontal[3+i] == 0:
                    if horizontal[0 + i] == self.upcoming_player:
                        self.horizontal_three_of_a_kinds.append(3)
                    else:
                        self.horizontal_three_of_a_kinds.append(-3)

                #0222
                elif horizontal[0 + i] == 0 and horizontal[1 + i] == horizontal[2 + i] == horizontal[3 + i] != 0:
                    if horizontal[1 + i] == self.upcoming_player:
                        self.horizontal_three_of_a_kinds.append(3)
                    else:
                        self.horizontal_three_of_a_kinds.append(-3)

                #0022
                elif horizontal[0 + i] == horizontal[1 + i] == 0 and horizontal[2+i] == horizontal[3 + i] != 0:
                    if horizontal[2 + i] == self.upcoming_player:
                        self.horizontal_three_of_a_kinds.append(2)
                    else:
                        self.horizontal_three_of_a_kinds.append(-2)
                #2200
                elif horizontal[0 + i] == horizontal[1 + i] != 0 and horizontal[2+i] == horizontal[3 + i] == 0:
                    if horizontal[0 + i] == self.upcoming_player:
                        self.horizontal_three_of_a_kinds.append(2)
                    else:
                        self.horizontal_three_of_a_kinds.append(-2)

                #0220
                elif horizontal[0 + i] == horizontal[3 + i] == 0 and horizontal[1+i] == horizontal[2 + i] != 0:
                    if horizontal[2 + i] == self.upcoming_player:
                        self.horizontal_three_of_a_kinds.append(2)
                    else:
                        self.horizontal_three_of_a_kinds.append(-2)
                #2002
                elif horizontal[0 + i] == horizontal[3 + i] != 0 and horizontal[1+i] == horizontal[2 + i] == 0:
                    if horizontal[0 + i] == self.upcoming_player:
                        self.horizontal_three_of_a_kinds.append(2)
                    else:
                        self.horizontal_three_of_a_kinds.append(-2)
                #0202
                elif horizontal[0 + i] == horizontal[2 + i] == 0 and horizontal[1+i] == horizontal[3 + i] != 0:
                    if horizontal[0 + i] == self.upcoming_player:
                        self.horizontal_three_of_a_kinds.append(2)
                    else:
                        self.horizontal_three_of_a_kinds.append(-2)
                #2020
                elif horizontal[0 + i] == horizontal[2 + i] != 0 and horizontal[1+i] == horizontal[3 + i] == 0:
                    if horizontal[0 + i] == self.upcoming_player:
                        self.horizontal_three_of_a_kinds.append(2)
                    else:
                        self.horizontal_three_of_a_kinds.append(-2)

        return sum(self.horizontal_three_of_a_kinds) + sum(self.horizontal_two_of_a_kinds)

    def classify_verticals(self):

        self.vertical_three_of_a_kinds = []
        self.vertical_two_of_a_kinds = []

        for vertical in self.columns:
            for i in range(3):
                #0222
                if vertical[0 + i] == 0 and vertical[1 + i] == vertical[2 + i] == vertical[3 + i] != 0:
                    if vertical[2 + i] == self.upcoming_player:
                        self.vertical_three_of_a_kinds.append(3)
                    else:
                        self.vertical_three_of_a_kinds.append(-3)
                #0022
                elif vertical[0 + i] == vertical[1 + i] == 0 and  vertical[2 + i] == vertical[3 + i] != 0:

                    if vertical[2 + i] == self.upcoming_player:
                        self.vertical_three_of_a_kinds.append(2)
                    else:
                        self.vertical_three_of_a_kinds.append(-2)

        return sum(self.vertical_three_of_a_kinds) + sum(self.vertical_two_of_a_kinds)

        self.diagonals_two_of_a_kinds = {}
        self.diagonals_three_of_a_kinds = {}

    def calc_heuristic_value(self):
        horizontal_total = self.classify_horizontals()
        vertical_total = self.classify_verticals()
        return ((horizontal_total + vertical_total ) / 40)

class Queue:
    def __init__(self):
        self.items = []

    def print(self):
        print(self.items)

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        self.items.pop(0)

class C4HeuristicTree:
    def __init__(self,root, initial_ply):

        self.root = C4Node(root)
        self.nodes = {}
        self.nodes[tuple([tuple(self.root.game_state[i]) for i in range(6)])] = self.root

        self.initial_ply = initial_ply

        self.generate_initial_tree()

    def generate(self, nodes, ply):

        queue = Queue()
        visited_nodes = set()
        for node in nodes:
            queue.enqueue(node)
            visited_nodes.add(self.get_board_tuple(node.game_state))

        while len(queue.items) != 0:

            current_node = queue.items[0]
            if current_node.depth >= ply:
                break

            if current_node.winner == None:
                avaliable_columns = current_node.remaining_columns()
                current_board = current_node.game_state

                for column in avaliable_columns:

                    new_move_board = current_node.copy_of_copies()
                    new_move_row_index = self.row_index_of_move(column, new_move_board)
                    new_move_board[new_move_row_index][column] = current_node.upcoming_player
                    new_move_tuple_board = self.get_board_tuple(new_move_board)

                    if new_move_tuple_board in visited_nodes:
                        new_node = self.nodes[new_move_tuple_board]
                        current_node.children.append(new_node)
                        new_node.parents.append(current_node)
                        new_node.depth = current_node.depth + 1
                        continue

                    new_node = C4Node(new_move_board)
                    new_node.depth = current_node.depth + 1
                    new_node.parents.append(current_node)
                    current_node.children.append(new_node)
                    queue.enqueue(new_node)
                    self.nodes[new_move_tuple_board] = new_node
                    visited_nodes.add(new_move_tuple_board)

            queue.dequeue()
        self.num_nodes = len(self.nodes)

    def generate_initial_tree(self):
        self.generate([self.root], self.initial_ply)

    def row_index_of_move(self, move, board):
        for i in range(6):
            row = 5-i
            if board[row][move] == 0:
                return row

    def get_board_tuple(self, game_state):
        return tuple(tuple(row) for row in game_state)

    def one_layer_tuple(self, depth):
        tuple_layer = []
        for nodes in self.nodes:
            node = self.nodes[nodes]
            if node.depth == depth:
                tuple_layer.append(nodes)
        return tuple_layer

    def prune_layer(self, depth):
        layer_to_prune = self.one_layer_tuple(depth)
        for nodes in layer_to_prune:
            self.nodes.pop(nodes)

        self.num_nodes = len(self.nodes)

    def add_layer(self, new_layer_depth):
        previous_layer_tuples = self.one_layer_tuple(new_layer_depth - 1)

        previous_layer_nodes = [self.nodes[node_tuples] for node_tuples in previous_layer_tuples]

        self.generate(previous_layer_nodes, new_layer_depth)

    def assign_heuristic_values(self, node):
        if node.children == []:
            if node.winner == 1:
                node.heuristic_value = 1
            elif node.winner == 2:
                node.heuristic_value = -1
            elif node.winner == 'Tie':
                node.heuristic_value = 0
            else:
                node.heuristic_value = node.calc_heuristic_value()


        else:
            children_heuristic_values = []

            for child in node.children:
                self.assign_heuristic_values(child)
                children_heuristic_values.append(child.heuristic_value)


            if node.upcoming_player == 1:
                node.heuristic_value = max(children_heuristic_values)
            else:
                node.heuristic_value = min(children_heuristic_values)

        return node.heuristic_value

        return