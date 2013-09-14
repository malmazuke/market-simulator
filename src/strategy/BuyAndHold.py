'''
Created on Sep 13, 2013

@author: Mark Feaver
'''

class BuyAndHold(object):
    '''
    Enters a long trade at the beginning of a training or test period, and exits at the end.
    There is only a single trade involved, so transaction costs are minimized using this strategy.
    '''
    
    _positions = []
    _market = None
#     _is_holding = False
    _previous_open_index = None

    def __init__(self):
        '''
        Constructor
        
        Keyword arguments:
        market -- the market simulator object
        '''
        
        _positions = []
        self._market = None
#         self._is_holding = True
    
    def set_market(self, market):
        self._market = market
        # Initialise the positions to be the same length as the number of entries 
        self._positions = [Position.OUT] * market.number_of_entries()
    
    def get_previous_open_index(self):
        '''
        Return the index of the last open trade
        '''
        return self._previous_open_index
    
    def get_position(self, index):
        '''
        Return the trading position i.e. Long, Short, etc at the specified position
        '''
        return self._positions[index]
    
#     def is_holding(self):
#         '''
#         Return a boolean describing whether the strategy is currently holding
#         '''
#         return self._is_holding
        
    def trade(self, index):
        '''
        Make a decision for a specific entry on whether to go long, short, hold, or be out of the market
        
        Keyword arguments:
        index -- the current index/entry that we're up to
        '''
        
        if index == 0:
            self._positions[index] = Position.LONG
            self._previous_open_index = 0
        else:
            self._positions[index] = Position.HOLD
#             self._is_holding = True

        return self._positions[index]

    def open_trade(self, index, position):
        '''
        Open a trade at the current index/time with a given position (i.e. Long, Short)
        '''
        self._positions[index] = position
        self._previous_open_index = index
        
class Position:
    '''
    Basically an enum, describing the type of trade position 
    '''
    OUT = 0 # Sit out of the market
    LONG = 1 # Go long
    SHORT = 2 # Go short
    HOLD = 3