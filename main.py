# helper functions for running sayama et all experiments

import generator
import simulate
import networkx as nx
import pickle as pk
import os
import numpy as np
from sklearn.model_selection import ParameterGrid


# use graph tool compatible formats “graphml”, or “gml” or pickle? try
# first
# need to figure out params to extract via nx to save on r/w time
# todo: use multiprocess


def main_sayama():  # for running sayama experiments
    """change_vec = [[d1,r1,w1][d2,r2,w2]] (means of params d, culturechange)
        std_devs = [sd_culture1, sd_tolerance1, sd_culture_change1, sd_w1],[cult2"""
    values = np.linspace(0.0, 0.5, 6)
    param_grid = {'std_d': values, 'std_rs': values, 'std_rw': values}
    grid = ParameterGrid(param_grid)
    for params in grid:
        graphs = []
        cultures = []
        dev = [0.1, params['std_d'], params['std_rs'], params['std_rw']]
        std_devs = [dev, dev]

        for i in range(100):  # 100 iters per param setting

            g, culturemat = run_sayama_sim(std_devs)

            # analyze+extract each run
            dataDict = analyze(g, culturemat, False)  # todo use dataframe for this, store frame?
            # load to dataframe

            graphs.append(g)
            cultures.append(culturemat)

        # save graphs for each parameter setting (100 trials)
        sayamaChangeVec = [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]
        store_graphs_cultures(graphs, cultures, std_devs, sayamaChangeVec,
                              'sayama', str(dev))


def run_sayama_sim(std_devs):
    change_vec = [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]
    g = generator.graph_gen(2, 50, 0.2, 0.02)
    culturemat = generator.culture_init(g, std_devs, change_vec)
    g, culturemat = simulate.simulate_iterstop(g, culturemat)

    return g, culturemat


def analyze(g, culturemat, culture_change_all, norm=2):  # for analysis of sayama sim
    dataDict = {}
    dataDict['diam'] = nx.diameter(g)
    dataDict['degrees'] = sorted([d for n, d in g.degree()], reverse=True)
    dataDict['clusterCoeff'] = nx.average_clustering(g)
    dataDict['reciprocity'] = nx.reciprocity(g)
    giant = max(nx.connected_components(g), key=len)
    dataDict['giantComponent'] = len(giant) / len(g.nodes())

    dataDict['SPL'] = nx.average_shortest_path_length(g)
    dataDict['CD'] = culture_distance(g, culturemat, culture_change_all, norm)

    return dataDict


def culture_distance(g, culturemat, culture_change_all, norm):
    blocks = list(g.nodes(data='block'))
    b1 = [v for v, block in blocks if block == 0]
    b2 = [v for v, block in blocks if block == 1]
    distance = 0.0
    # compute culture distance for every pair b1, b2
    if culture_change_all:
        for u in b1:
            for v in b2:
                distance += np.linalg.norm(culturemat[u] - culturemat[v], norm)
    else:
        for u in b1:
            for v in b2:
                distance += np.linalg.norm(culturemat[u, :-3]
                                   - culturemat[v, :-3], norm)
    return distance / (len(b1) * len(b2))


def store_graphs_cultures(graphs, cultures, std_devs, change_vec, subdir,
                          filename):  # pickle a bunch of graphs and cultures
    dataDict = {'graphs': graphs, 'cultures': cultures,
                'change1': change_vec[0], 'change2': change_vec[1],
                'std1': std_devs[0], 'std2': std_devs[1]}

    # now pickle
    # todo mkdir code

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "tests/" + subdir + '/' + filename
    abs_file_path = os.path.join(script_dir, rel_path)

    f = open(abs_file_path, 'wb')
    pk.dump(dataDict, f)
    f.close()
