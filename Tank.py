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
        self._game = game
        self._name = "Nemo"
        self._health = health
        self._bullet = None
        self._canon = Rotateable(direction = 0, # math.radians(random.uniform(0, 359)),
                                 rotateSpeed = canonSpeed)

        self._sprite = pygame.transform.scale(pygame.image.load(os.path.join (path, "tank.png")),
                                              (radius*2, radius*2))
        self._deadSprite = pygame.transform.scale(pygame.image.load(os.path.join (path, "deadTank.png")),
                                              (radius*2, radius*2))
        self._maxHealth = health

    def setName(self, name):
        assert(len(name) > 0)
        if name[-1] == '\n':
            name = name[:-1]

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
        self.hit()
        self.immediateStop(now)

    def hit(self):
        self._health -= 1
        if self._health <= 0:
            self._game.notifyDeadTank(self)

    def draw(self, screen, now: Time.Time):
        position = self.calculatePosition(now)
        speed = self.speed(now)
        canonAngle = self._canon.caclculateDirection(now)
        if self._game.showDebug():
            pygame.draw.circle(screen, (0, 0, 0), [position.x, position.y], self.radius())
            font = pygame.font.Font(pygame.font.get_default_font(), 20)
            healthText = font.render(str(self._health) , False, (255, 100, 125))
            screen.blit(healthText, (position.x  - healthText.get_width() / 2, position.y - healthText.get_height() / 2))

            font = pygame.font.Font(pygame.font.get_default_font(), 12)
            nameText = font.render(self.getName(), False, (200, 200, 200))
            screen.blit(nameText, (position.x - nameText.get_width() / 2, position.y - nameText.get_height() - self._radius*1.1))

        if self._game.showSkins():
            image = pygame.transform.rotate(self._sprite  if self.isAlive() else self._deadSprite,
                                             - 90 - math.degrees(canonAngle) )
            screen.blit(image, (position.x - image.get_width() / 2, position.y - image.get_height() / 2))

            def getHealthX(percent):
                healthLen = self._radius * 2
                healthXStart = position.x - self._radius
                return max(healthXStart + healthLen * percent, healthXStart)

            healthY = position.y + self._radius*1.1
            healthPercent = self._health / self._maxHealth
            healthX = getHealthX(healthPercent)
            pygame.draw.line(screen, (10, 255, 50), [getHealthX(0), healthY], [healthX, healthY])
            pygame.draw.line(screen, (255, 10, 50), [healthX, healthY], [getHealthX(1), healthY])

        if self._game.showDebug():
            canon = self._canon.directionOrt(now) * (self.radius() * 1.2)
            canonTarget = self._canon.targetOrt() * (self.radius() * 1.5)
            targetStart = self._canon.targetOrt() * self.radius()
            pygame.draw.line(screen, (0, 255, 255), [position.x, position.y], [position.x + speed.x, position.y + speed.y])
            pygame.draw.line(screen, (255, 0, 0), [position.x, position.y], [position.x + canon.x, position.y + canon.y])
            pygame.draw.line(screen, (255, 0, 0), [position.x + targetStart.x, position.y + targetStart.y], [position.x + canonTarget.x, position.y + canonTarget.y])

    def explodeBullet(self):
        self._bullet.explode()

    def removeBullet(self):
        self._bullet = None

    def bullet(self):
        return self._bullet

    def getJsonStruct(self, now: Time.Time) -> dict:
        result = super().getJsonStruct(now)
        result["canon_angle"] = self._canon.caclculateDirection(now)
        result["canon_rotate_speed"] = self._canon.rotateSpeed()
        result["health"] = self._health
        return result

