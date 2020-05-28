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


def solve(board):
    # Initialization with the input board
    squares = [Square(int(i / size), i % size, numbers.copy()) for i in range(len(board))]

    for i in range(len(board)):
        num = board[i]
        if num > 0:
            squares[i].set(num)
            update_related(squares, squares[i])

    candtable = CandidateTable(squares)

    restricted = candtable.get(1)
    while len(restricted) > 0:
        s = restricted[0]
        s.set_random()
        candtable.update(s, 1)
        update_related(squares, s, candtable)
        restricted = candtable.get(1)

    return squares_to_board(squares)


def generate(board):
    # Create the candidate hashtable, every square is empty
    squares = [Square(int(i / size), i % size, numbers.copy()) for i in range(len(board))]

    for i in range(len(board)):
        num = board[i]
        if num > 0:
            squares[i].set(num)
            update_related(squares, squares[i])

    candtable = CandidateTable(squares)

    # repeat until the candidate hashtable is empty
    while len(candtable.get(0)) < size ** 2:
        # Choose random position in the smallest non-empty chain
        square = candtable.get_random()

        if square is None:
            break

        # Assign the value randomly
        length = len(square.candidates)
        square.set_random()
        # update squares[] maybe
        candtable.update(square, length)

        # Go through related squares
        update_related(squares, square, candtable)

        # Update the candidate table, if any square has only 1 candidate fill it in the board
        restricted = candtable.get(1)
        while len(restricted) > 0:
            s = restricted[0]
            s.set_random()
            candtable.update(s, 1)
            update_related(squares, s, candtable)
            restricted = candtable.get(1)

    return squares_to_board(squares)


def update_related(squares, square, candtable=None):
    directly_related(squares, square, candtable)
    box_related(squares, square, candtable)


def directly_related(squares, square, candtable=None):
    # Go through col/row/box check if each empty square is the only option for for that col/row/box
    for rel in related_iterator(squares, square):
        # rel is a list of (size - 1) of all squares in col/row/box not including square
        empty = [i for i in rel if i.value is None]

        # With all of the empty squares, get the frequency for each candidate
        frequency = [0] * size
        for e in empty:
            # remove the square's value from the candidates list if it's there
            try:
                length = len(e.candidates)
                e.candidates.remove(square.value)
                if candtable is not None: candtable.update(e, length)
            except ValueError: pass  # Do nothing because we have already seen the square

            for num in e.candidates:
                frequency[num - 1] += 1

        # If a number only appears once, then the box with it must take that value
        constrained = [i + 1 for i in range(size) if frequency[i] == 1]
        for con in constrained:
            for e in empty:
                if e.candidates.count(con) > 0:
                    length = len(e.candidates)
                    e.candidates = [con]
                    if candtable is not None: candtable.update(e, length)


def box_related(squares, square, candtable=None):
    # TODO: Stop trying to remove candidates from boxes that contain the value
    # TODO: Revisit Logic to make it more clear

    # Maybe look at all the unrelated boxes, and the ones with the same value, look at the intersection box
    # (can be only one) to see if the empty squares with the value as candidate are in the same row/col
    box_coord = (int(square.coord[0] / n), int(square.coord[1] / n))
    others = unrelated_boxes(squares, square)
    possible = []
    for o in others:
        p1, p2 = (o[0], box_coord[1]), (box_coord[0], o[1])
        i1, i2 = index_of(possible, p1), index_of(possible, p2)

        if i1 == -1: possible.append(p1)
        if i2 == -1: possible.append(p2)

    for pos in possible:
        box = [squares[int(x / n) * size + (x % n) + n * (pos[1] + size * pos[0])] for x in range(size)]
        empty = [i for i in box if i.candidates.count(square.value) > 0]

        if len(empty) == 1:
            length = len(empty[0].candidates)
            empty[0].candidates = [square.value]
            if candtable is not None: candtable.update(empty[0], length)
        elif len(empty) > 1:
            # Check if the n squares with the value share n
            frequency = [0]*size
            for sq in box:
                for num in sq.candidates:
                    frequency[num - 1] += 1

            k = frequency[square.value - 1]
            possible = [i+1 for i in range(len(frequency)) if frequency[i] == k]
            actual = []
            for p in possible:
                hasall = True
                for e in empty:
                    if e.candidates.count(p) == 0:
                        hasall = False
                        break
                if hasall: actual.append(p)

            removed = []
            if len(actual) == k:
                for e in empty:
                    length = len(e.candidates)
                    removed += [x for x in e.candidates if actual.count(x) == 0 and removed.count(x) == 0]
                    e.candidates = actual.copy()
                    if candtable is not None: candtable.update(e, length)

            # Check if they are in the same row/col to remove
            removed.append(square.value)
            for num in removed:
                empty = [i for i in box if i.candidates.count(num) > 0]
                if len(empty) == 0: break
                row = empty[0].coord[0]
                col = empty[0].coord[1]
                same_row, same_col = True, True
                for e in range(1, len(empty)):
                    if same_row and row != empty[e].coord[0]: same_row = False
                    if same_col and col != empty[e].coord[1]: same_col = False

                if same_row:
                    for i in range(size-n):
                        tempc = (((col//n)+1)*n + i) % size
                        s = squares[row*size + tempc]
                        try:
                            length = len(s.candidates)
                            s.candidates.remove(num)
                            if candtable is not None: candtable.update(s, length)
                        except ValueError: pass

                if same_col:
                    for i in range(size-n):
                        tempr = (((row//n)+1)*n + i) % size
                        s = squares[tempr*size + col]
                        try:
                            length = len(s.candidates)
                            s.candidates.remove(num)
                            if candtable is not None: candtable.update(s, length)
                        except ValueError: pass


def index_of(arr, item):
    for i in range(len(arr)):
        if arr[i] == item:
            return i

    return -1


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


def related_boxes(squares, square):
    boxr, boxc = int(square.coord[0] / n), int(square.coord[1] / n)
    boxes = []

    for j in range(n):
        box = [squares[int(x / n) * size + (x % n) + n * (j + size * boxr)] for x in range(size)]
        if j != boxc: boxes.append(box)

    for j in range(n):
        box = [squares[int(x / n) * size + (x % n) + n * (boxc + size * j)] for x in range(size)]
        if j != boxr: boxes.append(box)

    return boxes


def unrelated_boxes(squares, square):
    boxr, boxc = int(square.coord[0] / n), int(square.coord[1] / n)
    boxes = []
    for r in range(1, n):
        nextr = (boxr + r) % n
        for c in range(1, n):
            nextc = (boxc + c) % n
            for x in range(size):
                if squares[int(x / n) * size + (x % n) + n * (nextc + size * nextr)].value == square.value:
                    boxes.append((nextr, nextc))
                    break

    return boxes


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


def shuffle(arr):
    for i in reversed(range(size)):
        index = random.randint(0, i)
        arr[index], arr[i] = arr[i], arr[index]

    return arr
