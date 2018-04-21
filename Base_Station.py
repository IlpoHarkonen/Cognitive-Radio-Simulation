"""
Operator:
0: To remove operator restrictions
1: DNA
2: Elisa
3: Telia
"""


class BaseStation:
    def __init__(self, x=0, y=0, tx_power=0):
        self.x = x
        self.y = y
        self.tx_power = tx_power
        self.all_frequencies = []
        self.current_frequencies = []
        #A list of frequencies which the base station senses being used nearby by someone else
        self.populated_frequencies = []
        self.operator = None
        
        self.users_in_range = []
        
    def update_users_in_range(self, user_list):