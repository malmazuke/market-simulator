'''
Created on Sep 3, 2013

@author: feaver
'''

class MarketSimulator(object):
    '''
    This trading simulator tests a trading strategy against historical data in order to evaluate 
    how well the strategy would have performed in the past. 
    
    This simulator:
    (i) simulates the price and volume of the market for each passing minute, 
    (ii) has functionality for simulating the entry and exit of trades at appropriate points, and 
    (iii) produces summary statistics showing how well the strategy performed overall on the historical data.
    Any open trades are automatically closed at the end of the simulation period.
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        