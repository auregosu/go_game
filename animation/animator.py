from animation.animation import Animation
from animation import easing
from ui.widgets.element import UIElement
from globals import HEIGHT

class Animator:
    def __init__(self):
        self.animations: list[Animation] = []
    
    def add(self, animation: Animation):
        animation.start()
        self.animations.append(animation)
    
    def update(self, delta_time: int):
        for animation in self.animations:
            animation.update(delta_time)
        # Remove completed
        self.animations = [i for i in self.animations if not i.finished]
    
    def clear(self):
        self.animations.clear()
    
    def is_busy(self):
        return len(self.animations) > 0

def fade_out_element(animator: Animator, element: UIElement, duration_ms: int, delay_ms: int = 0):
    def disable_element(e=element):
        e.enabled = False
    fade_out = Animation(disable_element)
    fade_out.add_property(element, "opacity", 1.0, 0, duration_ms, easing.linear, delay_ms)
    animator.add(fade_out)

def fade_in_element(animator: Animator, element: UIElement, duration_ms: int, delay_ms: int = 0):
    element.enabled = True
    fade_in = Animation()
    fade_in.add_property(element, "opacity", 0, 1.0, duration_ms, easing.linear, delay_ms)
    animator.add(fade_in)

def slide_out_element(animator: Animator, element: UIElement, duration_ms: int, delay_ms: int = 0):
    element.enabled = True
    fade_in = Animation()
    fade_in.add_property(element, "y", element.y, -HEIGHT, duration_ms, easing.in_quadratic, delay_ms)
    animator.add(fade_in)
