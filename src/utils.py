import math
import random
from src.CandidateTable import *

"""
We will be using a backtracking algorithm to create a board
(It is essentially the same as the solving algorithm) 
"""
size = 9
n = int(math.sqrt(size))
numbers = [i + 1 for i in range(size)]  # List of the possible numbers


def generate(board):
    # Create the candidate hashtable, every square is empty
    squares = [Square(int(i / size), i % size, numbers.copy()) for i in range(len(board))]

    for i in range(len(board)):
        num = board[i]
        if num > 0:
            squares[i].set(num)

    candtable = CandidateTable(squares)

    for g in candtable.get(0):
        rules(squares, candtable, g, g.value)

    for g in candtable.get(0):
        elimination(squares, candtable, g)

    # repeat until the candidate hashtable is empty
    while len(candtable.get(0)) < size ** 2:
        # Choose random position in the smallest non-empty chain
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

    return squares_to_board(squares)


def update_related(squares, candtable, square, num):
    rules(squares, candtable, square, num)
    elimination(squares, candtable, square)


def rules(squares, candtable, square, num):
    for c in related_iterator(squares, square):
        for s in c:
            try:
                length = len(s.candidates)
                s.candidates.remove(num)
                candtable.update(s, length)

            except ValueError:
                pass  # Do nothing because we have already seen the square


def elimination(squares, candtable, square):
    # TODO: Extend to look at related boxes (to solve board 3)
    # Go through col/row/box check if each empty square is the only option for for that col/row/box
    for rel in related_iterator(squares, square):
        # rel is a list of (size - 1) of all squares in col/row/box
        empty = [i for i in rel if i.value is None]
        if square.value is None: empty.append(square)
        frequency = [0] * size

        for e in empty:
            for num in e.candidates:
                frequency[num - 1] += 1

        constrained = [i + 1 for i in range(size) if frequency[i] == 1]
        for con in constrained:
            for e in empty:
                if e.candidates.count(con) > 0:
                    length = len(e.candidates)
                    e.candidates = [con]
                    candtable.update(e, length)


"""
Returns an iterator of length 3 with each element being a list (size - 1)
of squares in the column, row, then box respectively 
"""


def related_iterator(squares, square):
    cols, rows, boxs = [], [], []
    for j in range(size):
        col = squares[j * size + square.coord[1]]
        row = squares[square.coord[0] * size + j]

        boxr, boxc = int(square.coord[0] / n), int(square.coord[1] / n)
        box = squares[int(j / n) * size + (j % n) + n * (boxc + size * boxr)]

        if col != square: cols.append(col)
        if row != square: rows.append(row)
        if box != square: boxs.append(box)

    return [cols, rows, boxs]


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
    return generate(board)


def shuffle(arr):
    for i in reversed(range(size)):
        index = random.randint(0, i)
        arr[index], arr[i] = arr[i], arr[index]

    return arr


if __name__ == '__main__':
    b = [0] * size ** 2
    reg = generate(b)
