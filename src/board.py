from src.utils import *

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
    file = open("boards_16.txt", "w")
    for i in range(1000):
        n = Board()
        if n.board.count(0) == 0:
            file.write(str(n.board) + "\n")

    file.close()


if __name__ == "__main__":
    ex = [0, 4, 0, 6, 3, 0, 0, 8, 0,
          0, 8, 2, 0, 0, 9, 6, 0, 0,
          0, 0, 0, 0, 0, 5, 0, 0, 4,
          0, 0, 1, 0, 0, 0, 3, 6, 0,
          0, 0, 4, 0, 0, 0, 8, 0, 0,
          0, 7, 9, 0, 0, 0, 4, 0, 0,
          7, 0, 0, 9, 0, 0, 0, 0, 0,
          0, 0, 6, 4, 0, 0, 2, 5, 0,
          0, 2, 0, 0, 5, 6, 0, 3, 0]

    n = Board(ex)
    n.print()


