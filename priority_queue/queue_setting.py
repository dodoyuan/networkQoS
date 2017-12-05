#! /usr/bin/python
#  coding: utf-8

'''
Add queues to Mininet using ovs-vsctl and ovs-ofctl
@Author Ryan Wallner
'''

import os
import sys
import time
import subprocess

def find_all(a_str, sub_str):
    start = 0
    b_starts = []
    while True:
        start = a_str.find(sub_str, start)
        if start == -1: return b_starts
        #print start
        b_starts.append(start)
        start += 1


if os.getuid() != 0:
    print "Root permissions required"
    exit()


cmd = "ovs-vsctl show"
p = os.popen(cmd).read()
#print p

brdgs = find_all(p, "Bridge")
print brdgs

switches = []
for bn in brdgs:
    sw =  p[(bn+8):(bn+10)]
    switches.append(sw)

ports = find_all(p, "Port")
print ports

prts = []
for prt in ports:
    prt = p[(prt+6):(prt+13)]
    if '"' not in prt:
            print prt
            prts.append(prt)

for port in prts:
    cmd = 'ovs-vsctl clear port %s qos' % port
    os.popen(cmd)


config_strings = {}
for i in range(len(switches)):
    str = ""
    sw = switches[i]
    for n in range(len(prts)):
        #verify correct order
        if switches[i] in prts[n]:
            port_name = prts[n]
            str = str+" -- set port %s qos=@defaultqos" % port_name
    config_strings[sw] = str

# for sw in switches:
#     queuecmd = "sudo ovs-vsctl %s " \
#                "-- --id=@defaultqos create qos type=linux-htb queues=0=@q0,1=@q1,2=@q2 " \
#                "-- --id=@q0 create queue other-config:priority=0 " \
#                "-- --id=@q1 create queue other-config:priority=10 " \
#                "-- --id=@q2 create queue other-config:priority=100 " % config_strings[sw]
#     print 'exec cmd %s', queuecmd
#     q_res = os.popen(queuecmd).read()
#     # print q_res

for sw in switches:
    queuecmd = "sudo ovs-vsctl %s " \
               "-- --id=@defaultqos create qos type=linux-htb other-config:max-rate=12000000 queues=0=@q0,1=@q1,2=@q2 " \
               "-- --id=@q0 create queue other-config:min-rate=8000000 other-config:max-rate=8000000 " \
               "-- --id=@q1 create queue other-config:min-rate=4000000 other-config:max-rate=8000000 " \
               "-- --id=@q2 create queue other-config:min-rate=0 other-config:max-rate=12000000 " % config_strings[sw]
    print 'exec cmd %s', queuecmd
    q_res = os.popen(queuecmd).read()
    # print q_res



