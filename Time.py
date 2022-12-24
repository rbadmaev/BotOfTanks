import time

Time = float
Diff = float
sleep = time.sleep

pauseDuration = Diff(0)
pauseStart = Time(0)

def tick():
    global pauseStart

    assert(pauseStart > 0)
    pauseStart = pauseStart + 0.1
    print (getTime())

def pause(enablePause: bool = True):
    global pauseDuration
    global pauseStart

    if enablePause:
        pauseStart = time.time()
    else:
        pauseDuration += time.time() - pauseStart
        pauseStart = Time(0)

def getTime():
    def scaleTime(now):
        return now / 2

    if pauseStart > 0:
        return scaleTime(pauseStart - pauseDuration)

    return scaleTime(time.time() - pauseDuration)

