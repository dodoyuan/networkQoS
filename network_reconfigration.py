#! /usr/bin/env python
# --*--coding:utf-8--*--

# Copyright (C) 2017 Yuan qijie at Beijing University of Posts
# and Telecommunications.
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

# import setting
import pulp
from collections import defaultdict
import time

def exeTime(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)
        back = func(*args, **args2)
        print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)
        print "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__)
        return back
    return newFunc


def neighbor_head(node, edges):
    # return all the linked neighbors of node node
    linked_edges = []
    for e in edges:
        if node == e[1]:
            linked_edges.append(e)
    return linked_edges


def neighbor_tail(node, edges):
    # return all the linked neighbors of node node
    linked_edges = []
    for e in edges:
        if node == e[0]:
            linked_edges.append(e)
    return linked_edges

# @exeTime
def milp_constrains(nodes, edges, r, p, flow, capacity, src_dst):
    s, d = gene_matrix(nodes, src_dst)
    model = pulp.LpProblem("suitable path for higher priority", pulp.LpMaximize)
    y = pulp.LpVariable.dicts("handle this flow or not", flow, 0, 1, cat='Binary')
    u = pulp.LpVariable.dicts("selected path of flow", [(f, edge) for f in flow for edge in edges], 0, 1, cat='Binary')

    # objective function
    model += pulp.lpSum(p[i] * y[i] for i in flow), "shortest path with suitable controllers placement"

    # flow constrain
    for n in flow:      # traverse every node
        for m in nodes:  # arbitrarily intermediate node
            model += pulp.lpSum(u[(n, edge)] for edge in neighbor_head(m, edges)) - \
                     pulp.lpSum(u[(n, edge)] for edge in neighbor_tail(m, edges)) == (d[n][m] - s[n][m]) * y[n]
            # model += pulp.lpSum(u[(n, edge)] for edge in neighbor_head(m)) + \
            #          pulp.lpSum(u[(n, edge)] for edge in neighbor_tail(m)) <= 1

    for edge in edges:
        model += pulp.lpSum(r[n] * u[(n, edge)] for n in flow) <= capacity

    for n in flow:
        for edge in edges:
            model += u[(n, edge)] <= y[n]

    model.solve()
    status = pulp.LpStatus[model.status]
    print status

    max_priority = pulp.value(model.objective)
    # print "the max priority is {}".format(max_priority)

    path = defaultdict(dict)
    for v in model.variables():
        if v.varValue:
            # print v.name, '=', v.varValue
            # selected_path_of_flow_(1,_(1,_5))
            if 'path' in v.name:
                temp = v.name.split('_')
                flow_number = int(temp[4][-2])
                link_src, link_dst = int(temp[5][-2]), int(temp[6][-3])
                path[flow_number][link_src] = link_dst
    # print path
    #  {1: {1: 5, 5: 6, 6: 7, 7: 8}, 2: {1: 2, 2: 3, 3: 4, 4: 8}}
    path = path_extr(src_dst, path)
    return path


def path_extr(src_dst,path):
    '''
       {1: {1: 5, 5: 6, 6: 7, 7: 8}, 2: {1: 2, 2: 3, 3: 4, 4: 8}} --> {1:[1,5,6,7,8]}
    '''
    path_changed = defaultdict(list)
    for flow in path.keys():
        src, dst = src_dst[flow][0], src_dst[flow][1]
        current = src
        while current != dst:
            path_changed[flow].append(current)
            current = path[flow][current]
        path_changed[flow].append(dst)
    return path_changed


def gene_matrix(nodes, src_dst):
    source_matrix = defaultdict(lambda: [0 for _ in range(len(nodes) + 1)])
    des_matrix = defaultdict(lambda: [0 for _ in range(len(nodes) + 1)])
    for key, value in src_dst.items():
        source_matrix[key][value[0]] = 1
        des_matrix[key][value[1]] = 1
    return source_matrix, des_matrix

if __name__ == '__main__':

    print 'hope god help '
    # predefined data
    nodes = [1, 2, 3, 4, 5, 6, 7, 8]
    edges = [(1, 2), (2, 3), (3, 4), (4, 8), (1, 5), (5, 4), (5, 6), (6, 7), (7, 8),
             (2, 1), (3, 2), (4, 3), (8, 4), (5, 1), (4, 5), (6, 5), (7, 6), (8, 7)]
    r = [0, 5, 5, 2]

    p = [0, 4, 2, 1]
    flow = [1, 2, 3]
    capacity = 5
    src_dst = {1: (1, 8), 2: (1, 8), 3: (6, 7)}
    milp_constrains(nodes, edges, r, p, flow, capacity, src_dst)