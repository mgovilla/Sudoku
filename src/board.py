from src.utils import *

"""
Board class to hold the Sudoku 
"""


class Board:

    def __init__(self):
        # Generate the sudoku
        self.board = generate([0] * size ** 2)

    def print(self):
        for r in range(size):
            print([self.board[r*size + c] for c in range(size)])


if __name__ == "__main__":
    file = open("boards_16.txt", "w")
    for i in range(1000):
        n = Board()
        if n.board.count(0) == 0:
            file.write(str(n.board) + "\n")

    file.close()
