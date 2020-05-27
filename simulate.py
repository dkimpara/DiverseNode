#simulate dynamics on graph


def simulate_iterstop(g, iter=500):
    '''input graph g with initialized culture state, edge weights,'''

    for i in range(iter):
        g = sim_one_iter(g)

    #write adj matrix and culture vec to file
    return g #for prototyping purposes.

def sim_one_iter(g):

    return g