import pygame
from globals import WIDTH, HEIGHT, TEXT_NORMAL
from go.types import Color
from ui.views.view import UIView
from ui.widgets.solid import Solid
from ui.widgets.sprite import TextSprite

class FinishView(UIView):
    def __init__(self):
        super().__init__(WIDTH*0.6, HEIGHT*0.6)
        self.background = Solid("black", self.width, self.height)
        self.background.opacity = 0.5
        self.add_element(self.background)
        self.render()

    def init_scores(self, white_score: float, black_score: float, winner: Color):
        self.white_score = TextSprite(TEXT_NORMAL, "white", "text_label3.png")
        self.white_score.set_text(f"WHITE HAS {white_score} POINTS")
        self.white_score.center_at((self.width*0.5, self.height*(1/4)))
        self.black_score = TextSprite(TEXT_NORMAL, "white", "text_label.png")
        self.black_score.set_text(f"BLACK HAS {black_score} POINTS")
        self.black_score.center_at((self.width*0.5, self.height*(2/4)))
        winner_str = "WHITE WINS!" if winner == Color.WHITE else "BLACK WINS!"
        self.winner = TextSprite(TEXT_NORMAL, "white", "text_label2.png")
        self.winner.set_text(winner_str)
        self.winner.center_at((self.width*0.5, self.height*(3/4)))
        self.add_element(self.white_score)
        self.add_element(self.black_score)
        self.add_element(self.winner)
        self.notify_change()
    
    def handle_click(self):
        pass
