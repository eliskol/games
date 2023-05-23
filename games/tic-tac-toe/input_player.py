class InputPlayer:
    def choose_move(self, board):
        print(
            f"{board[0]} {board[1]} {board[2]}\n{board[3]} {board[4]} {board[5]}\n{board[6]} {board[7]} {board[8]}"
        )
        print("Please input your move:")
        move = input()
        return int(move)
