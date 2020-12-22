from math import sqrt, inf
from operator import attrgetter
import random


def get_stats(line, size):
    num = line % size
    pos = line // size
    row = pos // size
    col = pos % size
    sq = int(sqrt(size))
    box = row // sq * sq + col // sq
    return [pos, size ** 2 + num + size * row, 2 * size ** 2 + num + size * col, 3 * size ** 2 + num + size * box]


class DLXSudoku:
    generated = []

    def __init__(self, size):
        # Generate the list based on size
        self.size = size
        self.headers = []
        self.h = HeaderNode(size**3 + 1, "h")
        # create header row
        n = self.h
        for col in range(4 * size ** 2):
            n.add_right(HeaderNode(st=col))
            n = n.right
            self.headers.append(n)

        for line in range(size ** 3):
            line = size ** 3 - line - 1
            temp = iter(get_stats(line, size))
            val = next(temp)
            n = Node(self.headers[val], (val, line))
            self.headers[val].add_down(n)
            self.headers[val].value += 1

            for val in temp:
                n.add_right(Node(self.headers[val], (val, line)))
                n = n.right
                self.headers[val].add_down(n)
                self.headers[val].value += 1

            n.home = self.headers[val]

    def generate(self):
        lines = self._generate()
        board = [0]*self.size**2
        for line in lines:
            line = line.st[1]
            board[line // self.size] = line - (line // self.size * self.size) + 1

        return board

    def _generate(self, depth=0):
        if self.h.right == self.h:
            return self.generated

        col = min(self.h, key=attrgetter('value'))
        col.cover()
        order = random.sample([x for x in range(col.value)], col.value)
        for line in order:  # random sample later
            node = col.get(line)
            self.generated.append(node)
            j = node.right
            while j != node:
                j.home.cover()
                j = j.right

            board = self._generate(depth+1)
            if board is not None:
                j = node.left
                while j != node:
                    j.home.uncover()
                    j = j.left

                col.uncover()
                return board

            self.generated.pop()
            j = node.left
            while j != node:
                j.home.uncover()
                j = j.left

        col.uncover()

        return None


# Node for doubly linked list in two directions
class Node:
    def __init__(self, home=None, st=None):
        self.up = self
        self.down = self
        self.left = self
        self.right = self
        self.home = home
        self.st = st

    def __str__(self):
        return str(self.st)

    def __iter__(self):
        n = self.right
        while n != self:
            yield n
            n = n.right

    def add_right(self, node):
        node.left = self
        node.right = self.right
        self.right.left = node
        self.right = node

    def add_left(self, node):
        node.right = self
        node.left = self.left
        self.left.right = node
        self.left = node

    def add_up(self, node):
        node.down = self
        node.up = self.up
        self.up.down = node
        self.up = node

    def add_down(self, node):
        node.up = self
        node.down = self.down
        self.down.up = node
        self.down = node

    # method to cover the column and associated rows
    def cover(self):
        self.left.right = self.right
        self.right.left = self.left
        r = self.down
        while r != self:
            j = r.right
            while j != r:
                j.down.up = j.up
                j.up.down = j.down
                j.home.value -= 1
                j = j.right

            r = r.down

    # method to uncover the column and associated rows
    def uncover(self):
        r = self.up
        while r != self:
            j = r.left
            while j != r:
                j.down.up = j
                j.up.down = j
                j.home.value += 1
                j = j.left

            r = r.up

        self.left.right = self
        self.right.left = self


class HeaderNode(Node):
    def __init__(self, value=0, st=None):
        Node.__init__(self)
        self.value = value
        self.home = self
        self.st = st

    def get(self, index):
        n = self.down
        for _ in range(index):
            n = n.down

        return n
