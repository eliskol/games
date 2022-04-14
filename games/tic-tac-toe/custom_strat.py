import random
from random_player import RandomPlayer
from player import Player
from tic_tac_toe import Game


def strategy(board):

    player_number = 2

    if board == [0 for _ in range(9)]:
        player_number = 1
    

    for j in range(3):
        i = 3 * j
        if board[j] == board[j + 3] != 0 and board[j + 6] == 0:  # columns
            return j + 6
        elif board[j] == board[j + 6] != 0 and board[j + 3] == 0:
            return j + 3
        elif board[j + 3] == board[j + 6] != 0 and board[j] == 0:
            return j
        elif board[i] == board[i + 1] != 0 and board[i + 2] == 0:  # rows
            return i + 2
        elif board[i] == board[i + 2] != 0 and board[i + 1] == 0:
            return i + 1
        elif board[i + 1] == board[i + 2] != 0 and board[i] == 0:
            return i

    if board[0] == board[4] != 0 and board[8] == 0:  # diagonal
        return 8
    elif board[4] == board[8] != 0 and board[0] == 0:
        return 0
    elif board[0] == board[8] != 0 and board[4] == 0:
        return 4
    elif board[2] == board[4] != 0 and board[6] == 0:  # anti-diagonal
        return 6
    elif board[2] == board[6] != 0 and board[4] == 0:
        return 4
    elif board[4] == board[6] != 0 and board[2] == 0:
        return 2

    if player_number == 1:

        if board == [0 for _ in range(9)]:
            return 4
        if board[0] == 0:
            return 0
        elif board[2] == 0:
            return 2
        elif board[6] == 0:
            return 6
        elif board[8] == 0:
            return 8

    if player_number == 2:

        if board[4] == 0:
            return 4
        elif board[1] == 0:
            return 1
        elif board[3] == 0:
            return 3
        elif board[5] == 0:
            return 5
        elif board[7] == 0:
            return 7



    random_move = random.randrange(0, 9)
    while board[random_move] != 0:
        random_move = random.randrange(0, 9)
    return random_move

