from go.types import Position, Color

class Player:
    captures: int # Number of stones captured
    score: float # Points acquired, during most of the game <=> captures
    moves: list[Position] # Log of moves played
    passes: int # Number of consecutive passes
    color: Color
    main: bool

    def __init__(self, color: Color):
        self.captures = 0
        self.score = 0
        self.moves = [Position(-1, -1)] # Start with a pass move so it doen't break indexing
        self.passes = 0
        self.color = color
        self.main = False