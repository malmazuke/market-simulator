'''
Created on Sep 13, 2013

@author: Mark Feaver
'''

class BuyAndHold(object):
    '''
    Enters a long trade at the beginning of a training or test period, and exits at the end.
    There is only a single trade involved, so transaction costs are minimized using this strategy.
    '''
    
    _curr_position = None
    _market = None
    _is_holding = False
    _entry_holding = None

    def __init__(self, market):
        '''
        Constructor
        
        Keyword arguments:
        market -- the market simulator object
        '''
        
        self._curr_position = Position.LONG
        self._market = market
        self._entry_holding = self._market.get_entry(0)
        self._is_holding = True

    def trade(self, entry):
        '''
        Make a decision for a specific entry on whether to go long, short, hold, or be out of the market
        
        Keyword arguments:
        entry -- a single entry (i.e. minute), containing the time (datetime), price, and volume
        '''
        return

class Position:
    '''
    Basically an enum, describing the type of trade position 
    '''
    OUT = 0 # Sit out of the market
    LONG = 1 # Go long
    SHORT = 2 # Go short