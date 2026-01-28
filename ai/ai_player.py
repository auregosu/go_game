import random
from enum import Enum
from go.types import Position, Color
from go.game import Game, GameEventListener, GameEventType
from go import rules
from go.player import Player
from ai.queue import PriorityQueue
from ai.strategies import *

THINKING_DURATION_MS = 800

class AIPlayer(Player, GameEventListener):
    valid_strategies: dict[Strategy, bool]

    def __init__(self, color: Color):
        super().__init__(color)
        self.valid_strategies = {}
        for strategy in Strategy:
            self.valid_strategies[strategy] = True
        self.thinking = False
        self.thinking_elapsed_ms = 0
        self.thinking_duration_ms = 1000
    
    def finished_thinking(self, delta_time: float):
        self.thinking_elapsed_ms += delta_time
        if self.thinking_elapsed_ms >= self.thinking_duration_ms:
            self.thinking = False
            self.thinking_elapsed_ms = 0
            return True
        return False
    
    def play_opening(self, game: Game) -> tuple[int, int]: # Returns the play
        print("Play opening.")
        opening_play = Position(random.randint(2, game.board.size-3), random.randint(2, game.board.size-3))
        return (opening_play.x, opening_play.y)
    
    def restore_strategies(self):
        for strategy in Strategy:
            self.valid_strategies[strategy] = True

    def decide_move(self, game: Game) -> Position:
        print("iterationstart")
        if game.turn == 1:
            return self.play_opening(game)
        if game.is_white_turn:
            own_color = Color.WHITE
            enemy_color = Color.BLACK
            own_groups = game.board.white_groups
            enemy_groups = game.board.black_groups
        else:
            own_color = Color.BLACK
            enemy_color = Color.WHITE
            own_groups = game.board.black_groups
            enemy_groups = game.board.white_groups
        chosen_strategy = None
        next_move = None
        # Check if there is any enemy group in atari
        enemy_in_atari = None
        for group in enemy_groups:
            if len(rules.get_liberties(game.board, group)) == 1:
                enemy_in_atari = group
                break
        if enemy_in_atari is not None and self.valid_strategies[Strategy.ATTACK_ATARI]: # If there is an enemy group in atari, attack it
            chosen_strategy = Strategy.ATTACK_ATARI
        else:
            # Check if there is any own group in atari
            in_atari = None
            for group in own_groups:
                if len(rules.get_liberties(game.board, group)) == 1:
                    in_atari = group
                    break
            if in_atari is not None and self.valid_strategies[Strategy.DEFEND_ATARI]: # If there is a group in atari, defend it
                chosen_strategy = Strategy.DEFEND_ATARI
            else: # Else attack weakest group or play randomly
                picked_attack_weakest = random.choice((True, False))
                if picked_attack_weakest and self.valid_strategies[Strategy.ATTACK_WEAKEST]:
                    chosen_strategy = Strategy.ATTACK_WEAKEST
                else: # Playing random can always be valid
                    chosen_strategy = Strategy.RANDOM
        match chosen_strategy:
            case Strategy.ATTACK_ATARI:
                next_move = handle_atari(game, enemy_in_atari) 
            case Strategy.DEFEND_ATARI:
                next_move = handle_atari(game, in_atari) 
            case Strategy.ATTACK_WEAKEST:
                next_move = attack_weakest(game, enemy_groups)
            case Strategy.RANDOM:
                next_move = random_move(game, own_color)
        if next_move == Position(-1, -1):
            return Position(-1, -1)
        if rules.is_move_legal(game.board, next_move, self.color):
            self.restore_strategies()
            return next_move
        else:
            self.valid_strategies[chosen_strategy] = False
            return self.decide_move(game)
    
    def on_game_event(self, event):
        match event.type:
            case GameEventType.STONE_PLACED:
                if event.player.color != self.color:
                    self.thinking = True