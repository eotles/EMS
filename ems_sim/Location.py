# Author: Erkin Otles
# Author Email: eotles@gmail.com
# Research Group: McLay Lab
# Date Started: Spring '14
# Description: Class to keep track of location on a rectangular word

import math

#TODO: this is going to be a constituent of the WORLD class
##############################################################
# Location
# Class representing position on a 2D rectangular world
# inputs:
#    name - name of the location (i.e. hospital/station)
#    x_cord - the x coordinate of the location
#    y_cord - the y coordinate of the location
# returns: list of responders
class Location(object):
    def __init__(self, name, x_cord, y_cord):
        self.name = name
        self.x_cord = x_cord
        self.y_cord = y_cord
    
    def dist(self, Location):
        return(math.sqrt((Location.x_cord-self.x_cord)**2+(Location.y_cord-self.y_cord)**2)) 
    
    def toString(self):
        return("(%s,%s)" %(self.x_cord, self.y_cord))