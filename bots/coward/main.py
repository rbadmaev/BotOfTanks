#!/usr/bin/python3.8

import json
import math

def send_request(acceleration, canon_rotate_to, shoot):
    print(json.dumps({
        "acceleration": acceleration,
        "canon_rotate_to": canon_rotate_to,
        "shoot": shoot
    }),
    flush=True)

def getDistance(tank1, tank2):
    return math.sqrt(
        math.pow(tank1["position"][0] - tank2["position"][0], 2) +
        math.pow(tank1["position"][1] - tank2["position"][1], 2))

def getAngle(x, y):
    if x > 0 and y > 0:
        return math.atan(y / x)

    if x < 0 and y < 0:
        return 3/2*math.pi - math.atan(y / x)

    if x < 0:
        return math.pi - math.atan(abs(y / x))

    if x > 0:
        return 2*math.pi - math.atan(abs(y / x))

    if y > 0:
        return math.pi / 2

    return 3/2*math.pi

print("coward bot")

while True:
    dictRequest = json.loads(input())
    mapSize = dictRequest['map_size']
    me = dictRequest['me']
    enemies = dictRequest['enemies']
    bullets = dictRequest['bullets']

    closestEnemy = None
    closestEnemyDistance = 100000
    for enemy in enemies:
        distance = getDistance(me, enemy)
        if distance < closestEnemyDistance:
            closestEnemy = enemy
            closestEnemyDistance = distance

    if closestEnemy == None:
        send_request(acceleration = [0,0],
                     canon_rotate_to = 0,
                     shoot = False)
        continue

    xDistance = closestEnemy["position"][0] - me["position"][0]
    yDistance = closestEnemy["position"][1] - me["position"][1]
    canonAngle = me["canon_angle"]
    angleToEnemy = getAngle(xDistance, yDistance)
    send_request(acceleration = [yDistance, xDistance],
                 canon_rotate_to = angleToEnemy,
                 shoot = abs(canonAngle - angleToEnemy) < 0.1)



