from src.utils import *

"""
Board class to hold the Sudoku 
"""


class Board:
    board = [0] * size ** 2
    empty = []

    def __init__(self):
        # Generate the sudoku
        for i in range(size ** 2):
            self.empty.append(i)

        self.board = generate(self.board, self.empty)

    def print(self):
        for r in range(size):
            print([self.board[r*size + c] for c in range(size)])


if __name__ == "__main__":
    n = Board()
    n.print()
