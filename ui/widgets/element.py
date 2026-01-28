from abc import ABC, abstractmethod
import pygame

class UIElement(ABC):
    def __init__(self):
        self._x = 0
        self._y = 0
        self._opacity = 1.0
        self._scale = 1.0
        self._rotation = 0
        self._enabled = True
        self.surface = None
        self._composed = False
        self._rendered = False
        self._cached_composed = None
        self.parent = None # Another UIElement

    # Every UIElement should call notify_chaange()
    # if it needs to be rendered again
    def notify_change(self):
        self._composed = False
        self._rendered = False
        if self.parent is not None:
            self.parent.notify_change()
    
    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value: float):
        self._x = value
        if self.parent is not None:
            self.notify_change()

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: float):
        self._y = value
        if self.parent is not None:
            self.notify_change()
    
    @property
    def opacity(self):
        return self._opacity
    
    @opacity.setter
    def opacity(self, value: float):
        if value >= 0 and value <= 255:
            self._opacity = value
            self.notify_change()
        else:
            raise ValueError(f"{value} not within opacity range.")

    @property
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value: float):
        self._scale = value
        self.notify_change()

    @property
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self, value: float):
        self._rotation = value
        self.notify_change()
    
    # Blit everything into one composed surface
    @abstractmethod
    def compose(self) -> pygame.surface.Surface:
        pass

    # Apply the transform on the composed surface
    # It effectively applies any changes
    def render(self):
        if self._rendered:
            return
        if not self._composed:
            self._cached_composed = self.compose()
            self.notify_change()
        surface = self._cached_composed.copy()
        # Alpha
        if self.opacity != 1.0:
            surface.set_alpha(int(self.opacity*255))
        # Scale
        if self.scale != 1.0:
            surface = pygame.transform.scale_by(surface, self.scale)
        # Rotate
        if self.rotation != 0:
            surface = pygame.transform.rotate(surface, self.rotation)
        self._rendered = True
        self.surface = surface

    def center_at(self, position: tuple[float, float]):
        width, height = self.surface.get_size()
        self.x = position[0] - width/2
        self.y = position[1] - height/2

    # Offset the given coordinates so that, if the element
    # was in those coordinates, the returned would be the center
    def offset_center(self, position: tuple[float, float]) -> tuple[float, float]:
        width, height = self.surface.get_size()
        width *= self.scale
        height *= self.scale
        x = position[0] - width/2
        y = position[1] - height/2
        return (x, y)

    def draw_on(self, destination: pygame.surface.Surface):
        if self.enabled:
            if self._opacity == 0:
                return
            if not self._rendered or not self._composed:
                self.render()
            destination.blit(self.surface, (self.x, self.y))
    
    def __repr__(self):
        return f"{self.x}, {self.y}, {self.opacity}, {self.scale}, {self.rotation}, {self.enabled}, {self.surface}"