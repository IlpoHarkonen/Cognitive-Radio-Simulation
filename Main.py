from Base_Station import BaseStation
from User_Device import UserDevice
from Generic_Functions import *
from Global_Variables import *
import matplotlib.pyplot as plt
import numpy as np


"""Create and place 9 stations in 1 square kilometer.
Also assigns a minimal starting frequency range to each base station at random.
This will be grown dynamically later on."""
base_stations = create_base_station_grid(9, area_width, False)

"""Obligatory printing to confirm it works"""
print(len(base_stations))
for x in base_stations:
    print(x)
    
"""Place 50 users at random locations"""
users = create_users(50, area_width, False)




"""Let users connect to their nearest/best station first.
Strive for maximal signal strength without considering other users and interference (GADIA)."""
set_initial_user_stations(users, base_stations)

"""Obligatory printing to confirm it works"""
print(len(users))
for x in users:
    print(x)
    

"""Let base stations grow their frequency ranges up to the limit."""



"""LOOP START"""

"""Users can now switch to another less populated base station.
This is done with the following knowledge:
- Number of users that each nearby base station is serving
- Frequency ranges currently used by nearby stations."""


"""Let base stations adjust their frequency range dynamically according to the user count."""

"""LOOP END WHEN NOTHING CHANGES"""

"""Summarise and plot results"""
#Lines from users to their base stations
for user in users:
    plt.plot([user.x, user.current_base_station.x], [user.y, user.current_base_station.y], color = "green")
#Users as dots
for user in users:
    plt.plot(user.x, user.y, "o", color="blue")
#Stations as dots
for station in base_stations:
    plt.plot(station.x,station.y,"o", color="black")
    plt.text(station.x, station.y, str(station.id), color="red", fontsize=12)
plt.show()

