import pygame
from typing import Callable

class Button():
    on_click: Callable
    bounding_box: pygame.Rect

    def __init__(self, surface: pygame.surface.Surface, pos_x: float, pos_y: float):
        self.update_bounding_box(surface, int(pos_x), int(pos_y))

    def update_bounding_box(self, surface: pygame.surface.Surface, pos_x: int, pos_y: int):
        self.bounding_box = surface.get_rect()
        self.bounding_box.x = pos_x
        self.bounding_box.y = pos_y

    def set_action(self, func: Callable):
        self.on_click = func

    def click(self):
        self.on_click()

    # Calls on_click() if the mouse is inside the box
    def poll(self, origin: tuple[float, float], mouse: tuple[float, float]) -> bool:
        if hasattr(self, "parent"):
            if self.parent.enabled == False:
                return
        mouse = (mouse[0] - origin[0], mouse[1] - origin[1])
        if self.bounding_box.collidepoint(mouse):
            self.on_click()
            return True
        return False