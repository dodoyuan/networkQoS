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
    # y4 = all_data.sender_throughput.y4

    # x = np.array(x)
    # y1 = np.array(y1)
    # xnew = np.linspace(x.min(), x.max(), 300)
    # y1_smooth = spline(x, y1, xnew)
    plt.figure(figsize=(8, 5))
    # plt.plot(x, y1, 'k', marker='s', label="HP QoS flow(h1-h5)", markeredgewidth=1, mec='k',
    #          markerfacecolor="none", markersize=10)
    #
    # plt.plot(x, y2, 'r', marker='s', label="MP QoS flow(h2-h6)",
    #          markersize=10)
    #
    # plt.plot(x, y3, color='g', marker='h', markersize=10,
    #          label="LP QoS flow(h3-h7)")

    plt.plot(x, y1, 'k', marker='s', label="flow(h1-h5) priority 3", markeredgewidth=1, mec='k',
             markerfacecolor="none", markersize=10)

    plt.plot(x, y2, 'r', marker='^', label="flow(h2-h6) priority 2",
             markersize=10)

    plt.plot(x, y3, color='g', marker='h', markersize=10,
             label="flow(h3-h7) priority 1")

    # plt.plot(x, y4, color='b', marker='o', markersize=10,
    #          label="BE flow(h4-h8)")

    plt.ylabel('Throughput(Mbps)')
    plt.xlabel('Time(s)')
    plt.yticks(np.arange(0, 12, 1))
    plt.legend(loc='upper left')
    plt.show()

def CSWP_plot():

    x = np.arange(0, 31, 1)

    y1 = all_data.CWSP_throughput.y1
    y2 = all_data.CWSP_throughput.y2
    y3 = all_data.CWSP_throughput.y3
    # y4 = all_data.CWSP_throughput.y4

    plt.figure(figsize=(8, 5))
    # plt.plot(x, y1, 'k', marker='s', label="HP QoS flow(h1-h5)", markeredgewidth=1, mec='k',
    #          markerfacecolor="none", markersize=10)
    #
    # plt.plot(x, y2, 'r', marker='s', label="MP QoS flow(h2-h6)",
    #          markersize=10)
    #
    # plt.plot(x, y3, color='g', marker='h', markersize=10,
    #          label="LP QoS flow(h3-h7)")

    plt.plot(x, y1, 'k', marker='s', label="flow(h1-h5) priority 3", markeredgewidth=1, mec='k',
             markerfacecolor="none", markersize=10)

    plt.plot(x, y2, 'r', marker='s', label="flow(h2-h6) priority 2",
             markersize=10)

    plt.plot(x, y3, color='g', marker='h', markersize=10,
             label="flow(h3-h7) priority 1")

    # plt.plot(x, y4, color='b', marker='o', markersize=10,
    #          label="BE flow(h4-h8)")

    plt.ylabel('Throughput(Mbps)')
    plt.xlabel('Time(s)')
    plt.yticks(np.arange(0, 12, 1))
    plt.legend(loc='upper left')
    plt.show()

def ILP_plot():
    '''
      ILP model graph only
    '''

    x = np.arange(0, 31, 1)

    y1 = all_data.ILP_throughput.y1
    y2 = all_data.ILP_throughput.y2
    y3 = all_data.ILP_throughput.y3
    # y4 = all_data.ILP_throughput.y4

    plt.figure(figsize=(8, 5))

    # former data
    # plt.plot(x, y1, 'k', marker='s', label="HP QoS flow(h1-h5)", markeredgewidth=1, mec='k',
    #          markerfacecolor="none", markersize=10)
    #
    # plt.plot(x, y2, 'r', marker='s', label="MP QoS flow(h2-h6)",
    #          markersize=10)
    #
    # plt.plot(x, y3, color='g', marker='h', markersize=10,
    #          label="LP QoS flow(h3-h7)")

    plt.plot(x, y1, 'k', marker='s', label="flow(h1-h5) priority 3", markeredgewidth=1, mec='k',
             markerfacecolor="none", markersize=10)

    plt.plot(x, y2, 'r', marker='^', label="flow(h2-h6) priority 2",
             markersize=10)

    plt.plot(x, y3, color='g', marker='h', markersize=10,
             label="flow(h3-h7) priority 1")

    # plt.plot(x, y4, color='b', marker='o', markersize=10,
    #          label="BE flow(h4-h8)")

    plt.ylabel('Throughput(Mbps)')
    plt.xlabel('Time(s)')
    plt.yticks(np.arange(0, 12, 1))
    plt.legend(loc='upper left')
    plt.show()

def SP_plot():
    '''
      SP  graph only
    '''

    x = np.arange(0, 31, 1)

    y1 = all_data.SP_throughput.y1
    y2 = all_data.SP_throughput.y2
    y3 = all_data.SP_throughput.y3

    plt.figure(figsize=(8, 5))

    plt.plot(x, y1, 'k', marker='s', label="flow(h1-h5) priority 3", markeredgewidth=1, mec='k',
             markerfacecolor="none", markersize=10)

    plt.plot(x, y2, 'r', marker='o', label="flow(h2-h6) priority 2",
             markersize=10)

    plt.plot(x, y3, color='g', marker='h', markersize=10,
             label="flow(h3-h7) priority 1")

    # plt.plot(x, y4, color='b', marker='o', markersize=10,
    #          label="BE flow(h4-h8)")

    plt.ylabel('Throughput(Mbps)')
    plt.xlabel('Time(s)')
    plt.yticks(np.arange(0, 12, 1))
    plt.legend(loc='upper left')
    plt.show()


def total_throughput():
    '''
      compare the total throughput the the three method.(ECMP, SP, proposed)
    '''

    x = np.arange(0, 31, 1)

    y1 = all_data.SP_throughput.y1
    y2 = all_data.SP_throughput.y2
    y3 = all_data.SP_throughput.y3
    ysp = []
    for i in xrange(len(y1)):
        ysp.append(y1[i] + y2[i] + y3[i])

    y1 = all_data.ILP_throughput.y1
    y2 = all_data.ILP_throughput.y2
    y3 = all_data.ILP_throughput.y3
    yilp = []
    for i in xrange(len(y1)):
        yilp.append(y1[i] + y2[i] + y3[i])

    y1 = all_data.CWSP_throughput.y1
    y2 = all_data.CWSP_throughput.y2
    y3 = all_data.CWSP_throughput.y3
    yecmp = []
    for i in xrange(len(y1)):
        yecmp.append(y1[i] + y2[i] + y3[i])

    plt.figure(figsize=(8, 5))

    plt.plot(x, ysp, 'k', marker='s', label="shortest path", markeredgewidth=1, mec='k',
             markerfacecolor="none", markersize=10)

    plt.plot(x, yecmp, 'r', marker='o', label="ECMP",
             markersize=10)

    plt.plot(x, yilp, color='g', marker='^', markersize=10,
             label="proposed scheme")

    # plt.plot(x, y4, color='b', marker='o', markersize=10,
    #          label="BE flow(h4-h8)")

    plt.ylabel('total throughput(Mbps)')
    plt.xlabel('Time(s)')
    plt.yticks(np.arange(0, 20, 1))
    plt.legend(loc='lower right')
    plt.show()


if __name__ == '__main__':
    sender_plot()
    # CSWP_plot()
    # ILP_plot()
    total_throughput()

