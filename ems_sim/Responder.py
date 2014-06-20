# Author: Erkin Otles
# Author Email: eotles@gmail.com
# Research Group: McLay Lab
# Date Started: Spring '14
# Description: Class to represent responder

import abc

#TODO: Ways to represent off-line/on-line
#TODO: Keep track of responder utilization
#TODO: Reset responders to station?
#TODO: Fix the way speed is used
###############################################################################
# Responder
# Class representing responders that can be used during the simulation
# inputs:
#    env - simulation env
#    name - name of the responder
#    kind - the type of responder
#    station - the station of the responder
#    currLocation - the location that the responder starts at
#    speed - the speed at which at which a responder can travel (actually rate
#             because its used as time per distance)
#    displayStatus - if responder info should display status info during 
#                    simulation runs
class Responder(object):
    #__metaclass__ = abc.ABCMeta
    
    #@abc.abstractmethod
    def __init__(self, env, name, kind, station, currLocation, speed, displayStatus):
        self.env = env
        self.name = name
        self.kind = kind
        self.station = station
        self.currLocation = currLocation
        self.speed = speed
        self.timeAvail = env.now
        self.displayStatus = displayStatus
    
    #make the responder travel to a location
    #makes time elapse and updates responder location
    #@abc.abstractmethod
    def travelTo(self, Location):
        travelTime = self._getTravelTime(self.currLocation,Location)
        yield self.env.timeout(travelTime)
        self.currLocation = Location
        
    def _getTravelTime(self, fromLocation, toLocation): 
        return(self.speed*fromLocation.dist(toLocation))
    
    #assign to incident
    def assignToIncident(self, Incident):
        neededTime = 0
        neededTime += self._getTravelTime(self.currLocation, Incident.location)
        neededTime += Incident.caretime
        neededTime += self._getTravelTime(Incident.location, Incident.hospital)
        self.timeAvail = self.env.now + neededTime
        
    
    #care at incident
    #@abc.abstractmethod
    def careAtIncident(self, Incident):
        yield self.env.timeout(Incident.caretime)
    
    #depart from scene
    #@abc.abstractmethod
    def departIncidentScene(self, Incident):
        Incident.ambDep()
    
    #take to hospital
    #@abc.abstractmethod
    def toHospital(self, Incident):
        yield self.env.process(self.travelTo(Incident.hospital))
        Incident.ambHos()
    
   
    #TODO: make timeAvail work better
    #represents care process
    #set a time available
    #then heal patient or take them to the hospital 
    #@abc.abstractmethod
    def careIncident(self, Incident):
        self.assignToIncident(Incident)
        yield self.env.process(self.careAtIncident(Incident))
        if(Incident.priority>0):
            if(self.displayStatus):
                print("%s: *healed!*" %(Incident.name))
            self.departIncidentScene(Incident)
        else:
            self.departIncidentScene(Incident)
            if(self.displayStatus):
                print("%s: *needs hospitalization!*" %(Incident.name))
            self.toHospital(Incident)

#not sure this is the right way to proceed
class BLS(Responder):
    def __init__(self, env, name, kind, station, currLocation, speed, displayStatus):
        super(BLS, self).__init__(env, name, kind, station, currLocation, speed, displayStatus)
    
    #@abc.abstractmethod
    def careIncident(self, Incident):
        self.timeAvail = self.env.now + 3*Incident.caretime
        yield self.env.timeout(Incident.caretime)
        if(Incident.priority>0):
            if(self.displayStatus):
                print("%s: *healed!*" %(Incident.name))
            Incident.ambDep()
        else:
            Incident.ambDep()
            yield self.env.process(self.travelTo(Incident.hospital))
            if(self.displayStatus):
                print("%s: *needs hospitalization!*" %(Incident.name))
            Incident.ambHos()
    
    #@abc.abstractmethod
    def travelTo(self, Location):
        travelTime = self.speed*Location.dist(self.currLocation)
        yield self.env.timeout(travelTime)
        self.currLocation = Location
        
class ALS(Responder):
    def __init__(self, env, name, kind, station, currLocation, speed, displayStatus):
        super(ALS, self).__init__(env, name, kind, station, currLocation, speed, displayStatus)
    
    #@abc.abstractmethod
    def careIncident(self, Incident):
        self.timeAvail = self.env.now + 3*Incident.caretime
        Incident.ambDep()
        yield self.env.process(self.travelTo(Incident.hospital))
        if(self.displayStatus):
            print("%s: *needs hospitalization!*" %(Incident.name))
        Incident.ambHos()
    
    #@abc.abstractmethod
    def travelTo(self, Location):
        travelTime = self.speed*Location.dist(self.currLocation)
        yield self.env.timeout(travelTime)
        self.currLocation = Location

