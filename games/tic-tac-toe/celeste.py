import random


def is_board_empty(board):
    return board.count(board[0]) == len(board)


def is_move_possible(board):
    possible = []
    for i in range(len(board)):
        if board[i] != 0:
            possible.append(i)
    return possible


def celeste_strat(board):
    possible = is_move_possible(board)
    empty = is_board_empty(board)
    move = 0

    # 4
    if board[0] != 0 and board[1] != board[2] != 0:
        move = random.choice(possible)
    elif board[3] != 0 and board[4] != 0 and board[5] != 0:
        move = random.choice(possible)

    elif board[6] != 0 and board[7] != 0 and board[8] != 0:
        move = random.choice(possible)

    elif board[0] != 0 and board[3] != 0 and board[6] != 0:
        move = random.choice(possible)

    elif board[1] != 0 and board[4] != 0 and board[7] != 0:
        move = random.choice(possible)

    elif board[2] != 0 and board[5] != 0 and board[8] != 0:
        move = random.choice(possible)

    elif board[0] != 0 and board[4] != 0 and board[8] != 0:
        move = random.choice(possible)

    elif board[2] != 0 and board[4] != 0 and board[6] != 0:
        move = random.choice(possible)

    elif board[3] == board[5] != 0 and board[4] == 0:
        move = 4
    elif board[1] == board[7] != 0 and board[4] == 0:
        move = 4
    elif board[2] == board[6] != 0 and board[4] == 0:
        move = 4
    # 0
    elif board[1] == board[2] != 0 and board[0] == 0:
        move = 0
    elif board[3] == board[6] != 0 and board[0] == 0:
        move = 0
    elif board[4] == board[8] != 0 and board[0] == 0:
        move = 0
    elif board[4] == board[6] != 0 and board[0] == 0:
        move = 0
    # 2
    elif board[0] == board[1] != 0 and board[2] == 0:
        move = 2
    elif board[5] == board[8] != 0 and board[2] == 0:
        move = 2
    # 6
    elif board[7] == board[8] != 0 and board[6] == 0:
        move = 6
    elif board[0] == board[3] != 0 and board[6] == 0:
        move = 6
    elif board[2] == board[4] != 0 and board[6] == 0:
        move = 6
    # 8
    elif board[6] == board[7] != 0 and board[8] == 0:
        move = 8
    elif board[2] == board[5] != 0 and board[8] == 0:
        move = 8
    elif board[0] == board[4] != 0 and board[8] == 0:
        move = 8
    # 1
    elif board[0] == board[2] != 0 and board[1] == 0:
        move = 1
    elif board[4] == board[7] != 0 and board[1] == 0:
        move = 1
    # 3
    elif board[4] == board[5] != 0 and board[3] == 0:
        move = 3
    elif board[0] == board[6] != 0 and board[3] == 0:
        move = 3
    # 5
    elif board[3] == board[4] != 0 and board[5] == 0:
        move = 5
    elif board[2] == board[8] != 0 and board[5] == 0:
        move = 5
    # 7
    elif board[6] == board[8] != 0 and board[7] == 0:
        move = 7
    elif board[4] == board[1] != 0 and board[7] == 0:
        move = 7

    elif board[4] == 0:
        move = 4
    elif board[0] == 0:
        move = 0
    elif board[2] == 0:
        move = 2
    elif board[6] == 0:
        move = 6
    elif board[8] == 0:
        move = 8
    elif board[1] == 0:
        move = 1
    elif board[3] == 0:
        move = 3
    elif board[5] == 0:
        move = 5
    elif board[7] == 0:
        move = 7
    return move
