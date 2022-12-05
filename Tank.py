from Control import Control
from Moveable import Moveable
from Rotateable import Rotateable
from Vector import Vector
from Bullet import Bullet
import Angle
import Time

import random
import math
import pygame
import os
import time

class Tank(Moveable):
    def __init__(self,
                 game,
                 path,
                 position: Vector,
                 canonSpeed: Angle.Radians = 1,
                 radius: int = 15,
                 health: int = 3):
        super().__init__(maxSpeed = 50,
                          maxAcceleration = 10,
                          position = position,
                          radius = radius)
        self.game = game
        self._name = "Nemo"
        self._health = health
        self._bullet = None
        self._canon = Rotateable(direction = 0, # math.radians(random.uniform(0, 359)),
                                 rotateSpeed = canonSpeed)

        self._sprite = pygame.transform.scale(pygame.image.load(os.path.join (path, "tank.png")),
                                              (radius*2, radius*2))
        self._deadSprite = pygame.transform.scale(pygame.image.load(os.path.join (path, "deadTank.png")),
                                              (radius*2, radius*2))

    def setName(self, name):
        assert(len(name) > 0)
        self._name = name

    def getName(self):
        return self._name

    def setControl(self, control):
        now = Time.getTime()
        self.changeAcceleration(acceleration = control.acceleration,
                                now = now)
        self._canon.changeTargetAngle(targetAngle = control.canonAngle,
                                     now = now)
        # if control.shoot:
        #     print(self.getName(), "try shooting...")
        if self._bullet == None and control.shoot:
            print(self.getName(), "shooting...")
            shootDirection = self._canon.directionOrt(now)
            self._bullet = Bullet(position = self.calculatePosition(now) + shootDirection * self.radius(),
                                  direction = shootDirection)

    def isAlive(self) -> bool:
        return self._health > 0

    def hitAndStop(self, now: Time.Time):
        self.hit(now)
        self.immediateStop(now)

    def hit(self, now: Time.Time):
        self._health -= 1
        self.game.notifyDeadTank(self)

    def draw(self, screen, now: Time.Time):
        position = self.calculatePosition(now)
        speed = self.speed(now)
        canonAngle = self._canon.caclculateDirection(now)
        canon = self._canon.directionOrt(now) * (self.radius() * 1.2)
        pygame.draw.circle(screen, (0, 0, 0), [position.x, position.y], self.radius())
        image = pygame.transform.rotate(self._sprite  if self.isAlive() else self._deadSprite,
                                        math.degrees(canonAngle - math.pi / 2))
        screen.blit(image, (position.x - self._radius, position.y - self._radius))
        pygame.draw.line(screen, (0, 255, 255), [position.x, position.y], [position.x + speed.x, position.y + speed.y])
        pygame.draw.line(screen, (255, 0, 0), [position.x, position.y], [position.x + canon.x, position.y + canon.y])

    def explodeBullet(self):
        self._bullet = None

    def bullet(self):
        return self._bullet

    def getJsonStruct(self, now: Time.Time) -> dict:
        result = super().getJsonStruct(now)
        result["canon_angle"] = self._canon.caclculateDirection(now)
        result["canon_rotate_speed"] = self._canon.rotateSpeed()
        result["health"] = self._health
        return result

