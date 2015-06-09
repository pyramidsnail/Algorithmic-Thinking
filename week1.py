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


# if __name__ == '__main__':
    # test = {0:[1,2],1:[2,3]}
    # res1 = compute_in_degrees(test)
    # res2 = in_degree_distribution(test)
    # res3 = make_complete_graph(3)
    # print 
        
    
            
    
        
