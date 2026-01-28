from enum import Enum

class Color(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

# Representation of a position on the board
# Essentially a tuple with two integers
class Position():
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    @classmethod
    def tuple(cls, t: tuple):
        if len(t) == 2:
            return cls(t[0], t[1])

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __tuple__(self):
        return (self.x, self.y)

    def __iter__(self):
        return iter((self.x, self.y))

# Left, Right, Up, Down
ORTHOGONAL_DIRECTIONS = [Position(-1, 0), Position(1, 0), Position(0, -1), Position(0, 1)]

# Representation of a set of stones generally considered connected
Group = set[Position]