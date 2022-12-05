import Time
from Control import Control

import os
import threading
import json
from subprocess import Popen, PIPE, STDOUT
import sys

class Bot:
    def __init__(self, game, path, tank):
        self._game = game
        self._thread = threading.Thread(target=self._botFunc,
                                        args=([os.path.join(path, "main.py")], tank))

    def _botFunc(self, command, tank):
        process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=sys.stderr, text=True, bufsize=0, universal_newlines=True, shell=True)
        name = process.stdout.readline()
        tank.setName(name)
        print("start", name)
        while tank.isAlive() and not self._game.isFinished():
            if self._game.paused():
                Time.sleep(0.1)
                continue

            now = Time.getTime()
            s = self._game.getJsonStruct(tank, now)
            stateMsg = json.dumps(self._game.getJsonStruct(tank, now))
            process.stdin.write(stateMsg + "\n")
            answer = process.stdout.readline()
            control = Control.parse(answer)
            if tank.isAlive():
                tank.setControl(control)

        print("terminame ", name)
        process.terminate()

    def start(self):
        self._thread.start()
