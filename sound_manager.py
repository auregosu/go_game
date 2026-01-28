import pygame
from go.game import GameEventListener, GameEventType
from globals import SOUND

class SoundManager(GameEventListener):
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        
    def load_sound(self, name: str, filepath: str):
        try:
            sound = pygame.mixer.Sound(filepath)
            self.sounds[name] = sound
        except pygame.error as e:
            self.sounds[name] = None
    
    def load_all_sounds(self):
        self.load_sound("stone_placed", SOUND + "stone_placed.mp3")
        self.load_sound("capture", SOUND + "capture.mp3")
        self.load_sound("pass", SOUND + "pass.mp3")
        self.load_sound("game_start", SOUND + "game_start.mp3")
        self.load_sound("finish_game", SOUND + "finish_game.mp3")
        self.load_sound("invalid_move", SOUND + "invalid_move.mp3")
    
    def play_sound(self, name: str, volume: float = 1.0):
        if name in self.sounds and self.sounds[name] is not None:
            print("!")
            sound = self.sounds[name]
            sound.set_volume(volume)
            sound.play()
    
    def on_game_event(self, event):
        match event.type:
            case GameEventType.STONE_PLACED:
                self.play_sound("stone_placed")
            case GameEventType.STONE_CAPTURED:
                self.play_sound("capture")
            case GameEventType.TURN_PASSED:
                self.play_sound("pass")
            case GameEventType.GAME_STARTED:
                self.play_sound("game_start")
            case GameEventType.GAME_FINISHED:
                self.play_sound("finish_game")
            case GameEventType.ILLEGAL_MOVE:
                self.play_sound("invalid_move")