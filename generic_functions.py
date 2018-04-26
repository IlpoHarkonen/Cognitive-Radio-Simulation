import numpy as np

import settings


class GenericDevice:
    def __init__(self, x=0, y=0, gain=1, tx_power=0, operator=0):
        self.x = x
        self.y = y
        self.gain = gain
        self.tx_power = tx_power
        self.operator = operator
        self.currently_used_frequencies = []
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

    def __str__(self):
        text_to_print = "x: {}    \ty:{}     \tOperator: {}".format(
            self.x, self.y, self.operator)
        return text_to_print
