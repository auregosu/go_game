from typing import Callable
from animation.animated_property import AnimatedProperty
from animation.easing import linear

class Animation:
    properties: list[AnimatedProperty]
    on_complete: Callable
    finished: bool
    
    def __init__(self, on_complete: Callable = None):
        self.properties = []
        self.on_complete = on_complete
        self.finished = False
    
    def add_property(self, obj: any, property_name: str, 
                    start_value: float, end_value: float,
                    duration_ms: int, transition=linear, delay_ms=0):
        prop = AnimatedProperty(obj, property_name, start_value, end_value, 
                               duration_ms, transition, delay_ms)
        self.properties.append(prop)
    
    def start(self):
        for prop in self.properties:
            prop.start()
        self.finished = False
    
    def update(self, delta_time: int):
        if self.finished:
            return
        
        all_complete = True
        for prop in self.properties:
            prop.update(delta_time)
            if not prop.finished:
                all_complete = False
        
        if all_complete:
            self.finished = True
            if self.on_complete:
                self.on_complete()
