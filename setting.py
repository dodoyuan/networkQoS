# Common Setting for Networ awareness module.
from collections import defaultdict

DISCOVERY_PERIOD = 15  # For discovering topology.

MONITOR_PERIOD = 3  # For monitoring traffic

DELAY_DETECTING_PERIOD = 2  # For detecting link delay.

TOSHOW = True  # For showing information in terminal

MAX_CAPACITY = 281474976710655L  # Max capacity of link


# link_capacity = 10
def get_link_capacity(dpid, port):
    link_capacity = defaultdict(lambda :defaultdict(10))
    link_capacity[8][1] = 100
    link_capacity[1][1] = 100
    link_capacity[1][2] = 100
    link_capacity[1][3] = 100
    link_capacity[1][4] = 100
    return link_capacity[dpid][port]

k_paths = 2

WEIGHT = 'bw'

# predefined requirement band-with of each source IP
require_band = {"10.0.0.1": 8, "10.0.0.2": 8, "10.0.0.3": 8,
                "10.0.0.4": 1, "10.0.0.5": 1, "10.0.0.6": 1}

# predefined priority of each source IP
priority_weight = {"10.0.0.1": 32, "10.0.0.2": 16, "10.0.0.3": 8,
                   "10.0.0.4": 4,  "10.0.0.5": 2,  "10.0.0.6": 1}
