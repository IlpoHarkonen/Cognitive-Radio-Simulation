speed_of_light = 299792458

"""Choose to share all spectrum between all devices (True)
or restrict into different operators (False)"""
spectrum_sharing = True

"""Minimum received power for a device to be able to communicate with
another (-100 dBm)"""
power_threshold = 1e-13

"""Transmit powers as watts """
cell_phone_tx_power = 1 # Watts (= 30 dBm)
base_station_tx_power = 19.95 # Watts (~= 43 dBm)

"""Area width used (total area is width squared)"""
area_width = 1000

"""Starting frequency size (f_max - f_min).
This is the slice that is initially given to a base station.
KEEP THIS AS 1. (Hacker optimization in main.create_base_station_grid)"""
freq_start_size = 1 # MHz

"""The amount we either increase or decrease our frequency range at
once."""
freq_step = 1 # MHz

""" Noise factor """
noise_factor = 0.01

"""Chance that we hop to another base station.
This base chance is further divided by the number
of users the hopping user currently senses."""
base_hop_chance = 0.6

"""Scaling threshold. These are used as threshold  values
when deciding if we should scale our frequency up or down.
We compare the factor to division of bases station scores,
which are calculated from currently used bandwidth and number of users."""
scale_up_threshold = 0.7 #Lower than one
scale_down_threshold = 1.3 #Higher than one

"""Bandwidth increase probability"""
b_increase_prob = 0.5



"""1800 MHz and 2600 MHz frequencies.
Sublists feature min and max values of a licensed band."""
# Operator 1
DNA_frequencies =   [[758, 768], [791, 801], [925, 936], [1830, 1854], [2130, 2149], [2620, 2640]]
# Operator 2
Elisa_frequencies = [[768, 778], [811, 821], [948, 959], [1855, 1879], [2110, 2130], [2665, 2690]]
# Operator 3
Telia_frequencies = [[778, 788], [801, 811], [936, 948], [1805, 1829], [2149, 2169], [2640, 2665]]

operator_frequencies = [DNA_frequencies, Elisa_frequencies, Telia_frequencies]
