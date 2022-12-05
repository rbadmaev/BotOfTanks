import Angle
import Time
from Vector import Vector

import math

class Rotateable:
    def __init__(self,
                 direction: Angle.Radians,
                 rotateSpeed: Angle.Radians):
        self._direction = Angle.normalize(direction)
        self._time = Time.getTime()
        self._targetAngle = self._direction

        self._rotateSpeed = rotateSpeed

    def caclculateDirection(self,
                            now: Time.Time) -> Angle.Radians:
        assert(Angle.isNormal(self._direction))
        assert(Angle.isNormal(self._targetAngle))

        duration = now - self._time

        if duration * self._rotateSpeed >= math.pi:
            return self._targetAngle

        greaterAngle = self._targetAngle if self._targetAngle >= self._direction else self._targetAngle + 2*math.pi
        if greaterAngle - self._direction <= math.pi:
            rotateAngle = greaterAngle - self._direction
            if rotateAngle <= duration * self._rotateSpeed:
                return self._targetAngle
            else:
                return Angle.normalize(self._direction + duration * self._rotateSpeed)
        else:
            rotateAngle = 2*math.pi - (greaterAngle - self._direction)
            if rotateAngle <= duration * self._rotateSpeed:
                return self._targetAngle
            else:
                return Angle.normalize(self._direction - duration * self._rotateSpeed)

        assert(not "Unreachable code")

    def changeTargetAngle(self,
               now: Time.Time,
               targetAngle: Angle.Radians) -> None:
        self._direction = self.caclculateDirection(now)
        self._time = now
        self._targetAngle = Angle.normalize(targetAngle)


    def directionOrt(self, now: Time.Time) -> Vector:
        angle = self.caclculateDirection(now = now)
        return Vector(x = math.cos(angle),
                      y = math.sin(angle))

    def targetOrt(self) -> Vector:
        angle = self._targetAngle
        return Vector(x = math.cos(angle),
                      y = math.sin(angle))

    def rotateSpeed(self) -> Angle.Radians:
        return self._rotateSpeed
