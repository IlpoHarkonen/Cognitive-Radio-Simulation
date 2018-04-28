import numpy as np

import settings


class GenericDevice:
    def __init__(self, x=0, y=0, gain=1, tx_power=0, operator=0):
        self.x = x
        self.y = y
        self.gain = gain
        self.tx_power = tx_power
        self.operator = operator
        #The frequencies this device is using
        self.currently_used_frequencies = []
        
        # Lists of devices that we can communicate with.
        # (i.e. received power is over the threshold)
        # Example: [ [device 1, [freq_min, freq_max]], [device 2, [freq_min, freq_max]] ]
        self.users_in_range = []
        self.base_stations_in_range = []
        self.vote_to_stop = False

    def calculate_signal_power(self, sender, freq_range):
        """Calculate received signal power received from another transmitter
        according to Friis transmission formula (free space).
        This can be substituted with a more accurate formula later on.
        CALCULATION IS DONE FROM THE RECEIVER PERSPECTIVE. i.e. The object calling the function.
        """
        distance = np.sqrt(
            np.power(self.x - sender.x, 2) + np.power(self.y - sender.y, 2))
        avg_frequency = np.average(freq_range) * 1e6
        wavelength = settings.speed_of_light / avg_frequency
        received_signal_power = (
            sender.tx_power * sender.gain * self.gain * np.power(
                wavelength, 2)) / np.power(4 * np.pi * distance, 2)
        return received_signal_power
    
    def calculate_throughput(self,sender,noise_from_other_devices):
        """Calculate throughput according to Shannon Capacity."""
        B = 0
        sig_pow = 0
        for freq_range in sender.currently_used_frequencies:
            B += freq_range[1] - freq_range[0]
            sig_pow += self.calculate_signal_power(sender, freq_range)\
                            /(len(sender.currently_used_frequencies))
        throughput = B * np.log2(1 + sig_pow / (noise_from_other_devices + settings.noise_factor))
        return throughput
    
    
    def update_users_in_range(self, user_list):
        """Calculate the received power from each possible user to
        determine who we can communicate with.
        """
        self.users_in_range = []
        for user in user_list:
            if user != self:
                for freq_range in user.currently_used_frequencies:
                    received_power = self.calculate_signal_power(user, freq_range)
                    if received_power > settings.power_threshold:
                        tmp_freq = freq_range[:]
                        if tmp_freq not in self.users_in_range:
                            self.users_in_range.append(tmp_freq)
    
    
    def update_base_stations_in_range(self, base_station_list):
        """Calculate the received power from each possible base_station
        to determine who we can communicate with. Can also be used to
        refresh the list if a nreaby station switches frequency and
        thus turns invisible.
        """
        self.base_stations_in_range = []
        for station in base_station_list:
            # Don't compare a base station with itself
            if station != self:
                for freq_range in station.currently_used_frequencies:
                    received_power = self.calculate_signal_power(
                        station, freq_range)
                    if received_power > settings.power_threshold:
                        self.base_stations_in_range.append(
                            [station, freq_range])

    def __str__(self):
        text_to_print = "x: {}    \ty:{}     \tOperator: {}".format(
            self.x, self.y, self.operator)
        return text_to_print
