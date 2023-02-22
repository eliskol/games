import time


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
        if self.winner == None:
            self.turn = 1 if self.state.count(1) == self.state.count(2) else 2
        else:
            self.turn = None
        self.children = []
        self.parents = []
        self.possible_moves = self.find_possible_moves()
        # false by default, gets set to true during tree generation
        self.is_terminal_node = False

    def determine_winner(self):

        for j in range(3):
            i = 3 * j
            if self.state[j] == self.state[j + 3] == self.state[j + 6] != 0:  # columns
                return self.state[j]
            elif self.state[i] == self.state[i + 1] == self.state[i + 2] != 0:  # rows
                return self.state[i]

        if self.state[0] == self.state[4] == self.state[8] != 0:  # diagonal
            return self.state[4]
        elif self.state[2] == self.state[4] == self.state[6] != 0:  # anti-diagonal
            return self.state[4]
        elif 0 not in self.state:
            return 'Tie'

        return None

    def find_possible_moves(self):
        possible_moves = []
        for i in range(9):
            if self.state[i] == 0:
                possible_moves.append(i)
        return possible_moves


class TicTacToeRecombiningTreeCustomDepth:
    def __init__(self, first_game_state, n):
        self.generate_tree(first_game_state, n)

    def generate_tree(self, first_game_state, n):
        start_time = time.time()
        first_node = Node(first_game_state)
        first_node.depth = 0
        created_game_states = {tuple(first_node.state): first_node}
        terminal_nodes = []

        queue = Queue([first_node])
        a_variable = 1

        while queue.contents != []:

            dequeued_node = queue.dequeue()

            if dequeued_node.depth == n:
                terminal_nodes.append(dequeued_node)
                dequeued_node.is_terminal_node = True
                continue

            if dequeued_node.winner is not None:
                if dequeued_node not in terminal_nodes:
                    terminal_nodes.append(dequeued_node)
                    dequeued_node.is_terminal_node = True
                continue

            dequeued_node_board_state = dequeued_node.state
            next_player = dequeued_node.turn
            possible_moves = dequeued_node.possible_moves

            for move in possible_moves:
                a_variable += 1
                new_board_state = list(dequeued_node_board_state)
                new_board_state[move] = next_player

                if tuple(new_board_state) in created_game_states:
                    new_node = created_game_states[tuple(new_board_state)]
                    new_node.parents.append(dequeued_node)
                    dequeued_node.children.append(new_node)

                else:
                    new_node = Node(new_board_state)
                    new_node.depth = dequeued_node.depth + 1
                    new_node.parents.append(dequeued_node)
                    dequeued_node.children.append(new_node)
                    queue.enqueue(new_node)
                    created_game_states[tuple(new_board_state)] = new_node

        #         print(a_variable)
        # print('finished generating!')
        # print(time.time() - start_time)
        # print(leaf_node_count)
        self.root = first_node
        self.node_dict = created_game_states
        self.terminal_nodes = terminal_nodes
        # print((0 for _ in range(9)) in self.node_dict)

    def _generate_tree_using_cache(self, first_game_state):
        # transferring this poorly written function to a new, better written one
        # traverse the existing tree starting from first_game_state
        first_node = self.node_dict[tuple(first_game_state)]
        created_game_states = {tuple(first_game_state): first_node}
        for current_board_state in self.node_dict:
            current_node = self.node_dict[current_board_state]
            index_of_all_filled_in_spaces_of_first_node = [
                i for i in range(9) if first_node.state[i] != 0]
            for i in index_of_all_filled_in_spaces_of_first_node:
                if first_node.state[i] == current_node.state[i]:
                    is_a_possible_child = True
                else:
                    is_a_possible_child = False
                    break
            if is_a_possible_child is False:
                continue

            current_node.depth -= 2  # because we're starting from a
            created_game_states[tuple(current_board_state)] = current_node
            if current_node.is_terminal_node and current_node.winner is None:
                possible_moves = current_node.possible_moves
                for move in possible_moves:
                    new_board_state = list(current_node.state)
                    new_board_state[move] = current_node.turn
                    if tuple(new_board_state) in created_game_states:
                        new_node = created_game_states[tuple(new_board_state)]
                        new_node.parents.append(current_node)
                        current_node.children.append(new_node)
                    else:
                        new_node = Node(new_board_state)
                        new_node.parents.append(current_node)
                        current_node.children.append(new_node)
                        created_game_states[tuple(new_board_state)] = new_node
                    new_node.depth = current_node.depth + 1
                    new_node_possible_moves = new_node.possible_moves
                    # won't run if the game has a winner/is tied because possible_moves = []
                    for new_move in new_node_possible_moves:
                        second_new_board_state = list(new_node.state)
                        second_new_board_state[new_move] = new_node.turn
                        if second_new_board_state == [1, 2, 1, 2, 1, 2, 2, 1, 1]:
                            pass
                        if tuple(second_new_board_state) in created_game_states:
                            second_new_node = created_game_states[tuple(
                                second_new_board_state)]
                        else:
                            second_new_node = Node(second_new_board_state)
                            created_game_states[tuple(
                                second_new_board_state)] = second_new_node

                        second_new_node.parents.append(new_node)
                        new_node.children.append(second_new_node)
                        second_new_node.depth = new_node.depth + 1

        self.root = first_node

    def generate_tree_using_cache(self, starting_game_state):
        self.prune_tree(starting_game_state)
        node_dict = self.node_dict
        last_layer = []
        terminal_nodes = []
        for game_state in node_dict:
            current_node = node_dict[game_state]
            current_node.depth -= 2
            if current_node.is_terminal_node:
                last_layer.append(current_node)
                if current_node.winner is not None:
                    terminal_nodes.append(current_node)
        new_layer_nodes = self.create_new_layer(last_layer)
        for current_node in new_layer_nodes:
            if current_node.winner is not None:
                terminal_nodes.append(current_node)
        second_new_layer_nodes = self.create_new_layer(new_layer_nodes)
        terminal_nodes += second_new_layer_nodes
        self.terminal_nodes = terminal_nodes
        self.root = node_dict[tuple(starting_game_state)]
        self.node_dict = node_dict

    def prune_tree(self, new_state):
        new_node = self.node_dict[tuple(new_state)]
        node_dict = {tuple(new_state): new_node}
        for current_board_state in self.node_dict:
            current_node = self.node_dict[current_board_state]
            index_of_all_filled_in_spaces_of_first_node = [
                i for i in range(9) if new_node.state[i] != 0]
            is_a_possible_child = True
            for i in index_of_all_filled_in_spaces_of_first_node:
                if new_node.state[i] == current_node.state[i]:
                    is_a_possible_child = True
                else:
                    is_a_possible_child = False
                    break
            if is_a_possible_child is False:
                for child_node in current_node.children:
                    child_node.parents.remove(current_node)
                for parent_node in current_node.parents:
                    parent_node.children.remove(current_node)
                continue

            node_dict[tuple(current_board_state)] = current_node

        self.node_dict = node_dict

    def create_new_layer(self, current_layer):
        new_layer_nodes = []
        for current_node in current_layer:
            if current_node.winner is not None:
                continue
            current_board_state = current_node.state
            possible_moves = current_node.possible_moves
            for move in possible_moves:
                new_board_state = list(current_board_state)
                new_board_state[move] = current_node.turn

                if tuple(new_board_state) in self.node_dict:
                    new_node = self.node_dict[tuple(new_board_state)]
                    new_node.parents.append(current_node)
                    new_node.depth = current_node.depth
                    current_node.children.append(new_node)
                else:
                    new_node = Node(new_board_state)
                    new_node.is_terminal_node = True
                    new_node.parents.append(current_node)
                    new_node.depth = current_node.depth
                    current_node.children.append(new_node)
                    self.node_dict[tuple(new_board_state)] = new_node
                    new_layer_nodes.append(new_node)

        return new_layer_nodes

    def possible_moves(self, board_state):
        possible_moves = []
        for i in range(9):
            if board_state[i] == 0:
                possible_moves.append(i)
        return possible_moves
