"""
Operator:
0: To remove operator restrictions
1: DNA
2: Elisa
3: Telia
"""
import numpy as np
from Global_Variables import *
from Generic_Functions import *



class BaseStation(GenericDevice):
    def __init__(self, x=0, y=0,gain=1, tx_power=0,\
                 operator = 0, id = 0):
        GenericDevice.__init__(self, x=x, y=y, gain=gain, tx_power=base_station_tx_power, operator=operator)
        self.id = id #Unique id. This is manually given to each station to help with debugging.
        self.allowed_frequencies = self.determine_allowed_frequencies()
        self.currently_used_frequencies = []
        self.currently_sensed_frequencies = []
        #A list of frequencies which the base station senses being used nearby by someone else
        self.populated_frequencies = []
        
        #A list of users that can communicate with the base station.
        #(i.e. received power is over the threshold)
        self.users_in_range = []
        self.currently_served_users = []
        
        #List of base stations we can directly communicate with.
        self.base_stations_in_range = []
        
        #Assign random starting frequency
        self.get_random_frequency()
        
    
    """Sets the list self.allowed_frequencies according to the operator-parameter"""
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
            for freq_range in user.currently_used_frequencies:
                received_power = self.calculate_signal_power(user, freq_range)
                if received_power > power_threshold:
                    self.users_in_range.append([user, freq_range])
    
    """Calculate the received power from each possible base_station to determine who we can communicate with.
    Can also be used to refresh the list if a nreaby station switches frequency and thus turns invisible."""
    def update_base_stations_in_range(self, base_station_list):
        self.base_stations_in_range = []
        for station in base_station_list:
            if station.id != self.id: #Don't compare a base station with itself
                for freq_range in station.currently_used_frequencies:
                    received_power = self.calculate_signal_power(station, freq_range)
                    if received_power > power_threshold:
                        self.users_in_range.append([station, freq_range])
    
    """Assign a small random slice of frequency at the start."""
    def get_random_frequency(self):
        # Pick one random range
        rand_range = self.allowed_frequencies[np.random.randint(0,len(self.allowed_frequencies))]
        # Pick a small random slice of the chosen range
        f_min = np.random.randint(np.ceil(rand_range[0]), np.floor(rand_range[1]) - freq_start_size)
        f_max = f_min + freq_start_size
        self.currently_used_frequencies = [[f_min, f_max]]
        
                
    def __str__(self):
        text_to_print = "\tID: {} \tFrequency: {}"\
        .format(self.id, self.currently_used_frequencies)
        return GenericDevice.__str__(self) + text_to_print
                