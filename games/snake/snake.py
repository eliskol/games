import random


class Game:
    def __init__(self, player):
        self.player = player
        self.score = 0
        self.snake = [(4, 1), (4, 2), (4, 3)]
        self.board = [[' ' for _ in range(10)] for _ in range(10)]
        self.game_over = False
        self.num_moves = 0
        self.render_snake()
        self.place_berry()

    def render_snake(self):
        for segment in self.snake[:-1]:
            self.board[segment[0]][segment[1]] = 'o'
        snake_head = self.snake[-1]
        self.board[snake_head[0]][snake_head[1]] = 'e'

    def print_board(self):
        for row in reversed(self.board):
            print(row)
        print()

    def place_berry(self):
        random_coords = (random.randrange(0, 10), random.randrange(0, 10))
        while self.board[random_coords[0]][random_coords[1]] != ' ':
            random_coords = (random.randrange(0, 10), random.randrange(0, 10))

        self.board[random_coords[0]][random_coords[1]] = 'b' 
        self.berry = random_coords           

    def check_collision(self, move):
        snake_head_coords = self.snake[-1]
        
        if move == 'a': 
            if snake_head_coords[1] == 0:
                self.game_over = True
                return True
            elif (snake_head_coords[0], snake_head_coords[1] - 1) in self.snake:
                self.game_over = True
                return True

        elif move == 's':
            if snake_head_coords[0] == 0:
                self.game_over = True
                return True
            elif (snake_head_coords[0] - 1, snake_head_coords[1]) in self.snake:
                self.game_over = True
                return True

        elif move == 'w':
            if snake_head_coords[0] == 9:
                self.game_over = True
                return True
            elif (snake_head_coords[0] + 1, snake_head_coords[1]) in self.snake:
                self.game_over = True
                return True

        elif move == 'd':
            if snake_head_coords[1] == 9:
                self.game_over = True
                return True
            elif (snake_head_coords[0], snake_head_coords[1] + 1) in self.snake:
                self.game_over = True
                return True

        return False

    def check_if_game_won(self):
        filled_rows = []
        for row in self.board:
            if ('b' not in row) and (' ') not in row:
                filled_rows.append(None)
        if len(filled_rows == 10):
            self.game_over = True

    def make_move(self):
        snake_head_coords = self.snake[-1]
        last_segment = self.snake.pop(0)
        move = self.player.choose_move(self.board)
        creates_collision = self.check_collision(move)

        if creates_collision is True:
            return self.score
            # print('you died!')
        
        else:
            if move == 'a':
                self.snake.append((snake_head_coords[0], snake_head_coords[1] - 1))
            elif move == 's':
                self.snake.append((snake_head_coords[0] - 1, snake_head_coords[1]))
            elif move == 'd':
                self.snake.append((snake_head_coords[0], snake_head_coords[1] + 1))
            elif move == 'w':
                self.snake.append((snake_head_coords[0] + 1, snake_head_coords[1]))
            else:
                return


        self.board[last_segment[0]][last_segment[1]] = ' '

        if self.snake[-1] == self.berry:
            self.score += 1
            self.place_berry()
            self.snake.insert(0, last_segment)
            # if self.log is True:
                # print('berry eaten!')

        self.render_snake()
        self.num_moves += 1

    def run_game(self, log=False):
        self.log = log
        if self.log is True:
            self.print_board()
        while self.game_over is False:
            self.make_move()
            if self.log is True:
                self.print_board()
        # print('you died!!')
        # print(self.score)
        # print(self.num_moves)
        return {'score': self.score, 'moves': self.num_moves}

from input_strat import InputPlayer
from basic_winner_strat import Winner
import time


totals = {'score': 0, 'moves': 0}
beginning = time.time()
for i in range(1000):
    bruj = Winner()
    bruh = Game(bruj)
    result = bruh.run_game()
    totals['score'] += result['score']
    totals['moves'] += result['moves']
    if i % 50 == 0:
        print(i)
time_taken = time.time() - beginning
print('total time taken:', time_taken)
print('avg time per game:', time_taken / 1000)


averages = {'score': totals['score'] / 1000, 'moves': totals['moves'] / 1000}
print(averages)
print('moves per second:', averages['moves'] / (time_taken / 1000))

# todo -- rewrite rendering function