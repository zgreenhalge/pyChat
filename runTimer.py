import atexit
import time

def secondsToStr(t):
    print "*"*25 + str(t)
    return time.strptime("%H:%M:%S")

line = "="*40
def log(s, elapsed=None):
    print line
    print time.ctime() + ' - ' + s
    if elapsed:
        print "Elapsed time: " + elapsed
    print line
    print 

def endlog():
    end = time.clock()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))

def now():
    return time.ctime()

start = time.clock()
atexit.register(endlog)
log("Start Program")