from src.utils import *
from src.evaluate import *
"""
Board class to hold the Sudoku 
"""


class Board:

    def __init__(self, init=None):
        # Generate the sudoku
        if init:
            self.board = solve(init)
        else:
            self.board = generate([0] * size ** 2)

    def print(self):
        for r in range(size):
            print([self.board[r*size + c] for c in range(size)])


def generate_1000():
    file = open("boards_9.txt", "w")
    for i in range(1000):
        n = Board()
        if n.board.count(0) == 0:
            file.write(str(n.board) + "\n")

    file.close()


if __name__ == "__main__":
    n = Board(board3)
    n.print()


