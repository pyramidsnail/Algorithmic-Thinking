'''
code for the project of WEEK2
'''
import sys, os, re
import urllib2
import random
import time
import math
import matplotlib.pyplot as plt
import random


def make_complete_graph(num_nodes):
    """
    returns a dictionary corresponding to a complete directed graph
    with the specified number of nodes
    """
    complete_graph = {}
    if num_nodes<1:
        return complete_graph
    else:
        complete_graph = dict((x,[]) for x in xrange(num_nodes))
        for out_node in xrange(num_nodes):
            for in_node in xrange(num_nodes):
                if out_node!=in_node:
                    complete_graph[out_node].append(in_node)

        for key in complete_graph:
            complete_graph[key] = set(complete_graph[key])
    return complete_graph

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            if neighbor in new_graph and max_degree_node in new_graph[neighbor]:
                new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


def fast_targeted_order(ugraph):
    new_graph = copy_graph(ugraph)
    
    degreeSets = dict((x,[]) for x in range(len(new_graph)))
    for i in new_graph:
        degreeSets[len(new_graph[i])].append(i)
    res = []
    for k in range(len(ugraph)-1, -1, -1):
        while degreeSets[k] is not None and len(degreeSets[k])>0:
            u = degreeSets[k][0]
            degreeSets[k].remove(u)
            for node in ugraph[u]:
                d = len(ugraph[node])
                if degreeSets[d] is not None and degreeSets[d-1] is not None and node in degreeSets[d] and node in degreeSets[d-1]:
                    degreeSets[d] = degreeSets[d].remove(node)
                    degreeSets[d-1] = degreeSets[d-1].append(node)
            res.append(u)
            new_graph.pop(u, None)
            # for key in new_graph:
            #     if u in new_graph[key]:
            #         new_graph[key].remove(u)

    return res
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def bfs_visited(graph, start_node):
    '''
    Takes the undirected graph ugraph and the node start_node
    returns the set consisting of all nodes that are visited by a
    breadth-first search that starts at start_node.
    '''
    queue = []
    visited = [start_node]
    queue.append(start_node)
    while queue:
        node = queue.pop(0)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
    return set(visited)


def cc_visited(graph):
    '''
    Takes the undirected graph ugraph and returns a list of sets
    each set consists of all the nodes in a connected component
    '''
    remain = graph.keys()
    cc_set = []
    while remain:
        node = list(remain)[0]
        component = bfs_visited(graph, node)
        cc_set.append(component)
        remain = set(remain).difference(component)

    return cc_set

def largest_cc_size(graph):
    '''
    returns the size of the largest connected component in graph
    '''
    cc_set = cc_visited(graph)
    num = 0
    for item in cc_set:
        if len(item)>num:
            num = len(item)
    return num

def compute_resilience(graph, attack_order):
    '''
    study the connectivity of computer networks
    '''
    
    resilience = [largest_cc_size(graph)]
    for ith in attack_order:
        node = ith
        graph.pop(node, None)
        for key in graph:
            if node in graph[key]:
                graph[key].remove(node)

        resilience.append(largest_cc_size(graph))
        print len(graph)

    return resilience
        


def make_ER_graph(num_nodes, p):
    """
    returns a dictionary corresponding to a complete directed graph
    with the specified number of nodes
    """
    ER_graph = {}
    if num_nodes<1:
        return ER_graph
    else:
        ER_graph = dict((x,[]) for x in xrange(num_nodes))
        for out_node in xrange(num_nodes):
            for in_node in xrange(num_nodes):
                if out_node!=in_node and random.uniform(0,1)<p:
                    ER_graph[out_node].append(in_node)
                    ER_graph[in_node].append(out_node)

        for key in ER_graph:
            ER_graph[key] = set(ER_graph[key])
    return ER_graph



if __name__ == '__main__':
    # f = open('resilience', 'w')
    answer_graph = load_graph(NETWORK_URL)
    er_graph = make_ER_graph(1239, 0.002)

    #####  for the UPA graph
    #####  sum of edges 2476; sum of nodes: 1239
    upa_graph = make_complete_graph(5) 
    upa = UPATrial(5)
    for i in xrange(5, 1239):
        upa_graph[i] = []
        new_node_neighbors = upa.run_trial(5)
        for node in new_node_neighbors:
            list(upa_graph[node]).append(i)
        upa_graph[i].extend(new_node_neighbors)

    # start = time.time()
    # targeted_order = targeted_order(upa_graph)
    # print time.time()-start
    # start = time.time()
    # fast_targeted_order = fast_targeted_order(upa_graph)
    # print time.time()-start

    # #####  test for the running time of the two algorithms
    # targeted_time = []
    # fast_targeted_time = []
    # for total in range(10, 1000, 10):
    #     upa_graph = make_complete_graph(5) 
    #     upa = UPATrial(5)
    #     for i in xrange(5, total):
    #         upa_graph[i] = []
    #         new_node_neighbors = upa.run_trial(5)
    #         for node in new_node_neighbors:
    #             list(upa_graph[node]).append(i)
    #         upa_graph[i].extend(new_node_neighbors)

    #     start = time.time()
    #     targeted_order_res = targeted_order(upa_graph)
    #     targeted_time.append(time.time()-start)
    #     start = time.time()
    #     fast_targeted_order_res = fast_targeted_order(upa_graph)
    #     fast_targeted_time.append(time.time()-start)
    # ##### plot the time
    # plt.plot(range(10, 1000, 10), targeted_time, label= 'targeted_order',linestyle='-')
    # plt.plot(range(10, 1000, 10), fast_targeted_time, label = 'fast_targeted_order',linestyle='-')
    # plt.xlabel('number of nodes')
    # plt.ylabel('running times')
    # plt.title('running times of choosing targets ( desktop Python )')
    # plt.legend(bbox_to_anchor=(0., 1.05, 1., .102), loc=3,
    #        ncol=2, mode="expand", borderaxespad=0.)
    # plt.show()


    # # for key in upa_graph:
    # #     upa_graph[key] = set(upa_graph[key])

    # # total = 0
    # # for key in upa_graph:
    # #     total += len(upa_graph[key])

    # # er_total = 0
    # # for key in er_graph:
    # #     er_total += len(er_graph[key])


    # # ans_total = 0
    # # for key in answer_graph:
    # #     ans_total += len(answer_graph[key])

    # # keys = random.sample(range(1239), 1239)
    # answer_keys = random.sample(answer_graph.keys(), len(answer_graph))
    # er_keys = random.sample(er_graph.keys(), len(er_graph))
    # # upa_keys = random.sample(upa_graph.keys(), len(upa_graph))

    answer_keys = targeted_order(answer_graph)
    er_keys = targeted_order(er_graph)
    upa_keys = targeted_order(upa_graph)

    answer = compute_resilience(answer_graph, answer_keys)
    # f.write((' '.join(map(str, answer)))+'\n')
    er = compute_resilience(er_graph, er_keys)
    # f.write((' '.join(map(str, er)))+'\n')
    upa = compute_resilience(upa_graph, upa_keys)
    # # f.write((' '.join(map(str, upa)))+'\n')
    # f = open('resilience', 'r')
    # lines = f.readlines()
    # answer = lines[0].strip().split()
    # er = lines[1].strip().split()
    # f = open('upa_resilience', 'r')
    # upa = f.readline().strip().split()

    plt.plot(range(1240), answer, label= 'computer network',linestyle='-')
    plt.plot(range(1240), er, label = 'ER ( p=0.002 )',linestyle='-')
    plt.plot(range(1240), upa, label = 'UPA ( m=5 )',linestyle='-')
    plt.xlabel('number of nodes removed')
    plt.ylabel('size of the largest connect component in the graphs')
    plt.title('resilience plot')
    plt.legend(bbox_to_anchor=(0., 1.05, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)
    plt.show()


        
        
#     GRAPH0 = {0: set([1]),
#               1: set([0, 2]),
#               2: set([1, 3]),
#               3: set([2])}
#     print compute_resilience(GRAPH0, [1,2])
#     cc_visited(graph)

#     graph = {0:[1,3,4],
#              1:[2,3,0],
#              2:[1,4],
#              3:[1,0],
#              4:[0,5],
#              5:[4]}
#     # print bfs_visited(graph, 0)
#     # cc_visited(graph)
