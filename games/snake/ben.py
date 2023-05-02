class BenStrat:
    def choose_move(self, board):
        if "e" in board[9]:
            if board[9][9] == "e":
                return "w"
            else:
                return "d"
        if "e" in board[0]:
            for i in range(0, 10):
                if i % 2 == 0:
                    if board[0][i] == "e":
                        return "s"
                elif i % 2 == 1:
                    if board[0][i] == "e":
                        return "a"
        for row in board[:-2]:
            if row[0] == "e":
                return "s"
            elif row[2] == "e":
                return "s"
            elif row[4] == "e":
                return "s"
            elif row[6] == "e":
                return "s"
            elif row[8] == "e":
                return "s"
        for row in board[1:-1]:
            if row[1] == "e":
                return "w"
            elif row[3] == "e":
                return "w"
            elif row[5] == "e":
                return "w"
            elif row[7] == "e":
                return "w"
            elif row[9] == "e":
                return "w"
        if board[8][0] == "e":
            return "s"
        if "e" in board[8]:
            for i in range(1, 10):
                if i % 2 == 0:
                    if board[8][i] == "e":
                        return "a"
                if i % 2 == 1:
                    if board[8][i] == "e":
                        return "w"
