import random


def christine_strat(state):
    board = [state[i : i + 3] for i in range(0, 9, 3)]
    # print(board)

    if sum(x.count(1) for x in board) == sum(y.count(2) for y in board):
        player_num, opp_player_num = 1, 2
    else:
        player_num, opp_player_num = 2, 1

    open_spaces = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                open_spaces.append((i, j))

    rows = board
    cols = [[board[i][j] for i in range(3)] for j in range(3)]
    diags = [[board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]]

    for row_idx, row in enumerate(rows):
        if row.count(player_num) == 2 and row.count(0) == 1:
            return (row_idx, row.index(0))

    for col_idx, col in enumerate(cols):
        if col.count(player_num) == 2 and col.count(0) == 1:
            return (col.index(0), col_idx)

    for diag_idx, diag in enumerate(diags):
        if diag.count(player_num) == 2 and diag.count(0) == 1:
            if diag_idx == 0:
                return (diag.index(0), diag.index(0))
            else:
                return (diag.index(0), 2 - diag.index(0))

    for row_idx, row in enumerate(rows):
        if row.count(opp_player_num) == 2 and row.count(0) == 1:
            return (row_idx, row.index(0))

    for col_idx, col in enumerate(cols):
        if col.count(opp_player_num) == 2 and col.count(0) == 1:
            return (col.index(0), col_idx)

    for diag_idx, diag in enumerate(diags):
        if diag.count(opp_player_num) == 2 and diag.count(0) == 1:
            if diag_idx == 0:
                return (diag.index(0), diag.index(0))
            else:
                return (diag.index(0), 2 - diag.index(0))

    if len(open_spaces) == 8:
        if board[0][0] == 1 and board[1][1] == 0:
            return (1, 1)
        if board[0][2] == 1 and board[1][1] == 0:
            return (1, 1)
        if board[2][0] == 1 and board[1][1] == 0:
            return (1, 1)
        if board[2][2] == 1 and board[1][1] == 0:
            return (1, 1)

    if len(open_spaces) == 7:
        if board[0][0] == 1 and board[0][2] == 2 and board[2][0] == 0:
            return (2, 0)
        if board[0][0] == 1 and board[2][0] == 2 and board[0][2] == 0:
            return (0, 2)
        if board[0][0] == 1 and board[2][2] == 2 and board[0][2] == 0:
            return (0, 2)

    if board[0][0] == player_num and board[1][1] == opp_player_num and board[2][2] == 0:
        return (2, 2)
    if board[0][2] == player_num and board[1][1] == opp_player_num and board[2][0] == 0:
        return (2, 0)
    if board[2][0] == player_num and board[1][1] == opp_player_num and board[0][2] == 0:
        return (0, 2)

    edge_list = [(0, 1), (1, 0), (1, 2), (2, 1)]

    for edge in edge_list:
        if board[edge[0]][edge[1]] != 0:
            edge_list.remove(edge)
    if edge_list != 0:
        if board[0][0] == board[2][2] == opp_player_num:
            return edge_list[0]
        if board[0][2] == board[2][0] == opp_player_num:
            return edge_list[0]

    if player_num == 2 and board[1][1] == 0:
        return (1, 1)

    if (
        board[0][1] == opp_player_num
        and board[1][0] == opp_player_num
        and board[0][2] == 0
    ):
        return (0, 2)
    if (
        board[1][2] == opp_player_num
        and board[2][1] == opp_player_num
        and board[0][2] == 0
    ):
        return (0, 2)
    if (
        board[0][1] == opp_player_num
        and board[1][2] == opp_player_num
        and board[2][0] == 0
    ):
        return (2, 0)
    if (
        board[1][0] == opp_player_num
        and board[2][1] == opp_player_num
        and board[0][2] == 0
    ):
        return (0, 2)

    if board[1][2] == opp_player_num and board[0][0] == 0:
        return (0, 0)
    if board[1][2] == opp_player_num and board[2][0] == 0:
        return (2, 0)
    if board[0][1] == opp_player_num and board[2][0] == 0:
        return (2, 0)
    if board[0][1] == opp_player_num and board[2][2] == 0:
        return (2, 2)
    if board[1][0] == opp_player_num and board[0][2] == 0:
        return (0, 2)
    if board[1][0] == opp_player_num and board[2][2] == 0:
        return (2, 2)
    if board[2][1] == opp_player_num and board[0][0] == 0:
        return (0, 0)
    if board[2][1] == opp_player_num and board[0][2] == 0:
        return (0, 2)

    corner_list = [(0, 0), (0, 2), (2, 2), (2, 0)]

    for corner in corner_list:
        if board[corner[0]][corner[1]] != 0:
            corner_list.remove(corner)
    if len(corner_list) != 0:
        return corner_list[0]

    if board[1][1] == 0:
        return (1, 1)

    return random.choices(open_spaces)[0]
