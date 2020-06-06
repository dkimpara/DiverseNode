# simulate dynamics on graph

# optimize by making g,culturemat,ccomp datastruct?
import random
import networkx as nx
from conComp import Components
from numpy import linalg


def simulate_iterstop(g, culturemat, iter=500):
    '''input graph g with initialized culture state, edge weights,'''
    ccomp = Components(g)
    for i in range(iter):
        g, culturemat, ccomp = sim_one_iter(g, culturemat, ccomp)

    # write adj matrix and culture vec to file
    return g  # for prototyping purposes.

# TODO: test
def sim_one_iter(g, culturemat, ccomp, culture_change_all=False):
    # determine random sequence of individuals
    nodeList = list(g.nodes)
    random.shuffle(nodeList)

    for u in nodeList:
        # pick interaction randomly
        v, g, ccomp = pick_interaction(u, g, ccomp)  # use connected component class

        # carry out interaction
        prob_accept = p_accept(culturemat[u], culturemat[v], culture_change_all)

        if random.random() < prob_accept:
            # accept culture
            culturemat = update_culture(u, v, culturemat, culture_change_all)
            # update edge
            g = increase_edge(u, v, g)
        else:
            # reject culture no update to culturemat
            # check for node to remove
            g, ccomp = decrease_edge(u, v, g, ccomp)

    return g, culturemat, ccomp


# noinspection PyUnreachableCode
def pick_interaction(u, g, ccomp):
    if random.random() < 0.99:
        # interact with random incoming nbrs
        v = random.choice(list(g.predecessors(u)))
    else:  # interact with ccomp random
        v = random.choice(ccomp.find_component(u))

    g, ccomp = check_create_edge(v, u, g, ccomp)
    return v, g, ccomp


def check_create_edge(v, u, g, ccomp):  # create dir edge from v to u
    if (v, u) not in g.edges:
        g.add_edge(v, u)
        g.edges[v, u]['weight'] = 0.01

        # modify connected comp
        ccomp.merge(u, v)
    return g, ccomp

# TODO: test
def p_accept(culture_u, culture_v, culture_change_all, norm_p=2):
    d = culture_u[-2]
    if culture_change_all:  # entire culture vec change
        dist = linalg.norm(culture_u - culture_v, norm_p)
    else:  # only original culture vec change (as in sayama)
        dist = linalg.norm(culture_u[:-2] - culture_v[:-2], norm_p)

    return 0.5 ** (dist / d)

# TODO: test
def update_culture(node, other_node, culturemat, culture_change_all):
    r_s = culturemat[node, -1]  # rate of cultural state change for node u

    if culture_change_all:
        culturemat[node] = (1 - r_s) * culturemat[node] \
                           + r_s * culturemat[other_node]
    else:  # update as in sayama
        culturemat[node, :-2] = (1 - r_s) * culturemat[node, :-2] \
                                + r_s * culturemat[other_node, :-2]
    return culturemat

# TODO: test
def increase_edge(u, v, g):
    """if the received culture is accepted, function to update edge weight"""
    weight_vu = g.edges[v, u]['weight']
    # TODO: extract graph level property r_w rate of edge change

    # TODO: update weight with logistic

    # no need to check for edge removal
    return g

# TODO: test
def decrease_edge(u, v, g, ccomp):
    weight_vu = g.edges[v, u]['weight']
    # TODO: extract graph level property r_w rate of edge change

    # TODO: update weight with logistic

    # check for edge removal and update g and ccomp
    if weight_vu < 0.01:  # remove edge
        g.remove_edge(v, u)
        assert isinstance(ccomp, Components)
        ccomp.split(g)

    return g, ccomp






