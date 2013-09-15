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
    _previous_m_a = None # We store the previous moving average in memory, so we don't have to recalculate
    
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
        
        if index == 0: # If it's the first, sit it out
            self._positions[index] = Position.OUT
            self._previous_open_index = 0
        else:
            curr_m_a = self.moving_average(index, self._n) # Moving Av at current position
            prev_m_a = None
            if self._previous_m_a is not None:
                prev_m_a = self._previous_m_a
            else:
                prev_m_a = self.moving_average(index-1, self._n) # Moving Av at previous position
            self._previous_m_a = curr_m_a # Save in memory, to speed up search
            
            pos = Position.HOLD # If we don't need to change, we hold
            
            # If the moving average indicator turns down, we go short
            if curr_m_a < prev_m_a and self._positions[index-1] != Position.SHORT:
                pos = Position.SHORT
                self._previous_open_index = index
            # Else, if the moving average indicator turns up, we go long
            elif curr_m_a > prev_m_a and self._positions[index-1] != Position.LONG:
                pos = Position.LONG
                self._previous_open_index = index
            
            # Store the position
            self._positions[index] = pos
        
        return self._positions[index]
    
    def moving_average(self, index, n):
        '''
        Calculate the moving average for a given index, using the previous 'n' values 
        '''
        
        total = 0
        count = 0
        for x in xrange(index - n + 1, index+1):
            if x < 0: # Don't calculate values where they don't exist
                continue
            
            total += self._market.get_entry(x).get_price()
            count += 1
        
        if count == 0:
            return 0
        
        return total/float(count)
        