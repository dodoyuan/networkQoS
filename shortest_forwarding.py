# Copyright (C) 2016 Li Cheng at Beijing University of Posts
# and Telecommunications. www.muzixing.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding=utf-8
import logging
import struct
import networkx as nx
from operator import attrgetter
from ryu import cfg
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import arp

from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link

import network_awareness
import network_monitor
# import network_delay_detector
import setting
from network_reconfigration import milp_constrains


class ShortestForwarding(app_manager.RyuApp):
    """
        ShortestForwarding is a Ryu app for forwarding packets in shortest
        path.
        This App does not defined the path computation method.
        To get shortest path, this module depends on network awareness,
        network monitor and network delay detecttor modules.
    """

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {
        "network_awareness": network_awareness.NetworkAwareness,
        "network_monitor": network_monitor.NetworkMonitor,
        # "network_delay_detector": network_delay_detector.NetworkDelayDetector
        }

    WEIGHT_MODEL = {'hop': 'weight', "delay": "delay", "bw": "bw"}

    def __init__(self, *args, **kwargs):
        super(ShortestForwarding, self).__init__(*args, **kwargs)
        self.name = 'shortest_forwarding'
        self.awareness = kwargs["network_awareness"]
        self.monitor = kwargs["network_monitor"]
        # self.delay_detector = kwargs["network_delay_detector"]
        self.datapaths = {}
        self.weight = self.WEIGHT_MODEL[setting.WEIGHT]
        # below is data for ilp process
        # self.ilp_module_thread = hub.spawn(self._ilp_process)
        self.map = {}

        self.flow = {}   # (eth_type, ip_pkt.src, ip_pkt.dst, in_port)-->
                         # [require_band,priority,(src,dst)]
        self.flow_ip = []
        self.count = 1
        self.src_dst = []
        self.config_priority = 2  #
        self.config_flag = 0
        self.handle_flag = 0

    def set_weight_mode(self, weight):
        """
            set weight mode of path calculating.
        """
        self.weight = weight
        if self.weight == self.WEIGHT_MODEL['hop']:
            self.awareness.get_shortest_paths(weight=self.weight)
        return True

    def _ilp_process(self):
        '''
            the entry for ilp process
        '''
        # if flag is 1,denote there must be congestion
        self.logger.debug("config_flag:%s handle-flag %s" % (self.config_flag, self.handle_flag))
        if self.config_flag and self.handle_flag:
            self.logger.debug("enter reconfigration")
            self.handle_flag = 0  # avoid handle repeat request
            self.config_flag = 0
            allpath, flow_identity, max_priority = self.reconfigration()
            self.logger.info("path :%s" % allpath)
            for flow_num, path in allpath.items():
                flow_info = flow_identity[flow_num]
                self.install_flow(self.datapaths,
                                  self.awareness.link_to_port,
                                  self.awareness.access_table, path,
                                  flow_info, None, prio=self.config_priority)

            self.ilp_handle_info(max_priority, allpath.keys(), flow_identity)
            self.config_priority += 1

    def ilp_handle_info(self, max_priority, flow_list, flow_info):
        '''
           use to inform which flow handle,and which not
        '''
        for num in flow_list:
            self.logger.info("handle flow : %s" % flow_info[num])
            flow_info.pop(num)
        self.logger.info("the max priority weight is: %s" % max_priority)
        if flow_info:
            for flow in flow_info:
                self.logger.info("not handle flow : %s" % flow)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        """
            Collect datapath information.
        """
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if not datapath.id in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def add_flow(self, dp, p, match, actions, idle_timeout=0, hard_timeout=0):
        """
            Send a flow entry to datapath.
        """
        ofproto = dp.ofproto
        parser = dp.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        # SET flags=ofproto.OFPFF_SEND_FLOW_REM to inform controller about flow remove
        mod = parser.OFPFlowMod(datapath=dp, priority=p,
                                idle_timeout=idle_timeout,
                                hard_timeout=hard_timeout,
                                flags=ofproto.OFPFF_SEND_FLOW_REM,
                                match=match, instructions=inst)
        dp.send_msg(mod)

    def send_flow_mod(self, datapath, flow_info, src_port, dst_port, prio=1):
        """
            Build flow entry, and send it to datapath.
        """
        parser = datapath.ofproto_parser
        actions = []
        actions.append(parser.OFPActionOutput(dst_port))

        match = parser.OFPMatch(
            in_port=src_port, eth_type=flow_info[0],
            ipv4_src=flow_info[1], ipv4_dst=flow_info[2])

        self.add_flow(datapath, prio, match, actions,
                      idle_timeout=15, hard_timeout=60)

    def _build_packet_out(self, datapath, buffer_id, src_port, dst_port, data):
        """
            Build packet out object.
        """
        actions = []
        if dst_port:
            actions.append(datapath.ofproto_parser.OFPActionOutput(dst_port))

        msg_data = None
        if buffer_id == datapath.ofproto.OFP_NO_BUFFER:
            if data is None:
                return None
            msg_data = data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=buffer_id,
            data=msg_data, in_port=src_port, actions=actions)
        return out

    def send_packet_out(self, datapath, buffer_id, src_port, dst_port, data):
        """
            Send packet out packet to assigned datapath.
        """
        out = self._build_packet_out(datapath, buffer_id,
                                     src_port, dst_port, data)
        if out:
            datapath.send_msg(out)

    def get_port(self, dst_ip, access_table):
        """
            Get access port if dst host.
            access_table: {(sw,port) :(ip, mac)}
        """
        if access_table:
            if isinstance(access_table.values()[0], tuple):
                for key in access_table.keys():
                    if dst_ip == access_table[key][0]:
                        dst_port = key[1]
                        return dst_port
        return None

    def get_port_pair_from_link(self, link_to_port, src_dpid, dst_dpid):
        """
            Get port pair of link, so that controller can install flow entry.
        """
        if (src_dpid, dst_dpid) in link_to_port:
            return link_to_port[(src_dpid, dst_dpid)]
        else:
            self.logger.info("dpid:%s->dpid:%s is not in links" % (
                             src_dpid, dst_dpid))
            return None

    def flood(self, msg):
        """
            Flood ARP packet to the access port
            which has no record of host.
        """
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        for dpid in self.awareness.access_ports:
            for port in self.awareness.access_ports[dpid]:
                if (dpid, port) not in self.awareness.access_table.keys():
                    datapath = self.datapaths[dpid]
                    out = self._build_packet_out(
                        datapath, ofproto.OFP_NO_BUFFER,
                        ofproto.OFPP_CONTROLLER, port, msg.data)
                    datapath.send_msg(out)
        self.logger.debug("Flooding msg")

    def arp_forwarding(self, msg, src_ip, dst_ip):
        """ Send ARP packet to the destination host,
            if the dst host record is existed,
            else, flow it to the unknow access port.
        """
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        result = self.awareness.get_host_location(dst_ip)
        if result:  # host record in access table.
            datapath_dst, out_port = result[0], result[1]
            datapath = self.datapaths[datapath_dst]
            out = self._build_packet_out(datapath, ofproto.OFP_NO_BUFFER,
                                         ofproto.OFPP_CONTROLLER,
                                         out_port, msg.data)
            datapath.send_msg(out)
            self.logger.debug("Reply ARP to knew host")
        else:
            self.flood(msg)

    def get_path(self, src, dst, require_band, weight ):
        """
            Get shortest path from network awareness module.
        """
        shortest_paths = self.awareness.shortest_paths
        # graph = self.awareness.graph
        if weight == self.WEIGHT_MODEL['hop']:
            return shortest_paths.get(src).get(dst)[0]
        elif weight == self.WEIGHT_MODEL['bw']:
            path = shortest_paths[src][dst]
            bw_guarantee_path, reconf_flag = self.monitor.get_bw_guaranteed_path(path, require_band)
            return bw_guarantee_path, reconf_flag

    def get_sw(self, dpid, in_port, src, dst):
        """
            Get pair of source and destination switches.
        """
        src_sw = dpid
        dst_sw = None

        src_location = self.awareness.get_host_location(src)
        if in_port in self.awareness.access_ports[dpid]:
            if (dpid,  in_port) == src_location:
                src_sw = src_location[0]
            else:
                return None

        dst_location = self.awareness.get_host_location(dst)
        if dst_location:
            dst_sw = dst_location[0]

        return src_sw, dst_sw

    def install_flow(self, datapaths, link_to_port, access_table, path,
                     flow_info, buffer_id, data=None, prio=1):
        '''
            Install flow entires for roundtrip: go and back.
            @parameter: path=[dpid1, dpid2...]
                        flow_info=(eth_type, src_ip, dst_ip, in_port)
        '''
        if path is None or len(path) == 0:
            self.logger.info("Path error!")
            return
        in_port = flow_info[3]
        first_dp = datapaths[path[0]]
        # out_port = first_dp.ofproto.OFPP_LOCAL
        back_info = (flow_info[0], flow_info[2], flow_info[1])

        # inter_link
        if len(path) > 2:
            for i in xrange(1, len(path)-1):
                port = self.get_port_pair_from_link(link_to_port,
                                                    path[i-1], path[i])
                port_next = self.get_port_pair_from_link(link_to_port,
                                                         path[i], path[i+1])
                if port and port_next:
                    src_port, dst_port = port[1], port_next[0]
                    datapath = datapaths[path[i]]
                    self.send_flow_mod(datapath, flow_info, src_port, dst_port, prio)
                    self.send_flow_mod(datapath, back_info, dst_port, src_port, prio)
                    self.logger.debug("inter_link flow install")
        if len(path) > 1:
            # the last flow entry: tor -> host
            port_pair = self.get_port_pair_from_link(link_to_port,
                                                     path[-2], path[-1])
            if port_pair is None:
                self.logger.info("Port is not found")
                return
            src_port = port_pair[1]

            dst_port = self.get_port(flow_info[2], access_table)
            if dst_port is None:
                self.logger.info("Last port is not found.")
                return

            last_dp = datapaths[path[-1]]
            self.send_flow_mod(last_dp, flow_info, src_port, dst_port, prio)
            self.send_flow_mod(last_dp, back_info, dst_port, src_port, prio)

            # the first flow entry
            port_pair = self.get_port_pair_from_link(link_to_port,
                                                     path[0], path[1])
            if port_pair is None:
                self.logger.info("Port not found in first hop.")
                return
            out_port = port_pair[0]
            self.send_flow_mod(first_dp, flow_info, in_port, out_port, prio)
            self.send_flow_mod(first_dp, back_info, out_port, in_port, prio)
            if prio == 1:
                self.send_packet_out(first_dp, buffer_id, in_port, out_port, data)

        # src and dst on the same datapath
        else:
            out_port = self.get_port(flow_info[2], access_table)
            if out_port is None:
                self.logger.info("Out_port is None in same dp")
                return
            self.send_flow_mod(first_dp, flow_info, in_port, out_port, prio)
            self.send_flow_mod(first_dp, back_info, out_port, in_port, prio)
            if prio == 1:
                self.send_packet_out(first_dp, buffer_id, in_port, out_port, data)

    def shortest_forwarding(self, msg, eth_type, ip_src, ip_dst, require_band):
        """
            To calculate shortest forwarding path and install them into datapaths.

        """
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        result = self.get_sw(datapath.id, in_port, ip_src, ip_dst)
        if result:
            src_sw, dst_sw = result[0], result[1]
            if dst_sw:
                # self.logger.info("src %s dst %s " % (src_sw, dst_sw))
                path, self.config_flag = self.get_path(src_sw, dst_sw, require_band, weight=self.weight)
                self.logger.info("[PATH]%s<-->%s: %s" % (ip_src, ip_dst, path))
                flow_info = (eth_type, ip_src, ip_dst, in_port)
                # install flow entries to datapath along side the path.
                self.install_flow(self.datapaths,
                                  self.awareness.link_to_port,
                                  self.awareness.access_table, path,
                                  flow_info, msg.buffer_id, msg.data, 1)

        self._ilp_process()
        return

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        '''
            In packet_in handler, we need to learn access_table by ARP.
            Therefore, the first packet from UNKOWN host MUST be ARP.
        '''
        msg = ev.msg
        datapath = msg.datapath
        # in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        arp_pkt = pkt.get_protocol(arp.arp)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)

        if isinstance(arp_pkt, arp.arp):
            self.logger.debug("ARP processing")
            self.arp_forwarding(msg, arp_pkt.src_ip, arp_pkt.dst_ip)

        if isinstance(ip_pkt, ipv4.ipv4):
            self.logger.debug("IPV4 processing")
            if len(pkt.get_protocols(ethernet.ethernet)):
                require_band = setting.require_band[ip_pkt.src]
                eth_type = pkt.get_protocols(ethernet.ethernet)[0].ethertype
                self.ilp_data_handle(ip_pkt, eth_type, datapath.id, require_band)
                self.shortest_forwarding(msg, eth_type, ip_pkt.src, ip_pkt.dst, require_band)

    @set_ev_cls(ofp_event.EventOFPFlowRemoved, MAIN_DISPATCHER)
    def _flow_removed_handler(self, ev):
        '''
            In flow removed handler, get the ip address and unregister in
            the dict for require and priority.
        '''
        self.logger.info("flow removed handler")
        # msg = ev.msg
        # dp = msg.datapath
        # ofp = dp.ofproto
        # if msg.reason == ofp.OFPRR_IDLE_TIMEOUT or msg.reason == ofp.OFPRR_HARD_TIMEOUT:
        #     flow_dst = msg.match.get('ipv4_dst')
        #     flow_inport = msg.match.get('in_port')
        #     flow_ip = self.map[(flow_dst, flow_inport)]
        #     if flow_ip in self.require.keys():
        #         del self.require[flow_ip]
        #         del self.priority[flow_ip]

    def reconfigration(self):
        '''
           handle the network re-configration. calling the ilp module
        '''

        # nodes, edges, r, p, flow, capacity, src_dst
        switch = self.awareness.switches
        edges = self.awareness.edges
        capacity = setting.link_capacity
        src_dst, flow = [], []
        require, priority = [], []
        # (eth_type, ip_pkt.src, ip_pkt.dst, in_port)-->
        # [require_band,priority,(src_dp,dst_dp)]
        for key, value in self.flow.items():
            flow.append(key)
            require.append(value[0])
            priority.append(value[1])
            src_dst.append(value[2])

        self.logger.info('not enough bandwidth ILP enter')
        self.logger.info("flow info: %s" % flow)
        self.logger.info("require info: %s" % require)
        self.logger.info("priority info: %s" % priority)
        self.logger.info("src_dst info: %s" % src_dst)
        self.logger.info("switch info: %s" % switch)
        self.logger.info("edge info: %s" % edges)
        self.logger.info("capacity info: %s" % capacity)

        flow_num = range(len(flow))
        assert len(flow) == len(src_dst)
        path, max_priority = milp_constrains(switch, edges, require, priority,
                               flow_num, capacity, src_dst)
        return path, flow, max_priority

    def ilp_data_handle(self, ip_pkt, eth_type, datapath_id, require_band):
        '''
           generating the data for ilp module
        '''
        # avoid reverse path packet-in packet to controller
        if (ip_pkt.dst, ip_pkt.src) not in self.flow_ip:
            if (ip_pkt.src, ip_pkt.dst) not in self.flow_ip:
                in_port = self.get_port(ip_pkt.src, self.awareness.access_table)
                self.logger.debug("ip_src: %s,ip_dst: %s,in_port: %s" % (ip_pkt.src, ip_pkt.dst, in_port))
                self.logger.debug("count:%s" % self.count)
                self.handle_flag = 1   # this is new flow, can handle with ilp module

                result = self.get_sw(datapath_id, in_port, ip_pkt.src, ip_pkt.dst)
                flow_info = []
                flow_info.append(require_band)
                flow_info.append(setting.priority_weight[ip_pkt.src])
                flow_info.append((result[0], result[1]))
                # (eth_type, ip_pkt.src, ip_pkt.dst, in_port)--> [require_band,priority,(src_dp,dst_dp)]
                self.flow[(eth_type, ip_pkt.src, ip_pkt.dst, in_port)] = flow_info
                self.flow_ip.append((ip_pkt.src, ip_pkt.dst))

                self.map[(ip_pkt.dst, in_port)] = ip_pkt.src
                self.count += 1  # flow identification
                # assert self.count < 10

