'''
Created on Sep 14, 2013

@author: Mark Feaver
'''
from strategy import Strategy
from entities.position import Position

class SimpleTrend(Strategy):
    '''
    SimpleTrend is a very slightly more complex strategy. The idea is that if the 
    most recent n% price move was down, then a short position should be opened; 
    conversely if the most recent n% move was up, then a long position should be opened. 
    When a new position opens, the old one closes. This is a strategy that has a single parameter n 
    that should be tuned on the training data only.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        Strategy.__init__(self)
        
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

        return self._positions[index]