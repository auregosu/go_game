from typing import Callable
import pygame
from globals import WIDTH, HEIGHT, TEXT_NORMAL, TEXT_BIG
from go.types import Color
from go.game import Game
from events.game import GameEventListener, GameEventType
from ui.views.view import UIView
from ui.views.board_view import BoardView
from ui.views.finish_view import FinishView
from ui.widgets.sprite import Sprite, TextSprite, TextSpriteButton
from animation.animator import Animator, fade_in_element, fade_out_element, slide_out_element
from animation.animation import Animation
from animation import easing

class ScoreView(UIView):
    def __init__(self, pass_turn: Callable):
        super().__init__(WIDTH*0.4, HEIGHT)
        # Create child views
        self.animator = Animator()
        # Stone holders
        self.stone_holders = Sprite("stone_holders.png")
        self.stone_holders.center_at((0, self.height*0.5))
        self.stone_holders.x = 0
        # Labels for the scores
        self.white_scoremark = TextSprite(TEXT_BIG, pygame.Color("black"), "score_white.png")
        self.white_scoremark.scale = 0.6
        self.black_scoremark = TextSprite(TEXT_BIG, pygame.Color("white"), "score_black.png")
        self.black_scoremark.scale = 0.6
        # Button to pass the turn
        self.pass_turn_button = TextSpriteButton(TEXT_BIG, pygame.Color("white"), "text_label.png")
        self.pass_turn_button.scale = 0.6
        self.pass_turn_button.set_text("PASS")
        self.pass_turn_button.center_at((self.width*0.8, self.height*0.95))
        self.pass_turn_button.set_action(pass_turn)
        # Add every element
        self.add_element(self.stone_holders)
        self.add_element(self.white_scoremark)
        self.add_element(self.black_scoremark)
        self.add_element(self.pass_turn_button)
        self.render()

    def update(self, delta_time: float):
        if self.animator.is_busy():
            self.animator.update(delta_time)

    def update_captured(self, owner_color: Color, owner, captured_by):
        if owner_color == Color.WHITE:
            self.white_scoremark.set_text(f"{captured_by:3.1f}")
            self.black_scoremark.set_text(f"{owner:3.1f}")
        else:
            self.white_scoremark.set_text(f"{owner:3.1f}")
            self.black_scoremark.set_text(f"{captured_by:3.1f}")
        self.notify_change()

    def init_scoremarks(self, white_main: bool):
        # Set the position of the scoremarks
        scoremark_x = self.width*0.8
        main_y = self.height*0.65
        not_main_y = self.height*0.25
        if white_main:
            self.white_scoremark.center_at((scoremark_x, main_y))
            self.black_scoremark.center_at((scoremark_x, not_main_y))
        else:
            self.white_scoremark.center_at((scoremark_x, not_main_y))
            self.black_scoremark.center_at((scoremark_x, main_y))
        # Set the text on the scoremarks
        self.white_scoremark.set_text(f"{0:3.1f}")
        self.black_scoremark.set_text(f"{0:3.1f}")
        self.notify_change()

    def handle_click(self, origin: tuple[float, float], mouse_pos: tuple[float, float]):
        self.poll_buttons(origin, mouse_pos)
        self.notify_change()
    
    def scoring_started(self):
        fade_out_element(self.animator, self.pass_turn_button, 400, 0)
        slide_out_element(self.animator, self.stone_holders, 400, 0)
