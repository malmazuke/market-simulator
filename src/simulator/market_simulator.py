'''
Created on Sep 3, 2013

@author: Mark Feaver
'''
import datetime
from entities.position import Position
from strategy.buy_and_hold import BuyAndHold

# In dollar values
DEFAULT_STARTING_INVESTMENT = 100000.0
DEFAULT_ROUND_TRADE_COST = 10.0
DEFAULT_STRATEGY = BuyAndHold()
    
class MarketSimulator(object):
    '''
    This trading simulator tests a trading strategy against historical data in order to evaluate 
    how well the strategy would have performed in the past.
    
    This simulator:
    (i) simulates the price and volume of the market for each passing minute, 
    (ii) has functionality for simulating the entry and exit of trades at appropriate points, and 
    (iii) produces summary statistics showing how well the strategy performed overall on the historical data.
    Any open trades are automatically closed at the end of the simulation period.
    
    The following assumptions have been made:
    - the starting investment at the beginning of a six month period is always
        $100,000
    - each round trip trade costs $10
    - your strategy can only make a single trade at a time, and can therefore only
        chose a single direction (long or short) at a time
    - 100% of capital is invested into the market for each trade
    - trades can be held overnight or for as long as needed without extra charges
    '''
    
    # The dollar value of the investments
    _original_investment = None
    _current_investment = None
    # How much each trade costs
    _round_trade_cost = None
    # CSV files
    _training_file = None
    _testing_file = None
    # The type of trading strategy: 
    _strategy = None
    # The trading entries
    _entries = []
    # The number of entries in the training data
    _num_entries_training = 0

    def __init__(self, training_file_csv, test_file_csv = None, starting_investment = DEFAULT_STARTING_INVESTMENT, round_trade_cost = DEFAULT_ROUND_TRADE_COST, strategy = DEFAULT_STRATEGY):
        '''
        Constructor - takes two file locations pointing to the training and testing data. 
        Should be in the following csv format: 
        Date (in MM/DD/YYYY format), Time (in HHMM format), Price, and Volume.
        
        Keyword arguments:
        training_file_csv -- the location of the csv file containing training data.
        test_file_csv -- the location of the csv file to test with (default 'None')
        '''
        self.set_training_file(training_file_csv)
        self._original_investment = starting_investment
        self._current_investment = starting_investment
        self._round_trade_cost = round_trade_cost
        self._strategy = strategy
        
        if test_file_csv is not None:
            self.set_test_file(test_file_csv)
    
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
        
    def get_entry(self, index):
        '''
        Return the entry at the given index 
        '''
        return self._entries[index]
    
    def number_of_entries(self):
        '''
        Return the number of entries
        '''
        return len(self._entries)
        
    def load_training_data(self, training_file_csv=None):
        '''
        Load in the training data from the training file.
        
        Keyword arguments (optional):
        training_file_csv -- the location of the csv file containing training data.
        '''
        
        # Check if an argument is passed
        if training_file_csv is not None:
            self.set_training_file(training_file_csv)
        
        if self._training_file is None:
            raise IOError('No training file specified. Please set a training file.')
            return
        
        self._entries = []
        
        # Load the file
        f = open(self._training_file, 'r')
        
        # Skip the first line
        line = f.readline()
        
        for line in f.xreadlines():
            parts = line.strip().split(',')
            time = datetime.datetime.strptime(parts[0] + parts[1], "%m/%d/%Y%H%M")
            price = float(parts[2])
            volume = int(parts[3])
            self._entries.append(Entry(time, price, volume))
        
        self._num_entries_training = len(self._entries)
        f.close()
        
    def load_testing_data(self, testing_file_csv=None):
        # Check if an argument is passed
        if testing_file_csv is not None:
            self.set_training_file(testing_file_csv)
        
        if self._training_file is None:
            raise IOError('No testing file specified. Please set a testing file.')
            return
        
        self._entries = []
        
        # Load the file
        f = open(self._testing_file, 'r')
        
        # Skip the first line
        line = f.readline()
        
        for line in f.xreadlines():
            parts = line.strip().split(',')
            time = datetime.datetime.strptime(parts[0] + parts[1], "%m/%d/%Y%H%M")
            price = float(parts[2])
            volume = int(parts[3])
            self._entries.append(Entry(time, price, volume))
        
        f.close()
        
    def train(self):
        '''
        Train the market strategy, using the training data
        '''
        # Reset the investment
        self._current_investment = self._original_investment
        
        self._strategy.set_market(self) #Only set up the strategy during training
        
        # For each entry in the market
        for x in xrange(len(self._entries)):
            # if it's the final entry, force the close
            if x == len(self._entries) - 1:
                self.close(x, self._strategy.get_previous_open_index())
                continue
            
            # Calculate the position to take for the given index
            position = self._strategy.trade(x)
            
            # If we're currently holding or out, don't do anything
            if position == Position.HOLD or position == Position.OUT:
                continue
            # Otherwise, close the previous trade, then open a trade
            else:
                if x != 0: # Don't close the first trade
                    self.close(x, self._strategy.get_previous_open_index())
                self.open(x, position)
    
    def test(self):
        '''
        Test the market strategy, using the testing data
        '''
        # Reset the investment
        self._current_investment = self._original_investment
        
        # For each entry in the market
        for x in xrange(self._num_entries_training):
            # if it's the final entry, force the close
            if x == self._num_entries_training - 1:
                self.close(x, self._strategy.get_previous_open_index())
                continue
            
            # Get the position calculated during training
            position = self._strategy.get_position(x)
            
            # If we're currently holding or out, don't do anything
            if position == Position.HOLD or position == Position.OUT:
                continue
            # Otherwise, close the previous trade, then open a trade
            else:
                if x != 0: # Don't close the first trade
                    self.close(x, self._strategy.get_previous_open_index())
                self.open(x, position)
        
    def open(self, index, position):
        '''
        Open a trade at the specified index i.e. time
        
        index -- the index of the trade to open (from self._entries)
        position -- the type of trade (either LONG or SHORT)
        '''
        self._strategy.open_trade(index, position)
        
    def close(self, close_index, open_index):
        '''
        Close a trade at the specified index i.e. time
        
        Keyword arguments:
        close_index -- the index of the trade to close (from self._entries)
        open_index -- the index where the trade was originally opened
        '''
        
        close_price = self._entries[close_index].get_price()
        open_price = self._entries[open_index].get_price()
        price_change = self.calc_price_change(close_price, open_price)
        amount = price_change * self._current_investment # The amount gained/lost
        
        previous_position = self._strategy.get_position(open_index)
        
        # If going long, we need a positive stock price increase in order to make money.
        # The opposite is true for going short
        if previous_position == Position.LONG:
            self._current_investment += amount
        elif previous_position == Position.SHORT:
            self._current_investment -= amount
            
        # Subtract the trading costs too
        self._current_investment -= self._round_trade_cost
        
    def calc_price_change(self, close_price, open_price):
        '''
        Calculates the price change between two stock prices
        
        Keyword arguments:
        close_price -- the price of the stock when trade was exited
        open_price -- the price of the stock when trade was entered 
        '''
        return (close_price/open_price - 1) 
                
        
class Entry(object):
    '''
    A wrapper class that holds information about a minute of trading.
    '''
    
    _time = None # This is a 'datetime' object, and contains the date + time
    _price = None
    _volume = None
    
    def __init__(self, time, price, volume):
        '''
        Constructor that takes a time (as a datetime object), price of the entry, and the volume of shares traded
        '''
        
        self._time = time
        self._price = price
        self._volume = volume
        
    def __str__(self):
        out = "(" + self._time.strftime("%m/%d/%Y, %H%M") + ", " + str(self._price) + ", " + str(self._volume) + ")"
        return out
    
    def __repr__(self):
        return self.__str__()
    
    def get_price(self):
        return self._price
    
if __name__ == '__main__':
    sim = MarketSimulator("../../data/training/SPY.2010.jan_jun.csv", "../../data/testing/SPY.2010.jul_dec.csv")
    sim.load_training_data()
    sim.train()
    print sim._current_investment
    
    sim.load_testing_data()
    sim.test()
    print sim._current_investment