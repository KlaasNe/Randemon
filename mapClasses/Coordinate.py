from typing import Iterable


class Coordinate:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"C({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def pos(self):
        return self.x, self.y

    def up(self, i: int = 1):
        return Coordinate(self.x, self.y - i)

    def down(self, i: int = 1):
        return Coordinate(self.x, self.y + i)

    def left(self, i: int = 1):
        return Coordinate(self.x - i, self.y)

    def right(self, i: int = 1):
        return Coordinate(self.x + i, self.y)

    def udlr(self) -> tuple:
        yield self.up()
        yield self.down()
        yield self.left()
        yield self.right()

    def around(self, radius: int = 1) -> Iterable[tuple]:
        for y in range(self.y - radius, self.y + radius + 1):
            for x in range(self.x - radius, self.x + radius + 1):
                yield x, y

    def distance(self, coordinate):
        return abs(self.x - coordinate.x) + abs(self.y - coordinate.y)

    def in_bounds(self, lower, upper):
        return lower[0] <= self.x <= upper[0] and lower[1] <= self.y <= upper[1]
