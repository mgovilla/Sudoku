import math
import random


class CandidateTable:

    def __init__(self, board):
        self.size = int(math.sqrt(len(board)))
        self.buckets = {i: [] for i in range(self.size + 1)}
        for square in board:
            self.buckets[len(square.candidates)].append(square)

    def update(self, square, prev):
        self.buckets[prev].remove(square)
        self.buckets[len(square.candidates)].append(square)

    def get(self, key):
        return self.buckets.get(key)

    def get_random(self):
        for i in range(2, self.size + 1):
            if len(self.buckets[i]) > 0:
                return random.sample(self.buckets[i], 1)[0]

        return None


class Square:

    # TODO: Replace r and c because they are not useful
    def __init__(self, r, c, candidates, value=None):
        self.coord = (r, c)
        self.candidates = candidates
        self.value = value

    def __eq__(self, other):
        if other.coord == self.coord:
            return True

    def __str__(self):
        if self.value is None:
            return "{ " + str(self.coord[0]) + ", " + str(self.coord[1]) + " : " + str(self.candidates) + " }"
        else:
            return "{ " + str(self.coord[0]) + ", " + str(self.coord[1]) + " : " + str(self.value) + " }"

    def set(self, value):
        self.value = value
        self.candidates.clear()

    def set_random(self):
        self.value = random.sample(self.candidates, 1)[0]
        self.candidates.clear()
        return self.value