from typing import Callable
import pygame
from globals import WIDTH, HEIGHT, TEXT_SMALL, TEXT_BIG
from go.types import Color, Position
from go.game import Game
from ui.views.view import UIView
from ui.widgets.sprite import Sprite, TextSprite, TextSpriteButton
from animation.animator import Animator, fade_in_element, fade_out_element
from animation.animation import Animation

class DeadStonesView(UIView):
    def __init__(self, board_to_screen: Callable, remove_selected_stones):
        super().__init__(WIDTH, HEIGHT)
        self.board_to_screen_ref = board_to_screen
        self.remove_selected_stones_ref = remove_selected_stones
        self.animator = Animator()
        self.selection_scale = 1.0
        # Button to confirm the selected stones
        self.confirm_stones_button = TextSpriteButton(TEXT_BIG, pygame.Color("white"), "text_label3.png")
        self.confirm_stones_button.set_text("CONFIRM")
        self.confirm_stones_button.scale = 0.6
        self.confirm_stones_button.center_at((self.width*0.9, self.height*0.95))
        self.confirm_stones_button.set_action(self.finish_selection)
        self.instructions = TextSprite(TEXT_SMALL, "white", "text_label2.png")
        self.instructions.set_text("SELECT THE DEAD STONES")
        self.instructions.center_at((self.width*0.5, self.height*0.5))
        # Add every element
        self.add_element(self.confirm_stones_button)
        self.add_element(self.instructions)
        self.render()
    
    def update(self, delta_time: float):
        if self.animator.is_busy():
            self.animator.update(delta_time)

    def set_selection_scale(self, scale: float):
        self.selection_scale = scale
    
    def init_selections(self, size: int):
        self.board_size = size
        self.selected_stones = [[Sprite("stone_selected.png") for _ in range(size)] for _ in range(size)]
        for x in range(size):
            for y in range(size):
                selection = self.selected_stones[x][y]
                selection.scale = self.selection_scale
                selection.enabled = False
                selection.center_at(self.board_to_screen_ref((x, y)))
                self.add_element(selection)
        self.notify_change()

    def check_selection(self, position: tuple[int, int]):
        if self.instructions.enabled:
            fade_out_element(self.animator, self.instructions, 400)
            return
        selection = self.selected_stones[position[0]][position[1]]
        if selection.enabled == False:
            fade_in_element(self.animator, selection, 150, 0)
        else:
            fade_out_element(self.animator, selection, 150, 0)
        self.notify_change()
    
    def finish_selection(self):
        selected_positions = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.selected_stones[x][y].enabled:
                    selected_positions.append(Position(x, y))
        self.remove_selected_stones_ref(selected_positions)
        self.notify_change()

    def handle_click(self, origin: tuple[float, float], mouse_pos: tuple[float, float]):
        self.poll_buttons(origin, mouse_pos)
        self.notify_change()
