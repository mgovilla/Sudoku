import random


class Square:

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

    def __copy__(self):
        return Square(self.coord[0], self.coord[1], self.candidates, self.value)

    def set(self, value):
        self.value = value

    def random_cand(self):
        return random.sample(self.candidates, 1)[0]
