import random


class CustomPlayer:
    def __init__(self):
        self.player_num = None
        self.opp_player_num = None


    def find_player_num(self, state):
        return 1 if sum(i.count(1) for i in state) == sum(i.count(2) for i in state) else 2

    def find_opponent_player_num(self, state):
        return 2 if sum(i.count(1) for i in state) == sum(i.count(2) for i in state) else 1




    def choose_move(self, board):
        # board = [state[i:i+7] for i in range(0,42,7)]
        columns = get_columns(board)
        self.player_num = self.find_player_num(board)
        self.opp_player_num = self.find_opponent_player_num(board)
        open_spaces = check_for_open_spaces(board)
        best_spot = random.choices(open_spaces)[0]
        best_score = 0

        if self.player_num == 1:
            for space in open_spaces:
                current_board = board.copy()
                score = score_position(current_board, self.player_num, self.opp_player_num)
                if score > best_score:
                    best_score = score
                    best_spot = space


        if self.player_num == 2:
            for space in open_spaces:
                current_board = board.copy()
                for r in range(6):
                    for c in range(4):
                        window = board[c:c+4]
                        score = evaluate_window(current_board, window, self.player_num, self.opp_player_num)
                        if score > best_score:
                            best_score = score
                            best_spot = space

            if board[0][6] == board[1][6] == board[2][6] == self.player_num:
                if (3,6) in open_spaces:
                    best_spot = (3,6)
            elif board[0][5] == board[1][5] == board[2][5] == self.player_num:
                if (3,5) in open_spaces:
                    best_spot = (3,5)
            elif board[0][4] == board[1][4] == board[2][4] == self.player_num:
                if (3,4) in open_spaces:
                    best_spot = (3,4)
            elif board[0][3] == board[1][3] == board[2][3] == self.player_num:
                if (3,3) in open_spaces:
                    best_spot = (3,3)
            elif board[0][2] == board[1][2] == board[2][2] == self.player_num:
                if (3,2) in open_spaces:
                    best_spot = (3,2)
            elif board[0][1] == board[1][1] == board[2][1] == self.player_num:
                if (3,1) in open_spaces:
                    best_spot = (3,1)
            elif board[0][0] == board[1][0] == board[2][0] == self.player_num:
                if (3,0) in open_spaces:
                    best_spot = (3,0)
            elif board[0][6] == board[0][5] == board[0][4] == self.player_num:
                if (0,3) in open_spaces:
                    best_spot = (0,3)
            elif board[0][5] == board[0][4] == board[0][3] == self.player_num:
                if (0,2) in open_spaces:
                    best_spot = (0,2)
                elif (0,6) in open_spaces:
                    best_spot = (0,6)
            elif board[0][4] == board[0][3] == board[0][2] == self.player_num:
                if (0,1) in open_spaces:
                    best_spot = (0,1)
                elif (0,5) in open_spaces:
                    best_spot = (0,5)
            elif board[0][3] == board[0][2] == board[0][1] == self.player_num:
                if (0,0) in open_spaces:
                    best_spot = (0,0)
                elif (0,4) in open_spaces:
                    best_spot = (0,4)
            elif board[0][2] == board[0][1] == board[0][0] == self.player_num:
                if (0,3) in open_spaces:
                    best_spot = (0,3)



        return best_spot







def evaluate_window(board, window, player_num, opp_player_num):
    score = 0
    if window.count(player_num) == 4:
        score += 100
    elif window.count(opp_player_num) == 3 and window.count(0) == 1:
        score += 80
    elif window.count(player_num) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(player_num) == 2 and window.count(0) == 2:
        score += 5
    elif player_num == 2:
        columns = get_columns(board)
        center_array = [columns[2], columns[3], columns[4]]
        center_count = sum(i.count(player_num) for i in center_array)
        score += center_count * 6

    return score



def score_position(board, player_num, opp_player_num):
    score = 0
    columns = get_columns(board)
    center_array = [columns[2], columns[3], columns[4]]
    center_count = sum(i.count(player_num) for i in center_array)
    score = center_count * 6

    for r in range(6):
        for c in range(4):
            window = board[c:c+4]
            new_score = evaluate_window(board, window, player_num, opp_player_num)
            if new_score > score:
                score = new_score

    for c in range(7):
        columns = get_columns(board)
        for r in range(3):
            window = columns[r:r+4]
            new_score = evaluate_window(board, window, player_num, opp_player_num)
            if new_score > score:
                score = new_score

    for r in range(3):
        for c in range(4):
            window = [board[r+i][c+i] for i in range(4)]
            new_score = evaluate_window(board, window, player_num, opp_player_num)
            if new_score > score:
                score = new_score

    for r in range(3):
        for c in range(4):
            window = [board[r+3-i][c+i] for i in range(4)]
            new_score = evaluate_window(board, window, player_num, opp_player_num)
            if new_score > score:
                score = new_score


    return score



def check_for_open_spaces(board):
    columns = get_columns(board)
    open_spaces = []
    for column in columns:
        index_of_zero = get_index_of_zero(column)
        if index_of_zero is not False:
            open_spaces.append((column.index(0), columns.index(column)))
            # (how high it is (the row), which column)

    return open_spaces


def get_index_of_zero(column):
    zeroes = 0
    for num in column:
        if num == 0:
            zeroes += 1
            return column.index(0)
            break
    if zeroes == 0:
        return False


def get_columns(board):
    columns = [[board[i][j] for i in range(6)] for j in range(7)]
    for column in columns:
        column = reversed(column)
    return columns