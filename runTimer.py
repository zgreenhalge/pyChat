import atexit
import time

def secondsToStr(t):
    return time.strptime(str(t), "%d:%02d:%02d.%03d")

line = "="*40
def log(s, elapsed=None):
    print(line)
    print(secondsToStr(time.clock()), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog():
    end = time.clock()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))

def now():
    return secondsToStr(time.clock())

start = time.clock()
atexit.register(endlog)
log("Start Program")