import math

Radians = float

def normalize(angle: Radians) -> Radians:
    while (angle < 0):
        angle += 2*math.pi

    while (angle >= 2*math.pi):
        angle -= 2*math.pi

    return angle

def isNormal(angle: Radians) -> bool:
    return 0 <= angle < 2*math.pi
