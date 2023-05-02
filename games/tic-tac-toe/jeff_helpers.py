def is_end_copy(board):
    for i in range(0, 3):
        if board[3 * i + 0] == board[3 * i + 1] == board[3 * i + 2] != 0:
            return "Player " + str(board[3 * i + 0])
        if board[0 + i] == board[3 + i] == board[6 + i] != 0:
            return "Player " + str(board[0 + i])

    if board[0] == board[4] == board[8] != 0:
        return "Player " + str(board[0])
    if board[2] == board[4] == board[6] != 0:
        return "Player " + str(board[2])

    if 0 not in board:
        return "Tie"
    return False


def possible_moves(board):
    empty_spaces = []
    for i in range(0, len(board)):
        if board[i] == 0:
            empty_spaces.append(i)
    return empty_spaces


def find_all(i, board):
    spaces = []
    for a in range(0, len(board)):
        if board[a] == i:
            spaces.append(a)
    return spaces


def is_almost_end(board):
    empty_spaces = possible_moves(board)
    p_one = []
    p_two = []
    ends = [p_one, p_two]
    # player 1's turn
    for b in range(1, 3):
        for i in empty_spaces:
            tboard = list(board)
            tboard[i] = b
            if is_end_copy(tboard) not in ["Tie", False]:
                ends[b - 1].append(i)
    return ends


def print_board(array):
    a = 1
    board = [0 for i in range(9)]
    for i in array:
        board[i] = a
        a = a % 2 + 1
    print(
        f"{board[0]} {board[1]} {board[2]}\n{board[3]} {board[4]} {board[5]}\n{board[6]} {board[7]} {board[8]}"
    )
    print("")
