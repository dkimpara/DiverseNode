import networkx as nx
import pandas as pd
import os
import json
import pickle as pk

from analysis import read_pickle, data_cleanup


def modify_main(experiment_name):
    dataframename = 'df_' + experiment_name
    df = read_pickle(dataframename)
    df = data_cleanup(df)
    df.drop(columns = ['SPL', 'diam']) #drop cols, replace in data_dict_processing
    df = analyze_data_sequential(df, experiment_name)
    
    #write pickle with new modified dataframe
    df.name = experiment_name + 'modsc'
    df.to_pickle('./tests/df_' + df.name)
    
def analyze_data_sequential(df, experiment_name):
    abs_folder_path = get_exp_path(experiment_name)
    for filename in os.listdir(abs_folder_path):
        with open(os.path.join(abs_folder_path, filename), 'rb') as f: 
            data_dict = pk.load(f)
            df = data_dict_processing(df, data_dict)
    return df
            
def data_dict_processing(df, data: dict):
    sd = data['std1'] #sd 0.1, sd d, rs, rw
    tags = df.loc[(df['std_d'] == sd[1]) & 
                      (df['std_rs'] == sd[2]) &
                      (df['std_rw'] == sd[3]), 'tags']
    #verify subframe is correct order
    assert(list(tags) == list(range(100)))
    spl, d, scratios = process_g_list(data['graphs'])
    #modify subframe 
    df.loc[(df['std_d'] == sd[1]) &
       (df['std_rs'] == sd[2]) &
       (df['std_rw'] == sd[3]), 'SPL'] = spl
    df.loc[(df['std_d'] == sd[1]) &
       (df['std_rs'] == sd[2]) &
       (df['std_rw'] == sd[3]), 'diam'] = d
    df.loc[(df['std_d'] == sd[1]) &
       (df['std_rs'] == sd[2]) &
       (df['std_rw'] == sd[3]), 'sc'] = scratios
    return df #check

def process_g_list(graphs):
    slist, dlist, scomp = [], [], []
    for g in graphs:
        s, diam, scratio = analyze_g_sc(g)
        slist.append(s)
        dlist.append(diam)
        scomp.append(scratio)
    return slist, dlist, scomp

def analyze_g_sc(g):
    try:
        d = nx.diameter(g)
        spl = nx.average_shortest_path_length(g)
        ratio = 1.0
    except nx.NetworkXError:
        sc_nodes = max(nx.strongly_connected_components(g), key=len)
        sc = g.subgraph(sc_nodes)
        
        d = nx.diameter(sc)
        spl = nx.average_shortest_path_length(sc)
        ratio = len(sc_nodes)/len(g.nodes())
    return spl, d, ratio
    

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

