# helper functions for running sayama et all experiments
from typing import Dict, List, Any, Union

import generator
import simulate
import networkx as nx
import pickle as pk
import os
import numpy as np
import pandas as pd
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
    data = []
    for params in grid:
        graphs = []
        cultures = []
        dev = [0.1, params['std_d'], params['std_rs'], params['std_rw']]
        std_devs = [dev, dev]

        for i in range(100):  # 100 iters per param setting

            g, culturemat = run_sayama_sim(std_devs)
            graphs.append(g)
            cultures.append(culturemat)

            # analyze+extract each run
            dataDict = analyze(g, culturemat, False)
            dataDict['std_d'] = params['std_d']
            dataDict['std_rs'] = params['std_rs']
            dataDict['std_rw'] = params['std_rw'] #no need to store anything else cuz sayama base sim

            data.append(dataDict) #add to list of dicts to be turned into dataframe


        # save graphs for each parameter setting (100 trials)
        sayamaChangeVec = [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]
        store_graphs_cultures(graphs, cultures, std_devs, sayamaChangeVec,
                              'sayama', str(dev))
    df = pd.DataFrame(data)
    df.name = 'Sayama'
    df.to_pickle("./tests/df_" + df.name)

    '''to unpickle:
    df =pd.read_pickle("./dummy.pkl")
    '''

def run_sayama_sim(std_devs):
    #generate
    change_vec = [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]
    g = generator.graph_gen(2, 50, 0.2, 0.02)
    culturemat = generator.culture_init(g, std_devs, change_vec)

    #simulate
    g, culturemat = simulate.simulate_iterstop(g, culturemat)

    return g, culturemat


def analyze(g, culturemat, culture_change_all, norm=2):  # for analysis of sayama sim
    data_dict = {'diam': nx.diameter(g),
                 'degrees': sorted([d for n, d in g.degree()], reverse=True),
                 'clusterCoeff': nx.average_clustering(g),
                 'reciprocity': nx.reciprocity(g)}
    giant = max(nx.connected_components(g), key=len)
    data_dict['giantComponent'] = len(giant) / len(g.nodes())

    data_dict['SPL'] = nx.average_shortest_path_length(g)
    data_dict['CD'] = culture_distance(g, culturemat, culture_change_all, norm)

    return data_dict


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


def store_graphs_cultures(graphs: nx.DiGraph, cultures: np.ndarray,
                          std_devs: list, change_vec: list, subdir: str,
                          filename: str) -> None:  # pickle a bunch of graphs and cultures
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
