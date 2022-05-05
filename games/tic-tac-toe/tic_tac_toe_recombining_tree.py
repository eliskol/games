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


class TicTacToeRecombiningTree:
    def __init__(self):
        self.generate_tree()

    def generate_tree(self):
        start_time = time.time()
        first_node = Node([0 for _ in range(9)])
        created_game_states = {tuple(first_node.state): first_node}

        queue = Queue([first_node])
        a_variable = 1

        while queue.contents != []:

            dequeued_node = queue.dequeue()

            if dequeued_node.winner is not None:
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
                    new_node.parents.append(dequeued_node)
                    dequeued_node.children.append(new_node)
                    queue.enqueue(new_node)
                    created_game_states[tuple(new_board_state)] = new_node



                print(a_variable)
        print('finished generating!')
        print(time.time() - start_time)
        self.root = first_node

    def possible_moves(self, board_state):
        possible_moves = []
        for i in range(9):
            if board_state[i] == 0:
                possible_moves.append(i)
        return possible_moves


bruh = TicTacToeRecombiningTree()
leaf_node_count = 0
root_node = bruh.root
queue = Queue([root_node])
while queue.contents != []:
    current_node = queue.dequeue()
    for child_node in current_node.children:
        if child_node.children == []:
            leaf_node_count += 1
        # print(leaf_node_count)
        queue.enqueue(child_node)
print(leaf_node_count)
