## generate graphs

import networkx as nx
from networkx.generators.community import stochastic_block_model
import numpy as np
from numpy import random, linalg

def graph_gen(num_groups, num_nodes, intra_edge_density, extra_edge_density):
    """num_groups is number of nodes in each group
    num_nodes uses SBM as graph generator"""
    sizes = [int(num_nodes/num_groups)] * 2
    p = generate_density_matrix(intra_edge_density, extra_edge_density)
    
    g = stochastic_block_model(sizes, p, directed=True, selfloops=False)
    return g

def culture_init(g, std_dev, change_vec, dim=10, distance=3.0):
    """change_vec = [[d1,r1][d2,r2]]"""
    culture1 = random.rand(dim)
    culture2 = culture1 + sample_n_sphere_surface(dim, change_vec, distance)

    culture1 = np.append(culture1, change_vec[0])
    culture2 = np.append(culture2, change_vec[1])

    #now init cultures for each node

    print(linalg.norm(culture2-culture1, 2)) #check norm worked
    return g

def random_perturb_culture(ndim, change_vec, distance, norm_p=2):
    """generate random vector with norm of distance keeping change_vec
    components constant (last two indices)"""

    vec = sample_n_sphere_surface(ndim, norm_p)

    diff1 = abs(change_vec[0, 0]-change_vec[0, 1])
    diff2 = abs(change_vec[1, 0]-change_vec[1, 1])
    vec *= np.power(distance ** norm_p - diff1 ** norm_p - diff2 ** norm_p,
                    1.0/norm_p)
    return vec

def sample_n_sphere_surface(ndim, norm_p=2):
    """sample random vector from S^n-1 with norm_p"""

    vec = random.randn(ndim) #random vector to put distance between cultures
    vec = vec / linalg.norm(vec, norm_p) #create random vector with norm 1
    return vec

def edge_weight_init(g, distribution='uniform'):
    for edge in g.edges():
        edges[edge]['weight'] = random.uniform(0.1)
    return g

# noinspection PyStatementEffect
def generate_density_matrix(intra_edge_density, extra_edge_density):
    assert isinstance(intra_edge_density, float)
    assert isinstance(extra_edge_density, float)
    intra = intra_edge_density
    out = extra_edge_density
    return [[intra, out], [out, intra]]

        