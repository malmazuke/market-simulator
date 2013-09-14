'''
Created on Sep 7, 2013

@author: Mark Feaver
'''
from entities.position import Position
from strategy import Strategy

class BuyAndHold(Strategy):
    '''
    Enters a long trade at the beginning of a training or test period, and exits at the end.
    There is only a single trade involved, so transaction costs are minimized using this strategy.
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