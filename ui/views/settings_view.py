import pygame
from ui.views.view import UIView
from ui.widgets.sprite import TextSpriteButton

class SettingsView(UIView):
    def __init__(self):
        super().__init__()
        self.select_white = TextSpriteButton()
        self.select_black = TextSpriteButton()
        self.select_size_9 = TextSpriteButton()
        self.select_size_13 = TextSpriteButton()
        self.select_size_19 = TextSpriteButton()

    def draw_on(self, destination: pygame.surface.Surface):
        self.select_white.draw_on(destination)
        self.select_black.draw_on(destination)
        self.select_size_9.draw_on(destination)
        self.select_size_13.draw_on(destination)
        self.select_size_19.draw_on(destination)