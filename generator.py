## graph_gen generates graph and edge weights
## culture_init generates the culture matrix

import networkx as nx
from networkx.generators.community import stochastic_block_model
import numpy as np
from numpy import random, linalg


def graph_gen(num_groups, num_nodes, intra_edge_density, extra_edge_density):
    """num_groups is number of nodes in each group
    num_nodes uses SBM as graph generator
    initializes graph and edge weights"""

    sizes = [int(num_nodes / num_groups)] * 2
    p = generate_density_matrix(intra_edge_density, extra_edge_density)

    g = stochastic_block_model(sizes, p, directed=True, selfloops=False)
    g = edge_weight_init(g)
    return g


def culture_init(g, std_devs, change_vec, dim=10, distance=3.0, norm_p=2):
    """change_vec = [[d1,r1,w1][d2,r2,w2]]
        std_devs = [sd_culture1, sd_tolerance1, sd_culture_change1, sd w1],[cult2"""
    culture1 = random.rand(dim)
    culture2 = culture1 + random_perturb_culture(dim, change_vec, distance)

    culture1 = np.append(culture1, change_vec[0])
    culture2 = np.append(culture2, change_vec[1])
    # vec is dim+3

    # now init cultures for each node as entries in a n x dim+3 matrix
    culturemat = np.empty([g.number_of_nodes(), dim + 3])

    for v, b in g.nodes(data='block'):  # iterate thru vtx, group pairs
        if b == 0:
            culturemat[v] = generate_node_culture(culture1, std_devs[0])
        elif b == 1:
            culturemat[v] = generate_node_culture(culture2, std_devs[1])

    return culturemat


#  todo edit distribution
def generate_node_culture(culture_center, distribution, std_devs):
    """generate culture for a node given its culture center vec"""
    # dimension of culture features
    dim = len(culture_center) - 3
    # generates std devs for entire culture vec (dim*culture) + tol,change
    noise = random.normal(0, dim * [std_devs[0]] + std_devs[1:])

    # np matrices are all same dtype
    return culture_center + noise


def random_perturb_culture(ndim, change_vec, distance, norm_p=2):
    """generate random vector with norm of distance keeping change_vec
    components constant (last two indices)"""

    vec = sample_n_sphere_surface(ndim, norm_p)

    diff1 = abs(change_vec[0][0] - change_vec[1][0])
    diff2 = abs(change_vec[0][1] - change_vec[1][1])
    diff3 = abs(change_vec[0][2] - change_vec[1][2])
    vec *= np.power(distance ** norm_p
                    - diff1 ** norm_p
                    - diff2 ** norm_p
                    - diff3 ** norm_p,
                    1.0 / norm_p)
    return vec


def sample_n_sphere_surface(ndim, norm_p=2):
    """sample random vector from S^n-1 with norm_p"""

    vec = random.randn(ndim)  # random ve ctor to put distance between cultures
    vec = vec / linalg.norm(vec, norm_p)  # create random vector with norm 1
    return vec


def edge_weight_init(g, distribution='uniform'):
    for u, v, d in g.edges(data=True):
        d['weight'] = random.uniform(0.1)
    return g


# noinspection PyStatementEffect
def generate_density_matrix(intra_edge_density, extra_edge_density):
    assert isinstance(intra_edge_density, float)
    assert isinstance(extra_edge_density, float)
    intra = intra_edge_density
    out = extra_edge_density
    return [[intra, out], [out, intra]]
