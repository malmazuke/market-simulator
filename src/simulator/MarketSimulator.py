'''
Created on Sep 3, 2013

@author: feaver
'''

class MarketSimulator(object):
    
    _training_file = None
    _testing_file = None
    
    '''
    This trading simulator tests a trading strategy against historical data in order to evaluate 
    how well the strategy would have performed in the past.
    
    This simulator:
    (i) simulates the price and volume of the market for each passing minute, 
    (ii) has functionality for simulating the entry and exit of trades at appropriate points, and 
    (iii) produces summary statistics showing how well the strategy performed overall on the historical data.
    Any open trades are automatically closed at the end of the simulation period.
    '''


    def __init__(self, training_file_csv, test_file_csv = None):
        '''
        Constructor - takes two file locations pointing to the training and testing data. 
        Should be in the following csv format: 
        Date (in MM/DD/YYYY format), Time (in HHMM format), Price, and Volume.
        
        Keyword arguments:
        training_file_csv -- the location of the csv file containing training data.
        test_file_csv -- the location of the csv file to test with (default none)
        '''
        self.set_trainingfile(training_file_csv)
        
        if test_file_csv is not None:
            self.set_testfile(test_file_csv)
    
    def set_training_file(self, training_file_csv):
        '''
        Set the training file. Should be in the following csv format: 
        Date (in MM/DD/YYYY format), Time (in HHMM format), Price, and Volume.
        '''
        self._training_file = training_file_csv
        
    def set_test_file(self, test_file_csv):
        '''
        Set the test file. Should be in the following csv format: 
        Date (in MM/DD/YYYY format), Time (in HHMM format), Price, and Volume.
        '''
        self._testing_file = test_file_csv
        
    def load_training_data(self, training_file_csv=None):
        '''
        Load in the training data from the training file.
        
        Optional arguments:
        training_file_csv --
        '''
        if training_file_csv is not None:
            self.set_training_file(training_file_csv)
        
        if self._training_file is None:    
            raise IOError('No training file specified. Please set a training file.')
            return