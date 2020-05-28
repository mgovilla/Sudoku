import unittest
from src.board import *


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

    def initialize(self, board):
        self.squares = [Square(int(i / size), i % size, numbers.copy()) for i in range(len(board))]

        for i in range(len(board)):
            num = board[i]
            if num > 0:
                self.squares[i].set(num)
                update_related(self.squares, self.squares[i])

        self.candtable = CandidateTable(self.squares)

    def test_rules(self):
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.initialize(board)
        square = self.squares[31]
        square.set(5)
        self.candtable.update(square, 9)
        rules(self.squares, square, self.candtable)

        flag = True
        for rel in related_iterator(self.squares, square):
            for square in rel:
                if square.candidates != [1, 2, 3, 4, 6, 7, 8, 9]:
                    flag = False

        self.assertTrue(flag)

    def test_elimination_row(self):
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 5, 0, 0, 0, 0,
                 2, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 5, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.initialize(board)
        square = self.squares[37]
        length = len(square.candidates)
        square.set(1)
        self.candtable.update(square, length)
        directly_related(self.squares, square, self.candtable)

        self.assertEquals(self.squares[38].candidates, [5])

    def test_elimination_col(self):
        board = [0, 0, 0, 0, 0, 2, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 5, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 5, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.initialize(board)
        square = self.squares[14]
        length = len(square.candidates)
        square.set(1)
        self.candtable.update(square, length)
        directly_related(self.squares, square, self.candtable)

        self.assertEquals(self.squares[23].candidates, [5])

    def test_elimination_box(self):
        board = [0, 0, 0, 3, 0, 0, 0, 0, 0,
                 0, 0, 0, 4, 0, 0, 0, 0, 0,
                 5, 0, 0, 6, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 5, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.initialize(board)
        square = self.squares[5]
        length = len(square.candidates)
        square.set(1)
        self.candtable.update(square, length)
        directly_related(self.squares, square, self.candtable)

        self.assertEquals(self.squares[14].candidates, [5])

    def test_elimination_fail1(self):
        board = [0, 0, 0, 3, 0, 1, 0, 0, 0,
                 0, 0, 0, 4, 0, 0, 0, 0, 0,
                 0, 0, 0, 6, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 5, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.initialize(board)
        square = self.squares[18]
        length = len(square.candidates)
        square.set(5)
        self.candtable.update(square, length)
        directly_related(self.squares, square, self.candtable)

        self.assertNotEqual(self.squares[14].candidates, [5])

    def test_elimination_fail2(self):
        board = [0, 0, 0, 3, 0, 0, 0, 0, 0,
                 0, 0, 0, 4, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 5, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.initialize(board)
        square = self.squares[31]
        length = len(square.candidates)
        square.set(5)
        self.candtable.update(square, length)
        directly_related(self.squares, square, self.candtable)

        self.assertNotEquals(self.squares[21].candidates, [5])

    def test_boxrules_row(self):
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 2, 1, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 5, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.initialize(board)
        square = self.squares[31]
        length = len(square.candidates)
        square.set(5)
        self.candtable.update(square, length)
        box_related(self.squares, square, self.candtable)

        self.assertEquals(self.squares[38].candidates, [5])

    def test_boxrules_col(self):
        board = [0, 0, 0, 0, 0, 2, 0, 0, 0,
                 0, 0, 0, 0, 0, 1, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 5, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.initialize(board)
        square = self.squares[31]
        length = len(square.candidates)
        square.set(5)
        self.candtable.update(square, length)
        box_related(self.squares, square, self.candtable)

        self.assertEquals(self.squares[23].candidates, [5])

    def test_board_generation(self):
        example = Board()
        example.print()

    def test_generate_many(self):
        generate_1000()


if __name__ == '__main__':
    unittest.main()
