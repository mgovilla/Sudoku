import unittest
from src.CandidateTable import *
from src.utils import *


class TestCandidates(unittest.TestCase):
    def test_square(self):
        d = {1: [1, 2, 3]}
        print(len(d.get(0)))

    def test_list_squares(self):
        bucket4 = [Square(1, 1, [1, 2, 3, 4]), Square(2, 1, [1, 2, 3, 4]), Square(2, 2, [1, 2, 3, 4])]
        d = {i: [] for i in range(5)}
        d[4] = bucket4

        updated = Square(2, 1, [1, 2, 4])
        d[4].remove(updated)
        print(d)


if __name__ == '__main__':
    unittest.main()
