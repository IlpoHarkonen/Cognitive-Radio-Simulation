from Base_Station import BaseStation
from User_Device import UserDevice
from Generic_Functions import *
from Global_Variables import *
import matplotlib
import numpy as np


"""Create and place 9 stations in 1 square kilometer"""
base_stations = create_base_station_grid(9, area_width, False)

"""Obligatory printing to confirm it works"""
print(len(base_stations))
for x in base_stations:
    print(x)
    
"""Place 50 users at random locations"""
users = create_users(50, area_width, False)

"""Obligatory printing to confirm it works"""
print(len(users))
for x in users:
    print(x)