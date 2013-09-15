'''
Created on Sep 14, 2013

@author: Mark Feaver
'''
from strategy import Strategy
from entities.position import Position

DEFAULT_N = 1
class SimpleTrend(Strategy):
    '''
    SimpleTrend is a very slightly more complex strategy. The idea is that if MA(n) indicator turns down 
    (i.e. MA(t,n)<MA(t-1,n)), then a short position should be opened; conversely if the MA(t,n) indicator turns up 
    (i.e. MA(t,n)>MA(t-1,n), then a long position should be opened. When a new position opens, the old one closes.
    
    This is a strategy that has a single positive integer parameter n that should be tuned on the training data only.
    '''

    _n = 1
    def __init__(self, n=DEFAULT_N):
        '''
        Constructor
        '''
        Strategy.__init__(self)
        self._n = n
        
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