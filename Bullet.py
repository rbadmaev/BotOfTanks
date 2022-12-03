from Moveable import Moveable
from Vector import Vector
import Time

import pygame

class Bullet(Moveable):
    def __init__(self,
                 position: Vector,
                 direction: Vector,
                 maxSpeed: float = 100,
                 radius: int = 5):
        assert(direction.lenght() > 0)
        super().__init__(position = position,
                         maxSpeed = maxSpeed,
                         speed = direction.resize(maxSpeed),
                         maxAcceleration = 0,
                         radius = radius)

    def draw(self, screen, now: Time.Time):
        position = self.calculatePosition(now)
        pygame.draw.circle(screen, (255, 0, 0), [position.x, position.y], self.radius())

    def drawExplosion(self, screen, now: Time.Time):
        position = self.calculatePosition(now)
        pygame.draw.circle(screen, (255, 0, 0), [position.x, position.y], 2*self.radius())
