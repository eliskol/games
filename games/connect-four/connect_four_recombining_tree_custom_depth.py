import time


# todo: update generate_tree_using_cache
# note: getting "ghost" games appearing -- have no parents, and technically impossible game states:
# e.g. [[1, 2, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
# how to get rid of ghost games: rewrite prune_tree to use a traversal starting at the new game state
# instead of using the template method
# (template method doesn't account for previous moves determining future moves)


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
            self.turn = 1 if sum(row.count(1) for row in self.state) == sum(row.count(2) for row in self.state) else 2
        else:
            self.turn = None
        self.children = []
        self.parents = []
        self.possible_moves = self.find_possible_moves()
        self.is_terminal_node = False  # false by default, gets set to true during tree generation

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
        self.generate_tree(first_game_state, n)

    def generate_tree(self, first_game_state, n):
        start_time = time.time()
        first_node = Node(first_game_state)
        first_node.depth = 0
        created_game_states = {self.deeptuple(first_game_state): first_node}
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
                new_board_state = self.deeplist(dequeued_node_board_state)
                new_board_state = self.drop_token(next_player, new_board_state, move)

                if self.deeptuple(new_board_state) in created_game_states:
                    new_node = created_game_states[self.deeptuple(new_board_state)]
                    new_node.parents.append(dequeued_node)
                    dequeued_node.children.append(new_node)

                else:
                    new_node = Node(new_board_state)
                    new_node.depth = dequeued_node.depth + 1
                    new_node.parents.append(dequeued_node)
                    dequeued_node.children.append(new_node)
                    queue.enqueue(new_node)
                    created_game_states[self.deeptuple(new_board_state)] = new_node

        #         print(a_variable)
        # print('finished generating!')
        # print(time.time() - start_time)
        # print(leaf_node_count)
        self.root = first_node
        self.node_dict = created_game_states
        self.terminal_nodes = terminal_nodes
        # print((0 for _ in range(9)) in self.node_dict)

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
        self.root = node_dict[self.deeptuple(starting_game_state)]
        self.node_dict = node_dict

    def prune_tree(self, template_state):
        template_node = self.node_dict[self.deeptuple(template_state)]
        node_dict = {self.deeptuple(template_state): template_node}
        queue = Queue([template_node])

        while queue.contents != []:



        self.node_dict = node_dict

    def create_new_layer(self, current_layer):
        new_layer_nodes = []
        for current_node in current_layer:
            if current_node.winner is not None:
                continue
            current_board_state = current_node.state
            possible_moves = current_node.possible_moves
            for move in possible_moves:
                new_board_state = self.deeplist(current_board_state)
                new_board_state = self.drop_token(current_node.turn, new_board_state, move)

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
                    self.node_dict[self.deeptuple(new_board_state)] = new_node
                    new_layer_nodes.append(new_node)

        return new_layer_nodes

    def find_possible_moves(self):
        possible_moves = []
        for i in range(7):
            if self.check_move_validity(i):
                possible_moves.append(i)
        return possible_moves

    def drop_token(self, player: int, board, column) -> list:
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


i = 5
bruh = ConnectFourRecombiningTreeCustomDepth([[0 for _ in range(7)]
                                              for _ in range(6)], i)
print('depth of ', i, 'has', len(bruh.node_dict), 'nodes')
game_state = [[0 for _ in range(7)] for _ in range(5)]
game_state.insert(0, [1, 2, 0, 0, 0, 0, 0])
bruh.generate_tree_using_cache(game_state)

print(len(bruh.node_dict))

bruh2 = ConnectFourRecombiningTreeCustomDepth(game_state, 5)
print(len(bruh2.node_dict))

for game_state_tuple in bruh.node_dict:
    if game_state_tuple not in bruh2.node_dict:
        for row in game_state_tuple[::-1]:
            print(row)
        print()