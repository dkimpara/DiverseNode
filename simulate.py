# simulate dynamics on graph

# optimize by making g,culturemat,ccomp datastruct?
import random
import networkx as nx
from conComp import Components
from numpy import linalg
import math


def simulate_iterstop(g, culturemat, culture_change_all=False, iterstop=500):
    """input graph g with initialized culture state, edge weights,"""
    ccomp = Components(g)
    for i in range(iterstop):
        g, culturemat, ccomp = sim_one_iter(g, culturemat, ccomp, culture_change_all)

    # write adj matrix and culture vec to file
    return g, culturemat


# TODO: test
def sim_one_iter(g, culturemat, ccomp, culture_change_all):
    # determine random sequence of individuals
    nodeList = list(g.nodes)
    random.shuffle(nodeList)

    for u in nodeList:
        # pick interaction randomly
        v, g, ccomp = pick_interaction(u, g, ccomp)  # use connected component class

        # carry out interaction
        prob_accept = p_accept(culturemat[u], culturemat[v], culture_change_all)

        r_w = culturemat[u, -1]  # edge rate change for receiving node
        if random.random() < prob_accept:
            # accept culture
            culturemat = update_culture(u, v, culturemat, culture_change_all)
            # update edge
            g = increase_edge(u, v, g, r_w)
        else:
            # reject culture no update to culturemat
            # update edge and check for edge to remove
            g, ccomp = decrease_edge(u, v, g, ccomp, r_w)

    return g, culturemat, ccomp


#  edge case handling
def pick_interaction(u, g, ccomp):
    try:
        if random.random() < 0.99:
            # interact with random incoming nbrs
            v = random.choice(list(g.predecessors(u)))
        else:  # interact with ccomp random
            v = random.choice(list(ccomp.find_component(u)))
    except:
        try:  # if no predecessors
            v = random.choice(list(ccomp.find_component(u)))
        except:  # if disconnected?
            nodes = list(g.nodes())
            v = random.choice(nodes.remove(u))

    g, ccomp = check_create_edge(u, v, g, ccomp)
    return v, g, ccomp


def check_create_edge(u, v, g, ccomp):  # create dir edge from v to u
    if (v, u) not in g.edges:
        g.add_edge(v, u)
        g.edges[v, u]['weight'] = 0.01
    ccomp.merge(u, v)  # merge components if any part of graph disconnected
    return g, ccomp


def p_accept(culture_u, culture_v, culture_change_all, norm_p=2):
    d = culture_u[-3]
    if culture_change_all:  # entire culture vec change
        dist = linalg.norm(culture_u - culture_v, norm_p)
    else:  # only original culture vec change (as in sayama)
        dist = linalg.norm(culture_u[:-3] - culture_v[:-3], norm_p)
    z = dist / d
    return 0.5 ** z


def update_culture(node, other_node, culturemat, culture_change_all):
    r_s = culturemat[node, -2]  # rate of cultural state change for node u

    if culture_change_all:  # update entire culturemat row
        culturemat[node] = (1 - r_s) * culturemat[node] \
                           + r_s * culturemat[other_node]
    else:  # update as in sayama
        culturemat[node, :-3] = (1 - r_s) * culturemat[node, :-3] \
                                + r_s * culturemat[other_node, :-3]
    return culturemat


def increase_edge(u, v, g, r_w):
    """if the received culture is accepted, function to update edge weight"""
    weight_vu = g.edges[v, u]['weight']
    # update weight
    g.edges[v, u]['weight'] = sigmoid(logit(weight_vu) + r_w)
    # no need to check for edge removal
    return g


def decrease_edge(u, v, g, ccomp, r_w):
    weight_vu = g.edges[v, u]['weight']

    # update weight
    weight_vu = sigmoid(logit(weight_vu) - r_w)

    # check for edge removal and update g and ccomp
    if weight_vu < 0.01:  # remove edge
        g.remove_edge(v, u)
        assert isinstance(ccomp, Components)
        ccomp.split(g)
    else:
        g.edges[v, u]['weight'] = weight_vu

    return g, ccomp

#todo zero division errors messing up edge weights?
def logit(x):
    try:
        odds = x / (1 - x)
        return math.log(odds)

    except ZeroDivisionError:
        return 1000.0


def sigmoid(x):
    return 1 / (1 + math.exp(-x))
