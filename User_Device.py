


class UserDevice:
    def __init__(self, x=0, y=0, tx_power=0, operator=0):
        self.x = x
        self.y = y
        self.tx_power = tx_power
        self.operator = operator
        
        self.current_base_station = None
        self.stations_in_range = []