import math

def linear(t: float) -> float:
    return t

def sin(t: float) -> float:
    return math.sin(t*math.pi*0.5)

def sin_bounce(t: float) -> float:
    return 0.5 * (math.sin(math.pi * (2*t - 0.5)) + 1)

def out_quadratic(t: float) -> float:
    return -t * (t - 2)

def out_cubic(t: float) -> float:
    t -= 1
    return t * t * t + 1

def out_cubic_2x(t: float) -> float:
    return out_cubic(t)**2

def in_quadratic(t: float) -> float:
    return t * t

def in_cubic(t: float) -> float:
    return t * t * t
