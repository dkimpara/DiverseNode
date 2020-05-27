## generate graphs

import networkx as nx
from networkx.generators.community import stochastic_block_model
import numpy as np

def graph_gen(num_groups, num_nodes, intra_edge_density, extra_edge_density):
    """num_groups is number of nodes in each group
    num_nodes uses SBM as graph generator"""
    sizes = [int(num_nodes/num_groups)] * 2
    p = generate_density_matrix(intra_edge_density, extra_edge_density)
    
    g = stochastic_block_model(sizes, p, directed=True, selfloops=False)
    return g

def culture_init(g, distance, std_dev):
    
    return g

def edge_weight_init(g, distribution='uniform'):
    
    return g


# noinspection PyStatementEffect
def generate_density_matrix(intra_edge_density, extra_edge_density):
    assert isinstance(intra_edge_density, float)
    assert isinstance(extra_edge_density, float)
    intra = intra_edge_density
    out = extra_edge_density
    return [[intra, out],[out, intra]]

        