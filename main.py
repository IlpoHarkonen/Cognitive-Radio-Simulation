import argparse
import logging
import math
import pickle

import matplotlib.pyplot as plt
import numpy as np

import settings
from base_station import BaseStation
from user_device import UserDevice
#from pytz.tzfile import base

LOG = logging.getLogger("main")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-a", "--area-width", help="Length of the square's (area) side", type=float)
parser.add_argument(
    "-b", "--base-hop-chance", help="Chance to hop to another base station, if possible.", type=float)
parser.add_argument(
    "-f", "--frequency-step", help="The amount of frequency increased or decreased at once.", type=float)

parser.add_argument(
    "-n", "--noise-factor", help="Noise factor.", type=float)
parser.add_argument(
    "-su", "--scale-up-threshold", help="Threshold value when deciding frequency scaling up.", type=float)
parser.add_argument(
    "-sd", "--scale-down-threshold", help="Threshold value when deciding frequency scaling down.", type=float)
parser.add_argument(
    "-t", "--cell-phone-tx-power", help="Transmit power of cell phone", type=float)
parser.add_argument(
    "-T", "--base-station-tx-power", help="Transmit power of base station", type=float)
parser.add_argument(
    "-v", "--verbose", help="increase output verbosity", action="store_true")

args = parser.parse_args()

if args.verbose:
    LOG.debug("Verbosity turned on")
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if args.area_width:
    settings.area_width = args.area_width
    LOG.info("Adjusting area width NxN with N value of {} m2".format(settings.area_width))

if args.base_hop_chance:
    settings.base_hop_chance = args.base_hop_chance
    LOG.info("Adjusting base hop chance to {}".format(settings.base_hop_chance))

if args.frequency_step:
    settings.freq_step = args.frequency_step
    LOG.info("Adjusting frequency step to {} MHz".format(settings.freq_step))
if args.noise_factor:
    settings.noise_factor= args.noise_factor
    LOG.info("Adjusting noise factor to {} ".format(settings.noise_factor))
if args.scale_up_threshold:
    settings.scale_up_threshold = args.scale_up_threshold
    LOG.info("Adjusting scale up threshold to {}".format(settings.scale_up_threshold))
if args.scale_down_threshold:
    settings.scale_down_threshold = args.scale_down_threshold
    LOG.info("Adjusting scale down threshold to {}".format(settings.scale_down_threshold))
if args.cell_phone_tx_power:
    settings.cell_phone_tx_power = args.cell_phone_tx_power
    LOG.info("Adjusting cell phone transmit power to {} W".format(settings.cell_phone_tx_power))
if args.base_station_tx_power:
    settings.base_station_tx_power = args.base_station_tx_power
    LOG.info("Adjusting base station transmit power to {} W".format(settings.base_station_tx_power))




def create_base_station_grid(number_of_stations, width, spectrum_sharing=True):
    """Create a set of base stations and place them into a square grid.
    The result is more even if the square root of the station count is
    an integer. (Should be)
    """
    # Determine the number of rows/columns
    rows = math.ceil(np.sqrt(number_of_stations))
    increment = width / (rows - 1)
    # Fill the grid with stations
    assigned_stations = []
    taken_frequencies = []
    oper_index = 1
    cnt = 0
    for i in range(0, rows):
        for j in range(0, rows):
            if len(assigned_stations) < number_of_stations:
                cnt += 1
                if spectrum_sharing == True:
                    station = BaseStation(
                        x=i * increment, y=j * increment, id=cnt)
                else:
                    station = BaseStation(
                        x=i * increment,
                        y=j * increment,
                        operator=oper_index,
                        id=cnt)
                    oper_index = ((oper_index + 1) % 3) + 1
                while station.currently_used_frequencies[0] in taken_frequencies:
                    station.get_random_frequency()
                taken_frequencies.append(station.currently_used_frequencies[0])
                assigned_stations.append(station)
    return assigned_stations


def create_users(number_of_users, width, spectrum_sharing=True):
    """Create a set of users and place them randomly into our designated
    area.
    """
    user_list = []
    oper_index = 1
    for i in range(0, number_of_users):
        x = np.random.randint(0, width)
        y = np.random.randint(0, width)
        if spectrum_sharing == True:
            user = UserDevice(x=x, y=y)
        else:
            user = UserDevice(x=x, y=y, operator=oper_index)
            oper_index = ((oper_index + 1) % 3) + 1
        user_list.append(user)
    return user_list




######################
#  START SIMULATING  #
######################
"""Create and place 9 stations in 1 square kilometer.
Also assigns a minimal starting frequency range to each base station at random.
This will be grown dynamically later on."""

# Load
f = open('store_stations.pckl', 'rb')
base_stations = pickle.load(f)
f.close()
# Store
f = open('store_stations.pckl', 'wb')
pickle.dump(base_stations, f)
f.close()

base_stations = create_base_station_grid(9, settings.area_width, settings.spectrum_sharing)
"""Obligatory LOG.debuging to confirm it works"""
LOG.debug("Base Stations")
for x in base_stations:
    LOG.debug(x)
"""Place 50 users at random locations"""
# Load them from file
# Load
f = open('store_users.pckl', 'rb')
users = pickle.load(f)
f.close()
f = open('store_users.pckl', 'wb')
pickle.dump(users, f)
f.close()

users = create_users(30, settings.area_width, settings.spectrum_sharing)
"""Let users connect to their nearest/best station first.
Strive for maximal signal strength without considering other users and interference (GADIA)."""
for user in users:
    user.set_initial_user_station(base_stations)
#set_initial_user_stations(users, base_stations)
"""Obligatory LOG.debuging to confirm it works"""
LOG.debug("\nUsers")
for x in users:
    LOG.debug(x)
"""Make base stations listen to each other on initial frequency slices."""
for station in base_stations:
    station.update_base_stations_in_range(base_stations)
    LOG.debug("CUR FREQ " + str(station.currently_used_frequencies))
"""Obligatory LOG.debuging to confirm it works."""
LOG.debug("\nWhich station needs hearing aids?")
for station_1 in base_stations:
    for station_2 in station_1.base_stations_in_range:
        station_2_id = station_2[0].id
        LOG.debug(
            "Basestation id: {} sees another station id: {}".
            format(station_1.id, station_2_id))
        LOG.debug(str(station_1.id) + "\t" + str(station_2_id))
"""Let base stations grow their frequency ranges up to the limit.
At this stage we do not listen to users, only nearby stations. IS THIS STEP EVEN NEEDED?"""
"""LOOP START"""
LOG.debug(str())
vote_stop = False
round_count = 1
while vote_stop == False:
    print("Game rounds taken: {}".format(round_count))
    round_count += 1
    vote_stop = True
    """Users can now switch to another base station.
    This is done with the following knowledge:
    - Number of users that each nearby base station is serving
    - Frequency ranges currently used by nearby stations.
    - Sensed noise from other users subscribed to different base stations"""
    # 1. Update devices in range of all users
    # Dynamic frequencies might occasionally hide some users which we previously heard
    for user in users:
        user.update_users_in_range(users)
        user.update_base_stations_in_range(base_stations)
        # Change base stations
        user.look_for_new_station(users)

    

    # 2. Check if any user votes to stop
    for user in users:
        if user.vote_to_stop == False:
            vote_stop = False
    """Let base stations adjust their frequency range dynamically according to the user count."""
    # 3. Update devices in range of all base stations and
    # let base stations scale their frequencies
    for station in base_stations:
        station.update_users_in_range(users)
        station.update_base_stations_in_range(base_stations)
        station.scale_frequency()
    # 4. Check if any base station votes to stop
    # Uncomment when done with dynamic spectrum allocation
    for station in base_stations:
        if station.vote_to_stop == False:
            vote_stop = False


"""LOOP END WHEN NOTHING CHANGES"""
for station in base_stations:
    print(station)

agg_throughput = 0
min_throughput = 9001
max_throughput = 0
for user in users:
    noise = user.calculate_noise_from_users(users, user.current_base_station)
    throughput = user.calculate_throughput(user.current_base_station, noise)
    agg_throughput += throughput
    if throughput < min_throughput:
        min_throughput = throughput
    if throughput > max_throughput:
        max_throughput = throughput
avg_throughput = agg_throughput/len(users)

print("Aggregate throughput: {:.2f} kpbs".format(agg_throughput))
print("Average throughput: {:.2f} kpbs".format(avg_throughput))
print("Minimum throughput: {:.2f} kbps".format(min_throughput))
print("Maximum throughput: {:.2f} kbps".format(max_throughput))


"""Summarise and plot results"""
# Lines from users to their base stations
for user in users:
    plt.plot(
        [user.x, user.current_base_station.x],
        [user.y, user.current_base_station.y],
        color="green")
# Users as dots
for user in users:
    plt.plot(user.x, user.y, "o", color="blue")
# Stations as dots
for station in base_stations:
    plt.plot(station.x, station.y, "o", color="black")
    plt.text(station.x, station.y, str(station.id), color="red", fontsize=12)
plt.show()
