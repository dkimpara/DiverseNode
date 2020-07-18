import networkx as nx
import mainMethods as mmeth
import pandas as pd
import os
import json

from analysis import read_pickle, data_cleanup


def modify_main(experiment_name):
    dataframename = 'df_' + experiment_name
    df = read_pickle(dataframename)

    df = data_cleanup(df) #split tuples in cols SPL/diam

def read_analyze_folder(experiment_name):
    abs_folder_path = get_exp_path(experiment_name)
    for filename in os.listdir(abs_folder_path):
        with open(os.path.join(abs_folder_path, filename), 'r') as f: 
            data_dict = pk.load(f)
            
def data_dict_processing(data: dict):
    sdevs = data['std1'] #sd 0.1, sd d, rs, rw
    
            
def analyze_g(g):
    g_undir = nx.DiGraph.to_undirected(g)
    try:
        d = nx.diameter(g_undir)
        spl = nx.average_shortest_path_length(g_undir)
    except nx.NetworkXError:
        giant_nodes = max(nx.connected_components(g_undir), key=len)
        gc = g_undir.subgraph(giant_nodes)
        d = nx.diameter(gc)
        spl = nx.average_shortest_path_length(gc)
    
    return spl, d

def get_exp_path(expname):
    subpath = expname
    script_dir = os.path.dirname(__file__)
    rel_path = "tests/" + subpath 
    return os.path.join(script_dir, rel_path)

