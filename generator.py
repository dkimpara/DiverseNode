## generate graphs

import graph_tool.all
import numpy as np
import itertools
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
from mpl_toolkits import mplot3d
from multiprocessing import Pool, TimeoutError

def graph_gen():
#num_groups, num_nodes, intra_edge_density, extra_edge_density):
    '''num_groups is number of nodes in each group
    num_nodes
        uses SBM as graph generator'''
    g, bm = graph_tool.generation.random_graph(50, poisson(2),
                                    directed=True,
                                    model="blockmodel",
                                    block_membership=membership,
                                    edge_probs=prob)
    graph_tool.graph_draw(g, vertex_fill_color=bm, edge_color="black", output="blockmodel.pdf")
    return g

def culture_init(g, distance, std_dev):
    
    return g

def edge_weight_init(g, distribution='uniform'):
    
    return g

def prob(a,b):
    '''probability function for edge density between groups'''
    if a == b: return 0.2
    else: return 0.02
def membership(a):
    if a < 25: return 0
    else: return 1

        