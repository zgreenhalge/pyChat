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