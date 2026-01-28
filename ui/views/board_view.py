import random
import pygame
from globals import IMAGE, WIDTH, HEIGHT
from go.types import Color
from go.board import Board
from ui.widgets.element import UIElement
from ui.views.view import UIView
from ui.widgets.sprite import Sprite
from animation.animator import Animator, fade_out_element
from animation.animation import Animation
from animation import easing

class BoardView(UIView):
    lines: list[Sprite]

    def __init__(self):
        super().__init__(WIDTH, HEIGHT)
        self.animator = Animator()
        # Add the wood and lines/lines
        self.wood = Sprite("board.png")
        self.wood.center_at((self.width*0.33, self.height*0.5))
        self.wood_width, self.wood_height = self.wood.surface.get_size()
        self.lines = []
        self.add_element(self.wood)
        self.render()
    
    def update(self, delta_time: float):
        self.animator.update(delta_time)

    def set_board_size(self, board_size):
        self.board_size = board_size
        self.stone_scale = 8.0/board_size
        self.stone_size, _ = Sprite("stone_white.png").surface.get_size()
        self.stones = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.stone_shadows = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.init_lines()
        self.notify_change()
    
    def init_lines(self):
        self.usable_origin = (self.wood.x + 33, self.wood.y + 32)
        self.usable_width = self.wood_width - 2*self.usable_origin[0] + 2*self.wood.x
        self.usable_height = self.wood_height - 2*self.usable_origin[1] + 2*self.wood.y
        for i in range(self.board_size*2):
                line = Sprite("board_line.png")
                if i < self.board_size:
                    line.x = self.usable_origin[0] + self.usable_width*(i/(self.board_size-1))
                    line.y = self.usable_origin[1]
                else:
                    line.rotation = 90
                    line.x = self.usable_origin[0]
                    line.y = self.usable_origin[1] + self.usable_height*((i-self.board_size)/(self.board_size-1))
                self.lines.append(line)
                self.add_element(line)
        self.notify_change()
    
    # Translate the space of the board to the space of the screen
    def board_to_screen(self, coordinates: tuple[int, int]) -> tuple[float, float]:
        x = self.usable_origin[0] + coordinates[0] * self.usable_width / (self.board_size - 1)
        y = self.usable_origin[1] + coordinates[1] * self.usable_height / (self.board_size - 1)
        return (x, y)

    # Translate the space of the screen to the space of the board
    def screen_to_board(self, position: tuple[float, float]) -> tuple[int, int]:
        x = position[0] - (self.x + self.usable_origin[0])
        y = position[1] - (self.y + self.usable_origin[1])
        x /= self.usable_width / (self.board_size - 1)
        y /= self.usable_height / (self.board_size - 1)
        x = round(x)
        y = round(y)
        if x < 0:
            x = 0
        if y >= self.board_size:
            y = self.board_size-1
        return (x, y)
    
    def in_bounds(self, mouse_pos: tuple[float, float]):
        if mouse_pos[0] < self.wood.x or mouse_pos[0] > self.wood.x + self.wood_width:
            return False
        if mouse_pos[1] < self.wood.y or mouse_pos[1] > self.wood.y + self.wood_height:
            return False
        return True

    def add_stone(self, position: tuple[int, int], color: Color, main: bool):
        # Make and animate the added stone
        stone = Sprite("stone_white.png") if color == Color.WHITE else Sprite("stone_black.png")
        stone.scale = self.stone_scale
        start_x = self.wood.x + random.random()*self.wood_width
        start_y = self.height + self.stone_size*1.5 if main else -self.stone_size*1.5
        end_x, end_y = stone.offset_center(self.board_to_screen(position))
        duration = 400
        slide_in = Animation()
        slide_in.add_property(stone, "scale", stone.scale*1.25, stone.scale*1.0, duration, easing.sin)
        slide_in.add_property(stone, "x", start_x, end_x, duration, easing.out_quadratic)
        slide_in.add_property(stone, "y", start_y, end_y, duration, easing.out_quadratic)
        self.animator.add(slide_in)
        # Make and animate the added shadow
        start_x, start_y = self.offset_shadow(start_x, start_y)
        end_x, end_y = self.offset_shadow(end_x, end_y)
        shadow = Sprite("stone_shadow.png")
        shadow.scale = self.stone_scale
        slide_in = Animation()
        slide_in.add_property(shadow, "opacity", 0, 1.0, duration, easing.linear)
        slide_in.add_property(shadow, "x", start_x, end_x, duration, easing.sin)
        slide_in.add_property(shadow, "y", start_y, end_y, duration, easing.sin)
        self.animator.add(slide_in)
        self.stones[position[0]][position[1]] = stone
        self.stone_shadows[position[0]][position[1]] = shadow
        self.add_element(shadow, 2)
        self.add_element(stone, 3)
        self.notify_change()

    def remove_stone(self, position: tuple[int, int]):
        stone = self.stones[position[0]][position[1]]
        fade_out = Animation(lambda element=stone: self.remove_element(element))
        fade_out.add_property(stone, "opacity", 1.0, 0.0, 250, easing.in_quadratic)
        self.animator.add(fade_out)
        self.stones[position[0]][position[1]] = None
        shadow = self.stone_shadows[position[0]][position[1]]
        fade_out = Animation(lambda element=shadow: self.remove_element(element))
        fade_out.add_property(shadow, "opacity", 1.0, 0.0, 300, easing.in_quadratic)
        self.animator.add(fade_out)
        self.stone_shadows[position[0]][position[1]] = None
        self.notify_change()

    # Returns the position of a shadow previously aligned with
    # the center of a stone, now offset
    def offset_shadow(self, x: float, y: float) -> tuple[float, float]:
        return x - self.stone_size * 0.3, y + self.stone_size * 0.15
