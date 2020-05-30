from src.utils import *
from src.evaluate import *
"""
Board class to hold the Sudoku 
"""


class Sudoku:

    def __init__(self, init=None):
        # Generate the sudoku
        # factory = SudokuFactory(9)
        if init is None:
            # self.board = factory.generate()
            self.board = generate()
        else:
            self.board = init

        self.solution = solve(self.board)

        # self.solution = factory.solve(self.board)
        # self.difficulty = factory.difficulty

    def print_solution(self):
        # size = int(sqrt(len(self.solution)))
        for r in range(size):
            print([self.solution[r*size + c] for c in range(size)])

    def print_puzzle(self):
        for r in range(size):
            print([self.board[r*size + c] for c in range(size)])


def generate_1000():
    file = open("generated/boards_9_recursive.txt", "w")
    for i in range(1000):
        board = Sudoku()
        file.write(str(board.solution) + "\n")

    file.close()


if __name__ == "__main__":
    n = Sudoku()
    n.print_puzzle()
    n.print_solution()


