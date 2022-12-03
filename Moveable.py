from Vector import Vector

import Time

class Moveable:
    def __init__(self,
                 maxSpeed: float,
                 maxAcceleration: float,
                 radius: int,
                 position: Vector = Vector(0,0),
                 speed: Vector = Vector(0,0)):
        self._position = position
        self._speed = speed
        self._acceleration = Vector(0,0)
        self._time = Time.getTime()

        self._radius = radius
        self._maxSpeed = maxSpeed
        self._maxAcceleration = maxAcceleration

    def changeAcceleration(self,
                           acceleration: Vector,
                           now: Time.Time) -> None:
        assert(now > self._time)
        duration = now - self._time
        self._position = self.calculatePosition(now)
        self._speed =  self.speed(now)
        self._time = now
        self._acceleration = acceleration.shorten(self._maxAcceleration)

    def calculatePosition(self,
                          now: Time.Time) -> Vector:
        duration = now - self._time
        # TODO: take in account maxSpeed
        return self._position + self._speed * duration + self._acceleration * (duration * duration / 2)

    def radius(self) -> int:
        return self._radius

    def smoothStop(self, now: Time.Time):
        self._acceleration = Vector(0,0)
        self._speed *= 0.9
        if self._speed.lenght() < 1:
            self._speed = Vector(0,0)

        self._position = self.calculatePosition(now)
        self._time = now

    def immediateStop(self, now: Time.Time):
        self._position = self.calculatePosition(now)
        self._speed = Vector(0,0)
        self._acceleration = Vector(0,0)
        self._time = now

    def speed(self, now: Time.Time):
        duration = now - self._time
        return (self._speed + self._acceleration * duration).shorten(self._maxSpeed)

    def intersect(self,
                  other,
                  now: Time.Time) -> bool:
        selfPosition = self.calculatePosition(now)
        otherPosition = other.calculatePosition(now)
        distance = (selfPosition - otherPosition).lenght()
        return distance < (self.radius() + other.radius())

    def getJsonStruct(self, now: Time.Time):
        speed = self.speed(now)
        return {"position": self.calculatePosition(now).getJsonStruct(),
                "radius": self.radius(),
                "movement": [speed.x, speed.y],
                "max_acceleration": self._maxAcceleration}
