from copy import deepcopy
from go.types import Position, Color, Group, ORTHOGONAL_DIRECTIONS
from go.game import Board

class MoveResult:
    def __init__(self, 
                 position: Position,
                 captured_by_white: set[Position],
                 captured_by_black: set[Position]):
        self.position = position
        self.captured_by_white = captured_by_white
        self.captured_by_black = captured_by_black
    
    def __repr__(self):
        return f"result:\n{self.position}\ncaptured by white:{self.captured_by_white}\ncaptured by black{self.captured_by_black}"

# -- LIBERTIES --
# Get the positions of the liberties of a group
def get_liberties(board: Board, group: Group) -> set[Position]:
    liberties = set()
    for pos in group:
        for neighbor in board.get_orthogonal_neighbors(pos):
            if board.get_color(neighbor) == Color.EMPTY:
                liberties.add(neighbor)
    return liberties

# Check if a group has at least one liberty
def is_group_alive(board: Board, group: Group) -> bool:
    liberties = get_liberties(board, group)
    return len(liberties) > 0


# -- GROUPS --
# Find the stones that form a group at a given position
def find_group_at(board: Board, pos: Position) -> Group:
    color = board.get_color(pos)
    group = Group()
    # Flood fill algorithm
    stack = [pos]
    visited = set()
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        if board.get_color(current) == color:
            group.add(current)
            for neighbor in board.get_orthogonal_neighbors(current):
                if neighbor not in visited:
                    stack.append(neighbor)
    return group

# Find all groups of a given color
def find_all_groups(board: Board, color: Color) -> list[Group]:
    visited = set()
    groups = []
    for x in range(board.size):
        for y in range(board.size):
            pos = Position(x, y)
            if pos not in visited and board.get_color(pos) == color:
                group = find_group_at(board, pos)
                groups.append(group)
                visited.update(group)
    return groups

# -- MOVE VALIDATION --
# Check if placing a stone surrounded by enemy stones
# would be illegal (it's not if it has liberties after capturing)
def would_be_suicide(board: Board, pos: Position, color: Color) -> bool:
    # Simulate placing the stone
    simulated_board = deepcopy(board)
    move_result = execute_move(simulated_board, pos, color)
    # If stones get captured, it's valid
    captured_stones = move_result.captured_by_white if color == Color.WHITE else move_result.captured_by_black
    if len(captured_stones) > 0:
        return False
    # Else, if the stone has disappeared from the board, it's suicide
    elif simulated_board.get_color == Color.EMPTY:
        return True
    # In case it didn't capture nor get captured, it isn't suicide either
    return False

# Check if the move would repeat a previous state (illegal)
def violates_ko(board: Board, pos: Position, color: Color) -> bool:
    # Simulate the full move including captures
    simulated_board = deepcopy(board)
    execute_move(simulated_board, pos, color)
    # Check if this state appeared before
    simulated_map = simulated_board.get_map()
    return simulated_map in board.get_log()

# Check if a move is legal in general
def is_move_legal(board: Board, pos: Position, color: Color) -> bool:
    if not board.in_bounds(pos):
        return False
    if board.get_color(pos) != Color.EMPTY:
        return False
    if would_be_suicide(board, pos, color):
        return False
    if violates_ko(board, pos, color):
        return False
    return True

# -- MOVE EXECUTION --
# Execute a move on the board, thereby modifiyng it
# The move is assumed to be legal
def execute_move(board: Board, pos: Position, color: Color) -> MoveResult:
    # Place the stone
    board.set_color(pos, color)
    opponent_color = Color.WHITE if color == Color.BLACK else Color.BLACK
    # Capture groups with no liberties
    rebuild_groups(board, color)
    rebuild_groups(board, opponent_color)
    captured_by_me = remove_dead_groups(board, opponent_color)
    captured_by_opponent = remove_dead_groups(board, color)
    # Update group structures
    rebuild_groups(board, color)
    rebuild_groups(board, opponent_color)
    # Return the resulting information
    if color == Color.WHITE:
        return MoveResult(
            position=pos,
            captured_by_white=captured_by_me,
            captured_by_black=captured_by_opponent,
        )
    else:
        return MoveResult(
            position=pos,
            captured_by_white=captured_by_opponent,
            captured_by_black=captured_by_me,
        )

# Remove all dead groups of the given color
# Returns the set of positions captured
def remove_dead_groups(board: Board, color: Color) -> set[Position]:
    captured = set()
    groups_list = board.white_groups if color == Color.WHITE else board.black_groups
    dead_groups = []
    for group in groups_list:
        liberties = get_liberties(board,group)
        #if len(get_liberties(board, group)) == 0:
        if len(liberties) == 0:
            dead_groups.append(group)
            captured.update(group)
            for pos in group:
                board.set_color(pos, Color.EMPTY)
    for group in dead_groups:
        groups_list.remove(group)
    return captured

# Rebuild the list of groups tracked by the board
def rebuild_groups(board: Board, color: Color) -> None:
    new_groups = find_all_groups(board, color)
    if color == Color.WHITE:
        board.white_groups = new_groups
    else:
        board.black_groups = new_groups


# -- SCORING --
# The name says it all...
def find_empty_regions(board: Board) -> list[set[Position]]:
    regions = []
    visited = set()
    for x in range(board.size):
        for y in range(board.size):
            pos = Position(x, y)
            if board.get_color(pos) == Color.EMPTY and pos not in visited:
                region = find_group_at(board, pos)
                regions.append(region)
                visited |= region
    return regions

# Determine which color controls an empty region
def get_region_owner(board: Board, region: set[Position]) -> Color | None:
    bordering_colors = set()
    for pos in region:
        for neighbor in board.get_orthogonal_neighbors(pos):
            color = board.get_color(neighbor)
            if color in [Color.BLACK, Color.WHITE]:
                bordering_colors.add(color)
    if len(bordering_colors) > 1:
        return None  # Neutral territory
    elif len(bordering_colors) == 1:
        return bordering_colors.pop()
    else:
        return None  # No bordering stones

# Calculate the points given by each territory to their
# respective owners.
def score_territories(board: Board) -> tuple[float, float]:
    regions = find_empty_regions(board)
    white_score = 0.0
    black_score = 0.0
    for region in regions:
        owner = get_region_owner(board, region)
        if owner == Color.WHITE:
            white_score += len(region)
        elif owner == Color.BLACK:
            black_score += len(region)
    return white_score, black_score

