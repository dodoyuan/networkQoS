# Common Setting for Networ awareness module.


DISCOVERY_PERIOD = 10  # For discovering topology.

MONITOR_PERIOD = 10  # For monitoring traffic

DELAY_DETECTING_PERIOD = 5  # For detecting link delay.

TOSHOW = True  # For showing information in terminal

MAX_CAPACITY = 281474976710655L  # Max capacity of link

k_paths = 2

WEIGHT = 'bw'

# predefined requirement band-with of each source IP
require_band = {"10.0.0.1": 50000000, "10.0.0.2": 50000000, "10.0.0.3": 20000000,
                "10.0.0.4": 10000000, "10.0.0.5": 10000000, "10.0.0.6": 10000000}

# predefined priority of each source IP
priority_weight = {"10.0.0.1": 32, "10.0.0.2": 16, "10.0.0.3": 8,
                   "10.0.0.4": 4,  "10.0.0.5": 2,  "10.0.0.6": 1}
