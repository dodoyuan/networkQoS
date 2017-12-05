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
    sw = p[(bn+8):(bn+10)]
    switches.append(sw)

ports = find_all(p, "Port")
print ports

prts = []
for prt in ports:
    prt = p[(prt+6):(prt+13)]
    if '"' not in prt:
            print prt
            prts.append(prt)

for sw in switches:
    cmd = "ovs-vsctl set Bridge %s protocols=OpenFlow13" % sw
    q_res = os.popen(cmd).read()

for port in prts:
    queuecmd = "sudo ovs-vsctl -- set port %s qos=@defaultqos " \
               "-- --id=@defaultqos create qos type=linux-htb other-config:max-rate=12000000 queues=0=@q0,1=@q1,2=@q2 " \
               "-- --id=@q0 create queue other-config:min-rate=8000000 other-config:max-rate=8000000 " \
               "-- --id=@q1 create queue other-config:min-rate=3000000 other-config:max-rate=3000000 " \
               "-- --id=@q2 create queue other-config:min-rate=0 other-config:max-rate=10000000 " % port
    print 'exec cmd:', queuecmd
    q_res = os.popen(queuecmd).read()
# print q_res

# ovs-vsctl -- set Port s1-eth3 qos=@defaultqos\
#     -- --id=@defaultqos create QoS type=linux-htb other-config:max-rate=300000000 queues=1=@q1\
#      -- --id=@q1 create Queue other-config:min-rate=5000000 other-config:max-rate=200000000


