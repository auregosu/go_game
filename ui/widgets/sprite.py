import pygame
from globals import IMAGE
from ui.widgets.element import UIElement

class Sprite(UIElement):
    src_image: pygame.surface.Surface

    def __init__(self, src_image: str | pygame.surface.Surface):
        super().__init__()
        if isinstance(src_image, str):
            self.src_image = pygame.image.load(IMAGE + src_image)
        else:
            self.src_image = src_image
        self.render()
    
    def compose(self) -> pygame.surface.Surface:
        return self.src_image.copy()

from ui.widgets.text import Text

class TextSprite(Sprite):
    text: Text
    def __init__(self, font_size: int, fg_color: str | pygame.Color, src_image: str | pygame.surface.Surface):
        self.text = Text(font_size, fg_color)
        Sprite.__init__(self, src_image)
    
    def compose(self) -> pygame.surface.Surface:
        # Center the text
        text_width, text_height = self.text.font.size(self.text.string)
        image_width, image_height = self.src_image.get_size()
        text_offset = [(image_width-text_width)/2, (image_height-text_height)/2]
        # Draw it on a copy of the source image
        src_image_copy = self.src_image.copy()
        self.text.draw_on(src_image_copy, text_offset)
        return src_image_copy
    
    def set_text(self, string: str):
        self.text.string = string
        self.notify_change()

from ui.widgets.button import Button, Callable

class TextSpriteButton(TextSprite, Button):
    def __init__(self, font_size: int, fg_color: pygame.Color, src_image: str | pygame.surface.Surface):
        TextSprite.__init__(self, font_size, fg_color, src_image)
        Button.__init__(self, self.surface, self.x, self.y)
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value: float):
        self._x = value
        self.update_bounding_box(self.surface, self.x, self.y)

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: float):
        self._y = value
        self.update_bounding_box(self.surface, self.x, self.y)