#sic AI on it
#preparedness evaluator
#state of the system variables
#figure out whether or not ambulance will be done in 5 minutes
#dispositions - predicted vs true states

import random
import simpy

SEED = 42
NUM_AMB = 2
TBA = 6
SIM_TIME = 100000
TRAVELRATE = 0.25

#EMS Resources
#TODO: Support Different Types of Emergency Responders
#TODO: Implement book-keeping - maybe by making a subclass of resources??
#TODO: Prioritize calls coming in
#TODO: Keep summary statistics
#TODO: Scheduling of resources
class EMS(object):
    #AMS has limited number of ambulances (NUM_AMB)
    def __init__(self, env, num_amb):
        self.env = env
        self.amb = simpy.Resource(env, num_amb)
    #Care process - either heal or stabilize and take to hospital based on priority
    def care(self, inc):
        #
        inc.setResponder(id(self.amb))
        if(inc.priority>0):
            yield self.env.timeout(inc.caretime)
            print("%s: *healed!*" %(inc.name))
            inc.ambDep()
        else:
            yield self.env.timeout(inc.caretime)
            inc.ambDep()
            yield self.env.timeout(random.expovariate(.75)*TRAVELRATE*(9-inc.location))
            print("%s: *needs hospitalization!*" %(inc.name))
            inc.ambHos()
    #Process to travel to patient initially
    def travelToInc(self, inc):
        yield self.env.timeout(random.expovariate(1)*TRAVELRATE*inc.location)
        inc.ambArr()

#Individual call incidents - randomly generates call information and has book-keeping methods
#TODO: Input analysis for call information
#TODO: Summary statistic reports                
class Incident(object):
    def __init__(self,env,name):
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
        #tab = "\t"
        return('%s\t%i\t%i\t%s\t%s\t%s\t%s\t%s\t%s' 
               %(self.name, self.priority, self.location, tToS(self.calltime), tToS(self.ambDisTime), tToS(self.ambArrTime), tToS(self.ambDepTime), tToS(self.ambHosTime), str(self.responder)))

#Creates a nice string of simulation clock time
def tToS(time):
            outString = "None"
            if(time):
                outString = ("%.2f" %time)
            return outString

#Initiates call process - creates incident objects
#Requests resource (EMS)
#Waits for resources - time resources available for incident is ambulance dispatch time
#Resource travels to incident (from home base (location 0))
#Resource arrives and begins care process
#TODO: This will likely be the home of dispatcher logic
def call(env, incList, name, ems):
    #keep track of all calls/incidents in a incident list
    inc = Incident(env, name)
    incList.append(inc)
    with ems.amb.request() as request:
        #request and wait
        yield request
        inc.ambDis()
        #travel and care
        yield env.process(ems.travelToInc(inc))
        yield env.process(ems.care(inc))

#Sets up the simulation
#Process to generates all calls over the time period
#Ensures that incidents cannot start after time horizon (SIM_TIME)  
def setup(env, incList, num_amb, tba):
        #make emergency responder resources
        ems = EMS(env, num_amb)
        #starts all call processes
        i=0
        condition = True
        while condition:
            intArr = random.expovariate(1.0/tba)
            if(intArr < SIM_TIME-env.now):
                yield env.timeout(intArr)
                env.process(call(env, incList, 'Person %d' %i, ems))
                i+=1
            else:
                condition = False


horizBar = "----------------------------------------------------------------------"            
print('EMS!\n%s' %horizBar)

#setup environment and simulation
random.seed(SEED)
env = simpy.Environment()
incList = list()
env.process(setup(env, incList, NUM_AMB, TBA))

#run simulation
env.run()

#print incident summary table
print(horizBar)
for inc in incList:
    print(inc.toString())