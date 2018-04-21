from Base_Station import BaseStation
from User_Device import UserDevice
import numpy as np
import math



"""Create a set of base stations and place them into a square grid.
The result is more even if the square root of the station count is an integer. (Should be)"""
def create_base_station_grid(number_of_stations, width, spectrum_sharing = True):
    #Determine the number of rows/columns
    rows = math.ceil(np.sqrt(number_of_stations))
    increment = width / (rows-1)
    #Fill the grid with stations
    assigned_stations = []
    oper_index = 1
    for i in range(0, rows):
        for j in range(0, rows):
            if len(assigned_stations) < number_of_stations:
                if spectrum_sharing == True:
                    station = BaseStation(x=i*increment, y=j*increment)
                else:
                    station = BaseStation(x=i*increment, y=j*increment, operator=oper_index)
                    oper_index = ((oper_index + 1) % 3) + 1
                assigned_stations.append(station)
    return assigned_stations
    
"""Create a set of users and place them randomly into our designated area."""
def create_users(number_of_users, width, spectrum_sharing = True):
    user_list = []
    oper_index = 1
    for i in range(0, number_of_users):
        x = np.random.randint(0,width)
        y = np.random.randint(0,width)
        if spectrum_sharing == True:
            user = UserDevice(x=x, y=y)
        else:
            user = UserDevice(x=x, y=y, operator=oper_index)
            oper_index = ((oper_index + 1) % 3) + 1
        user_list.append(user)
    return user_list

"""Calculate received signal power received from another transmitter
according to Friis transmission formula (free space).
This can be substituted with a more accurate formula later on."""
def calculate_signal_power(receiver, sender):
    distance = np.sqrt(np.power(receiver.x - sender.x,2) + np.power(receiver.y - sender.y,2))
    avg_wavelength = np.average(sender.frequency)
    received_signal_power = (sender.tx_power * sender.gain * receiver.gain * np.power(avg_wavelength,2))\
                             / np.power(4 * np.pi * distance, 2)
    return received_signal_power


