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
        self.obtainable_frequencies = []

        

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
                    frequency_list.append(freq_range[:])
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
        """List which frequency ranges we hear being used and are not used by ourselves.
        Also update the list of frequencies we deem available."""
        # See which frequencies we currently hear.
        self.currently_sensed_frequencies = []
        for [user, freq_range] in self.users_in_range:
            if freq_range not in self.currently_sensed_frequencies:
                self.currently_sensed_frequencies.append(freq_range)
        for [station, freq_range] in self.base_stations_in_range:
            if freq_range not in self.currently_sensed_frequencies:
                self.currently_sensed_frequencies.append(freq_range)
        # Determine which frequencies are currently free
        self.obtainable_frequencies = self.allowed_frequencies[:]
        i = 0
        while i < len(self.obtainable_frequencies):
            freq_range_1 = self.obtainable_frequencies[i]
            for freq_range_2 in self.currently_sensed_frequencies:
                # Check if f_min is inside the band and split lists accordingly
                if freq_range_1[0] < freq_range_2[0] < freq_range_1[1]:
                    tmp_freq = [freq_range_1[0], freq_range_2[0]]
                    if tmp_freq not in self.obtainable_frequencies and tmp_freq not in self.currently_used_frequencies:
                        self.obtainable_frequencies.append(tmp_freq)
                    if freq_range_1 in self.obtainable_frequencies:
                        self.obtainable_frequencies.remove(freq_range_1)
                    i -= 1
                # Check the same for f_max
                if freq_range_1[0] < freq_range_2[1] < freq_range_1[1]:
                    tmp_freq = [freq_range_2[1], freq_range_1[1]]
                    if tmp_freq not in self.obtainable_frequencies and tmp_freq not in self.currently_used_frequencies:
                        self.obtainable_frequencies.append(tmp_freq)
                    if freq_range_1 in self.obtainable_frequencies:
                        self.obtainable_frequencies.remove(freq_range_1)
                    i -= 1
            i += 1
            if i < 0:
                i = 0
        
    
    def minimize_currently_used_frequency_list(self):
        """Optimization function to speed up computing.
        Looks at currently used frequency lists and merges two frequencies that are next to each other."""
        i = 0
        while i < len(self.currently_used_frequencies):
            k = 0
            while k < len(self.currently_used_frequencies):
                tmp_freq = []
                freq_range_1 = self.currently_used_frequencies[i]
                freq_range_2 = self.currently_used_frequencies[k]
                if freq_range_1[1] == freq_range_2[0]:
                    tmp_freq = [freq_range_1[0], freq_range_2[1]]
                elif freq_range_1[0] == freq_range_2[1]:
                    tmp_freq = [freq_range_2[0], freq_range_1[1]]
                if len(tmp_freq) > 0:
                    self.currently_used_frequencies.remove(freq_range_1)
                    self.currently_used_frequencies.remove(freq_range_2)
                    self.currently_used_frequencies.append(tmp_freq)
                    k -= 1
                k += 1
            i += 1

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
        #worst_factor = int(worst_factor * 1000)
        #best_factor = int(best_factor * 1000)
        #own_scale_factor = int(own_scale_factor * 1000)
        scale_direction = 0
        # Should we scale up?
        if own_scale_factor <= worst_factor:
            proportion = worst_factor / own_scale_factor
            if proportion >= settings.scale_up_threshold:
                scale_direction = 1
        # Should we scale down (if we can)?
        if own_scale_factor >= best_factor and own_bandwidth >= settings.freq_start_size + settings.freq_step:
            proportion = own_scale_factor / best_factor
            if proportion > settings.scale_down_threshold:
                scale_direction = -1
        return scale_direction


    def acquire_more_spectrum(self):
        """Get a new frequency slice according to settings.freq_step."""
        # Remove frequencies we use from the available frequency list
        for freq in self.currently_used_frequencies:
            if freq in self.obtainable_frequencies:
                self.obtainable_frequencies.remove(freq)
        # Acquire spectrum
        if len(self.obtainable_frequencies) > 0:
            if len(self.obtainable_frequencies) == 1:
                r = 0
            else:
                r = np.random.randint(0,len(self.obtainable_frequencies)-1)
            self.currently_used_frequencies.append(self.obtainable_frequencies[r])
            for user in self.currently_served_users:
                user.currently_used_frequencies.append(self.obtainable_frequencies[r])
            self.obtainable_frequencies.pop(r)

    def decrease_own_spectrum(self):
        """Choose a random frequency range we use and decrease it or remove completely if it is small."""
        if len(self.currently_used_frequencies) == 1:
            r = 0
        else:
            r = np.random.randint(0,len(self.currently_used_frequencies)-1)
        
        tmp_freq = self.currently_used_frequencies[r]
        # Remove completely if small
        if tmp_freq[1] - tmp_freq[0] - settings.freq_step < settings.freq_start_size\
        and len(self.currently_used_frequencies) > 1:
            self.currently_used_frequencies.pop(r)
        # Otherwise decrease the size
        else:
            self.currently_used_frequencies[r][0] += settings.freq_step
        #Update served users to the same frequencies
        for user in self.currently_served_users:
            user.currently_used_frequencies = []
            user.currently_used_frequencies = self.currently_used_frequencies[:]

    
    
    def scale_frequency(self):
        """A base station can obtain more bandwidth if it does not sense anyone else using said bandwidth.
        The bandwidth is incremented in small hops. We let stations have bandwidth proportional to their
        subscirbed user counts + 1."""
        self.update_currently_sensed_frequencies()
        # Optimize lists
        self.minimize_currently_used_frequency_list()
        # Determine if we are allowed to scale.
        # If scale direction is up (1), available spectrum is not guaranteed to exist.
        scale_direction = self.determine_proportional_scaling_direction()
        # End if we shouldn't scale
        if scale_direction == 0:
            #dice_roll = np.random.randint(0,100)/100
            #if dice_roll <= settings.b_increase_prob:
            #    self.acquire_more_spectrum()
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
