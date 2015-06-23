'''
code for the project of WEEK2
'''
# import sys, os, re

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

    return resilience
        





# if __name__ == '__main__':
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
