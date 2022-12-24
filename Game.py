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
        self._paused = False
        self._showSkins = True
        self._showDebug = True

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

    def draw(self, screen, now):
        screen.fill((255, 255, 255))
        for tank in self._tanks:
            tank.draw(screen, now)
            if tank.bullet():
                tank.bullet().draw(screen, now)

    def showWinner(self, screen, now, winner):
        self.draw(screen, now)
        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font.render(winner , False, (0, 0, 0))
        screen.blit(text, ((self._size.x  - text.get_width()) / 2, self._size.y / 2))
        pygame.display.flip()

    def start(self):
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode([self._size.x, self._size.y])
        for bot in self._bots:
            bot.start()

        now = Time.getTime()
        while not self.isFinished():
            prevTime = now
            now = Time.getTime()
            self._processUserActions(now, prevTime)

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
                        if tank.bullet().isExploided():
                            tank.removeBullet()
                        elif tank.bullet().intersect(otherTank, now):
                            otherTank.hit()
                            tank.explodeBullet()
                        elif otherTank.bullet() and tank.bullet().intersect(otherTank.bullet(), now):
                            tank.explodeBullet()
                            otherTank.explodeBullet()
                        elif self.outOfField(tank.bullet(), now):
                            tank.explodeBullet()

            self.draw(screen, now)
            pygame.display.flip()
            Time.sleep(0.03)

        if (len(self._aliveTanks) > 0):
            for winner in self._aliveTanks:
                break
            self.showWinner(screen, now, "Winner is " + winner.getName())

        else:
            self.showWinner(screen, now, "Draw!!!")

        self._waitForAnyKey()

        pygame.quit()

    def _waitForAnyKey(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return None

            Time.sleep(0.03)

    def _processUserActions(self, now, prevTime):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self._paused:
                        self._paused = True
                        Time.pause(self._paused)
                    else:
                        Time.tick()
                elif event.key == pygame.K_p:
                    self._paused = not self._paused
                    Time.pause(self._paused)
                elif event.key == pygame.K_d:
                    self._showDebug = not self._showDebug
                elif event.key == pygame.K_s:
                    self._showSkins = not self._showSkins
                elif event.key == pygame.K_ESCAPE:
                    self._aliveTanks.clear()

    def paused(self) -> bool:
        return self._paused

    def showDebug(self) -> bool:
        return self._showDebug

    def showSkins(self) -> bool:
        return self._showSkins

    def outOfField(self, moveable, now: Time.Time):
        position = moveable.calculatePosition(now)
        return (position.x - moveable.radius() < 0) or \
            (position.x + moveable.radius() >= self._size.x) or \
            (position.y - moveable.radius() < 0) or \
            (position.y + moveable.radius() >= self._size.y)

    def notifyDeadTank(self, tank):
        self._aliveTanks.discard(tank)
