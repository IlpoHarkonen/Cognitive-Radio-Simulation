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
    cnt = 0
    for i in range(0, rows):
        for j in range(0, rows):
            if len(assigned_stations) < number_of_stations:
                cnt += 1
                if spectrum_sharing == True:
                    station = BaseStation(x=i*increment, y=j*increment, id = cnt)
                else:
                    station = BaseStation(x=i*increment, y=j*increment, operator=oper_index, id= cnt)
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
def calculate_signal_power(receiver, sender, freq_range):
    distance = np.sqrt(np.power(receiver.x - sender.x,2) + np.power(receiver.y - sender.y,2))
    avg_wavelength = np.average(freq_range)
    received_signal_power = (sender.tx_power * sender.gain * receiver.gain * np.power(avg_wavelength,2))\
                             / np.power(4 * np.pi * distance, 2)
    return received_signal_power



    
"""Initial station is chosen purely on best received signal power"""
def set_initial_user_stations(user_list, station_list):
    for user in user_list:
        #Find the best station
        best_pow = 0
        for station in station_list:
            sig_pow = calculate_signal_power(user, station, station.currently_used_frequencies[0])
            if sig_pow > best_pow:
                best_pow = sig_pow
                best_station = station
        #Update class attributes to correspond to the choice
        user.current_base_station = best_station
        best_station.currently_served_users.append(user)
    

