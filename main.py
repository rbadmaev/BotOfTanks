from Game import Game
from Vector import Vector

import os

game = Game(Vector(x=800, y=600))
for path in os.listdir("bots/"):
    game.addBot(os.path.abspath(os.path.join("bots", path)))

game.start()


