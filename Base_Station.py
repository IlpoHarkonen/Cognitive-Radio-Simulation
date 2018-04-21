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
        self.tx_power = tx_power #Watts
        self.operator = operator
        self.all_frequencies = []
        self.current_frequencies = []
        #A list of frequencies which the base station senses being used nearby by someone else
        self.populated_frequencies = []
        
        self.users_in_range = []
    
    """Calculate the received power from each possible user to determine who we can communicate with"""
    def update_users_in_range(self, user_list):
        self.users_in_range = []
        for user in user_list:
            received_power = calculate_signal_power(self, user)
            if received_power > power_threshold:
                self.users_in_range.append(user)
                