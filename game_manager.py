import pygame
from globals import WIDTH, HEIGHT, SOUND
from go.types import Color, Position
from go.player import Player
from go.game import Game
from ui.views.game_view import GameView
from ai.ai_player import AIPlayer
from sound_manager import SoundManager

class GameManager:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Settings
        self.size = 9
        self.komi = 6.5
        self.as_white = False

        self.sound_manager = SoundManager()
        self.sound_manager.load_all_sounds()
        
        # Create game and view
        self.game = None
        self.view = GameView(self.start_game, self.start_ai_game)
    
    def run(self):
        # Main game loop
        while self.running:
            delta_time = self.clock.tick() # In miliseconds
            
            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.view.handle_click(event.pos)
            
            # Update
            self.view.update(delta_time)
            
            # AI turn handling
            if self.game is not None and isinstance(self.game.get_current_player(), AIPlayer):
                ai_player = self.game.get_current_player()
                if not ai_player.thinking:
                    ai_player.thinking = True
                    ai_player.thinking_elapsed_ms = 0
                
                if ai_player.finished_thinking(delta_time):
                    move = ai_player.decide_move(self.game)
                    assert move is not None, "wtff"
                    if move != Position(-1, -1):
                        self.game.move_to(move)
                    else:
                        self.game.pass_turn()
            # Draw
            self.window.fill("black")
            self.view.draw_on(self.window)
            pygame.display.flip()
        
        pygame.quit()

    def start_game(self) -> Game:
        self.game = Game(self.size, self.komi)
        self.game.white = Player(Color.WHITE)
        self.game.black = Player(Color.BLACK)
        if self.as_white:
            self.game.white.main = True
        else:
            self.game.black.main = True

        self.game.add_listener(self.sound_manager)

        return self.game

    def start_ai_game(self) -> Game:
        self.game = Game(self.size, self.komi)
        if self.as_white:
            self.game.white = Player(Color.WHITE)
            self.game.white.main = True
            ai_player = AIPlayer(Color.BLACK)
            self.game.black = ai_player
            self.game.add_listener(ai_player)
        else:
            self.game.black = Player(Color.BLACK)
            self.game.black.main = True
            ai_player = AIPlayer(Color.WHITE)
            self.game.white = ai_player
            self.game.add_listener(ai_player)
        
        self.game.add_listener(self.sound_manager)

        return self.game