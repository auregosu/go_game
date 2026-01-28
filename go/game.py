from go.types import Position, Color
from go.player import Player
from go.board import Board
from events.game import *

from go import rules
# Manages the state of the game, applies the rules
class Game:
    board: Board
    white: Player
    black: Player
    is_white_turn: bool
    turn: int
    komi: float
    is_finished: bool
    event_listeners: list[tuple[GameEventListener, tuple[GameEventType]]]

    def __init__(self, size: int, komi: float = 6.5):
        self.board = Board(size)
        self.white = Player(Color.WHITE)
        self.black = Player(Color.BLACK)
        # Game state
        self.is_white_turn = False
        self.turn = 1
        self.komi = komi
        self.is_finished = False
        self.event_listeners = []
    
    # Add an event listener to receive events
    def add_listener(self, listener: GameEventListener):
        self.event_listeners.append(listener)
    
    # Emit an event
    def emit_event(self, event: GameEvent):
        for listener in self.event_listeners:
            listener.on_game_event(event)
    
    # Returns the player whose turn it is
    def get_current_player(self) -> Player:
        return self.white if self.is_white_turn else self.black
    
    def is_move_legal(self, pos: Position) -> bool:
        """Check if a move at the given position is legal."""
        return rules.is_move_legal(
            self.board, 
            pos, 
            self.get_current_player().color
        )
    
    # Execute a move at the given position and
    # return information about the result
    def move_to(self, position: tuple[int, int]) -> rules.MoveResult:
        if isinstance(position, tuple):
            position = Position.tuple(position)
        if not self.is_move_legal(position):
            event = IllegalMoveEvent()
            self.emit_event(event)
            return
        result = rules.execute_move(
            self.board, 
            position, 
            self.get_current_player().color
        )
        current_player = self.get_current_player()
        current_player.moves.append(position)
        current_player.passes = 0
        self.white.captures += len(result.captured_by_white)
        self.black.captures += len(result.captured_by_black)
        self.board.log()
        # Emit the events for capturing a stone
        if len(result.captured_by_white) > 0:
            event = StoneCapturedEvent(
                owner=self.black,
                captured_by=self.white,
                group=result.captured_by_white
            )
            self.emit_event(event)
        if len(result.captured_by_black) > 0:
            event = StoneCapturedEvent(
                owner=self.white,
                captured_by=self.black,
                group=result.captured_by_black
            )
            self.emit_event(event)
        # Emit the event for placing a stone
        event = StonePlacedEvent(
            current_player,
            position,
            result.captured_by_white,
            result.captured_by_black)
        self.emit_event(event)
        # Next turn
        self.next_turn()
        return result
    
    # Pass the turn, update the player and send the event
    # Enter scoring if necessary
    def pass_turn(self):
        current_player = self.get_current_player()
        current_player.passes += 1
        current_player.moves.append(current_player.moves[-1] if current_player.moves else Position(-1, -1))
        event = TurnPassedEvent(current_player)
        self.emit_event(event)
        if self.white.passes >= 1 and self.black.passes >= 1:
            self.enter_scoring()
        self.next_turn()
    
    # Transition to the scoring
    def enter_scoring(self):
        event = ScoringStartedEvent()
        self.emit_event(event)

    def remove_selected_stones(self, stones: Group):
        white_extra = 0
        black_extra = 0
        for stone in stones:
            color = self.board.get_color(stone)
            if color == Color.WHITE:
                white_extra += 1
            if color == Color.BLACK:
                black_extra += 1
            self.board.set_color(stone, Color.EMPTY)
        self.white.captures += white_extra
        self.black.captures += black_extra
        self.finish()
    
    # Update scores
    def next_turn(self):
        self.white.score = self.white.captures + self.komi
        self.black.score = self.black.captures
        self.is_white_turn = not self.is_white_turn
        self.turn += 1
    
    # Calculate the score that finalizes the game
    def calculate_final_score(self) -> tuple[float, float]:
        white_territory, black_territory = rules.score_territories(self.board)
        white_total = self.white.captures + white_territory + self.komi
        black_total = self.black.captures + black_territory
        return white_total, black_total
    
    # End the game, determine the winner
    def finish(self) -> Color | None:
        if self.is_finished:
            return None
        self.is_finished = True
        white_score, black_score = self.calculate_final_score()
        self.white.score = white_score
        self.black.score = black_score
        winner = None
        if white_score > black_score:
            winner = Color.WHITE
        elif black_score > white_score:
            winner = Color.BLACK
        event = GameFinishedEvent(
            winner,
            white_score,
            black_score
        )
        self.emit_event(event)
        return winner