import os
import sys
import time
import subprocess

def find_all(a_str, sub_str):
    start = 0
    b_starts = []
    while True:
        start = a_str.find(sub_str, start)
        if start == -1:
            return b_starts
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

# ovs-vsctl clear port %s qos queues

for port in prts:
    cmd = 'ovs-vsctl clear port %s qos' % port
    os.popen(cmd)
    # print "*** Removing former QoS & Queue"
os.popen("ovs-vsctl --all destroy qos")
os.popen("ovs-vsctl --all destroy queue")