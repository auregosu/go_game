import pygame
from ui.widgets.element import UIElement

class Solid(UIElement):
    color: pygame.Color
    width: float
    height: float

    def __init__(self, color: str | pygame.Color, width: float, height: float):
        super().__init__()
        if isinstance(color, str):
            self.color = pygame.Color(color)
        else:
            self.color = color
        self.width = width
        self.height = height
        self.render()
    
    def compose(self) -> pygame.surface.Surface:
        canvas = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        canvas.fill(self.color)
        return canvas