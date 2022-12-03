from Tank import Tank
from Vector import Vector
from Bot import Bot
import Time

import pygame
import random
import json


class Game:
    def __init__(self, size: Vector):
        self._size = size
        self._tankRadius = 20
        self._tanks = []
        self._bots = []
        self._aliveTanks = set()

    def isFinished(self):
        return len(self._aliveTanks) <= 1

    def _createTank(self, path):
        intersect = True
        while intersect:
            intersect = False
            tank = Tank(game= self,
                        position=Vector(x=random.uniform(a=self._tankRadius, b=self._size.x - self._tankRadius),
                                        y=random.uniform(a=self._tankRadius, b=self._size.y - self._tankRadius)),
                        path=path,
                        radius=self._tankRadius)
            for existingTank in self._tanks:
                if tank.intersect(existingTank, Time.getTime()):
                    intersect = True
                    break

        self._tanks.append(tank)
        self._aliveTanks.add(tank)
        return tank

    def getJsonStruct(self, tank, now):
        result = {"map_size": [self._size.x, self._size.y],
                  "me": tank.getJsonStruct(now),
                  "enemies": [],
                  "bullets": []}
        enemies = result["enemies"]
        bullets = result["bullets"]
        for enemy in self._tanks:
            if enemy != tank:
                enemies.append(enemy.getJsonStruct(now))

            if enemy.bullet():
                bullets.append(enemy.bullet().getJsonStruct(now))

        return result

    def addBot(self, path):
        tank = self._createTank(path);
        self._bots.append(Bot(self, path, tank))

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode([self._size.x, self._size.y])
        for bot in self._bots:
            bot.start()

        now = Time.getTime()
        while len(self._aliveTanks) > 1:
            prevTime = now
            now = Time.getTime()
            screen.fill((255, 255, 255))
            for tank in self._tanks:
                if not tank.isAlive():
                    tank.smoothStop(now)
                    tank.draw(screen, now)
                    continue

                for otherTank in self._tanks:
                    if tank == otherTank:
                        continue

                    if tank.intersect(otherTank, now):
                        tank.hitAndStop(prevTime)
                        otherTank.hitAndStop(prevTime)

                    if self.outOfField(tank, now):
                        tank.hitAndStop(prevTime)

                    if tank.bullet():
                        if tank.bullet().intersect(otherTank, now):
                            otherTank.hit(now)
                            tank.bullet().drawExplosion(screen, now)
                            tank.explodeBullet()
                        elif otherTank.bullet() and tank.bullet().intersect(otherTank.bullet(), now):
                            tank.bullet().drawExplosion(screen, now)
                            tank.explodeBullet()
                            otherTank.explodeBullet()
                        elif self.outOfField(tank.bullet(), now):
                            tank.bullet().drawExplosion(screen, now)
                            tank.explodeBullet()
                        else:
                            tank.bullet().draw(screen, now)

            for tank in self._tanks:
                tank.draw(screen, now)

            pygame.display.flip()
            Time.sleep(0.07)

        Time.sleep(3)
        if (len(self._aliveTanks) > 0):
            for winner in self._aliveTanks:
                break
            print("Winner is", winner.getName())
        else:
            print("Draw!!")

        pygame.quit()

    def outOfField(self, moveable, now: Time.Time):
        position = moveable.calculatePosition(now)
        return (position.x - moveable.radius() < 0) or \
            (position.x + moveable.radius() >= self._size.x) or \
            (position.y - moveable.radius() < 0) or \
            (position.y + moveable.radius() >= self._size.y)

    def notifyDeadTank(self, tank):
        self._aliveTanks.remove(tank)
