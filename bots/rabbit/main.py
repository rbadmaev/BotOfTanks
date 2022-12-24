#!/usr/bin/python3.8

import json
import math
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def send_request(acceleration, canon_rotate_to, shoot):
    print(json.dumps({
        "acceleration": acceleration,
        "canon_rotate_to": canon_rotate_to,
        "shoot": shoot
    }),
    flush=True)

def getDistance(position1, position2):
    return math.sqrt(
        math.pow(position1[0] - position2[0], 2) +
        math.pow(position1[1] - position2[1], 2))

def getTanksDistance(tank1, tank2):
    return getDistance(tank1["position"], tank2["position"])

def normalizeAngle(angle):
    while (angle < 0):
        angle += 2*math.pi

    while (angle >= 2*math.pi):
        angle -= 2*math.pi

    return angle

def getAngle(x, y):
    if x > 0:
        return normalizeAngle(math.atan(y / x))
    elif x < 0:
        if y > 0:
            return math.atan(y / x) + math.pi
        else:
            return math.atan(y / x) + math.pi

    assert(x == 0)
    if y == 0:
        return 0

    return math.pi / 2 + (math.pi if y < 0 else 0)

def rotateVector(vector, angle):
    return [
        vector[0]*math.cos(angle) - vector[1]*math.sin(angle),
        vector[0]*math.sin(angle) + vector[1]*math.cos(angle)
    ]

def getVector(angle, lenght):
    return [math.cos(angle) * lenght, math.sin(angle) * lenght]

def getVecotorSize(vector):
    return math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))

def shortenVector(vector, size):
    currentSize = getVecotorSize(vector)
    return[vector[0] * size / currentSize, vector[1] * size / currentSize]

def avoidBorders(size, position, speed, acceleration, maxAcceleration, radius):
    result = acceleration
    realAcceleration = maxAcceleration / math.sqrt(2) # use max half of acceleration to avoid borders
    def getAcceleration(dim):
        speedInDim = abs(speed[dim])
        timeToStop = speedInDim / realAcceleration
        stopDistance = speedInDim * timeToStop + realAcceleration * math.pow(timeToStop, 2) / 2
        distance = (size[dim] - position[dim] if speed[dim] > 0 else position[dim]) - radius
        if 1.05 * distance <= stopDistance:

            return -math.copysign(realAcceleration, speed[dim])

        futureTime = 0.5
        distance = (size[dim] - position[dim] if acceleration[dim] > 0 else position[dim]) - radius
        moveDistance = abs(acceleration[dim]) * math.pow(futureTime, 2) / 2
        if moveDistance >= distance:
            return 0

        return acceleration[dim]


    return [getAcceleration(0), getAcceleration(1)]

print("Rabbit")

while True:
    dictRequest = json.loads(input())
    mapSize = dictRequest['map_size']
    me = dictRequest['me']
    enemies = dictRequest['enemies']
    bullets = dictRequest['bullets']

    mainEnemy = None
    mainEnemyDistance = 100000
    for enemy in enemies:
        if enemy["health"] <= 0:
            continue

        distance = getTanksDistance(me, enemy)
        if distance < mainEnemyDistance:
            mainEnemy = enemy
            mainEnemyDistance = distance

    if mainEnemy == None:
        send_request(acceleration = [0,0],
                     canon_rotate_to = 0,
                     shoot = False)
        continue

    xDistance = mainEnemy["position"][0] - me["position"][0]
    yDistance = mainEnemy["position"][1] - me["position"][1]
    canonAngle = me["canon_angle"]
    angleToEnemy = getAngle(xDistance, yDistance)

    send_request(acceleration = avoidBorders(size = mapSize,
                                             position = me["position"],
                                             speed = me["movement"],
                                             acceleration = shortenVector([yDistance, -xDistance], me["max_acceleration"]),
                                             maxAcceleration = me["max_acceleration"],
                                             radius = me["radius"]),
                 canon_rotate_to = angleToEnemy,
                 shoot = abs(canonAngle - angleToEnemy) < 0.05)



