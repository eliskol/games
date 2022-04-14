from random import randrange


def ben_strat(board):
    move = 0
    if board[2] == board[6] != 0 and board[4] == 0:
        move = 4
    elif board[2] == board[4] != 0 and board[6] == 0:
        move = 6
    elif board[0] == board[1] != 0 and board[2] == 0:
        move = 2
    elif board[4] == board[6] != 0 and board[2] == 0:
        move = 2
    elif board[4] == board[8] != 0 and board[0] == 0:
        move = 0
    elif board[0] == board[2] != 0 and board[1] == 0:
        move = 1
    elif board[1] == board[2] != 0 and board[0] == 0:
        move = 0
    elif board[3] == board[4] != 0 and board[5] == 0:
        move = 5
    elif board[3] == board[5] != 0 and board[4] == 0:
        move = 4
    elif board[4] == board[5] != 0 and board[3] == 0:
        move = 3
    elif board[6] == board[7] != 0 and board[8] == 0:
        move = 8
    elif board[6] == board[8] != 0 and board[7] == 0:
        move = 7
    elif board[7] == board[8] != 0 and board[6] == 0:
        move = 6
    elif board[0] == board[3] != 0 and board[6] == 0:
        move = 6
    elif board[0] == board[6] != 0 and board[3] == 0:
        move = 3
    elif board[3] == board[6] != 0 and board[0] == 0:
        move = 0
    elif board[1] == board[4] != 0 and board[7] == 0:
        move = 7
    elif board[1] == board[7] != 0 and board[4] == 0:
        move = 4
    elif board[4] == board[7] != 0 and board[1] == 0:
        move = 1
    elif board[2] == board[5] != 0 and board[8] == 0:
        move = 8
    elif board[2] == board[8] != 0 and board[5] == 0:
        move = 5
    elif board[5] == board[8] != 0 and board[2] == 0:
        move = 2
    elif board[0] == board[4] != 0 and board[8] == 0:
        move = 8
    elif board[0] == board[8] != 0 and board[4] == 0:
        move = 4
    elif board[4] == 0:
        move = 4
    elif board[0] == 0:
        move = 0
    elif board[2] == 0:
        move = 2
    elif board[5] == 0:
        move = 5
    elif board[1] == 0:
        move = 1
    elif board[6] == 0:
        move = 6
    elif board[8] == 0:
        move = 8
    return move
