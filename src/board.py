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
    n = Board()
    n.print()
