from Global_Variables import *
import numpy as np
import math

class GenericDevice:
    def __init__(self, x=0, y=0,gain=1, tx_power=0, operator = 0):
        self.x = x
        self.y = y
        self.gain = gain
        self.tx_power = tx_power
        self.operator = operator
        self.currently_used_frequencies = []


    

    """Calculate received signal power received from another transmitter
    according to Friis transmission formula (free space).
    This can be substituted with a more accurate formula later on.
    CALCULATION IS DONE FROM THE RECEIVER PERSPECTIVE. i.e. The object calling the function"""
    def calculate_signal_power(self, sender, freq_range):
        distance = np.sqrt(np.power(self.x - sender.x,2) + np.power(self.y - sender.y,2))
        avg_frequency = np.average(freq_range)
        wavelength = speed_of_light/avg_frequency
        received_signal_power = (sender.tx_power * sender.gain * self.gain * np.power(wavelength,2))\
                                 / np.power(4 * np.pi * distance, 2)
        return received_signal_power


    def __str__(self):
        text_to_print = "x: {}    \ty:{}     \tOperator: {}"\
        .format(self.x, self.y, self.operator)
        return text_to_print
    

    

