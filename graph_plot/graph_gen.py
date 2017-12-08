#! /usr/bin/env python
# --*-- coding:utf8--*--

from collections import defaultdict
#from shortestSum import mod_dijkstra
import numpy as np
import matplotlib.pyplot as plt
import all_data


def sender_plot():
    x = np.arange(0, 60, 1)
    y1 = all_data.sender_throughput.y1
    y2 = all_data.sender_throughput.y2
    y3 = all_data.sender_throughput.y3
    y4 = all_data.sender_throughput.y4

    plt.figure(figsize=(15, 7))
    plt.plot(x, y1, 'b--', marker='+', label="$high QoS level$")
    plt.plot(x, y2, 'r--', marker='*', label="$medium QoS level$")
    plt.plot(x, y3, color='g',linestyle='--', marker='x',
             label="$low QoS level$",
             linewidth=2)
    plt.plot(x, y4, color='k', linestyle='--', marker='2',
             label="$best effort$",
             linewidth=2)
    plt.ylabel('average controller plane availability')
    plt.xlabel('Node availability')
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    sender_plot()

