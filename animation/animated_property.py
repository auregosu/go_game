from animation.easing import linear

class AnimatedProperty:
    def __init__(self, obj: any, property_name: str, 
                 start_value: float, end_value: float, 
                 duration_ms: int, transition=linear, delay_ms=0):
        self.obj = obj
        self.property_name = property_name
        self.start_value = start_value
        self.end_value = end_value
        self.duration_ms = duration_ms
        self.delay_ms = delay_ms
        self.transition = transition
        self.elapsed_ms = 0
        self.delay_elapsed_ms = 0
        self.ready = True if delay_ms == 0 else False
    
    def start(self):
        setattr(self.obj, self.property_name, self.start_value)
        self.elapsed_ms = 0
        self.ready = True if self.delay_ms == 0 else False
        self.finished = False
    
    def update(self, delta_time: int):
        if self.finished:
            return
        # First go through the delay
        if not self.ready:
            self.delay_elapsed_ms += delta_time
            setattr(self.obj, self.property_name, self.start_value)
            if self.delay_elapsed_ms >= self.delay_ms:
                self.ready = True
            # Then start the animation
        else:
            self.elapsed_ms += delta_time
            if self.elapsed_ms >= self.duration_ms:
                setattr(self.obj, self.property_name, self.end_value)
                self.finished = True
            else:
                t = self.elapsed_ms / self.duration_ms
                eased_t = self.transition(t)
                value = self.start_value + (self.end_value - self.start_value) * eased_t
                setattr(self.obj, self.property_name, value)
