#! /usr/bin/env python
# --*-- coding:utf8--*--

from collections import defaultdict
#from shortestSum import mod_dijkstra
import numpy as np
import matplotlib.pyplot as plt
import all_data
from scipy import interpolate


def sender_plot():

    x = np.arange(0, 31, 1)

    y1 = all_data.sender_throughput.y1
    y2 = all_data.sender_throughput.y2
    y3 = all_data.sender_throughput.y3
    y4 = all_data.sender_throughput.y4

    # x = np.array(x)
    # y1 = np.array(y1)
    # xnew = np.linspace(x.min(), x.max(), 300)
    # y1_smooth = spline(x, y1, xnew)
    plt.figure(figsize=(10, 7))
    plt.plot(x, y1, 'k', marker='s', label="high QoS level", markeredgewidth=1, mec='k',
             markerfacecolor="none", markersize=10)

    plt.plot(x, y2, 'r', marker='s', label="medium QoS level",
             markersize=10)

    plt.plot(x, y3, color='g', marker='o', markersize=10, markeredgewidth=1, mec='g',
             markerfacecolor="none", label="low QoS level")

    plt.plot(x, y4, color='b', marker='o', markersize=10,
             label="best effort")

    plt.ylabel('Throughput(Mbps)')
    plt.xlabel('Time(s)')
    plt.yticks(np.arange(0, 10, 1))
    plt.legend(loc='best')
    plt.show()

def CSWP_plot():

    x = np.arange(0, 31, 1)

    y1 = all_data.CWSP_throughput.y1
    y2 = all_data.CWSP_throughput.y2
    y3 = all_data.CWSP_throughput.y3
    y4 = all_data.CWSP_throughput.y4

    plt.figure(figsize=(10, 7))
    plt.plot(x, y1, 'k', marker='s', label="high QoS level", markeredgewidth=1, mec='k',
             markerfacecolor="none", markersize=10)

    plt.plot(x, y2, 'r', marker='s', label="medium QoS level",
             markersize=10)

    plt.plot(x, y3, color='g', marker='o', markersize=10, markeredgewidth=1,mec='g',
             markerfacecolor="none",label="low QoS level")

    plt.plot(x, y4, color='b', marker='o', markersize=10,
             label="best effort")

    plt.ylabel('Throughput(Mbps)')
    plt.xlabel('Time(s)')
    plt.yticks(np.arange(0, 10, 1))
    plt.legend(loc='best')
    plt.show()

def ILP_plot():

    x = np.arange(0, 31, 1)

    y1 = all_data.ILP_throughput.y1
    y2 = all_data.ILP_throughput.y2
    y3 = all_data.ILP_throughput.y3
    y4 = all_data.ILP_throughput.y4

    plt.figure(figsize=(8, 5))
    plt.plot(x, y1, 'k', marker='s', label="high QoS level", markeredgewidth=1, mec='k',
             markerfacecolor="none", markersize=10)

    plt.plot(x, y2, 'r', marker='s', label="medium QoS level",
             markersize=10)

    plt.plot(x, y3, color='g', marker='h', markersize=10,
              label="low QoS level")

    plt.plot(x, y4, color='b', marker='o', markersize=10,
            label="best effort")

    plt.ylabel('Throughput(Mbps)')
    plt.xlabel('Time(s)')
    plt.yticks(np.arange(0, 11, 1))
    plt.legend(loc='best')
    plt.show()

if __name__ == '__main__':
    sender_plot()
    CSWP_plot()
    ILP_plot()

