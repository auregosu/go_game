from enum import Enum
import random
from go.types import Position, Color, Group, ORTHOGONAL_DIRECTIONS
from go.game import Game
from go import rules
from ai.queue import PriorityQueue

class Strategy(Enum):
    ATTACK_ATARI = 0
    DEFEND_ATARI = 1
    ATTACK_WEAKEST = 2
    RANDOM = 3

# Play the atari of a group, either friend or foe
def handle_atari(game: Game, group: Group) -> Position:
    # Get the last liberty of a group in atari
    for position in group:
        for direction in ORTHOGONAL_DIRECTIONS:
            neighbor = position + direction
            if not game.board.in_bounds(neighbor):
                continue
            if game.board.map[neighbor.x][neighbor.y] == Color.EMPTY:
                return neighbor

# Play a random position that doesn't suck
def random_move(game: Game, own_color: Color) -> Position:
    print("Play random.")
    # Play randomly only inside neutral or enemy regions
    possible_positions = set()
    regions = rules.find_empty_regions(game.board)
    for region in regions:
        owner = rules.get_region_owner(game.board, region)
        if owner != own_color and len(region) >= 4:
            possible_positions |= region
    if len(possible_positions) == 0: # If there are no viable random positions, pass
        print("Pass.")
        return Position(-1, -1)
    # Discard positions on the edges if there are other options
    # Ignore if half of the map is unavailable.
    if len(possible_positions) >= (game.board.size**2)/2: # A bit of a magic number
        bad_positions = set()
        for position in possible_positions:
            if position.x == 0 or position.x == game.board.size-1 or position.y == 0 or position.y == game.board.size-1:
                bad_positions.add(position)
        if len(bad_positions) != len(possible_positions):
            possible_positions -= bad_positions
    # Randomly choose from the filtered set of possible positions
    random_play = random.choice(list(possible_positions))
    while game.board.map[random_play.x][random_play.y] != Color.EMPTY:
        random_play = Position(random.randint(2, game.board.size-3), random.randint(2, game.board.size-3))
    return random_play

# Attach to the enemy group with the least liberties
def attack_weakest(game: Game, enemy_groups: list[Group]) -> Position:
    print("Attack the weakest group.")
    # Consider the enemy group with the least liberties
    weakest_group = enemy_groups[0]
    weakest_group_liberties = 100
    for group in enemy_groups:
        liberties = len(rules.get_liberties(game.board, group))
        if weakest_group_liberties > liberties:
            weakest_group_liberties = liberties
            weakest_group = group
    possible_plays = PriorityQueue()
    for position in weakest_group:
        # Get every position that neighbors the group
        for direction in ORTHOGONAL_DIRECTIONS:
            number_of_liberties = 4
            neighbor = position + direction
            if not game.board.in_bounds(neighbor):
                continue
            neighbor_color = game.board.map[neighbor.x][neighbor.y]
            if neighbor_color != Color.EMPTY:
                continue
            # Check the amount of liberties each neighboring position has
            for liberty_direction in ORTHOGONAL_DIRECTIONS:
                liberty = neighbor + liberty_direction
                if not game.board.in_bounds(liberty):
                    number_of_liberties -= 1
                    continue
                # If the neighboring position is touching a stone, it loses a liberty
                if neighbor_color != Color.EMPTY:
                    number_of_liberties -= 1
            # Add and sort the neighbors to the group by how many liberties they have
            possible_plays.put((number_of_liberties, neighbor))
    # Get the position with the most liberties
    best_option = possible_plays.get()
    print(possible_plays._data)
    print(best_option)
    return best_option[1]