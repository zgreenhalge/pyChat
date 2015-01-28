import atexit
import time

#Provides a timing framework for a python program
#Will automatically record the time on running the script
#And registers itself for execution on interpreter termination

def secondsToStr(t):
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

line = "="*40
def log(s):
    print(line)
    print(time.ctime() + ' - ' + s)
    if start:
        dif = elapsed()
        print("Elapsed time: " + secondsToStr(dif) + " (" + str(dif)[:16] + ")")
    print(line)
    print()

start = time.clock()
def elapsed():
    return time.clock()-start

def endlog():
    log("End Program")

def now():
    return time.ctime()

atexit.register(endlog)
log("Start Program")

