import numpy as np
from Global_Variables import *


class UserDevice:
    def __init__(self, x=0, y=0, gain=1,\
                 tx_power=0, operator=0,\
                 f_min=0, f_max = 0):
        self.x = x
        self.y = y
        self.gain = gain
        self.tx_power = cell_phone_tx_power #Watts
        self.operator = operator
        self.current_frequency = [f_min, f_max]
        
        self.current_base_station = None
        self.stations_in_range = []
        
    def __str__(self):
        text_to_print = "x: {}\ty:{}\tOperator: {}".format(self.x, self.y, self.operator)
        return text_to_print