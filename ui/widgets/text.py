import pygame

class Text():
    string: str
    font_size: pygame.font.Font
    color: pygame.Color

    def __init__(self, font_size: int, fg_color: str | pygame.Color):
        self.string = ""
        self.font = pygame.font.SysFont("arial", font_size)
        self.font.set_bold(True)
        if isinstance(fg_color, str):
            self.color = pygame.Color(fg_color)
        else:
            self.color = fg_color

    def draw_on(self, destination: pygame.surface.Surface, position: tuple[int, int]):
        rendered_text = self.font.render(self.string, True, self.color)
        destination.blit(rendered_text, position)