# Author: Erkin Otles
# Author Email: eotles@gmail.com
# Research Group: McLay Lab
# Date Started: Spring '14
# Description: Set of classes that help keep track of incident related info

import random
import Location

#TODO: Clean up self.times - come up with a better way
###############################################################################
# Times
# Class that keeps track of important response times  
class Times(object):
    def __init__(self, callTime, ambDisTime, ambArrTime, ambDepTime, ambHosTime):
        self.callTime = callTime
        self.ambDisTime = ambDisTime
        self.ambArrTime = ambArrTime
        self.ambDepTime = ambDepTime
        self.ambHosTime = ambHosTime
        
        self.timeList = list()
        self.timeList.append(self.callTime)
        self.timeList.append(self.ambDisTime)
        self.timeList.append(self.ambArrTime)
        self.timeList.append(self.ambDepTime)
        self.timeList.append(self.ambHosTime)
        
        self.difList = list()
        
        for i,t in enumerate(self.timeList):
            if(i>0):
                if(t==None):
                    self.timeList[i] = self.timeList[i-1]
                self.difList.append(self.timeList[i]-self.timeList[i-1])
                
    
    def toString(self):
        return("%s\t%s\t%s\t%s\t%s" %(tToS(self.callTime), tToS(self.ambDisTime), 
                                      tToS(self.ambArrTime), tToS(self.ambDepTime), 
                                      tToS(self.ambHosTime)))
        
###############################################################################
# IncidentStatus
# Class to keep track of incident status information
# Params:
#    priority
#    kind
#    hospital
class IncidentStatus(object):
    def __init__(self, priority, kind, hospital):
            self.priority = priority
            self.kind = kind
            self.hospital = hospital

###############################################################################
# IncidentStatusPair
# Class to keep track of hidden (true) status vs observed status  
class IncidentStatusPair(object):
    def __init__(self,priority,kind, hospital):
        self.hid = IncidentStatus(priority, kind, hospital)
        self.obs = self.genObs()
    
    def genObs(self):
        return IncidentStatus(self.hid.priority, self.hid.kind, self.hid.hospital)

#TODO: keep track of incident status pairs
#TODO: make this ABC with two children (display & no display) for performance
#TODO: Use the Times object better
###############################################################################
# Incident
# Class to keep track of information pertaining to a specific
#    incident
# Params:
#    env - simulation env
#    name - name of caller
#    hospital - hospital caller would need to go to
#    displayStatus - if incident should display info during simulation runs 
class Incident(object):
    def __init__(self, env, name, hospital, displayStatus):
        self.location = Location.Location("",random.randint(1,9),random.randint(1,9))
        self.env = env
        self.name = name
        self.calltime = env.now
        self.priority = random.randint(0,1)
        self.caretime = random.randint(3,20)
        self.ambDisTime = None
        self.ambArrTime = None
        self.ambDepTime = None
        self.ambHosTime = None
        self.responder = None
        self.hospital = hospital
        self.displayStatus = displayStatus
        self.status = IncidentStatusPair(self.priority, self.priority, self.hospital)
        self.status.hid.priority = random.randint(0,1)
        self.disTime = dict()
        self.arrTime = dict()
        self.depTime = dict()
        self.hosTime = dict()

        if(self.displayStatus):
            print('%s: calls 911 at %.2f.' %(self.name, self.calltime))
        
    #call when a responder has been dispatched for incident    
    def ambDis(self, responder=None):
        self.ambDisTime = self.env.now
        if(self.displayStatus):
            print('%s: Amb dispatched at %.2f.' %(self.name, self.ambDisTime))
        if(responder != None):
            self.dispatch(responder)
    #logic to protect against multiple calls?
    def dispatch(self, responder):
        self.disTime.update({responder: self.env.now})
        
    #call when a responder has arrived at incident
    def ambArr(self, responder = None):
        self.ambArrTime = self.env.now
        if(self.displayStatus):
            print('%s: Amb arrived at %.2f.' %(self.name, self.ambArrTime))
        if(responder != None):
            self.arrival(responder)
    #logic to protect against multiple calls?
    def arrival(self, responder):
        self.arrTime.update({responder: self.env.now})
            
    #call when responder has departed the incident scene
    def ambDep(self, responder = None):
        self.ambDepTime = self.env.now
        if(self.displayStatus):
            print('%s: Amb leaves at %.2f.' %(self.name, self.ambDepTime))
        if(responder != None):
            self.departure(responder)
    #logic to protect against multiple calls?
    def departure(self, responder):
        self.depTime.update({responder: self.env.now})
            
    #call when the responder arrives at the hospital for given incident
    def ambHos(self, responder = None):
        self.ambHosTime = self.env.now
        if(self.displayStatus):
            print('%s: Amb-Hosp at %.2f' %(self.name, self.ambHosTime))
        if(responder != None):
            self.hospitalize(responder)
    #logic to protect against multiple calls?
    def hospitalize(self, responder):
        self.hosTime.update({responder: self.env.now})
            
    #sets the responder
    def setResponder(self, x):
        self.responder =  x
    #put weird self.times into usable Times objects
    def getTimesList(self):
        self.times = Times(self.calltime, self.ambDisTime, self.ambArrTime, 
                           self.ambDepTime, self.ambHosTime)
        return(self.times)
    #return string of incident information
    def toString(self):
        self.getTimesList()
        return('%s\t%i\t%s\t%s\t%s' 
               %(self.name, self.status.hid.priority, self.location.toString(), 
                 self.times.toString(), str(self.responder)))

#Method to convert times (numbers) into pretty strings       
def tToS(time):
        outString = "None"
        if(time):
            outString = ("%.2f" %time)
        return outString
