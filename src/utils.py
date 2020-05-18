import math
import random

"""
We will be using a backtracking algorithm to create a board
(It is essentially the same as the solving algorithm) 
"""
size = 4
n = int(math.sqrt(size))


def generate(board, empty):
    if len(empty) == 0:
        return board
    # Choose a random position to enter the number
    pos = random.sample(empty, 1)[0]
    empty.remove(pos)  # Remove that position

    # Figure out which numbers can be added to the position
    numbers = [i + 1 for i in range(size)]  # Assume all of them can
    possible = []
    for p in numbers:
        if valid(p, (int(pos / size), pos % size), board):
            possible.append(p)
    # Possible is a cleaned array of possible values
    # If it is empty, there are no possible values in the square which means the puzzle is invalid
    if len(possible) == 0:
        return None

    # Shuffle the values
    random.shuffle(possible)

    for num in possible:
        board[pos] = num
        newboard = generate(board, empty)
        if newboard is not None:
            return newboard
    # If the board that is returned is None, then try a different number in the position
    return None
    # If no numbers can be added in the box, this must be an impossible structure return as is


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
    b = [0] * size**2
    e = [i for i in range(size)]

    print(generate(b, e))
