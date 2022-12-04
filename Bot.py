import Time
from Control import Control

import os
import threading
import json
from subprocess import Popen, PIPE, STDOUT

class Bot:
    def __init__(self, game, path, tank):
        self._game = game
        self._thread = threading.Thread(target=self._botFunc,
                                        args=([os.path.join(path, "main.py")], tank))

    def _botFunc(self, command, tank):
        process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, text=True, bufsize=0, universal_newlines=True, shell=True)
        name = process.stdout.readline()
        tank.setName(name)
        print("start", name)
        while tank.isAlive() and not self._game.isFinished():
            now = Time.getTime()
            # try:
            s = self._game.getJsonStruct(tank, now)
            stateMsg = json.dumps(self._game.getJsonStruct(tank, now))
            # print(name, stateMsg)
            process.stdin.write(stateMsg + "\n")
            answer = process.stdout.readline()
            # print(name, answer)
            control = Control.parse(answer)
            if tank.isAlive():
                tank.setControl(control)
            # except:
            #     pass

        print("terminame ", name)
        process.terminate()

    def start(self):
        self._thread.start()