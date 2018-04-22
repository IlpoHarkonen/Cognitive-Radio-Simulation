"""
Operator:
0: To remove operator restrictions
1: DNA
2: Elisa
3: Telia
"""
import numpy as np
from Global_Variables import *

class BaseStation:
    def __init__(self, x=0, y=0,gain=1, tx_power=0,\
                 operator = 0, id = 0):
        self.id = id #Unique id. This is manually given to each station to help with debugging.
        self.x = x
        self.y = y
        self.gain = gain
        self.tx_power = base_station_tx_power #Watts
        self.operator = operator
        self.allowed_frequencies = self.determine_allowed_frequencies()
        self.currently_used_frequencies = []
        self.currently_sensed_frequencies = []
        #A list of frequencies which the base station senses being used nearby by someone else
        self.populated_frequencies = []
        
        #A list of users that can communicate with the base station
        #(i.e. received power is over the threshold)
        self.users_in_range = []
        self.currently_served_users = []
        
        #Assign random starting frequency
        self.get_random_frequency()
        
    
    """Sets the list self.alowed frequencies according to the operator-parameter"""
    def determine_allowed_frequencies(self):
        frequency_list = []
        if self.operator != 0:
            frequency_list = operator_frequencies[self.operator - 1]
        else:
            for operator in operator_frequencies:
                for freq_range in operator:
                    frequency_list.append(freq_range)
        return frequency_list
    
    """Calculate the received power from each possible user to determine who we can communicate with"""
    def update_users_in_range(self, user_list):
        self.users_in_range = []
        for user in user_list:
            received_power = calculate_signal_power(self, user)
            if received_power > power_threshold:
                self.users_in_range.append(user)
    
    """Assign a small random slice of frequency at the start."""
    def get_random_frequency(self):
        # Pick one random range
        rand_range = self.allowed_frequencies[np.random.randint(0,len(self.allowed_frequencies))]
        # Pick a small random slice of the chosen range
        f_min = np.random.randint(np.ceil(rand_range[0]), np.floor(rand_range[1]) - freq_start_size)
        f_max = f_min + freq_start_size
        self.currently_used_frequencies = [[f_min, f_max]]
        
                
    def __str__(self):
        text_to_print = "ID: {}\tx: {:.2f}  \ty:{:.2f}   \tOperator: {}\tFrequency: {}"\
        .format(self.id, self.x, self.y, self.operator, self.currently_used_frequencies)
        return text_to_print
        
                