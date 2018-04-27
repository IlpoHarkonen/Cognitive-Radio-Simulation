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
base_hop_chance = 0.9

"""Scaling threshold. These are used as threshold  values
when deciding if we should scale our frequency up or down.
We compare the factor to division of bases station scores,
which are calculated from currently used bandwidth and number of users."""
scale_up_threshold = 1.05
scale_down_threshold = 1.3

"""Bandwidth increase probability"""
b_increase_prob = 0.5



"""1800 MHz and 2600 MHz frequencies.
Sublists feature min and max values of a licensed band."""
# Operator 1
DNA_frequencies =   [[1735, 1759], [2500, 2520]]
# Operator 2
Elisa_frequencies = [[1760, 1784], [2545, 2570]]
# Operator 3
Telia_frequencies = [[1710, 1734], [2520, 2545]]

operator_frequencies = [DNA_frequencies, Elisa_frequencies, Telia_frequencies]
