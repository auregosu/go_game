from abc import ABC, abstractmethod
import pygame
from ui.widgets.element import UIElement
from ui.widgets.button import Button

# Representation of a composition of UI elements,
# which is in itself, a UI element
class UIView(UIElement):
    # List of elements for each layer, layers are composed on top of each other
    layers: list[list[UIElement]]
    width: float
    height: float

    def __init__(self, width: float, height: float):
        super().__init__()
        self.all_children = []
        self.layers = []
        self.width = width
        self.height = height
        self.add_layer()

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        #for layer in self.layers:
            #for element in layer:
                #element.enabled = value

    def compose(self) -> pygame.surface.Surface:
        canvas = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        for layer in self.layers[1:]:
            for element in layer:
                element.draw_on(canvas)
        if len(self.layers[0]) > 0:
            for button in self.layers[0]:
                button.draw_on(canvas)
        return canvas

    def add_layer(self):
        self.layers.append(list())
    
    def add_element(self, element: UIElement, layer: int = 1):
        # Layer 0 is reserved for buttons
        if isinstance(element, Button):
            layer = 0
        while len(self.layers) < layer+1:
            self.add_layer()
        self.layers[layer].append(element)
        element.parent = self

    def remove_element(self, removed_element: UIElement):
        is_element_present = False
        layer = None
        for layer in self.layers:
            for element in layer:
                if element == removed_element:
                    is_element_present = True
                    break
            if is_element_present:
                layer = layer
                break
        layer.remove(removed_element)
    
    def poll_buttons(self, origin: tuple[float, float], mouse_pos: tuple[int, int]):
        mouse_pos = (mouse_pos[0]-origin[0], mouse_pos[1]-origin[1])
        for element in self.layers[0]:
            if element.enabled:
                element.poll((self.x, self.y), mouse_pos)