import time
import pathos.multiprocessing as mp


class Queue:

    def __init__(self, contents=None):

        if contents is None:
            self.contents = []

        else:
            self.contents = contents

    def print(self):

        for item in self.contents:

            print(item)

    def enqueue(self, item_to_queue):

        self.contents.append(item_to_queue)

    def dequeue(self):

        return self.contents.pop(0)


class Node:
    def __init__(self, board_state):
        self.state = board_state
        self.winner = self.determine_winner()
        if self.winner is None:
            self.turn = 1 if sum(row.count(1) for row in self.state) == sum(
                row.count(2) for row in self.state) else 2
        else:
            self.turn = None
        self.children = []
        self.parents = []
        self.possible_moves = self.find_possible_moves()
        # false by default, gets set to true during tree generation
        self.is_terminal_node = False

    def determine_winner(self):
        if self.state == [[0 for _ in range(7)] for _ in range(6)]:
            return None

        for i in range(0, 6):
            for j in range(0, 4):
                if self.state[i][j] == self.state[i][j + 1] == self.state[i][j + 2] == self.state[i][j + 3] != 0:
                    return self.state[i][j]

        for i in range(0, 3):
            for j in range(0, 7):
                if self.state[i][j] == self.state[i + 1][j] == self.state[i + 2][j] == self.state[i + 3][j] != 0:
                    return self.state[i][j]

        for i in range(0, 3):
            for j in range(0, 4):
                if self.state[i][j] == self.state[i + 1][j + 1] == self.state[i + 2][j + 2] == self.state[i + 3][j + 3] != 0:
                    return self.state[i][j]

                elif self.state[5 - i][j] == self.state[5 - (i + 1)][j + 1] == self.state[5 - (i + 2)][j + 2] == self.state[5 - (i + 3)][j + 3] != 0:
                    return self.state[5 - i][j]

        if any(0 in row for row in self.state):
            pass
        else:
            return 'Tie'

        return None

    def check_move_validity(self, move):
        for row in self.state:
            if row[move] == 0:
                return True
        return False

    def find_possible_moves(self):
        possible_moves = []
        for i in range(7):
            if self.check_move_validity(i):
                possible_moves.append(i)
        return possible_moves


class ConnectFourRecombiningTreeCustomDepth:
    def __init__(self, first_game_state, n):
        self.n = n
        self.generate_tree(first_game_state, n)

    def generate_tree(self, first_game_state, n):
        start_time = time.time()
        first_node = Node(first_game_state)
        first_node.depth = 0
        created_game_states = mp.Manager().dict()
        created_game_states[self.deeptuple(first_game_state)] = first_node
        terminal_nodes = mp.Manager().list()

        queue = mp.Queue()
        queue.put(first_node)

        while not queue.empty():

            if queue.qsize() >= 2:
                dequeued_node_1 = queue.get()
                dequeued_node_2 = queue.get()

                process1 = mp.Process(
                    target=self.create_child_nodes, args=(dequeued_node_1, created_game_states, queue))
                process2 = mp.Process(
                    target=self.create_child_nodes, args=(dequeued_node_2, created_game_states, queue))

                process1.start()
                process2.start()
                process1.join()
                process2.join()

            else:
                dequeued_node_1 = queue.get()

                process1 = mp.Process(

                    target=self.create_child_nodes, args=(dequeued_node_1, created_game_states, queue))

                process1.start()

                process1.join()

        end_time = time.time()
        # print(end_time - start_time)
        self.root = first_node
        self.node_dict = created_game_states
        self.terminal_nodes = terminal_nodes

    def create_child_nodes(self, node, created_game_states, terminal_nodes, queue):
        if node.depth == self.n:
            terminal_nodes.append(node)
            node.is_terminal_node = True
            return

        if node.winner is not None and node.is_terminal_node is False:
            terminal_nodes.append(node)
            node.is_terminal_node = True
            return

        for move in node.possible_moves:
            new_board_state = self.deeplist(node.state)
            new_board_state = self.drop_token(node.turn, new_board_state, move)
            self.create_and_hook_in_node(
                self, new_board_state, node, created_game_states, queue)

    def create_and_hook_in_node(self, new_board_state, old_node, created_game_states, queue):
        if self.deeptuple(new_board_state) in created_game_states:
            new_node = created_game_states[self.deeptuple(new_board_state)]
            new_node.parents.append(old_node)
            old_node.children.append(new_node)
            return

        # continue seems to be slightly faster than the regular if/else, not sure if its a fluke
        # else:
        new_node = Node(new_board_state)
        new_node.depth = old_node.depth + 1
        new_node.parents.append(old_node)
        old_node.children.append(new_node)
        queue.put(new_node)
        created_game_states[self.deeptuple(new_board_state)] = new_node

    def generate_tree_using_cache(self, starting_game_state):
        self.prune_tree(starting_game_state)
        node_dict = self.node_dict
        bottom_layer_nodes = self.bottom_layer_nodes
        terminal_nodes = []
        for terminal_node in self.terminal_nodes:
            if terminal_node.winner is not None:  # if the game is over
                terminal_nodes.append(terminal_node)
        new_layer_nodes = self.create_new_layer(bottom_layer_nodes)
        for current_node in new_layer_nodes:
            if current_node.winner is not None:
                terminal_nodes.append(current_node)
        second_new_layer_nodes = self.create_new_layer(new_layer_nodes)
        terminal_nodes += second_new_layer_nodes
        self.terminal_nodes = terminal_nodes
        self.root = node_dict[self.deeptuple(starting_game_state)]
        self.node_dict = node_dict
        self.previous_game_state = starting_game_state  # to help debug

    def prune_tree(self, template_state):
        template_node = self.node_dict[self.deeptuple(template_state)]
        node_dict = {self.deeptuple(template_state): template_node}
        queue = Queue([template_node])
        terminal_nodes = []
        bottom_layer_nodes = []

        while queue.contents != []:
            dequeued_node = queue.dequeue()
            if dequeued_node.is_terminal_node:
                terminal_nodes.append(dequeued_node)
                if dequeued_node.winner is None:
                    # excludes nodes that have already finished the game
                    bottom_layer_nodes.append(dequeued_node)

            for child_node in dequeued_node.children:
                child_node_state = child_node.state
                tuple_of_child_node_state = self.deeptuple(child_node_state)
                if tuple_of_child_node_state not in node_dict:
                    node_dict[tuple_of_child_node_state] = child_node
                    queue.enqueue(child_node)

                node_dict[tuple_of_child_node_state].parents = [
                    parent for parent in node_dict[tuple_of_child_node_state].parents if self.deeptuple(parent.state) in node_dict]

        self.node_dict = node_dict
        self.terminal_nodes = terminal_nodes
        self.bottom_layer_nodes = bottom_layer_nodes

    def create_new_layer(self, layer):
        new_layer_nodes = []
        for current_node in layer:
            if current_node.winner is not None:
                continue
            current_board_state = current_node.state
            possible_moves = current_node.possible_moves
            for move in possible_moves:
                new_board_state = self.deeplist(current_board_state)
                new_board_state = self.drop_token(
                    current_node.turn, new_board_state, move)

                if self.deeptuple(new_board_state) in self.node_dict:
                    new_node = self.node_dict[self.deeptuple(new_board_state)]
                    new_node.parents.append(current_node)
                    new_node.depth = current_node.depth
                    current_node.children.append(new_node)
                else:
                    new_node = Node(new_board_state)
                    new_node.is_terminal_node = True
                    new_node.parents.append(current_node)
                    new_node.depth = current_node.depth
                    current_node.children.append(new_node)
                    current_node.is_terminal_node = False
                    self.node_dict[self.deeptuple(new_board_state)] = new_node
                    new_layer_nodes.append(new_node)

        return new_layer_nodes

    def find_possible_moves(self):
        possible_moves = []
        for i in range(7):
            if self.check_move_validity(i):
                possible_moves.append(i)
        return possible_moves

    def drop_token(self, player, board, column):
        for row in range(6):
            if board[row][column] == 0:
                board[row][column] = player
                break
        return board

    def deeptuple(self, board):
        return tuple(tuple(row) for row in board)

    def find_filled_in_spaces(self, board):
        filled_in_spaces = []
        for i in range(6):
            for j in range(7):
                if board[i][j] != 0:
                    filled_in_spaces.append((i, j))
        return filled_in_spaces

    def deeplist(self, board):
        return list(list(row) for row in board)


bruh = ConnectFourRecombiningTreeCustomDepth(
    [[0 for _ in range(7)] for _ in range(6)], 6)
print(bruh.node_dict)
