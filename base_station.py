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

    
    def update_currently_sensed_frequencies(self):
        """List which frequency ranges we hear being used and are not used by ourselves."""
        self.currently_sensed_frequencies = []
        for [user, freq_range] in self.users_in_range:
            if freq_range not in self.currently_sensed_frequencies:
                self.currently_sensed_frequencies.append(freq_range)
        for [station, freq_range] in self.base_stations_in_range:
            if freq_range not in self.currently_sensed_frequencies:
                self.currently_sensed_frequencies.append(freq_range)
                

    def determine_proportional_scaling_direction(self):
        """Most fortunate station is forced to scale down (if able)
        while most unfortunate stations are allowed to scale up.
        This is determined by: station badnwidth / (station user count + 1)
        Return values:
        0: don't scale frequency
        1: scale frequency up
        -1: scale frequency down
        """
        # Calculate own metric
        scale_direction = 0
        own_bandwidth = 0
        for freq_range in self.currently_used_frequencies:
            own_bandwidth += freq_range[1] - freq_range[0]
        own_scale_factor = own_bandwidth/(len(self.currently_served_users) + 1)
        
        # Calculate same metric for other stations we hear
        worst_factor = 9001
        best_factor = 0
        for station_listitem in self.base_stations_in_range:
            station = station_listitem[0]
            station_bandwidth = 0
            for freq_range in station.currently_used_frequencies:
                station_bandwidth += freq_range[1] - freq_range[0]
            station_scale_factor = station_bandwidth / (len(station.currently_served_users)+1)
            if station_scale_factor < worst_factor:
                worst_factor = station_scale_factor
            if station_scale_factor > best_factor:
                best_factor = station_scale_factor
                
        # Compare metrics
        worst_factor = int(worst_factor * 100000)
        best_factor = int(best_factor * 100000)
        own_scale_factor = int(own_scale_factor * 100000)
        # Should we scale up?
        if own_scale_factor <= worst_factor:
            proportion = worst_factor / own_scale_factor
            if proportion >= settings.scale_threshold:
                scale_direction = 1
        # Should we scale down (if we can)?
        if own_scale_factor >= best_factor and own_bandwidth >= settings.freq_start_size + settings.freq_step:
            proportion = own_scale_factor / best_factor
            if proportion > settings.scale_threshold:
                scale_direction = -1
        
        return scale_direction


    def acquire_more_spectrum(self):
        """Get a new frequency slice according to settings.freq_step."""
        pass
    
    
    def decrease_own_spectrum(self):
        """Decrement own f_max or increment f_min on one of our spectrum bands."""
        pass
    
    
    def scale_frequency(self):
        """A base station can obtain more bandwidth if it does not sense anyone else using said bandwidth.
        The bandwidth is incremented in small hops. We let stations have bandwidth proportional to their
        subscirbed user counts + 1."""
        self.update_currently_sensed_frequencies()
        # Determine if we are allowed to scale.
        # If scale direction is up (1), available spectrum is not guaranteed to exist.
        scale_direction = self.determine_proportional_scaling_direction()
        # End if we shouldn't scale
        if scale_direction == 0:
            self.vote_to_stop = True
            return 0
        else:
            self.vote_to_stop = False
        # If we have permission to scale up, check for free spectrum first.
        if scale_direction == 1:
            self.acquire_more_spectrum()
        elif scale_direction == -1:
            self.decrease_own_spectrum()
        
        
    def __str__(self):
        bandwidth = 0
        for freq_range in self.currently_used_frequencies:
            bandwidth += freq_range[1] - freq_range[0]
        text_to_print = "\tID: {} \tFrequency: {}\tTotal bandwidth: {} MHz"\
        .format(self.id, self.currently_used_frequencies, bandwidth)
        return GenericDevice.__str__(self) + text_to_print
