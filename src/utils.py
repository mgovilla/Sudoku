import math
import random
from src.CandidateTable import *

"""
We will be using a backtracking algorithm to create a board
(It is essentially the same as the solving algorithm) 
"""
size = 16
n = int(math.sqrt(size))
numbers = [i + 1 for i in range(size)]  # List of the possible numbers


def generate(board):
    # Create the candidate hashtable, every square is empty
    squares = [Square(int(i / size), i % size, numbers.copy()) for i in range(len(board))]

    for i in range(len(board)):
        num = board[i]
        if num > 0:
            squares[i].set(num)
            pos = squares[i].coord
            for j in range(size):
                try: squares[j * size + pos[1]].candidates.remove(num)
                except ValueError: pass  # Do nothing because its ok

                try: squares[pos[0] * size + j].candidates.remove(num)
                except ValueError: pass  # Do nothing because its ok

                boxr, boxc = int(pos[0] / n), int(pos[1] / n)

                index = int(j / n) * size + (j % n) + n * (boxc + size * boxr)
                try: squares[index].candidates.remove(num)
                except ValueError: pass  # Do nothing because its ok

    candtable = CandidateTable(squares)

    # repeat until the candidate hashtable is empty
    while len(candtable.get(0)) < size ** 2:
        # Choose random position in the smallest non-empty chain
        # TODO: Possibly implement backtracking here 
        square = candtable.get_random()

        if square is None:
            break

        # Assign the value randomly
        length = len(square.candidates)
        num = square.set_random()
        # update squares[] maybe
        candtable.update(square, length)

        # Go through related squares
        update_related(squares, candtable, square, num)

        # Update the candidate table, if any square has only 1 candidate fill it in the board
        restricted = candtable.get(1)
        while len(restricted) > 0:
            s = restricted[0]
            num = s.set_random()
            candtable.update(s, 1)
            update_related(squares, candtable, s, num)
            restricted = candtable.get(1)
            # TODO: Check if setting this causes any issues elsewhere: if so, need to implement backtracking

    return squares_to_board(squares)


def update_related(squares, candtable, square, num):
    for j in range(size):
        col = squares[j * size + square.coord[1]]
        row = squares[square.coord[0] * size + j]

        boxr, boxc = int(square.coord[0] / n), int(square.coord[1] / n)
        box = squares[int(j / n) * size + (j % n) + n * (boxc + size * boxr)]

        if col != square:
            try:
                length = len(col.candidates)
                col.candidates.remove(num)
                candtable.update(col, length)
            except ValueError:
                pass  # Do nothing because its ok

        if row != square:
            try:
                length = len(row.candidates)
                row.candidates.remove(num)
                candtable.update(row, length)
            except ValueError:
                pass  # Do nothing because its ok

        if box != square:
            try:
                length = len(box.candidates)
                box.candidates.remove(num)
                candtable.update(box, length)
            except ValueError:
                pass  # Do nothing because its ok


def squares_to_board(squares):
    board = []
    for s in squares:
        if s.value:
            board.append(s.value)
        else:
            board.append(0)

    return board


def print_board(squares):
    temp = []
    for r in range(size):
        temp.append([squares[r * size + c] for c in range(size)])

    return temp


def valid(num, pos, grid):
    for i in range(size):
        if num == grid[i * size + pos[1]]:
            return False
        if num == grid[pos[0] * size + i]:
            return False

        boxr = int(pos[0] / n)
        boxc = int(pos[1] / n)

        index = int(i / n) * size + (i % n) + n * (boxc + size * boxr)
        if num == grid[index]:
            return False

    return True


def solve(board):
    pass


def shuffle(arr):
    for i in reversed(range(size)):
        index = random.randint(0, i)
        arr[index], arr[i] = arr[i], arr[index]

    return arr


if __name__ == '__main__':
    b = [0] * size ** 2
    reg = generate(b)

