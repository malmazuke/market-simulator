'''
Created on Sep 13, 2013

@author: feaver
'''

class BuyAndHold(object):
    '''
    classdocs
    '''
    _curr_position = None
    _market = None
    _is_holding = False

    def __init__(self, market):
        '''
        Constructor
        
        Keyword arguments:
        market -- the market simulator object
        '''
        
        self._curr_position = Position.LONG
        self._market = market
        self._is_holding = True

    def trade(self, market, entry):
        '''
        Make a decision for a specific entry on whether to go long, short, hold, or be out of the market
        
        Keyword arguments:
        entry -- a single entry (i.e. minute), containing the time (datetime), price, and volume
        '''

class Position:
    '''
    Basically an enum, describing the type of trade position 
    '''
    OUT = 0 # Sit out of the market
    LONG = 1 # Go long
    SHORT = 2 # Go short