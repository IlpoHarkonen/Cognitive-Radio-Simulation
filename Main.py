from Base_Station import BaseStation
from User_Device import UserDevice
from Generic_Functions import *
from Global_Variables import *
import matplotlib
import numpy as np


"""Example of creatings and placing 100 stations in 1 square kilometer"""
lst = create_base_station_grid(100, 1000, 0)
print(len(lst))
for x in lst:
    print("x: {}\ty: {}".format(x.x,x.y))