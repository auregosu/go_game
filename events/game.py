from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from go.types import Position, Group, Color
from go.player import Player

class GameEventType(Enum):
    STONE_PLACED = 0
    STONE_CAPTURED = 1
    TURN_PASSED = 2
    GAME_STARTED = 3
    GAME_FINISHED = 4
    SCORING_STARTED = 5
    ILLEGAL_MOVE = 6

class GameEvent(ABC):
    type: GameEventType

@dataclass
class StonePlacedEvent(GameEvent):
    type = GameEventType.STONE_PLACED
    player: Player
    position: Position
    captured_by_white: set[Position]
    captured_by_black: set[Position]

@dataclass
class StoneCapturedEvent(GameEvent):
    type = GameEventType.STONE_CAPTURED
    owner: Player
    captured_by: Player
    group: Group

@dataclass
class TurnPassedEvent(GameEvent):
    type = GameEventType.TURN_PASSED
    player: Player

@dataclass
class GameStartedEvent(GameEvent):
    type = GameEventType.GAME_STARTED
    white: Player
    black: Player
    size: int

@dataclass
class GameFinishedEvent(GameEvent):
    type = GameEventType.GAME_FINISHED
    winner: Color
    white_score: float
    black_score: float

@dataclass
class ScoringStartedEvent(GameEvent):
    type = GameEventType.SCORING_STARTED

@dataclass
class IllegalMoveEvent(GameEvent):
    type = GameEventType.ILLEGAL_MOVE

class GameEventListener(ABC):
    @abstractmethod
    def on_game_event(self, event: GameEvent):
        pass