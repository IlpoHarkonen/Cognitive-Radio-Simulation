import numpy as np
from Global_Variables import *


class UserDevice:
    def __init__(self, x=0, y=0, gain=1,\
                 tx_power=0, operator=0):
        self.x = x
        self.y = y
        self.gain = gain
        self.tx_power = cell_phone_tx_power #Watts
        self.operator = operator
        self.currently_used_frequencies = []
        
        self.current_base_station = None
        self.stations_in_range = []
    

    
    def __str__(self):
        text_to_print = "x: {}\ty:{}\tOperator: {}\tStation: {}"\
        .format(self.x, self.y, self.operator, self.current_base_station.id)
        return text_to_print