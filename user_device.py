import numpy as np
import settings
from generic_functions import GenericDevice


class UserDevice(GenericDevice):
    def __init__(self, x=0, y=0, gain=1,\
                 tx_power=0, operator=0):
        GenericDevice.__init__(
            self,
            x=x,
            y=y,
            gain=gain,
            tx_power=settings.cell_phone_tx_power,
            operator=operator)
        self.currently_used_frequencies = []
        self.current_base_station = None
        self.stations_in_range = []

    """Initial station is chosen purely on best received signal power"""

    def set_initial_user_station(self, station_list):
        # Find the best station
        best_station = None
        best_pow = 0
        for station in station_list:
            sig_pow = self.calculate_signal_power(
                station, station.currently_used_frequencies[0])
            if sig_pow > best_pow:
                best_pow = sig_pow
                best_station = station
        #Update class attributes to correspond to the choice
        if best_station != None:
            self.current_base_station = best_station
            best_station.currently_served_users.append(self)

    def __str__(self):
        text_to_print = "\tStation: {}"\
        .format(self.current_base_station.id)
        return GenericDevice.__str__(self) + text_to_print
