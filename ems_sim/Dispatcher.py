# Author: Erkin Otles
# Author Email: eotles@gmail.com
# Research Group: McLay Lab
# Date Started: Spring '14
# Description: Set of classes that provide various dispatch logic

import abc
import sys
import simpy
from Responder import *

###############################################################################
# Dispatcher
# Abstract Base Class to provide a template of dispatcher functionality
# Params:
#    env - simulation env
#    responderList - list of available responders
#    status - if dispatcher should display status info during simulation runs
#    free - a resource store to keep track of free responders    
class Dispatcher(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __init__(self, env, responderList, status):
        self.env = env
        self.free = simpy.FilterStore(env)
        self.responderList = responderList
        self.status = status
        
        for responder in responderList:
            self.free.put(responder)
    
    #sends a responder to a given incident
    @abc.abstractmethod
    def _sendToIncident(self, Responder, Incident):
        yield self.env.process(Responder.travelTo(Incident.location))
        Incident.ambArr(Responder)
        yield self.env.process(Responder.careIncident(Incident))
        self.free.put(Responder)
    
    #method that holds logic for dispatcher responding to an incident 
    @abc.abstractmethod    
    def incidentRespose(self, inc):
        return
    
    #determines whether or not a responder is the best one    
    @abc.abstractmethod
    def _isBestResponder(self, resp, best):
        return
    
    #assigns a responder?
    @abc.abstractmethod
    def _assignResponder(self):
        return

###############################################################################
# SimpleDispatcher
# Child of Dispatcher
# Chooses the first free responder to respond to incidents     
class SimpleDispatcher(Dispatcher):
    def __init__(self, env, responderList, status):
        super(SimpleDispatcher, self).__init__(env, responderList, status)
    
    def _sendToIncident(self, Responder, Incident):
        yield self.env.process(Responder.travelTo(Incident.location))
        Incident.ambArr(Responder)
        yield self.env.process(Responder.careIncident(Incident))
        self.free.put(Responder)
    
    #first free    
    def incidentRespose(self, inc):
            responder = yield self.free.get()
            inc.ambDis(responder)
            inc.responder = responder.name
            yield self.env.process(self._sendToIncident(responder, inc))
        
    def _isBestResponder(self, resp, best):
        return(resp.name==best.name)
    
    def _assignResponder(self):
        firstAvailTime = sys.float_info.max
        firstResponder = None
        for Responder in self.responderList:
            if(Responder.timeAvail < firstAvailTime):
                firstAvailTime = Responder.timeAvail
                firstResponder = Responder
        return(firstResponder)

###############################################################################
# Priority Dispatcher
# Child of Dispatcher
# Chooses the first lowest possible free responder to respond to incidents     
class PriorityDispatcher(Dispatcher):
    
    def __init__(self, env, responderList, status):
        super(PriorityDispatcher, self).__init__(env, responderList, status)
        self.detail = False
    
    def _sendToIncident(self, Responder, Incident):
        if(self.detail):
            print("sending %s to incident %s @%s" %(Responder.name, Incident.name, self.env.now))
        yield self.env.process(Responder.travelTo(Incident.location))
        Incident.ambArr(Responder)
        if(Incident.status.hid.priority < Responder.kind):
            chooseSecondResponder = self.getCurrPriorFree(Incident.status.hid.priority)
            chooseSecondResponder.assignToIncident(Incident)
            if(self.detail):
                print("\t%s" %chooseSecondResponder.name)
            secondResponder = yield self.free.get(lambda x: self._isBestResponder(x, chooseSecondResponder))
            if(self.detail):
                print("\tgot second responder")
            secondResponder.assignToIncident(Incident)
            Incident.ambDis(secondResponder)
            yield self.env.process(self._sendToIncident(secondResponder, Incident))   
        else:
            yield self.env.process(Responder.careIncident(Incident))
        self.free.put(Responder)
        if(self.detail):
            print("freeing %s from incident %s @%s" %(Responder.name, Incident.name, self.env.now))
        
    
    #first free    
    def incidentRespose(self, inc):
            bestResponder = self.getCurrPriorFree(inc.status.obs.priority)
            responder = yield self.free.get(lambda x: self._isBestResponder(x, bestResponder))
            responder.assignToIncident(inc)        
            inc.ambDis(responder)
            inc.responder = responder.name
            yield self.env.process(self._sendToIncident(responder, inc))
            
    def getCurrPriorFree(self, priority):
        bestTime = float("inf")
        for responder in self.responderList:
            #print("%d,%d" %(priority, responder.kind))
            if(priority == responder.kind):
                if(responder.timeAvail<bestTime):
                    bestTime = responder.timeAvail
                    bestResponder = responder
        return bestResponder
        
        
    def _isBestResponder(self, resp, best):
        return(resp.name==best.name)
    
    def _assignResponder(self):
        firstAvailTime = sys.float_info.max
        firstResponder = None
        for Responder in self.responderList:
            if(Responder.timeAvail < firstAvailTime):
                firstAvailTime = Responder.timeAvail
                firstResponder = Responder
        return(firstResponder)





