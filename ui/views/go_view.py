from typing import Callable
import pygame
from globals import WIDTH, HEIGHT, TEXT_NORMAL, TEXT_BIG, TEXT_SMALL
from go.types import Color
from go.game import Game
from events.game import GameEventListener, GameEventType
from ui.views.view import UIView
from ui.views.board_view import BoardView
from ui.views.score_view import ScoreView
from ui.views.finish_view import FinishView
from ui.views.dead_stones_view import DeadStonesView
from ui.widgets.sprite import Sprite, TextSprite, TextSpriteButton
from animation.animator import Animator, fade_in_element, fade_out_element
from animation.animation import Animation
from animation import easing

class GoView(UIView, GameEventListener):
    def __init__(self, place_stone: Callable, pass_turn: Callable, remove_selected_stones: Callable):
        super().__init__(WIDTH, HEIGHT)
        # Create child views
        self.place_stone_ref = place_stone
        self.board_view = BoardView()
        self.score_view = ScoreView(pass_turn)
        self.score_view.center_at((self.width*0.8, self.height*0.5))
        self.dead_stones_view = DeadStonesView(self.board_view.board_to_screen, remove_selected_stones)
        self.dead_stones_view.enabled = False
        self.animator = Animator()
        self.finish_view = FinishView()
        self.finish_view.x = self.width*0.2
        self.finish_view.y = self.height*0.2
        self.finish_view.enabled = False
        #self.debug = True
        # Background overlay with the board and piece holders
        self.overlay = Sprite("board_shadow.png")
        # Hover to show the selected position
        # TODO: make it move correctly
        self.stone_hover = Sprite("stone_hover.png")
        self.stone_hover.scale = 1.2
        self.stone_hover.opacity = 0
        self.stone_hover.center_at((self.width*0.5, self.height*0.5))
        # Add every element
        self.add_element(self.overlay)
        self.add_element(self.board_view)
        self.add_element(self.score_view)
        self.add_element(self.dead_stones_view)
        self.add_element(self.stone_hover)
        self.add_element(self.finish_view)
        self.render()
    
    def update(self, delta_time: float):
        # Update the child board view
        self.board_view.update(delta_time)
        self.score_view.update(delta_time)
        if self.dead_stones_view.enabled:
            self.dead_stones_view.update(delta_time)
        # Animate the stone hover, first check if the mouse is on the board
        mouse_pos = pygame.mouse.get_pos()
        if self.board_view.in_bounds(mouse_pos):
            # If it's invisible, fade it in
            if self.stone_hover.opacity == 0:
                fade_in = Animation()
                fade_in.add_property(self.stone_hover, "opacity", 0, 1.0, 150)
                self.animator.add(fade_in)
            quantized_pos = self.board_view.screen_to_board(mouse_pos)
            quantized_pos = self.board_view.board_to_screen(quantized_pos)
            quantized_pos = self.stone_hover.offset_center(quantized_pos)
            follow_mouse = Animation()
            follow_mouse.add_property(self.stone_hover, "x", self.stone_hover.x, quantized_pos[0], 100)
            follow_mouse.add_property(self.stone_hover, "y", self.stone_hover.y, quantized_pos[1], 100)
            self.animator.add(follow_mouse)
        elif self.stone_hover.opacity == 1.0: # If it's visible and out of bounds, fade it out
            fade_out = Animation()
            fade_out.add_property(self.stone_hover, "opacity", 1.0, 0, 150)
            self.animator.add(fade_out)
        self.animator.update(delta_time)

    def on_game_event(self, event):
        match event.type:
            case GameEventType.GAME_STARTED:
                # Set the size of the board
                self.board_view.set_board_size(event.size)
                self.stone_hover.scale = self.board_view.stone_scale
                self.score_view.init_scoremarks(event.white.main)
                self.dead_stones_view.init_selections(event.size)
            case GameEventType.STONE_PLACED:
                self.board_view.add_stone(tuple(event.position), event.player.color, event.player.main)
            case GameEventType.STONE_CAPTURED:
                for position in event.group:
                    self.board_view.remove_stone((position.x, position.y))
                    self.score_view.update_captured(event.owner, event.owner.captures, event.captured_by.captures)
            case GameEventType.SCORING_STARTED:
                    fade_in_element(self.animator, self.dead_stones_view, 400)
                    self.dead_stones_view.enabled = True
                    self.dead_stones_view.set_selection_scale(self.board_view.stone_scale)
                    self.score_view.scoring_started()
                    self.stone_hover.enabled = False
            case GameEventType.GAME_FINISHED:
                    fade_out_element(self.animator, self.dead_stones_view, 300)
                    fade_in_element(self.animator, self.finish_view, 300, 300)
                    self.finish_view.init_scores(event.white_score, event.black_score, event.winner)
                    self.notify_change()
        self.notify_change()

    def handle_click(self, origin: tuple[float, float], mouse_pos: tuple[float, float]):
        self.poll_buttons(origin, mouse_pos)
        self.dead_stones_view.handle_click(origin, mouse_pos)
        self.score_view.handle_click(origin, mouse_pos)
        if self.board_view.in_bounds(mouse_pos):
            if not self.dead_stones_view.enabled and not self.finish_view.enabled:
                position = self.board_view.screen_to_board(mouse_pos)
                self.place_stone_ref(position)
            else:
                self.dead_stones_view.check_selection(self.board_view.screen_to_board(mouse_pos))
        if self.finish_view.enabled:
            self.finish_view.handle_click()
        self.notify_change()
