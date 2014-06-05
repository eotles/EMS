# Author: Erkin Otles
# Author Email: eotles@gmail.com
# Research Group: McLay Lab
# Date Started: Spring '14
# Description: Provides a toolkit to analyze data efficiently

import numpy

###############################################################################
# Data
# Class to encapsulate sets of data 
# Params:
#    dataFields - list of names of each of the various types of data
#    data - list of lists to hold data (row form)
#    trans - list of list to hold transposed data (col form)
class Data(object):
    def __init__(self, dataFields):
        self.dataFields = dataFields
        self.data = list()
        self.trans = [list() for _ in self.dataFields]
    
    def addData(self, data):
        self.data.append(data)
        for i,v in enumerate(data):
                self.trans[i].append(v)
        
#TODO: Clean up this class
###############################################################################
# Stats
# Class to take list of data and package it up in an object
# with summary statistics
# Params:
#    data - list holding data (taken from transform)
class stats(object):
    def __init__(self, data):
        self.mea = numpy.mean(data)
        self.std = numpy.std(data)
        self.max = numpy.max(data)
        self.min = numpy.min(data)
        self.med = numpy.median(data)
        self.arr = list()
        self.arr.append(self.mea)
        self.arr.append(self.std)
        self.arr.append(self.min)
        self.arr.append(self.med)
        self.arr.append(self.max)    

###############################################################################
# Analyzer
# Class to take streams of data, collate, and statistically 
# analyze it
# Params:
#    dataFields - list of names of each of the various types of data
#    data - list of lists to hold data (row form)
# Methods:
#    addData - adds a row of data to the data object
#    run - calculates statistics on all seen data thus far
class Analyzer(object):
    def __init__(self, dataFields):
        self.data = Data(dataFields)
    
    def addData(self, data):
        self.data.addData(data)

    #grab transpose data (col form)
    #for each set of data (col) create a stats object        
    def _calcStats(self):
        self.trans = self.data.trans
        self.stats = list()
        for i in self.trans:
            self.stats.append(stats(i))
    
    #displays stats in a summary table        
    def _printStats(self):
        for f in self.data.dataFields:
            print(f +"\t"),
        print("")
        for row,_ in enumerate(self.stats[0].arr):
            for j,__ in enumerate(self.stats):
                print(str(self.stats[j].arr[row]) + "\t"),
            print("")
           
    def run(self, displayStatus):
        self._calcStats()
        if(displayStatus):
            self._printStats()
        
    
        