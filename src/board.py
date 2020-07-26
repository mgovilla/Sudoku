from src.utils import *
from src.evaluate import *

"""
Board class to hold the Sudoku 
"""
class Sudoku:

    def __init__(self, init=None):
        # Generate the sudoku
        if init is None:
            self.board, self.solution = generate()
        else:
            self.board = init
            self.solution = solve(self.board)

    def print_solution(self):
        # size = int(sqrt(len(self.solution)))
        for r in range(size):
            print([self.solution[r*size + c] for c in range(size)])

    def print_puzzle(self):
        for r in range(size):
            print([self.board[r*size + c] for c in range(size)])


def generate_1000():
    with open("generated/boards_9_wsols.txt", "w") as file:
        for i in range(1000):
            board = Sudoku()
            file.write(str(board.board) + "\n")
            file.write(str(board.solution) + "\n")


def generate_1():
    n = Sudoku()
    n.print_puzzle()
    n.print_solution()


if __name__ == "__main__":
    n = Sudoku(g1)
    n.print_solution()
