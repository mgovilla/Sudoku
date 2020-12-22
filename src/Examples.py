import unittest
from src.board import *
from src.dlx import *
from concurrent.futures import ThreadPoolExecutor


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
                set_square(self.squares, self.squares[i], num)

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
        set_square(self.squares, square, 5)

        flag = True
        for rel in related_iterator(self.squares, self.squares[31]):
            for sq in rel:
                if sq != square:
                    if sq.candidates != [1, 2, 3, 4, 6, 7, 8, 9]:
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
        set_square(self.squares, square, 1)

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
        set_square(self.squares, square, 1)

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
        set_square(self.squares, square, 1)

        self.assertEquals(self.squares[14].candidates, [5])

    def test_elimination_compound1(self):
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
        set_square(self.squares, square, 5)

        self.assertEqual(self.squares[14].candidates, [5])

    def test_elimination_compound2(self):
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
        set_square(self.squares, square, 5)

        self.assertEquals(self.squares[21].candidates, [5])

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
        set_square(self.squares, square, 5)

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
        set_square(self.squares, square, 5)

        self.assertEquals(self.squares[23].candidates, [5])

    def test_board_generation(self):
        example = Sudoku()
        example.print_solution()

    def test_generate_many(self):
        generate_1000()

    def test_circularlist(self):
        start = Node(st=0)
        st = start
        for i in range(1, 8):
            st.add_right(Node(st=i))
            st = st.right

        print(start)

    def test_dlx(self):
        k = DLXSudoku(9)
        print(k.generate())
        print(k.generate())

    def test_dlx_many(self):
        k = DLXSudoku(9)
        for _ in range(1000):
            k.generate()

    def test_algx(self):
        headers = [HeaderNode(st=0)]
        # create header row
        n = headers[0]
        for col in range(1, 7):
            n.add_right(HeaderNode(st=col))
            n = n.right
            headers.append(n)

        vals = [(0, [2, 4, 5]), (1, [0, 3, 6]), (2, [1, 2, 5]), (3, [0, 3]), (4, [1, 6]), (5, [3, 4, 6])]
        vals.reverse()
        for i, temp in vals:
            line = iter(temp)
            val = next(line)
            n = Node(headers[val], (val, i))
            headers[val].add_down(n)
            headers[val].value += 1

            for val in line:
                n.add_right(Node(headers[val], (val, i)))
                n = n.right
                headers[val].add_down(n)
                headers[val].value += 1

            n.home = headers[val]

        k = DLXSudoku(9)
        k.headers = headers
        k.h = HeaderNode(8, "h")
        headers[0].add_left(k.h)
        k.generate()

        pass

    def test_iter(self):
        start = Node(st=0)
        st = start
        for i in range(1, 8):
            st.add_right(Node(st=i))
            st = st.right

        start.right.right.right.right = start.right.right.right.right.right
        start.right.right.right.right.right.left = start.right.right.right
        self.assertEquals([1, 2, 3, 5, 6, 7], list(map(lambda x: int(str(x)), iter(start))))


if __name__ == '__main__':
    unittest.main()
