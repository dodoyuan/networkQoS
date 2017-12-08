#! /usr/bin/env python
# --*-- coding:utf8--*--

from collections import defaultdict
#from shortestSum import mod_dijkstra
import numpy as np
import matplotlib.pyplot as plt
import all_data


def sender_plot():
    x = np.arange(0, 31, 1)
    y1 = all_data.sender_throughput.y1
    y2 = all_data.sender_throughput.y2
    y3 = all_data.sender_throughput.y3
    y4 = all_data.sender_throughput.y4

    plt.figure(figsize=(15, 7))
    plt.plot(x, y1, 'b', marker='+', label="high QoS level")
    plt.plot(x, y2, 'r', marker='*', label="medium QoS level")
    plt.plot(x, y3, color='g', marker='x',
             label="low QoS level")

    plt.plot(x, y4, color='k', marker='2',
             label="best effort")

    plt.ylabel('Throughput(Mbps)')
    plt.xlabel('Time(s)')
    plt.yticks(np.arange(0, 10, 1))
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    sender_plot()

