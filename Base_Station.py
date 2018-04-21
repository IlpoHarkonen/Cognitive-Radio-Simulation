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
                 operator = 0):
        self.x = x
        self.y = y
        self.gain = gain
        self.tx_power = base_station_tx_power #Watts
        self.operator = operator
        self.allowed_frequencies = self.determine_allowed_frequencies()
        self.current_frequencies = []
        #A list of frequencies which the base station senses being used nearby by someone else
        self.populated_frequencies = []
        
        #A list of users that can communicate with the base station
        #(i.e. received power is over the threshold)
        self.users_in_range = []
    
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
                
    def __str__(self):
        text_to_print = "x: {:.2f}  \ty:{:.2f}   \tOperator: {}".format(self.x, self.y, self.operator)
        return text_to_print
        
                