from go.types import Position, Group, Color, ORTHOGONAL_DIRECTIONS

class Board:
    size: int # 9x9, 13x13, 19x19
    map: list[list[Color]] # 2D list of Colors representing the state of the board
    various_positions: list[tuple[tuple[Color, ...], ...]] # Log of previous states
    white_groups: list[Group] # List of present white connected groups
    black_groups: list[Group] # List of present black connected groups

    def __init__(self, size: int):
        self.size = size
        self.map = [[Color.EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.various_positions = []
        self.white_groups = []
        self.black_groups = []

    # Check if a position fits in the board
    def in_bounds(self, pos: Position) -> bool:
        if isinstance(pos, tuple):
            pos = Position.tuple(pos)
        return 0 <= pos.x < self.size and 0 <= pos.y < self.size

    # Set the color of a position on the board
    def get_color(self, pos: Position) -> Color:
        if not self.in_bounds(pos):
            raise ValueError(f"Position {pos} out of bounds")
        return self.map[pos.x][pos.y]

    # Set the color of a position on the board
    def set_color(self, pos: Position, color: Color) -> None:
        if not self.in_bounds(pos):
            raise ValueError(f"Position {pos} out of bounds")
        self.map[pos.x][pos.y] = color

    # Get in-bounds orthogonal neighbors of a position (including empty positions)
    def get_orthogonal_neighbors(self, pos: Position) -> set[Position]:
        neighbors = set()
        for direction in ORTHOGONAL_DIRECTIONS:
            neighbor = pos + direction
            if self.in_bounds(neighbor):
                neighbors.add(neighbor)
        return neighbors
    
    # Get an immutable copy of the map
    def get_map(self) -> tuple[tuple[Color, ...], ...]:
        return tuple(tuple(row) for row in self.map)

    # Get an immutable copy of the log
    def get_log(self) -> tuple[tuple[tuple[Color, ...], ...], ...]:
        return tuple(tuple(tuple(row) for row in state) for state in self.various_positions)
    
    # Add the current state to the log
    def log(self):
        self.various_positions.append(tuple(tuple(row) for row in self.map))


