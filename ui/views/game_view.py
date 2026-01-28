import pygame
from typing import Callable
from globals import WIDTH, HEIGHT, IMAGE
from events.game import GameEventListener, GameEventType, GameStartedEvent
from go.types import Position
from go.game import Game
from ui.views.view import UIView
from ui.views.menu_view import MenuView
from ui.views.go_view import GoView
from ui.widgets.element import UIElement
from ui.widgets.sprite import Sprite, TextSprite
from animation.animator import Animator, fade_in_element, fade_out_element
from ai.ai_player import AIPlayer

class GameView(UIView, GameEventListener):
    def __init__(self, start_game: Callable, start_ai_game: Callable):
        super().__init__(WIDTH, HEIGHT)
        self.game = None # This will be set when the game starts
        self.start_game_ref = start_game
        self.start_ai_game_ref = start_ai_game
        # Add animator
        self.animator = Animator()
        # Create child elements
        self.background = Sprite("background.png")
        self.menu_view = MenuView(self.play_local, self.play_AI)
        self.menu_view.center_at((self.width/2, self.height/2))
        self.go_view = GoView(self.place_stone, self.pass_turn, self.remove_selected_stones)
        # Set the view for the game itself as disabled by default
        self.go_view.enabled = False
        # Add the elements
        self.add_element(self.background)
        self.add_element(self.menu_view)
        self.add_element(self.go_view)    
        fade_in_element(self.animator, self, 1000, 100)

        #self.play_local()

    def update(self, delta_time: float):
        if self.menu_view.enabled:
            self.menu_view.update(delta_time)
        else: # if self.go_view.enabled
            self.go_view.update(delta_time)
        self.animator.update(delta_time)
        
    def handle_click(self, mouse_pos: tuple[float, float]):
        if self.menu_view.enabled:
            self.menu_view.handle_click((self.x, self.y), mouse_pos)
        else: # if self.go_view.enabled
            self.go_view.handle_click((self.x, self.y), mouse_pos)
        self.notify_change()

    def play_local(self):
        fade_out_element(self.animator, self.menu_view, 500)
        fade_in_element(self.animator, self.go_view, 500)
        self.game = self.start_game_ref()
        self.game.add_listener(self.go_view)
        self.game.add_listener(self)
        self.game.emit_event(GameStartedEvent(self.game.white, self.game.black, self.game.board.size))
        self.notify_change()
    
    def play_AI(self):
        fade_out_element(self.animator, self.menu_view, 500)
        fade_in_element(self.animator, self.go_view, 500)
        self.game = self.start_ai_game_ref()
        self.game.add_listener(self.go_view)
        self.game.add_listener(self)
        self.game.emit_event(GameStartedEvent(self.game.white, self.game.black, self.game.board.size))
        self.notify_change()
    
    def place_stone(self, position: tuple[int, int]):
        if not isinstance(self.game.get_current_player(), AIPlayer):
            self.game.move_to(position)
    
    def pass_turn(self):
        self.game.pass_turn()

    def remove_selected_stones(self, selected_stones: list[Position]):
        self.game.remove_selected_stones(selected_stones)
    
    def on_game_event(self, event):
        self.notify_change()