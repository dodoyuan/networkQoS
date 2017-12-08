#! /usr/bin/env python
# --*-- coding:utf8--*--

from collections import defaultdict
#from shortestSum import mod_dijkstra
import numpy as np
import matplotlib.pyplot as plt
import all_data
from scipy.interpolate import spline


def sender_plot():
    x = np.arange(0, 31, 1)

    x_sm = np.array(x)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)

    y1 = np.array(all_data.sender_throughput.y1)
    y2 = np.array(all_data.sender_throughput.y2)
    y3 = np.array(all_data.sender_throughput.y3)
    y4 = np.array(all_data.sender_throughput.y4)

    plt.figure(figsize=(15, 7))

    y1_smooth = spline(x, y1, x_smooth)
    plt.plot(x_smooth, y1_smooth, 'b', marker='+', label="high QoS level",
             markersize=4)

    y2_smooth = spline(x, y2, x_smooth)
    plt.plot(x, y2_smooth, 'r', marker='*', label="medium QoS level",
             markersize=4)

    y3_smooth = spline(x, y3, x_smooth)
    plt.plot(x, y3_smooth, color='g', marker='x', markersize=4,
             label="low QoS level")

    y4_smooth = spline(x, y4, x_smooth)
    plt.plot(x, y4_smooth, color='k', marker='o', markersize=4,
             label="best effort")

    plt.ylabel('Throughput(Mbps)')
    plt.xlabel('Time(s)')
    plt.yticks(np.arange(0, 10, 1))
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    sender_plot()

