from typing import Callable
import pygame
from globals import TEXT_NORMAL, WIDTH, HEIGHT
from ui.views.view import UIView
from ui.views.settings_view import SettingsView
from ui.widgets.sprite import Sprite, TextSpriteButton
from ui.widgets.solid import Solid

class MenuView(UIView):
    def __init__(self, play_action: Callable, play_AI: Callable):
        super().__init__(WIDTH*0.8, HEIGHT*0.8)

        # Backgrounf that acts as a frame for the menu
        self.background = Solid("black", self.width, self.height)
        self.background.opacity = 0.5

        # Button to play a game of go
        self.play_local = TextSpriteButton(TEXT_NORMAL, pygame.Color("white"), "text_label.png")
        self.play_local.set_text("PLAY LOCAL")
        self.play_local.center_at((self.width/2, self.height/2))
        self.play_local.y = self.height * (1/4)
        self.play_local.set_action(play_action)

        # Button to play a game of go with the AI
        self.play_AI = TextSpriteButton(TEXT_NORMAL, pygame.Color("blue"), "text_label2.png")
        self.play_AI.set_text("PLAY AI")
        self.play_AI.center_at((self.width/2, self.height/2))
        self.play_AI.y = self.height * (2/4)
        self.play_AI.set_action(play_AI)

        # Button to make the settings appear
        self.settings = TextSpriteButton(TEXT_NORMAL, pygame.Color("green"), "text_label3.png")
        self.settings.set_text("SETTINGS")
        self.settings.center_at((self.width/2, self.height/2))
        self.settings.y = self.height * (3/4)

        #self.settings_view = SettingsView()
        #self.settings_view.set_text("test3")
        #self.settings_view.enabled = False
        # Add the elements
        self.add_element(self.background, 1)
        self.add_element(self.play_local, 2)
        self.add_element(self.play_AI, 2)
        self.add_element(self.settings, 2)
        self.render()
    
    def handle_click(self, origin: tuple[float, float], mouse_pos: tuple[float, float]):
        self.poll_buttons(origin, mouse_pos)

    def update(self, mouse_pos: tuple[float, float]):
        pass