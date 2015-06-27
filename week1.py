"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2, math
import matplotlib.pyplot as plt
# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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

"""
project for WEEK1
"""
EX_GRAPH0={0:set([1,2]),
           1:set([]),
           2:set([])
    }
EX_GRAPH1={0:set([1,4,5]),
           1:set([2,6]),
           2:set([3]),
           3:set([0]),
           4:set([1]),
           5:set([2]),
           6:set([])
    }
EX_GRAPH2={0:set([1,4,5]),
           1:set([2,6]),
           2:set([3,7]),
           3:set([7]),
           4:set([1]),
           5:set([2]),
           6:set([]),
           7:set([3]),
           8:set([1,2]),
           9:set([0,3,4,5,6,7])
    }
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

def compute_in_degrees(digraph):
    """
    computes the in-degrees for the nodes
    """
    dic = dict((x,0) for x in digraph.keys())
    for out_node in digraph:
        for in_node in digraph[out_node]:
            if not in_node in dic:
                dic[in_node] = 0
            dic[in_node] += 1
    return dic


def in_degree_distribution(digraph):
    """
    computes the unnormalized distribution of the in-degrees
    """
    dic = compute_in_degrees(digraph)
    res = dict((x,0) for x in set(dic.values()))
    for out_node in dic:
        res[dic[out_node]] += 1
    return res

import random


class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    # def update_graph(self):
    
if __name__ == '__main__':
    # test = {0:[1,2],1:[2,3]}
    # res1 = compute_in_degrees(test)
    # res2 = in_degree_distribution(test)
    # res3 = make_complete_graph(3)
    # print 
        
    # citation_graph = load_graph(CITATION_URL)
    # dis = in_degree_distribution(citation_graph)
    # #####  normalization
    # dis_nor = {}
    # total = 0
    # for i in dis:
    #     total += dis[i]

    # for i in dis:
    #     dis_nor[i] = 1.0*dis[i]/total

    # plt.plot([math.log(i  if i>0 else 1, 10) for i in dis_nor.keys()], [math.log(i, 10) for i in dis_nor.values()], 'ro')
    # plt.xlabel('log10 of citation numbers')
    # plt.ylabel('log10 of the normalized in-degree distribution')
    # plt.title('in-degree distribution of citation graph') 
    # plt.show()

    dpa = DPATrial(99)
    for i in xrange(181):
        dpa.run_trial(99)

    dis = dict((i,0) for i in xrange(280))
    for i in dpa._node_numbers:
        dis[i] += 1


    dis_nor = {}
    total = 0
    for i in dis:
        total += dis[i]

    for i in dis:
        dis_nor[i] = 1.0*dis[i]/total

    plt.plot([math.log(i  if i>0 else 1, 10) for i in dis_nor.keys()], [math.log(i, 10) for i in dis_nor.values()], 'ro')
    plt.xlabel('log10 of in-degree numbers')
    plt.ylabel('log10 of the normalized in-degree distribution')
    plt.title('in-degree distribution of DPA') 
    plt.show()

            
    
        



