import logging

import numpy as np

import settings
from generic_functions import GenericDevice

LOG = logging.getLogger(__name__)


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
        # Stations in range: [ [station1, [freq_min, freq_max], sig_pow] ]
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
                LOG.debug(
                    "Signal power for UserDevice at x: {} y: {} is {}".format(
                        self.x, self.y, 10 * np.log10(sig_pow / 0.001)))
        # Update class attributes to correspond to the choice
        if best_station != None:
            self.current_base_station = best_station
            best_station.currently_served_users.append(self)


    def update_stations_in_range(self, station_list):
        pass
    
    """Changes to a better base station on probability P if one if found. We only consider the best found station."""
    def look_for_new_station(self, user_list):
        best_throughput = 0
        best_station = None
        for [station, freq_range_1, recv_pow] in self.stations_in_range:
            # Calculate SNR on the given frequency range.
            # Only interference is from users subsribed to other base stations using the same frequency.
            noise = 0
            for user in user_list:
                if user != self and station != user.current_base_station:
                    for freq_range_2 in user.currently_used_frequencies:
                        # Check for frequency overlap
                        if freq_range_2[0] < freq_range_1[0] < freq_range_2[1] or \
                        freq_range_2[0] < freq_range_1[1] < freq_range_2[1]:
                            # Add noise in proportion to how often the colliding user transmits
                            noise += self.calculate_signal_power(user, freq_range_2)\
                            /len(user.current_base_station.currently_served_users)
                        
            # Calculate throughput if we choose the station
            obtainable_throughput = self.calculate_throughput(station, noise) / (len(station.currently_served_users)+1)
            if obtainable_throughput > best_throughput:
                best_throughput = obtainable_throughput
                best_station = station
        # Finally switch to the new station if one was found. Otherwise vote to stop
        if best_station != None:
            current_station = self.current_base_station
            current_station.currently_served_users.remove(self)
            best_station.currently_served_users.append(self)
            self.current_base_station = best_station
            self.vote_to_stop = False
        else:
            self.vote_to_stop = True
        
        
        
        """TODO: Docstring for function.

        Args:
            arg1 (TODO): TODO

        Returns: TODO

        """
        pass

    def __str__(self):
        text_to_print = "\tStation: {}"\
        .format(self.current_base_station.id)
        return GenericDevice.__str__(self) + text_to_print
