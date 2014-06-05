"""

"""
import simpy
import math
import random
import sys

SEED = 42
SIM_DURATION = 100
NUM_AMB = 5
TBA = 5
END_BUFFER = 5
#HOSPITAL = Location("Hospital", 0, 0)


class Location(object):
    def __init__(self, name, x_cord, y_cord):
        self.name = name
        self.x_cord = x_cord
        self.y_cord = y_cord
    
    def dist(self, Location):
        return(math.sqrt((Location.x_cord-self.x_cord)**2+(Location.y_cord-self.y_cord)**2))      

STATION = Location("Station", 0, 0)
HOSPITAL = Location("Hospital", 9, 9)

class Responder(object):
    def __init__(self, env, name, kind, station, currLocation, speed):
        self.env = env
        self.name = name
        self.kind = kind
        self.station = station
        self.currLocation = currLocation
        self.speed = speed
        self.timeAvail = env.now
    
    def travelTo(self, Location):
        travelTime = self.speed*Location.dist(self.currLocation)
        #print(travelTime)
        yield self.env.timeout(travelTime)
        self.currLocation = Location
        #print(self.currLocation)
    
    def careIncident(self, Incident):
        self.timeAvail = env.now + 3*Incident.caretime
        yield self.env.timeout(Incident.caretime)
        if(Incident.priority>0):
            print("%s: *healed!*" %(Incident.name))
            Incident.ambDep()
        else:
            Incident.ambDep()
            yield self.env.process(self.travelTo(HOSPITAL))
            print("%s: *needs hospitalization!*" %(Incident.name))
            Incident.ambHos()

class Dispatcher(object):
    def __init__(self, env):
        self.env = env
        self.free = simpy.FilterStore(env)
        self.incidentList = list()
        self.responderList = list()
        
        for i in xrange(NUM_AMB):
            tempAmb = Responder(self.env, "amb_"+str(i), "amb", STATION, STATION, 0.25)
            self.responderList.append(tempAmb)
            self.free.put(tempAmb)
        
        #self.env.process(self.incidentGenerator())

    def makeResponders(self):
            for i in xrange(NUM_AMB):
                tempAmb = Responder(self.env, "amb_"+str(i), "amb", STATION, STATION, 0.25)
                self.responderList.append(tempAmb)
                self.free.put(tempAmb)
    
    def sendToIncident(self, Responder, Incident):
        #self.env.process(self.send(Responder, Incident.Location))
        yield self.env.process(Responder.travelTo(Incident.Location))
        Incident.ambArr()
        yield self.env.process(Responder.careIncident(Incident))
        self.free.put(Responder)
    
    def incidentGenerator(self):
        while True:
            intArr = random.expovariate(1.0/TBA)
            yield env.timeout(intArr)
                  
            inc = Incident(env, 'Person %d' %len(self.incidentList))
            self.incidentList.append(inc)
            self.env.process(self.incidentRespose(inc))
        
    def incidentRespose(self, inc):
            best =  self.assignResponder()
            print(best.name)
    
            #responder = yield self.free.get(filter = lambda r : r.name==best.name)
            responder = yield self.free.get()

            inc.ambDis()
            inc.responder = responder.name
            yield self.env.process(self.sendToIncident(responder, inc))
        
    
    def isBestResponder(self, resp, best):
        return(resp.name==best.name)
    
    def assignResponder(self):
        firstAvailTime = sys.float_info.max
        firstResponder = None
        for Responder in self.responderList:
            if(Responder.timeAvail < firstAvailTime):
                firstAvailTime = Responder.timeAvail
                firstResponder = Responder
        return(firstResponder)
                

class IncidentGenerator(object):
    def __init__(self, env, Dispatcher):
        self.env = env
        self.Dispatcher = Dispatcher
        self.incidentList = list()
        self.env.process(self.incidentGenerator())
    
    def incidentGenerator(self):
        condition = True
        while condition:
            intArr = random.expovariate(1.0/TBA)
            if(intArr < SIM_DURATION - END_BUFFER - env.now):
                intArr = random.expovariate(1.0/TBA)
                yield env.timeout(intArr)
                      
                inc = Incident(env, 'Person %d' %len(self.incidentList))
                self.incidentList.append(inc)
                self.env.process(self.Dispatcher.incidentRespose(inc))
            else:
                condition = False
                        
            


class Incident(object):
    def __init__(self,env,name):
        self.Location = Location("",random.randint(1,9),random.randint(1,9))
        self.env = env
        self.name = name
        self.calltime = env.now
        self.priority = random.randint(0,2)
        self.location = random.randint(0,8)
        self.caretime = random.randint(3,20)
        self.ambDisTime = None
        self.ambArrTime = None
        self.ambDepTime = None
        self.ambHosTime = None
        self.responder = None
        #self.ambID = None
        print('%s: calls 911 at %.2f.' %(self.name, self.calltime))
    def ambDis(self):
        self.ambDisTime = env.now
        print('%s: Amb dispatched at %.2f.' %(self.name, self.ambDisTime))
    def ambArr(self):
        self.ambArrTime = env.now
        print('%s: Amb arrived at %.2f.' %(self.name, self.ambArrTime))
    def ambDep(self):
        self.ambDepTime = env.now
        print('%s: Amb leaves at %.2f.' %(self.name, self.ambDepTime))
    def ambHos(self):
        self.ambHosTime = env.now
        print('%s: Amb-Hosp at %.2f' %(self.name, self.ambHosTime))
    def setResponder(self, x):
        self.responder =  x
    def toString(self):
        return('%s\t%i\t%i\t%s\t%s\t%s\t%s\t%s\t%s' 
               %(self.name, self.priority, self.location, tToS(self.calltime), tToS(self.ambDisTime), tToS(self.ambArrTime), tToS(self.ambDepTime), tToS(self.ambHosTime), str(self.responder)))

#Creates a nice string of simulation clock time
def tToS(time):
            outString = "None"
            if(time):
                outString = ("%.2f" %time)
            return outString

# Setup and start the simulation
env = simpy.Environment()

#make emergency responder resources
ems = Dispatcher(env)
calls = IncidentGenerator(env, ems)

STATION = Location("Station", 0, 0)
HOSPITAL = Location("Hospital", 9, 9)


horizBar = "----------------------------------------------------------------------"            
print('EMS!\n%s' %horizBar)

#setup environment and simulation
random.seed(SEED)
#env = simpy.Environment()
#env.process(setup(env, ems, NUM_AMB, TBA))

#run simulation
env.run(until=SIM_DURATION)

#print incident summary table
print(horizBar)
for inc in calls.incidentList:
    print(inc.toString())