'''
Created on Sep 12, 2013

@author: Mark Feaver
'''

class Position:
    '''
    Basically an enum, describing the type of trade position 
    '''
    OUT = 0 # Sit out of the market
    LONG = 1 # Go long
    SHORT = 2 # Go short
    HOLD = 3