'''
Created on Sep 12, 2013

@author: Mark Feaver
'''
from entities.position import Position

class Strategy(object):
    '''
    A parent class that describes behaviour for a strategy
    '''

    _positions = []
    _market = None
    _previous_open_index = None

    def __init__(self):
        '''
        Constructor
        '''
        
        self._positions = []
        self._market = None
        self._previous_open_index = 0
        
    def set_market(self, market):
        '''
        Set the market object, and initialise the number of possible positions
        
        Keyword arguments:
        market -- a MarketSimulator object
        '''
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
    
    def trade(self, index):
        '''
        Make a decision for a specific entry on whether to go long, short, hold, or be out of the market
        
        Keyword arguments:
        index -- the current index/entry that we're up to
        '''
        
        return Position.HOLD
    
    def open_trade(self, index, position):
        '''
        Open a trade at the current index/time with a given position (i.e. Long, Short)
        '''
        self._positions[index] = position
        self._previous_open_index = index