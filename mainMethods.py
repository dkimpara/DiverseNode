# helper functions for running sayama et all experiments
import os
import pickle as pk
from functools import partial
from itertools import repeat
from multiprocessing import Pool
from typing import List
from pathlib import Path
from sklearn.model_selection import ParameterGrid

import networkx as nx
import numpy as np
import pandas as pd

import generator as gen
import simulate


def experiment_collect_store(g_func, grid, change_all, change_vec, experiment_name, norm=2, trials=100):
    """
    :type grid: iterable
    """
    create_dir(experiment_name)

    data = List[tuple]
    for params in grid:
        #modify for non-symmetric cultures_change
        #todo fix this constant, optimize this section?
        dev = [0.1, params['std_d'], params['std_rs'], params['std_rw']]
        std_devs = [dev, dev]
        input_data = (g_func, std_devs, change_vec, change_all, norm)
        data_per_iter: List[tuple] = []
        with Pool(processes=os.cpu_count() - 1) as pool:
            process = pool.map_async(run_and_analyze, repeat(input_data, trials))
            data_per_iter = process.get() # run iters, async
            #  data is a list of tuples, one tuple g,culturemat, dataDict for each run

        # non parallel code:
        #data_per_iter = list(map(run_one_sim, repeat(std_devs, trials)))

        graphs: nx.DiGraph
        graphs, cultures, iter_dicts = zip(*data_per_iter)  # unzip tuples
        # save graphs for each parameter setting (100 trials)
        assert isinstance(graphs, nx.DiGraph)
        store_graphs_cultures(list(graphs), list(cultures), std_devs, change_vec,
                              experiment_name, str(dev))
        data += list(iter_dicts)  # append list of data from each sim to the main data list
    write_dataframe(data, trials, experiment_name)

# todo: need to extract culture dat
def run_and_analyze(input_data):
    '''simulate and collect data
    input_data = (std_devs, change_vec, change_all)'''
    #unpack input tuple
    g_func, std_devs, change_vec, change_all, norm = input_data

    g = g_func()
    cmat, c1, c2 = gen.culture_init(g, std_devs, change_vec)
    g, culturemat = run_sayama_sim(g, cmat, change_all, norm)

    # analyze run
    dataDict = analyze(g, culturemat, change_all, norm)
    dataDict['c1_init'] = c1
    dataDict['c2_init'] = c2
    dataDict['c_avg_init'] = analyze_c_init(c1, c2)
    s_devs = std_devs[0]
    dataDict['std_d'] = s_devs[1]
    dataDict['std_rs'] = s_devs[2]
    dataDict['std_rw'] = s_devs[3]  # no need to store anything else cuz sayama base sim

    return g, culturemat, dataDict




def run_sayama_sim(g, cmat, change_all):
    '''simulate an instance'''
    # simulate
    g, culturemat = simulate.simulate_iterstop(g, cmat, change_all)

    return g, culturemat

#helper for run_and_analyze
def culture_analyze(data_dict, g, culturemat, norm):
    #need to add to datadict culture centers + overall center + average of two cultures
    pass


def analyze(g, culturemat, culture_change_all, norm=2):  # for analysis of sayama sim
    g_undir = nx.DiGraph.to_undirected(g)
    data_dict = {'degrees': sorted([d for n, d in g.degree()], reverse=True),
                 'clusterCoeff': nx.average_clustering(g),
                 'reciprocity': nx.reciprocity(g)}
    data_dict = culture_analyze(data_dict, g, culturemat, norm)
    giant = max(nx.connected_components(g_undir), key=len)
    data_dict['giantComponent'] = len(giant) / len(g.nodes())
    # analyze cultures

    try:
        data_dict['diam'] = nx.diameter(g_undir) #goto except if g_undir unconnected
        #g connected:
        data_dict['SPL'] = nx.average_shortest_path_length(g) #goes to except if g not weakly connected
    except nx.NetworkXError: #graph not strongly connected, throw away trial
        num_connected_components = len(list(nx.connected_components(g_undir)))

        d = nx.diameter(g_undir.subgraph(giant))
        data_dict['diam'] = (d, num_connected_components)
        #  analyze biggest component
        spl = nx.average_shortest_path_length(g.subgraph(giant))
        data_dict['SPL'] = (spl, num_connected_components)

    data_dict['CD'] = culture_distance(g, culturemat, culture_change_all, norm)
    return data_dict

#helper for analyze func
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

def analyze_c_init(c1, c2):
    return 0.5 * c1 + 0.5 * c2

def store_graphs_cultures(graphs: list, cultures: list,
                          std_devs: list, change_vec: list, subdir: str,
                          filename: str) -> None:  # pickle a bunch of graphs and cultures
    data_dict = {'graphs': graphs, 'cultures': cultures,
                'change1': change_vec[0], 'change2': change_vec[1],
                'std1': std_devs[0], 'std2': std_devs[1]}

    # now pickle
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

    # path for file
    rel_path = "tests/" + subdir + '/' + filename
    abs_file_path = os.path.join(script_dir, rel_path)

    f = open(abs_file_path, 'wb')
    pk.dump(data_dict, f)
    f.close()

def write_dataframe(data, trials, experiment_name):
    df = pd.DataFrame(data)  # empty dicts will be stored as NaNs
    tags = list(range(trials)) * (len(data) // trials)
    df['tags'] = tags

    df.name = experiment_name
    df.to_pickle('./tests/df_' + df.name)

    '''to unpickle:
    df =pd.read_pickle("./dummy.pkl")
    '''

def create_dir(subdir):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "tests/" + subdir
    abs_dir_path = os.path.join(script_dir, rel_path)
    # safely make dir
    Path(abs_dir_path).mkdir(parents=True, exist_ok=True)