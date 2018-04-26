"""
Operator:
0: To remove operator restrictions
1: DNA
2: Elisa
3: Telia
"""
import numpy as np
import settings
from generic_functions import GenericDevice


class BaseStation(GenericDevice):
    def __init__(self, x=0, y=0, gain=1, tx_power=0, operator=0, id=0):
        GenericDevice.__init__(
            self,
            x=x,
            y=y,
            gain=gain,
            tx_power=settings.base_station_tx_power,
            operator=operator)
        # Unique id. This is manually given to each station to help
        # with debugging.
        self.id = id
        self.allowed_frequencies = self.determine_allowed_frequencies()
        
        self.currently_sensed_frequencies = []
        # A list of frequencies which the base station senses being
        # used nearby by someone else
        self.populated_frequencies = []

        

        self.currently_served_users = []

        # List of base stations we can directly communicate with.
        self.base_stations_in_range = []

        # Assign random starting frequency
        self.get_random_frequency()

    def determine_allowed_frequencies(self):
        """Sets the list self.allowed_frequencies according to the
        operator-parameter.
        """
        frequency_list = []
        if self.operator != 0:
            frequency_list = settings.operator_frequencies[self.operator - 1]
        else:
            for operator in settings.operator_frequencies:
                for freq_range in operator:
                    frequency_list.append(freq_range)
        return frequency_list

    

    


    def get_random_frequency(self):
        """Assign a small random slice of frequency at the start."""
        # Pick one random range
        rand_range = self.allowed_frequencies[np.random.randint(
            0, len(self.allowed_frequencies))]
        # Pick a small random slice of the chosen range
        f_min = np.random.randint(
            np.ceil(rand_range[0]),
            np.floor(rand_range[1]) - settings.freq_start_size)
        f_max = f_min + settings.freq_start_size
        self.currently_used_frequencies = [[f_min, f_max]]

    def __str__(self):
        text_to_print = "\tID: {} \tFrequency: {}"\
        .format(self.id, self.currently_used_frequencies)
        return GenericDevice.__str__(self) + text_to_print
