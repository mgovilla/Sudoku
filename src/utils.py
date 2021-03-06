from math import sqrt
from statistics import mean
from src.CandidateTable import *
import copy

size = 9
n = int(sqrt(size))
numbers = [i + 1 for i in range(size)]  # List of the possible numbers


def generate():
    givens = []
    init_board = random.sample(numbers, size) + [0]*(size*(size - 1))
    squares = [Square(i // size, i % size, numbers.copy()) for i in range(size**2)]
    for i in range(size):
        set_square(squares, squares[i], init_board[i])

    board = squares_to_board(_generate(squares, givens))
    temp = [0]*size**2
    for g in givens:
        temp[g.coord[0]*size + g.coord[1]] = g.value
    return temp, board


def _generate(squares, givens):
    _empty = empty(squares)

    if len(_empty) == 0:
        return squares

    square = random.sample(_empty, 1)[0]
    possible = random.sample(square.candidates, len(square.candidates))
    for num in possible:
        new_board = copy.deepcopy(squares)
        try:
            set_square(new_board, new_board[square.coord[0]*size + square.coord[1]], num)
            generated = _generate(new_board, givens)
            if generated is not None:
                givens.append(new_board[square.coord[0]*size + square.coord[1]])
                return generated
        except IndexError:
            pass

    return None


def empty(squares):
    return [square for square in squares if square.value is None]


def solve(board):
    # Initialization with the input board
    squares = [Square(i // size, i % size, numbers.copy()) for i in range(size**2)]
    valid = True

    for i in range(len(board)):
        num = board[i]
        if num > 0:
            try:
                set_square(squares, squares[i], num)
            except IndexError:
                valid = False

    return squares_to_board(squares)


def set_square(squares, square, num):
    square.value = num
    related = related_iterator(squares, square)
    for rel in range(len(related)):
        for sq in related[rel]:
            # remove the square's value from the candidates list if it's there
            if sq != square:
                remove_candidates(squares, sq, [num], square)

    to_remove = [c for c in square.candidates if c != num]
    remove_candidates(squares, square, to_remove, None)


def remove_candidates(squares, square, candidates, came_from):
    relevant = []
    for num in candidates:
        try:
            square.candidates.remove(num)
            if len(square.candidates) == 1 and square.value is None:
                set_square(squares, square, square.candidates[0])
            relevant.append(num)
        except ValueError:
            pass

    related = related_iterator(squares, square)
    for rel in range(len(related)):
        if came_from is not None and related[rel].count(came_from) > 0: continue
        for r in relevant:
            has_r, rest = [], []
            for sq in related[rel]:
                if sq.candidates.count(r) > 0:
                    has_r.append(sq)
                else:
                    rest.append(sq)

            if len(rest) > n:
                candidate_array = [x.candidates for x in has_r]
                if len(candidate_array) > 0:
                    common = list(set.intersection(*map(set, candidate_array)))

                    # check if any of the values in common exist outside cand_r
                    actual = [c for c in common if not any(c in can.candidates for can in rest)]
                    if len(actual) == len(has_r):
                        # Remove all candidates from squares in has_r except those in actual
                        for sq in has_r:
                            temp = [c for c in sq.candidates if actual.count(c) == 0]
                            remove_candidates(squares, sq, temp, None)

                        for sq in rest:
                            remove_candidates(squares, sq, actual, None)

            unit = []
            # if rel is 2 (they are in the same box) check if the squares are in the same row/col
            if rel == 2:
                row = has_r[0].coord[0]
                col = has_r[0].coord[1]
                same_row, same_col = True, True
                for e in range(1, len(has_r)):
                    if same_row and row != has_r[e].coord[0]: same_row = False
                    if same_col and col != has_r[e].coord[1]: same_col = False

                if same_row:
                    for i in range(size - n):
                        tempc = (((col // n) + 1) * n + i) % size
                        unit.append(squares[row * size + tempc])

                elif same_col:
                    for i in range(size - n):
                        tempr = (((row // n) + 1) * n + i) % size
                        unit.append(squares[tempr * size + col])
            else:  # if rel is 0 or 1 check if the squares with r are in the same box
                box = (has_r[0].coord[0] // n, has_r[0].coord[1] // n)
                same_box = True
                for e in range(1, len(has_r)):
                    if same_box and box != (has_r[e].coord[0] // n, has_r[e].coord[1] // n): same_box = False

                if same_box:
                    # Append all of the squares that are not in the current unit (row/col) to unit
                    if rel == 0:
                        for i in range(size):
                            index = (i // n) * size + (i % n) + n * (box[1] + size * box[0])
                            if index % size != has_r[0].coord[1]:
                                unit.append(squares[index])
                    else:
                        for i in range(size):
                            index = (i // n) * size + (i % n) + n * (box[1] + size * box[0])
                            if index // size != has_r[0].coord[0]:
                                unit.append(squares[index])

            for sq in unit:
                remove_candidates(squares, sq, [r], has_r[0])


def related_iterator(squares, square):
    cols, rows, boxs = [], [], []
    for j in range(size):
        col = squares[j * size + square.coord[1]]
        row = squares[square.coord[0] * size + j]

        boxr, boxc = square.coord[0] // n, square.coord[1] // n
        box = squares[(j // n) * size + (j % n) + n * (boxc + size * boxr)]

        cols.append(col)
        rows.append(row)
        boxs.append(box)

    return [cols, rows, boxs]


def squares_to_board(squares):
    board = []
    for s in squares:
        board.append(s.value if s.value else 0)

    return board


def print_board(squares):
    temp = []
    for row in range(size):
        temp.append([squares[row * size + c] for c in range(size)])

    return temp
