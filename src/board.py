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
            self.board = generate()

    def print(self):
        for r in range(size):
            print([self.board[r*size + c] for c in range(size)])


def generate_1000():
    file = open("generated/boards_9_recursive.txt", "w")
    for i in range(1000):
        try:
            board = Board()
            file.write(str(board.board) + "\n")
        except IndexError:
            pass

    file.close()


if __name__ == "__main__":
    n = Board(board8)
    n.print()


