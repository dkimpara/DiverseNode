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


def sim_one_iter(g, culturemat, ccomp):
    # determine random sequence of individuals
    nodeList = list(g.nodes)
    random.shuffle(nodeList)

    for u in nodeList:
        # pick interaction randomly
        v, g, ccomp = pick_interaction(u, g, ccomp)  # use connected component class

        # carry out interaction
        prob_accept = p_accept(culturemat[u], culturemat[v])

        if random.random() < prob_accept:
            # accept culture
            # check if edge exists
            # add node?
            pass
        else:
            # reject culture
            # check for node to remove
            pass

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


def p_accept(culture_u, culture_v, norm_p=2):
    prob = 1
    d = culture_u[-2]
    dist = linalg.norm(culture_u - culture_v, norm_p)
    return 0.5 ** (dist / d)
