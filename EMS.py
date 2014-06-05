import math
import random
#import queue


seed = 42
population = 100
startTime = 0
#rnd = random.Random(seed)
random.seed(seed)



class Call(object):
    def __init__(self, time, location, severity):
        self.time = time
        self.location = location
        self.severity = severity
    def toString(self):
        return("%s | %s | %s" % (self.time, self.location, self.severity))
        
class Location(object):
    def __init__(self, pos):
        self.pos = pos
    def distance(self,toLocation):
        return math.fabs(self.pos - toLocation.pos)
    
def genCallList(startTime, population):
    calls = list()
    currTime = startTime
    for _ in range(population):
        tba = random.expovariate(1/10.0)
        loc = int(random.uniform(0,9))
        sev = int(random.uniform(0,4))
        currTime += tba
        currCall = Call(currTime,loc,sev)
        calls.append(currCall)
    return calls

def dispatch(calls):
    1+1
      
class responder(object):
    def __init__(self):
        self.timeAvail = 0 


def main():
    calls = genCallList(startTime, population);
    
    for call in calls:
        print(call.toString())

    
if __name__=='__main__':
    main()
