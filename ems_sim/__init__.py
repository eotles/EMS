# Author: Erkin Otles
# Author Email: eotles@gmail.com
# Research Group: McLay Lab
# Date Started: Spring '14
# Description: Initializes and runs simulation program from package

import simpy
import numpy
import random
import Analyzer
import Location
import Responder
import Dispatcher
import IncidentGenerator

#CONSTANTS
SEED = 42
SIM_DURATION = 86400
#SIM_DURATION = 3600
NUM_AMB = 3
TBA = 120
END_BUFFER = 0
STATION = Location.Location("Station", 0, 0)
HOSPITAL = Location.Location("Hospital", 9, 9)
DETAIL = False
DETAIL = True

###############################################################################
# makeResponders(env, station, numResp, status)
# Creates a list of responders to be used in a simulation env 
# inputs:
#    env - simulation env
#    station - location object of the station of the responder
#    numResp - the number of responders to be created
#    status  - if responder info should display status during simulation runs
# returns: list of responders
def makeResponders(env, station, numResp, status):
    responderList = list()
    for i in xrange(numResp):
        tempResp = Responder.Responder(env, "amb_"+str(i), i%2, station, station, 0.25, status)
        responderList.append(tempResp)
    return responderList


###############################################################################
# run(replications)
# Runs replications of simulation
# inputs:
#    replications - the number of runs
# returns: None
def run(replications):
    SEED = 42
    outAnal = Analyzer.Analyzer(["D1", "D2", "D3", "D4"])
    for i in xrange(replications):
        random.seed(SEED)
        print('EMS! Run %i of %i' %(i+1, replications))
        outAnal.addData(_runRep(DETAIL))
        SEED = random.random()
    outAnal.run(True)

###############################################################################
# _runRep(status)
# Runs a single replication of the simulation
# inputs:
#    status - if info should be displayed during the run
# returns: list of means for all analysis stats       
def _runRep(status):
    # Setup and start the simulation
    env = simpy.Environment()
    
    #make emergency responder resources
    #ems = Dispatcher.SimpleDispatcher(env, makeResponders(env, STATION, NUM_AMB, status), status)
    ems = Dispatcher.SimpleDispatcher(env, makeResponders(env, STATION, NUM_AMB, status), status)
    calls = IncidentGenerator.IncidentGenerator(env, ems, TBA, SIM_DURATION, END_BUFFER, HOSPITAL, status)
    
    horizBar = "----------------------------------------------------------------------"            
    if(status):
        print(horizBar)
    
    #run simulation
    #env.run(until=SIM_DURATION)
    env.run()
    
    #print incident summary table
    if(status):
        print(horizBar)
    
    #analysis
    analysis = Analyzer.Analyzer(["D1", "D2", "D3", "D4"])
    for inc in calls.incidentList:
        if(status):
            print(inc.toString())
        incTimes = inc.getTimesList()
        analysis.addData(incTimes.difList)
    analysis.run(status)
    
    return([i.mea for i in analysis.stats])

        
if __name__ == '__main__':
    run()