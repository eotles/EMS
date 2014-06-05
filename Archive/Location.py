'''
@author: eotles
'''
import math
class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, row, col):
        self.location[0] = row
        self.location[1] = col

    def distance(self, otherLoc):
        difX = math.fabs(otherLoc[0]-self[0])
        difY = math.fabs(otherLoc[1]-self[1])
        return(difX+difY)
        