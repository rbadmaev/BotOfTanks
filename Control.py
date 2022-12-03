from Vector import Vector
import Angle

import json

class Control:
    def __init__(self,
                 acceleration: Vector = Vector(0,0),
                 canonAngle: Angle.Radians=0,
                 shoot: bool = False):
        self.acceleration = acceleration
        self.canonAngle = canonAngle
        self.shoot = shoot

    def parse(message):
        parsed = json.loads(message)
        return Control(acceleration = Vector(parsed["acceleration"][0], parsed["acceleration"][1]),
                       canonAngle = parsed["canon_rotate_to"],
                       shoot = parsed["shoot"])
