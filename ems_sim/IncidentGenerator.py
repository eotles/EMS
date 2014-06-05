# Author: Erkin Otles
# Author Email: eotles@gmail.com
# Research Group: McLay Lab
# Date Started: Spring '14
# Description: Randomly generates incidents over the course of the simulation

import random
import Incident

#TODO: use WORLD Information
###############################################################################
# IncidentGenerator
# Class that generates incidents and starts response process
# inputs:
#    env - simulation env
#    Dispatcher - the dispatcher being used
#    TBA - the average time between arrival (assuming EXPO)
#    SIM_DURATION - the entire simulation run duration
#    END_BUFFER - if the amount of time left in the simulation is < than this
#                    stops generating incidents
#    HOSPITAL - the hospital all patients go to // NOTE: this should be replaced
#                with WORLD information
#    incidentList - the list of all incidents generated
class IncidentGenerator(object):
    def __init__(self, env, Dispatcher, TBA, SIM_DURATION, END_BUFFER, HOSPITAL, status):
        self.env = env
        self.Dispatcher = Dispatcher
        self.tba = TBA
        self.simDuration = SIM_DURATION
        self.endBuffer = END_BUFFER
        self.hospital = HOSPITAL
        self.incidentList = list()
        self.env.process(self.incidentGenerator(status))
    
    #while there is time left for generating an incident do so
    #add the incident to the incidentList and kick off a dispatcher response
    #process
    def incidentGenerator(self, status):
        condition = True
        while condition:
            intArr = random.expovariate(1.0/self.tba)
            if(intArr < self.simDuration - self.endBuffer - self.env.now):
                intArr = random.expovariate(1.0/self.tba)
                yield self.env.timeout(intArr)      
                inc = Incident.Incident(self.env, 'Person %d' %len(self.incidentList), 
                                        self.hospital, status)
                self.incidentList.append(inc)
                self.env.process(self.Dispatcher.incidentRespose(inc))
            else:
                condition = False
